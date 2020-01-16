# from config.kafka_consumer_config import consumer
from confluent_kafka.avro.serializer import SerializerError
# from config.kafka_consumer_config import unpack
from config.Config import Config
import threading
import uuid
import json
import io
import struct
from avro.io import BinaryDecoder, DatumReader
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient
# from flask import Flask
# from flask import current_app as app


class LocationKafkaListerner(object):
    __instance = None

    @staticmethod
    def create(app):
        if LocationKafkaListerner.__instance is None:
            LocationKafkaListerner(app)
        else:
            return LocationKafkaListerner.__instance

    def __init__(self, app):
        LocationKafkaListerner.__instance = self
        self.app = app
        self.config = Config.getInstance()
        self.register_client = CachedSchemaRegistryClient(
            url=app.config['KAFKA_SCHEMA_REGISTRY_URL']
        )
        self.client = self.config.getESClient()
        threading.Thread(target=self.readJobsData).start()
        threading.Thread(target=self.readMappingsData).start()
        threading.Thread(target=self.readSubmissionsData).start()

    def readJobsData(self):
        kafkaConsumer = self.config.getKafkaConsumer(
            'locationsearch_job_entity')
        kafkaConsumer.subscribe(['job_entity'])
        self.get_data(kafkaConsumer)

    def readMappingsData(self):
        kafkaConsumer = self.config.getKafkaConsumer(
            'locationsearch_jobCandidateMapping')
        kafkaConsumer.subscribe(['jobcandidatemapping_entity'])
        self.get_data(kafkaConsumer)

    def readSubmissionsData(self):
        kafkaConsumer = self.config.getKafkaConsumer(
            'locationsearch_jobCandidateInteraction')
        kafkaConsumer.subscribe(['jobcandidateinteraction_entity'])
        self.get_data(kafkaConsumer)

    def get_data(self, consumer):
        while True:
            try:
                msg = consumer.poll(10)
            except SerializerError as e:
                print("Message deserialization failed for {}: {}".format(msg, e))
                raise SerializerError

            if msg:
                if msg.error():
                    print("AvroConsumer error: {}".format(msg.error()))
                    return
                self.parseLocation(unpack(msg.value()))
            else:
                print("No Message!!")

    def parseLocation(self, message):
        entity = json.loads(json.dumps(message))
        if(entity['locations']):
            # Message from job index
            for l in entity['locations']:
                self.buildLocationLookupEntity(l)
        else:
            # Message from candidate index
            self.buildLocationLookupEntity(message.currentLocation)
            self.buildLocationLookupEntity(message.preferredLocations)

    def buildLocationLookupEntity(self, location):
        latlng = location['point'].split(",")
        if(location['point'] == '' or location['point'] is None or (float(latlng[0]) == 0 and float(latlng[1]) == 0)):
            print('no location latlng = {}'.format(latlng))
        else:
            addressComponents = []
            locationLookup = {}
            if location['city']:
                addressComponents.append(location['city'])
            if location['state']:
                addressComponents.append(location['state'])
            elif location['stateCode']:
                addressComponents.append(location['stateCode'])
            if location['country']:
                addressComponents.append(location['country'])
            elif location['countryCode']:
                addressComponents.append(location['countryCode'])
            if(addressComponents.count == 0):
                if location['continent']:
                    addressComponents.append(location['continent'])
                elif location['continentCode']:
                    addressComponents.append(location['continentCode'])

            locationLookup['id'] = str(uuid.uuid4())
            locationLookup['keywords'] = ", ".join(addressComponents)
            locationLookup['city'] = location['city']
            locationLookup['state'] = location['state']
            locationLookup['stateCode'] = location['stateCode']
            locationLookup['country'] = location['country']
            locationLookup['countryCode'] = location['countryCode']
            locationLookup['continent'] = location['continent']
            locationLookup['continentCode'] = location['continentCode']
            locationLookup['zipCode'] = location['zipCode']
            response = self.client.search(
                index="location_lookup",
                body={
                    "size": 1,
                    "query": {
                        "term": {
                            "keywords.lowercase": locationLookup['keywords'].lower()
                        }
                    }
                }
            )

            if(response['hits']['total'] == 0):
                print("Indexing " + locationLookup['keywords'])
                print(self.client.index(
                    index='location_lookup',
                    doc_type='location_lookup',
                    id=locationLookup['id'],
                    refresh='wait_for',
                    body=locationLookup)
                )
            else:
                print("Ignoring" + locationLookup['keywords'])

    def unpack(self, payload):
        MAGIC_BYTES = 0
        magic, schema_id = struct.unpack('>bi', payload[:5])
        # Get Schema registry
        # Avro value format
        if magic == MAGIC_BYTES:
            schema = self.register_client.get_by_id(schema_id)
            reader = DatumReader(schema)
            output = BinaryDecoder(io.BytesIO(payload[5:]))
            abc = reader.read(output)
            return abc
        # String key
        else:
            # Timestamp is inside my key
            return payload[:-8].decode()

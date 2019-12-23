from elasticsearch6 import Elasticsearch
from confluent_kafka import Consumer


class Config(object):

    __instance = None

    @staticmethod
    def create(app):
        if Config.__instance is None:
            Config(app)
        else:
            return Config.__instance

    @staticmethod
    def getInstance():
        return Config.__instance

    def __init__(self, app):
        Config.__instance = self
        self.app = app
        self.client = Elasticsearch(
            app.config['ELASTICSEARCH_CLUSTER_NODES']
        )

    def getESClient(self):
        return self.client

    def getKafkaConsumer(self, groupId):
        return Consumer({
            'bootstrap.servers': self.app.config['KAFKA_BOOTSTRAP_ADDRESS'],
            'group.id': '31' + groupId,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True,
            'auto.commit.interval.ms': 5000,
        })

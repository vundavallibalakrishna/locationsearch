#!/usr/bin/python3
from services.location_kafka_consumer import LocationKafkaListerner
from config.Config import Config
from api.location import LocationAutoComplete, LocationSearch
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
api.add_resource(LocationAutoComplete, '/api/location/search')
api.add_resource(LocationSearch, '/api/location/suggest')
app.config.from_envvar('APP_CONFIG_FILE')


if __name__ == '__main__':
    Config(app)
    LocationKafkaListerner(app)
    app.run()

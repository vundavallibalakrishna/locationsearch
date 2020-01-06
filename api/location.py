from flask import request, jsonify
from flask_restful import Resource
from services.location_service import autocomplete, search


class LocationAutoComplete(Resource):
    def get(self):
        query = request.args['query']
        return jsonify({'query': autocomplete(query)})


class LocationSearch(Resource):
    def get(self):
        query = request.args['query']
        return jsonify({'query': search(query)})

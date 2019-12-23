from flask import request, jsonify
from flask_restful import Resource
from services.location_service import autocomplete, search


class LocationAutoComplete(Resource):
    def get(self):
        query = request.args['query']
        autocomplete(query)
        return jsonify({'query': query})


class LocationSearch(Resource):
    def get(self):
        query = request.args['query']
        search(query)
        return jsonify({'query': query})

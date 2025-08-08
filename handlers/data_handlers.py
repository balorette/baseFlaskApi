from flask_restful import Resource
from flask import request, jsonify
from utils.mongo_db import SyncMongo
from config import config


class MongoHandler(Resource):
    """Resource for basic MongoDB interactions."""
    mg = SyncMongo(config)
    col = 'exrts'

    def get(self):
        key = request.args.get('key')
        value = request.args.get('value')
        if not key or not value:
            return "Provide a key and value query", 400
        try:
            results = self.mg.read(self.col, kvPair={key: value})
        except Exception as e:
            return str(e), 500
        return jsonify(results)

    def post(self):
        if not request.is_json:
            return "Need JSON data", 400
        d = request.get_json()
        docid = self.mg.write(self.col, data=d)
        return jsonify(docid)

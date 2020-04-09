from flask_restful import Resource
from flask import request, jsonify
import json
from box import Box
from utils.mongo_db import SyncMongo
from conf import uri

config = Box({'db': {'mongo':{'uri': uri, 'db': 'data01'}}})


class mongo_handler(Resource):
    mg = SyncMongo(config)
    col = 'exrts'

    def get(self):
        if request.args:
            key = request.args['key']
            value = request.args['value']
        else:
            return "Provide a request please"

        results = {}

        try:
            results = self.mg.read(self.col, kvPair={key: value})

        except Exception as E:
            return E

        return jsonify(results)

    def post(self):
        if request.json:
            d = request.json
            docid = self.mg.write(self.col, data=d)
            return jsonify(docid)
        else:
            return "Need Json Data"

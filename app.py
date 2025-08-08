import os
from flask import Flask
from flask_restful import Api
from handlers.data_handlers import MongoHandler


def create_app():
    app = Flask(__name__)
    api = Api(app)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    api.add_resource(MongoHandler, '/mgo')
    return app


app = create_app()

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port)

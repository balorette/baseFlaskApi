from flask import Flask
from flask_restful import Api
from handlers.data_handlers import mongo_handler


host = '0.0.0.0'
prt = 5000
app = Flask(__name__)
api = Api(app)



@app.route('/')
def hello_world():
    return 'Hello World!'

api.add_resource(mongo_handler, '/mgo')

if __name__ == '__main__':
    app.run(host, prt)

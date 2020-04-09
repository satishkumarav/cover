import os
from flask import Blueprint
from flask import Flask
from flask_restful import Api
import configparser
from cover.resources.locationlist import LocationList
basedir = os.path.abspath(os.path.dirname(__file__))


blueprint = Blueprint('api',__name__)
api = Api(blueprint)
app = Flask(__name__)
app.config.from_object('config.Config')
app.config["DEBUG"]

app.register_blueprint(api.blueprint,url_prefix='/cover/api/v1.0')
api.add_resource(LocationList, '/locations')

sqlconfig = configparser.ConfigParser()
sqlconfig.optionxform = str

sqlconfig.read(os.path.join(basedir,"SQL.properties"))
for section in sqlconfig.sections():
    for (k,v) in sqlconfig.items(section):
        app.config[k]=v


if __name__ == '__main__':
    app.run(host='0.0.0.0')


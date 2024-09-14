from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# CORS(app, support_credentials=True)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], supports_credentials=True)
api = Api(app, version='1.0', title='Sample API', description='A simple Flask-RESTx API')
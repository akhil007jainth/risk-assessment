from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from app import app, api
from lib.utils import format_response
from lib.general_utils import data_envelope
from web.models.main import User

ns = api.namespace('admin', description='User Admin')

# Define the response model for serialization
admin_serializer = api.model('Admin', {
    'username': fields.String(required=True, description='Admin Name'),
    'email': fields.String(required=True, description='Admin Email')
})

# Create a request parser for input data
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Admin Name')
parser.add_argument('email', type=str, required=True, help='Admin Email')


@ns.route('/init')
class AdminClient(Resource):
    """Admin"""

    @ns.expect(parser)
    @ns.marshal_with(data_envelope(admin_serializer))
    def get(self):
        args = parser.parse_args()
        username = args["name"]
        email = args["email"]

        client = User()
        client.username = username
        client.email = email

        return format_response(client, 200, "success")

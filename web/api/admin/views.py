from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from app import app, api
from lib.utils import format_response
from lib.general_utils import data_envelope
from web.models.main import User

ns = api.namespace('todos', description='Todo operations')

# Define the response model for serialization
todo_model = api.model('Todo', {
    'name': fields.String(required=True, description='The todo item'),
})

# Create a request parser for input data
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the todo item')



@ns.route('/init')
class TodoResource(Resource):
    '''Show a single todo item and lets you delete them'''

    @ns.expect(parser)  # Attach the parser to expect input arguments
    @ns.marshal_with(data_envelope(todo_model))  # Serialize the output with todo_model
    def get(self):
        # Parse arguments from the request
        args = parser.parse_args()
        user = User(username=args["name"], email="akhil@gmail.com")
        user.save()
        print("Received argument:", args['name'])

        # Return the response serialized with the todo_model
        return format_response(None, 200, "sucess", custom_ob={"name":"akhil"})

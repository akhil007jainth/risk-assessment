from flask import request
from flask_restx import Resource

from app import api
from lib.general_utils import data_envelope
from lib.utils import format_response
from web.api.admin import parser
from web.api.admin.serializer import user_serializer
from web.models.main import User, WebhookClient

ns = api.namespace('admin', description='User Admin')


@ns.route('/init')
class AdminClient(Resource):
    """Admin"""

    @ns.expect(parser.user_parser)
    @ns.marshal_with(data_envelope(user_serializer))
    def post(self):
        args = parser.user_parser.parse_args()
        full_name = args["name"]
        email = args["email"]

        if not full_name or not email:
            return format_response(None, 400, message="Name or Email can not be empty")

        client = User()
        user_id = client.generate_id()
        client.user_id = user_id
        client.full_name = full_name
        client.email = email

        if User.objects(email=email).first():
            return format_response(None, 422, "fail", custom_ob="User Already Exits")

        return format_response(client, 200, "success")


@ns.route('/get-users')
class UserList(Resource):
    def get(self):
        """Get Users List"""

        users = User.objects.only('full_name', 'email')
        user_list = [{'full_name': user.full_name, 'email': user.email} for user in users]

        return format_response(None, 200, "success", custom_ob=user_list)


@ns.route('/webhook')
class webhook(Resource):
    def get(self):
        """Result"""

        data = request.json
        client = WebhookClient()
        client.data = data
        client.save()

        return format_response(None, 200, "Success")


import json
import os

import requests
from flask import request
from flask_restx import Resource, reqparse

from app import api
from lib.general_utils import data_envelope
from lib.utils import format_response
from web.api.admin import parser as init_parser
from web.api.admin.serializer import user_serializer
from web.api.magic_link.utils import create_magic_link
from web.models.main import User, WebhookClient

ns = api.namespace('admin', description='User Admin')


@ns.route('/init')
class AdminClient(Resource):
    """Admin"""

    @ns.expect(init_parser.user_parser)
    @ns.marshal_with(data_envelope(user_serializer))
    def post(self):
        args = init_parser.user_parser.parse_args()
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

        users = User.objects().all()
        user_list = [{'full_name': user.full_name, 'email': user.email, 'status': user.status, 'created_at': user.created_at.strftime('%Y-%m-%dT%H:%M:%S')} for user in users]

        return format_response(None, 200, "success", custom_ob=user_list)


parser_user = reqparse.RequestParser()
parser_user.add_argument("email", type=str, required=True, help="Super Link")


@ns.route('/user-details')
class UserDetails(Resource):
    @ns.expect(parser_user)
    def get(self):
        """Get Users List"""
        args = parser.parse_args()
        email = args['email']

        users = User.objects(email=email).exclude("id").first()

        return format_response(None, 200, "success", custom_ob=users.to_mongo().to_dict())


@ns.route('/webhook')
class Webhook(Resource):
    def get(self):
        """Result"""

        data = request.json
        if not data:
            return format_response(None, 400, "Fail")

        client = WebhookClient()
        client.data = data
        client.save()

        user = User.objects(user_id=client.data["user_id"]).first()
        user.raw_data = data
        user.save()

        return format_response(None, 200, "Success")


# Create a request parser for input data
parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True, help='Email')
parser.add_argument('question_id', type=str, required=True, help='question_id')
parser.add_argument('category', type=str, required=True, help='category')


@ns.route("/send-assessment-email")
class SendAssessmentEmail(Resource):
    @ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        email = args["email"]
        question_id = args["question_id"]
        category = args["category"]

        link = create_magic_link(email, question_id, category)

        url = "https://api.resend.com/emails"

        payload = json.dumps({
            "from": "onboarding@zapcircle.net",
            "to": [
                email
            ],
            "subject": "hello world",
            "html": f"<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Assessment Invitation</title></head><body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;\"><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"background-color: #f8f8f8; border-radius: 10px; overflow: hidden;\"><tr><td style=\"padding: 40px 30px; text-align: center; background-color: #4a90e2;\"><h1 style=\"color: #ffffff; margin: 0;\">Assessment Invitation</h1></td></tr><tr><td style=\"padding: 30px;\"><p style=\"margin-bottom: 20px;\">Dear Participant,</p><p style=\"margin-bottom: 20px;\">We invite you to take part in an important assessment. Your participation is crucial for our evaluation process.</p><p style=\"margin-bottom: 30px;\">Please click the button below to access the assessment:</p><p style=\"text-align: center;\"><a href=\"{link}\" style=\"display: inline-block; padding: 12px 24px; background-color: #4a90e2; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold;\">Start Assessment</a></p><p style=\"margin-top: 30px;\">If you have any questions or concerns, please don't hesitate to contact us.</p><p style=\"margin-bottom: 20px;\">Best regards,<br>The Assessment Team</p></td></tr><tr><td style=\"background-color: #eeeeee; padding: 20px; text-align: center; font-size: 12px;\"><p style=\"margin: 0;\">This email was sent by Example Company. © 2024 All Rights Reserved.</p></td></tr></table></body></html>"
        })
        headers = {
            'Authorization': f'Bearer {os.getenv("RESEND_EMAIL_KEY")}',
            'Content-Type': 'application/json'
        }

        _x = requests.request("POST", url, headers=headers, data=payload)

        return format_response(None, 200, "Success")

import secrets

from flask import request, redirect
from flask_restx import Resource, reqparse, fields
from app import api
from lib.utils import format_response
from web.api.magic_link.utils import email_verification_token_serializer, create_magic_link
from web.models.magic_link_model import FlowConnectLink, SuperLinkModel

ns = api.namespace('magic-link', description='Magic Link')


parser = reqparse.RequestParser()
parser.add_argument("email", type=str, required=True, help="Super Link")
parser.add_argument("question_id", type=str, required=True, help="Question ID")

send_flow_connect_link_parser = reqparse.RequestParser()
send_flow_connect_link_parser.add_argument("email", type=str, help="Email Of User")

send_flow_connect_link_serializer = api.model("Templates ", {
    "super_link_id": fields.String(attribute="superlink_id", description="Flow Connect ID"),
    "email": fields.String(description="Root User Email"),
    "connect_link": fields.String(description=" Flow Connect Link", attribute="superlink")
})


# @ns.route('/superlink')
# class GenerateSuperlink(Resource):
#
#     @ns.expect(parser)
#     def get(self):
#         """Generate super link"""
#
#         args = parser.parse_args()
#         email = args['email']
#         question_id = args['question_id']
#
#         obj = SuperLinkModel.objects(email=email).first()
#
#         link = create_magic_link(obj.email, question_id)
#
#         return format_response(None, 200, "success", custom_ob={"link": link})


@ns.route("/verify-magic-link")
class VerifyMagicLink(Resource):
    def get(self):
        verification_uri = request.args['verification_uri']

        data = email_verification_token_serializer.loads(
            verification_uri,
            max_age=86400,
        )

        client_id = data['client_id']
        verification_token = data["verification_token"]

        obj = FlowConnectLink.objects(client_id=client_id).order_by('-created_at').first()

        if obj.is_expired:
            return format_response(None, 404, message="Magic link is already expired")

        if not secrets.compare_digest(obj.token_id, verification_token):
            return format_response(None, 422, message="Invalid email verification token")

        return redirect(f"https://ocelot-flying-safely.ngrok-free.app/form?doc_question_id={obj.question_id}&email={obj.email}&category={obj.category}")

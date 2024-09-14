import os
import secrets

from itsdangerous import URLSafeTimedSerializer

from web.models.magic_link_model import FlowConnectLink

email_verification_token_serializer = URLSafeTimedSerializer("ABCDE", "verification-token")
# os.getenv("RISK_ASSESSMENT_SECRETS")


class FlowLinkConnect:
    def __init__(self, client_id):
        self.client_id = client_id
        self.verification_token, self.verification_uri = generate_email_verification_token(
            self.client_id
        )

    @property
    def verification_url(self):
        return f"https://curious-walrus-miserably.ngrok-free.app/magic-link/verify-magic-link?verification_uri={self.verification_uri}"

    def flow_link_data(self):
        return self.verification_token, self.verification_url


def create_magic_link(root_user_email, question_id, category):

    flow_connect_link = FlowConnectLink()
    flow_connect_link.client_id = flow_connect_link.generate_id()
    flow_connect_link.email = root_user_email
    flow_connect_link.question_id = question_id
    flow_connect_link.category = category
    flow_connect_link.save()

    flow_link_data = FlowLinkConnect(flow_connect_link.client_id)

    token, connect_link = flow_link_data.flow_link_data()

    flow_connect_link.token_id = token
    flow_connect_link.connect_link = connect_link
    flow_connect_link.save()

    return connect_link


def generate_email_verification_token(client_id):
    verification_token = secrets.token_hex(32)
    verification_uri = email_verification_token_serializer.dumps({
        "client_id": client_id,
        "verification_token": verification_token
    })
    return verification_token, verification_uri

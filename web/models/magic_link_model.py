from mongoengine import Document, StringField, EmailField, BooleanField

from lib.utils import generate_id


class FlowConnectLink(Document):
    prepend_string = 'flow_connect'

    client_id = StringField(required=True)
    email = EmailField(required=True)
    connect_link = StringField()
    token_id = StringField()
    is_expired = BooleanField(default=False)

    @classmethod
    def generate_id(cls):
        return generate_id(cls.prepend_string)


class SuperLinkModel(Document):
    prepend_string = 'superlink'

    email = StringField()
    superlink_id = StringField(required=True, unique=True)
    superlink = StringField()

    @classmethod
    def generate_id(cls):
        return generate_id(cls.prepend_string)

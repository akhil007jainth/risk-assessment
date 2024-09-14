from datetime import datetime
from lib.utils import generate_id
from mongoengine import Document, StringField, DateTimeField, DictField


class User(Document):
    prepend_string = "user"

    STATUS_CHOICES = {"Pending", "Inactive", "Completed", "Failed"}

    user_id = StringField(required=True, unique=True)
    full_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)
    status = StringField(default="Inactive", choices=STATUS_CHOICES)

    @classmethod
    def generate_id(cls):
        return generate_id(cls.prepend_string)


class WebhookClient(Document):
    data = DictField()

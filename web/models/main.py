from datetime import datetime

from mongoengine import Document, StringField, DateTimeField


class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)

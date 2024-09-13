from mongoengine import Document, StringField, DictField, ListField

from lib.utils import generate_id


class PdfData(Document):
    prepend_string = 'pdf_response'

    client_id = StringField(required=True)
    question = StringField(max_length=100)
    answer_t = StringField(max_length=100)
    answer_f = StringField(null=True)

    @classmethod
    def generate_id(cls):
        return generate_id(cls.prepend_string)


class Question(Document):
    prepend_string = "question"
    question_documents_id = StringField(required=True)
    question = ListField(DictField())
    categories = StringField()
    categories_description = StringField()

    @classmethod
    def generate_id(cls):
        return generate_id(cls.prepend_string)

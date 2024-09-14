from mongoengine import Document, StringField, DictField, ListField, EmbeddedDocument, EmbeddedDocumentListField

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


class QuestionDetails(EmbeddedDocument):
    question_id = StringField(required=True)
    raw_ques = DictField()


class Question(Document):
    # prepend_string = "question"
    question_document_id = StringField(required=True)
    questions = EmbeddedDocumentListField(QuestionDetails)
    categories = StringField()
    file_name = StringField()
    categories_description = StringField()

    @classmethod
    def generate_id(cls, prepend_string):
        return generate_id(prepend_string)

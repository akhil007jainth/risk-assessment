import json
from enum import Enum
from flask_restx import Api, Resource, fields, reqparse
from app import app, api
from lib.utils import format_response, generate_id
from lib.general_utils import data_envelope
from web.models.question_model import Question, QuestionDetails
from lib.claude_prompting.base import CalculatePromptExecutor

ns = api.namespace('questions', description='question operations')


class Category(Enum):
    PYTHON = 'Python'
    STOCK = 'Stock'
    APTITUDE = 'Aptitude'
    DATA_SCIENCE = 'Data Science'
    MACHINE_LEARNING = 'Machine Learning'


# Define the response model for serialization
question_model = api.model('Data', {
    'question_documents_id': fields.String(required=True, description='The question document Id'),
    'categories': fields.String(required=True, description='The document categories'),
    'categories_description': fields.String(required=True, description='The categories description'),
})

# Create a request parser for input data
parser = reqparse.RequestParser()
parser.add_argument('data', type=list, location='json', required=True, help='Name of the todo item', action="append")
parser.add_argument('categories', type=str, choices=[cat.value for cat in Category], required=True, help='Categories of Quiz')
parser.add_argument('categories_description', type=str, required=True, help='Categories of Quiz')


@ns.route('/insert-question')
class SetQuestion(Resource):

    @ns.expect(parser)
    @ns.marshal_with(data_envelope(question_model))
    def post(self):
        # Parse arguments from the request
        args = parser.parse_args()
        data = args['data']
        categories = args['categories']
        categories_description = args['categories_description']
        data = data[0]

        question_ = Question()
        question_.question_document_id = Question.generate_id("question_doc_id")
        question_.categories = categories
        question_.categories_description = categories_description

        for question_data in data:
            nes_ques = QuestionDetails()
            nes_ques.question_id = Question.generate_id("question_id")
            nes_ques.raw_ques = question_data
            question_.questions.append(nes_ques)

        question_.save()

        return format_response(question_, 200, "success")


parser_1 = reqparse.RequestParser()
parser_1.add_argument("question_documents_id", type=str, required=True, help='Categories of Quiz')
parser_1.add_argument('data', type=list, location='json', required=True, help='Name of the todo item', action="append")


@ns.route('/get-score')
class GetQuestion(Resource):
    @ns.expect(parser_1)
    def post(self):
        args = parser_1.parse_args()
        doc_id = args['question_documents_id']
        answers = args['data']
        question = Question.objects(question_document_id=doc_id).first()

        if not question:
            return format_response(None, 400, "Document's Id Not Exit")

        questions_x = [i.to_mongo().to_dict() for i in question.questions]

        rv = CalculatePromptExecutor.execute(answers, questions_x)

        return format_response(None, 200, "Success", custom_ob={"data": rv})


@ns.route('/question-list')
class QuestionList(Resource):
    def get(self):
        document = Question.objects().exclude("id").all()

        if not document:
            return format_response(None, 422, 'Fail')

        data = [i.to_mongo().to_dict() for i in document]

        return format_response(None, 200, 'success', custom_ob=data)


from enum import Enum
from flask_restx import Api, Resource, fields, reqparse
from app import app, api
from lib.utils import format_response, generate_id
from lib.general_utils import data_envelope
from web.models.question_model import Question

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


@ns.route('/set-score')
class SetQuestion(Resource):

    @ns.expect(parser)
    @ns.marshal_with(data_envelope(question_model))
    def post(self):
        # Parse arguments from the request
        args = parser.parse_args()
        data = args['data']
        categories = args['categories']
        categories_description= args['categories_description']
        data = data[0]

        questions_to_save = []

        for question_data in data:
            question_text = question_data.get('question')
            options = question_data.get('options')
            answer = question_data.get('answer')
            score = question_data.get('score')

            questions_to_save.append({
                'question_id': Question.generate_id(),
                'question': question_text,
                'options': options,
                'answer': answer,
                'score': score
            })

        question_collection = Question(
            question_documents_id=Question.generate_id(),
            question=questions_to_save,
            categories=categories,
            categories_description=categories_description
        )
        question_collection.save()

        return format_response(question_collection, 200, "success")


parser_1 = reqparse.RequestParser()
parser_1.add_argument("question_documents_id", type=str, required=True, help='Categories of Quiz')
parser_1.add_argument('data', type=list, location='json', required=True, help='Name of the todo item', action="append")


@ns.route('/get-score')
class GetQuestion(Resource):
    @ns.expect(parser_1)
    def post(self):
        args = parser_1.parse_args()
        doc_id = args['question_documents_id']
        question_answer = args['data']
        question = Question.objects(question_documents_id=doc_id).first()
        if not question:
            return format_response(None, 400, "Document's Id Not Exit")

        response = question.question

        return format_response(None, 200, "Success")

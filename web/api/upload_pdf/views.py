import os

from PyPDF2 import PdfReader
import anthropic
from flask_restx import Resource, reqparse
from app import api
from lib.utils import format_response
from werkzeug.datastructures import FileStorage
from lib.claude_prompting.base import PdfPromptExecutor
from web.models.question_model import Question, QuestionDetails


ns = api.namespace('pdf', description='Upload PDF')

# Create a request parser for input data
parser = reqparse.RequestParser()
parser.add_argument('file', location='files', type=FileStorage, required=True, help='PDF file to be processed')
parser.add_argument('categories', location='form', type=str, required=True, help='PDF file to be processed')
parser.add_argument('categories_description', location='form', type=str, required=True, help='PDF file to be processed')


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


@ns.route('/upload-pdf')
class UploadPdf(Resource):

    # API for Initialize User
    @ns.expect(parser)
    def post(self):
        # Parse arguments from the request
        args = parser.parse_args()
        pdf_file = args['file']
        categories = args['categories']
        categories_description = args['categories_description']

        if not pdf_file:
            return format_response(None, 400, "Pdf file is required")

        pdf_content = extract_text_from_pdf(pdf_file)
        rv = PdfPromptExecutor.execute(pdf_content=pdf_content)

        question_ = Question()
        question_.question_document_id = Question.generate_id("question_doc_id")
        question_.categories = categories
        question_.categories_description = categories_description

        for question_data in rv:
            nes_ques = QuestionDetails()
            nes_ques.question_id = Question.generate_id("question_id")
            nes_ques.raw_ques = question_data
            question_.questions.append(nes_ques)

        question_.save()

        return format_response(None, 200, "Success", custom_ob={"question_doc_id": question_.question_document_id})

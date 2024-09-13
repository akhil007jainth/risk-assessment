import os

from PyPDF2 import PdfReader
import anthropic
from flask_restx import Resource, reqparse
from app import api
from lib.utils import format_response
from werkzeug.datastructures import FileStorage

ns = api.namespace('pdf', description='Upload PDF')


# Create a request parser for input data
parser = reqparse.RequestParser()
parser.add_argument('file', location='files', type=FileStorage, required=True, help='PDF file to be processed')


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)


def evaluate(pdf_file):
    system_prompt = """

        You are an expert in analyzing documents and creating insightful questions. Your task is to read the provided PDF content, extract key information, and generate questions to assess the understanding of the material. For each question, provide two answers: one concise correct (True) and one similar but incorrect (False). Then, assign a score based on the Rubric-Based Grading System. The total score is 100 marks, with 5 points for a false answer and 10 marks for a true answer.

        """

    user_prompt = f"""Based on the following PDF content, please:

    1. Generate 10 important questions that cover the key concepts and information presented in the document.
    2. For each question:
       a) Provide one concise, correct answer
       b) Provide one plausible but incorrect answer
    3. Assign marks value to each answer, where correct answer is marked for 10 points and 5 marks for incorrect answer.


    PDF Content:
    {pdf_file}

    Please ensure that the questions cover a range of topics from the PDF content and vary in their mark allocations."""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    generated_questions = message.content
    return generated_questions


class BackendError:
    pass


@ns.route('/upload-pdf')
class UploadPdf(Resource):

    # API for Initialize User
    @ns.expect(parser)
    # @ns.marshal_with(data_envelope(todo_model))
    def get(self):
        # Parse arguments from the request
        args = parser.parse_args()
        pdf_file = args['file']

        if not pdf_file:
            return format_response(None, 400, "Pdf file is required")

        pdf_content = extract_text_from_pdf(pdf_file)
        try:
            response = evaluate(pdf_content)
        except Exception as e:
            raise BackendError
        # Since response is a very rich text it can be display, but it is under progress
        # We will save in DB Later on
        return format_response(None, 200, "Success")

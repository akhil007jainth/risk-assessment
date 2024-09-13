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


@ns.route('/upload-pdf')
class UploadPdf(Resource):

    # API for Initialize User
    @ns.expect(parser)
    def post(self):
        # Parse arguments from the request
        args = parser.parse_args()
        pdf_file = args['file']

        if not pdf_file:
            return format_response(None, 400, "Pdf file is required")

        # pdf_content = extract_text_from_pdf(pdf_file)
        # try:
        #     response = evaluate(pdf_content)
        # Since response is a very rich text it can be display, but it is under progress
        # We will save in DB Later on
        return format_response(None, 200, "Success")

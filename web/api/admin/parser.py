from flask_restx import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Admin Name')
parser.add_argument('email', type=str, required=True, help='Admin Email')


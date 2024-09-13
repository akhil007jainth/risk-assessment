from flask_restx import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, help='Admin Name')
user_parser.add_argument('email', type=str, required=True, help='Admin Email')

from flask_restx import fields

from app import api

admin_serializer = api.model('Admin', {
    'username': fields.String(required=True, description='Admin Name'),
    'email': fields.String(required=True, description='Admin Email')
})

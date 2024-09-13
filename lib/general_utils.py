

from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from app import app, api

def data_envelope(nested_model, as_list=False, skip_none=False):
    nested_model = fields.Nested(model=nested_model, description="Nested Model", allow_null=True, skip_none=skip_none)

    if as_list is True:
        data_field = fields.List(nested_model, description="List of objects")
    else:
        data_field = nested_model

    return api.model("Envelope Model for all APIs", {
        "data": data_field,
        "status_code": fields.Integer(required=True, description="Status code of the response"),
        "success": fields.Boolean(required=True, description="Success status of the response"),
        "message": fields.String(required=True, description="Additional Message in the response"),
        "message_code": fields.String(required=True, description="Additional Message Code in the response")
    })

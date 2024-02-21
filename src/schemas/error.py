from marshmallow import fields

from src.schemas import BaseSchema


class CustomErrorSchema(BaseSchema):
    """Error schema to be used for all errors."""
    code = fields.Int(required=True)
    status = fields.Str(required=True)
    message = fields.Str(required=True)

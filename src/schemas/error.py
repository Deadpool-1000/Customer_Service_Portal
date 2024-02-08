from marshmallow import Schema, fields


class CustomErrorSchema(Schema):
    """Error schema to be used for all errors."""
    code = fields.Int(required=True)
    status = fields.Str(required=True)
    message = fields.Str(required=True)

from marshmallow import Schema, fields


class ErrorSchema(Schema):
    code = fields.Int(required=True)
    status = fields.Str(required=True)
    message = fields.Str(required=True)

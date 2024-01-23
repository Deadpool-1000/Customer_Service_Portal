from marshmallow import Schema, fields, validate


class AuthSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(error="Not a valid email address"))
    password = fields.Str(required=True)


class TokenSchema(Schema):
    token = fields.Str(required=True)


class UserSignupSchema(AuthSchema):
    full_name = fields.Str(required=True)
    phn_num = fields.Str(required=True)
    address = fields.Str(required=True)


class UserSchema(Schema):
    email = fields.Str(required=True)
    full_name = fields.Str(required=True)
    phn_num = fields.Str(required=True)
    address = fields.Str(required=True)


class SuccessSchema(Schema):
    # In the future, we can add links to next actions
    message = fields.Str(required=True)

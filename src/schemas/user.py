from marshmallow import Schema, fields, validate
from flask import current_app


class AuthSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(error=current_app.config['INVALID_EMAIL_ERROR_MESSAGE']))
    password = fields.Str(required=True, validate=validate.Regexp(regex=rf"{current_app.config['PWD_REGEXP']}", error=current_app.config['WEAK_PASSWORD_ERROR_MESSAGE']))


class TokenSchema(Schema):
    token = fields.Str(required=True)


class UserSignupSchema(AuthSchema):
    full_name = fields.Str(required=True)
    phn_num = fields.Str(required=True)
    address = fields.Str(required=True)


class UserSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(error=current_app.config['INVALID_EMAIL_ERROR_MESSAGE']))
    full_name = fields.Str(required=True)
    phn_num = fields.Str(required=True)
    address = fields.Str(required=True)


class SuccessSchema(Schema):
    # In the future, we can add links to next actions
    message = fields.Str(required=True)

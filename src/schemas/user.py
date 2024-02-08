from flask import current_app
from marshmallow import Schema, fields, validate


class AuthSchema(Schema):
    """Schema representing format needed for authentication"""
    email = fields.Str(required=True, validate=validate.Email(error=current_app.config['INVALID_EMAIL_ERROR_MESSAGE']))
    password = fields.Str(required=True, validate=validate.Regexp(regex=rf"{current_app.config['PWD_REGEXP']}",
                                                                  error=current_app.config[
                                                                      'WEAK_PASSWORD_ERROR_MESSAGE']))


class TokenSchema(Schema):
    """Schema representing format returned on successful authentication"""
    token = fields.Str(required=True)


class UserSignupSchema(AuthSchema):
    """Schema representing format required for signup"""
    full_name = fields.Str(required=True)
    phn_num = fields.Str(required=True)
    address = fields.Str(required=True)


class SuccessSchema(Schema):
    """Schema representing success message"""
    # In the future, we can add links to next actions
    message = fields.Str(required=True)

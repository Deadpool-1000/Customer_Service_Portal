import typing

from flask import current_app
from marshmallow import fields, validate, ValidationError
from flask_smorest import abort
from src.schemas import BaseSchema


class AuthSchema(BaseSchema):
    """Schema representing format needed for authentication"""
    email = fields.Str(required=True, validate=validate.Email(error=current_app.config['INVALID_EMAIL_ERROR_MESSAGE']), example="abc@gmail.com")
    password = fields.Str(required=True, validate=validate.Regexp(regex=rf"{current_app.config['PWD_REGEXP']}",
                                                                  error=current_app.config[
                                                                      'WEAK_PASSWORD_ERROR_MESSAGE']), example='Abcdef@2')


class AuthSchemaRole(AuthSchema):
    """Schema representing format needed for authentication"""
    role = fields.Str(required=True, validate=validate.OneOf([current_app.config['EMPLOYEE_'], current_app.config['CUSTOMER_']]))


class TokenSchema(BaseSchema):
    """Schema representing format returned on successful authentication"""
    token = fields.Str(required=True)
    expiresIn = fields.Float(required=True)


class UserSignupSchema(AuthSchema):
    """Schema representing format required for signup"""
    full_name = fields.Str(required=True, example="John Doe")
    phn_num = fields.Str(required=True, example='8984322112', validate=validate.Regexp(regex=rf"{current_app.config['PHN_NUM_REGEXP']}", error=current_app.config['INVALID_PHN_NUM_ERROR_MESSAGE']))
    address = fields.Str(required=True, example='Abc street, my-avenue, xyz city, 313001')


class SuccessSchema(BaseSchema):
    """Schema representing success message"""
    # In the future, we can add links to next actions
    message = fields.Str(required=True)


class ProfileSchema(BaseSchema):
    """Schema representing format for update"""
    full_name = fields.Str(required=True, example="John Doe")
    phn_num = fields.Str(required=True, example='8984322112')
    address = fields.Str(required=True, example='Abc street, my-city')
    email = fields.Str(required=True, example='abc@gmail.com')
    role = fields.Str(required=True, example='CUSTOMER')
    c_id = fields.Str(example='ABCvf3')
    e_id = fields.Str(example='ABCvf3')
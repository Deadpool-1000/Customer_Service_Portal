from marshmallow import Schema, fields, validate

INVALID_EMAIL_MESSAGE = "Not a valid email address"
PWD_REGEX = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"


class AuthSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(error=INVALID_EMAIL_MESSAGE))
    password = fields.Str(required=True, validate=validate.Regexp(regex=PWD_REGEX))


class TokenSchema(Schema):
    token = fields.Str(required=True)


class UserSignupSchema(AuthSchema):
    full_name = fields.Str(required=True)
    phn_num = fields.Str(required=True)
    address = fields.Str(required=True)


class UserSchema(Schema):
    email = fields.Str(required=True, validate=validate.Email(error=INVALID_EMAIL_MESSAGE))
    full_name = fields.Str(required=True)
    phn_num = fields.Str(required=True)
    address = fields.Str(required=True)


class SuccessSchema(Schema):
    # In the future, we can add links to next actions
    message = fields.Str(required=True)

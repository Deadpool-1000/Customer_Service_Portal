import typing

from flask import current_app
from marshmallow import Schema, ValidationError
from flask_smorest import abort


class BaseSchema(Schema):
    def handle_error(
            self, error: ValidationError, data: typing.Any, *, many: bool, **kwargs
    ):
        current_app.logger.error(error.messages)
        abort(422, message=error.args)
        
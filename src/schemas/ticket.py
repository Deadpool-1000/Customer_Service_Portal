from marshmallow import fields, validate, ValidationError
from src.schemas import BaseSchema


class UnionField(fields.Field):
    """Field that deserializes multi-type input data to app-level objects."""
    def __init__(self, types: list = None, *args, **kwargs) -> None:
        if types is None:
            types = []

        super().__init__(*args, **kwargs)
        if types:
            self.types = types
        else:
            raise AttributeError('No types provided on union field')

    def _deserialize(self, value, attr, data, **kwargs):
        if bool([isinstance(value, i) for i in self.types if isinstance(value, i)]):
            return value
        else:
            raise ValidationError(
                f'Field shoud be any of the following types: [{", ".join([str(i) for i in self.types])}]'
            )


class UserSchema(BaseSchema):
    """Schema representing public information of the user"""
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=10))
    email = fields.Str(required=True)
    phn_num = fields.Str(required=True)


class TicketSchema(BaseSchema):
    """Schema representing concise view of the ticket."""
    ticket_id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    created_on = fields.Str(required=True)
    status = fields.Str(required=True)
    message_from_helpdesk = fields.Str()


class DepartmentSchema(BaseSchema):
    """Schema department details"""
    dept_id = fields.Str(required=True)
    dept_name = fields.Str(required=True)


class TicketRaisingSchema(BaseSchema):
    """Schema representing the format needed for raising ticket."""
    d_id = fields.Str(required=True, validate=validate.Length(min=1, max=2))
    title = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    description = fields.Str(required=True)


class FeedbackSchema(BaseSchema):
    """Schema representing the feedback format"""
    stars = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    description = fields.Str(required=True)
    ticket_id = fields.Str(required=True, dump_only=True)
    created_on = fields.Str(required=True, dump_only=True)


class MessageSchema(BaseSchema):
    created_on = fields.Str(required=True, dump_only=True)
    ticket_id = fields.Str(required=True, dump_only=True)
    message = fields.Str(required=True)


class MessageFromHelpdeskSchema(BaseSchema):
    """Schema representing message from helpdesk"""
    message_from_helpdesk = fields.Str(required=True)


class MessageFromManager(BaseSchema):
    """Schema representing message from manager"""
    message_from_manager = fields.Str(required=True)


class MessageFromHelpdeskInTicket(BaseSchema):
    created_at = fields.Str(required=True)
    message = fields.Str(required=True)


class TicketDetailedView(TicketSchema):
    department = fields.Nested(DepartmentSchema)
    customer = fields.Nested(UserSchema)
    helpdesk_assigned = fields.Nested(UserSchema)
    message_from_helpdesk = UnionField(types=[str, MessageFromHelpdeskInTicket])

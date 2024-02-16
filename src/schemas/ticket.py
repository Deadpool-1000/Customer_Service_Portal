from marshmallow import fields, Schema, validate

class UnionField(fields.Field):
    """Field that deserializes multi-type input data to app-level objects."""
    def __init__(self, types: list = [], *args, **kwargs) -> None:
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


class UserSchema(Schema):
    """Schema representing public information of the user"""
    full_name = fields.Str(required=True)
    email = fields.Str(required=True)
    phn_num = fields.Str(required=True)


class TicketSchema(Schema):
    """Schema representing concise view of the ticket."""
    ticket_id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    created_on = fields.Str(required=True)
    status = fields.Str(required=True)
    message_from_helpdesk = fields.Str()


class DepartmentSchema(Schema):
    """Schema department details"""
    dept_id = fields.Str(required=True)
    dept_name = fields.Str(required=True)


class TicketRaisingSchema(Schema):
    """Schema representing the format needed for raising ticket."""
    d_id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)


class FeedbackSchema(Schema):
    """Schema representing the feedback format"""
    stars = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    description = fields.Str(required=True)
    ticket_id = fields.Str(required=True, dump_only=True)
    created_on = fields.Str(required=True, dump_only=True)


class MessageSchema(Schema):
    created_on = fields.Str(required=True, dump_only=True)
    ticket_id = fields.Str(required=True, dump_only=True)
    message = fields.Str(required=True)


class MessageFromHelpdeskSchema(Schema):
    """Schema representing message from helpdesk"""
    message_from_helpdesk = fields.Str(required=True)


class MessageFromManager(Schema):
    """Schema representing message from manager"""
    message_from_manager = fields.Str(required=True)


class MessageFromHelpdeskInTicket(Schema):
    created_at = fields.Str(required=True)
    message = fields.Str(required=True)


class TicketDetailedView(TicketSchema):
    department = fields.Nested(DepartmentSchema)
    customer = fields.Nested(UserSchema)
    helpdesk_assigned = fields.Nested(UserSchema)
    message_from_helpdesk = UnionField(types=[str, MessageFromHelpdeskInTicket])

from marshmallow import fields, Schema, validate


class UserSchema(Schema):
    full_name = fields.Str(required=True)
    email = fields.Str(required=True)
    phn_num = fields.Str(required=True)


class TicketSchema(Schema):
    t_id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    created_on = fields.Str(required=True)
    status = fields.Str(required=True)
    message_from_helpdesk = fields.Str()


class DepartmentSchema(Schema):
    dept_id = fields.Str(required=True)
    dept_name = fields.Str(required=True)


class TicketCustomerView(TicketSchema):
    department = fields.Nested(DepartmentSchema)
    helpdesk_assigned = fields.Nested(UserSchema)


class TicketHelpdeskView(TicketSchema):
    department = fields.Nested(DepartmentSchema)
    customer = fields.Nested(UserSchema)


class TicketManagerView(TicketSchema):
    department = fields.Nested(DepartmentSchema)
    customer = fields.Nested(UserSchema)
    helpdesk_assigned = fields.Nested(UserSchema)


class TicketRaisingSchema(Schema):
    d_id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)


class FeedbackSchema(Schema):
    stars = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    description = fields.Str(required=True)
    t_id = fields.Str(required=True)
    created_on = fields.Str(required=True, dump_only=True)


class MessageSchema(Schema):
    created_on = fields.Str(required=True, dump_only=True)
    t_id = fields.Str(required=True, dump_only=True)
    message = fields.Str(required=True)

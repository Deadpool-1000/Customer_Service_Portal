from marshmallow import fields, Schema, validate


class TicketSchema(Schema):
    t_id = fields.Str(required=True)
    title = fields.Str(required=True)
    created_on = fields.Str(required=True)
    status = fields.Str(required=True)
    message_from_helpdesk = fields.Str(required=True)


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

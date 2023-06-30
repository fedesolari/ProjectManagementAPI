from marshmallow import Schema, fields, validate, ValidationError

class TicketSchemas(Schema):
    id = fields.Integer()
    description = fields.Str()
    title = fields.Str()
    state = fields.Integer()
    severity = fields.Integer()
    priority = fields.Integer()
    SLA = fields.DateTime()
    product_version_id = fields.Integer()
    resource_name = fields.Str()
    client_id = fields.Integer()
    created_date = fields.DateTime()
    updated_date = fields.DateTime()
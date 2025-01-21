from marshmallow import Schema, fields

#схема для API
class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    sum = fields.Int(required=True)
    commission = fields.Int(required=True)
    status = fields.Str()
    user_id = fields.Int(required=True)

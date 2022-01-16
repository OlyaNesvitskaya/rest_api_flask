from marshmallow import Schema, fields, ValidationError, post_dump, validates, validate
from re import fullmatch
from datetime import datetime

class NamespacedSchema(Schema):
    @post_dump()
    def qet_correct_date(self, data, many):
        if data['created_at']:
            data['created_at'] = datetime.strptime(data['created_at'], "%Y-%m-%d").strftime("%d/%m/%Y")
        if data['updated_at']:
            data['updated_at'] = datetime.strptime(data['updated_at'], "%Y-%m-%d").strftime("%d/%m/%Y")
        return data

class DriverSchema(NamespacedSchema):

    id = fields.Integer(dump_only=True)
    first_name = fields.Str(required=True, validate=[validate.Length(max=20)])
    last_name = fields.Str(required=True, validate=[validate.Length(max=20)])
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)

class VehicleSchema(NamespacedSchema):
    id = fields.Integer(dump_only=True)
    driver_id = fields.Integer()
    driver = fields.Nested(DriverSchema)
    make = fields.Str(required=True)
    model = fields.Str(required=True)
    plate_number = fields.Str(required=True)
    created_at = fields.Str()
    updated_at = fields.Str()

    @validates("plate_number")
    def validate_plate_number(self, value):
        pattern = r'[A-Z]{2}\s\d{4}\s[A-Z]{2}'
        res = fullmatch(pattern, value)
        if res is None:
            raise ValidationError("The field format must correspond to the following format: 'AA 1234 OO'.")


class UserSchema(Schema):
    name = fields.String(required=True, validate=[validate.Length(max=50)])
    email = fields.String(required=True, validate=[validate.Length(max=50)])
    password = fields.String(required=True, validate=[validate.Length(max=50)])


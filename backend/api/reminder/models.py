from api import db
from sqlalchemy import Enum, extract
import enum
from marshmallow import Schema, fields, post_load

class ContactRelation(enum.Enum):
    father = 1
    mother = 2
    brother = 3
    sister = 4
    friend = 5

class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("custom_user.id", ondelete="cascade"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    relation = db.Column(Enum(ContactRelation))


class ContactSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    user_id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    date_of_birth = fields.Date(required=True)
    relation = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return Contact(**data)

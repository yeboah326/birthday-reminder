from api import db
from sqlalchemy import Enum
import enum

class ContactRelation(enum.Enum):
    father = 1
    mother = 2
    brother = 3
    sister = 4
    friend = 5

class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    relation = db.Column(Enum(ContactRelation))
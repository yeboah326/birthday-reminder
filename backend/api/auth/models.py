from werkzeug.security import generate_password_hash, check_password_hash
from api import db, ma
from marshmallow import Schema, fields, post_load


class User(db.Model):
    __tablename__ = "custom_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(10), nullable=False, default="normal")
    contacts = db.relationship("Contact", backref="user", cascade="all, delete", passive_deletes=True)

    @property
    def password(self):
        raise AttributeError("Password is a write-only field")

    @password.setter
    def password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)\

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return f"<User | {self.name} | {self.email}>"

class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    type = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

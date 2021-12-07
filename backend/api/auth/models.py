from werkzeug.security import generate_password_hash, check_password_hash
from api import db, ma

class User(db.Model):
    __table__ = "user"

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False, default="normal")

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

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "type")
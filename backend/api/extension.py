from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
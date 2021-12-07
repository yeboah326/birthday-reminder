from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from dotenv import dotenv_values, load_dotenv
import os

# Load environment variables
load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
ma = Marshmallow()

class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "very-simple-jwt-key")


def create_app(config: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    # Load flask extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    ma.init_app(app)

    # Import blueprints
    from api.auth.controllers import auth
    from api.reminder.controllers import reminder

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(reminder)

    @app.route("/happy")
    def sayHappyBirthday():
        return {"message": "Happy birthday"}

    return app
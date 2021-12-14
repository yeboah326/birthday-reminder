from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from .extension import cors, db, jwt, ma
import os

from api.reminder.utils import get_all_users_contacts_birthdays


# Load environment variables
load_dotenv()

# TODO: Add configutaions for a development database
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
    scheduler = BackgroundScheduler()
    

    # Import blueprints
    from api.auth.controllers import auth
    from api.reminder.controllers import reminder

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(reminder)

    @app.route("/happy")
    def sayHappyBirthday():
        print("Happy birthday")
        return {"message": "Happy birthday"}

    return app

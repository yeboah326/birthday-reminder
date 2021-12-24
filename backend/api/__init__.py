from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from api.config import config_dict
from .extension import cors, db, jwt, ma
import os

from api.reminder.utils import get_all_users_contacts_birthdays


# Load environment variables
load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)

    # Project configurations
    env = os.getenv("FLASK_ENV")
    app.config.from_object(f"api.config.{config_dict[env]}")

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

    @app.errorhandler(ValidationError)
    def register_validation_error(error):
        return jsonify({'message': error.messages}), 400

    return app

# Setup scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    get_all_users_contacts_birthdays,
    timezone='UTC',
    trigger='cron',
    hour=7,
    minute=19,
    second=30
)
scheduler.start()

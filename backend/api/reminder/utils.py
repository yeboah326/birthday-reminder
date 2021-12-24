import datetime
import os
from sqlalchemy import extract
from flask import Flask
from api.config import config_dict
from api import db
from api.reminder.models import Contact, ContactSchema
from api.auth.models import User
contacts_schema = ContactSchema(many=True)

def get_all_users_contacts_birthdays():
    app = Flask(__name__)
    env = os.getenv("FLASK_ENV")
    app.config.from_object(f"api.config.{config_dict[env]}")
    db.init_app(app)

    with app.app_context():

        # Get all registered normal users
        try:
            users = db.session.query(User).filter_by(type="normal").all()
        except:
            print("Didnt happen")
        # Get today's date
        today = datetime.date.today()

        # Get all the contacts for the users and
        # check if their date of birth is today
        birthdays = {}

        for user in users:
            birthdays[user.id] = contacts_schema.dump(
                db.session.query(Contact)
                .filter(
                    extract("day", Contact.date_of_birth) == today.day,
                    extract("month", Contact.date_of_birth) == today.month,
                    Contact.user_id==user.id
                )
                .all()
            )
        print(birthdays)
        # for user, contacts in birthdays.items():
        #     print(user)
        #     print(contacts)

        if len(birthdays) == 0:
            print("No birthday today")

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "Sepetember",
    "October",
    "November",
    "December"
]

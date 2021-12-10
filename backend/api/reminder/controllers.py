from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api import db
from api.reminder.models import Contact, ContactSchema
from marshmallow import ValidationError
from sqlalchemy import extract
import datetime

reminder = Blueprint("reminder", __name__, url_prefix="/api/reminder")

# contact schema
contact_schema = ContactSchema(unknown="EXCLUDE")
contacts_schema = ContactSchema(many=True, unknown="EXCLUDE")


@reminder.get("/hello")
def reminder_hello():
    return {"message": "Reminder blueprint working"}


@reminder.post("/contact")
@jwt_required()
def reminder_create_contact():

    # Retrieve the data
    data = request.json

    try:
        # Create a new instance of the contact
        new_contact = contact_schema.load(data)
        new_contact.user_id = get_jwt_identity()

        # Save the contact
        db.session.add(new_contact)
        db.session.commit()

        return {"message": "Contact created successfully"}, 200

    except ValidationError as err:
        return {"message": "Bad data format"}, 400


@reminder.get("/contact")
@jwt_required()
def reminder_get_all_contacts():
    # Get the user id
    user_id = get_jwt_identity()

    # Get all user contacts
    contacts = Contact.query.filter_by(user_id=user_id)

    # Serialize the data
    return jsonify(contacts_schema.dump(contacts)), 200


@reminder.get("/birthday/upcoming")
@jwt_required()
def reminder_get_all_upcoming_birthdays():
    # Get today's date
    today = datetime.date.today()

    # Find all users who birthdays are after today for the rest of the year
    upcoming = (
        db.session.query(Contact)
        .filter(
            extract("day", Contact.date_of_birth) >= today.day,
            extract("month", Contact.date_of_birth) >= today.month,
            user_id=get_jwt_identity(),
        )
        .order_by(
            extract("day", Contact.date_of_birth),
            extract("month", Contact.date_of_birth),
            extract("year", Contact.date_of_birth),
        )
        .all()
    )
    
    return jsonify(contacts_schema.dump(upcoming)), 200


@reminder.get("/birthday/current")
@jwt_required()
def reminder_get_all_birthdays_current_year():
    # Get today's date
    today = datetime.date.today()

    # Find all contacts
    upcoming = (
        db.session.query(Contact)
        .filter(user_id=get_jwt_identity())
        .order_by(
            extract("day", Contact.date_of_birth),
            extract("month", Contact.date_of_birth),
            extract("year", Contact.date_of_birth),
        )
        .all()
    )

    return jsonify(contacts_schema.dump(upcoming)), 200

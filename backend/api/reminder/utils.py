import datetime
from sqlalchemy import extract
from api import db
from api.reminder.models import Contact, ContactSchema
from api.auth.models import User

contacts_schema = ContactSchema(many=True)

def get_all_users_contacts_birthdays():    
    # Get all registered normal users
    users = db.session.query(User).filter_by(type="normal").all()

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

    for user, contacts in birthdays.items():
        print(user)
        print(contacts)
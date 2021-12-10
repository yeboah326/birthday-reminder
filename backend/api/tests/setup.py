from api import db
from api.auth.models import User, UserSchema
from api.reminder.models import Contact, ContactSchema
from api.tests.data import (
    super_user,
    test_user_1,
    test_user_2,
    valid_contacts
)

# Setting up the schema for the models
user_schema = UserSchema(dump_only=["id"], unknown="EXCLUDE")
users_schema = UserSchema(many=True, dump_only=["id"], unknown="EXCLUDE")
contact_schema = ContactSchema(unknown="EXCLUDE")


def reset_db():
    User.query.delete()
    Contact.query.delete()
    db.session.commit()

# Creating Users
def create_super_user(client):
    # Create super user
    client.post(
        "/api/auth/users",
        json=super_user
    )

    super = User.find_by_email(super_user['email'])

    # Login the super user
    response = client.post(
        "/api/auth/login",
        json={"email": super_user['email'], "password": super_user['password']}
    )

    return response.json



def create_one_test_user(client):
    # Create first user
    client.post(
        "/api/auth/users",
        json=test_user_1
    )

    # Login the  user
    response = client.post(
        "/api/auth/login",
        json={"email": test_user_1['email'], "password": test_user_1['password']}
    )

    return response.json



def create_two_test_users(client):
    # Create first user
    client.post(
        "/api/auth/users",
        json=test_user_1
    )

    # Create the second user
    client.post(
        "/api/auth/users",
        json=test_user_2
    )

    users = User.query.all()

    return users_schema.dump(users)


# Contacts
def create_one_contact(client, user):
    response = client.post(
        "api/reminder/contact",
        json=valid_contacts[0],
        headers={"Authorization": f"Bearer {user['token']}"},
    )

def create_multiple_contacts(client, user):
    for i in range(len(valid_contacts)):
        response = client.post(
            "api/reminder/contact",
            json=valid_contacts[i],
            headers={"Authorization": f"Bearer {user['token']}"},
        )

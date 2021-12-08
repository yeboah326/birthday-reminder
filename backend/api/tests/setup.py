from api import db
from api.auth.models import User, UserSchema
from api.reminder.models import Contact
from api.tests.data import (
    test_user_1,
    test_user_2
)

# Setting up the schema for the models
user_schema = UserSchema(dump_only=["id"], unknown="EXCLUDE")
users_schema = UserSchema(many=True, dump_only=["id"], unknown="EXCLUDE")


def reset_db():
    User.query.delete()
    Contact.query.delete()
    db.session.commit()

def create_one_test_user(client):
    # Create first user
    client.post(
        "/api/auth/users",
        json=test_user_1
    )

    user = User.find_by_email(test_user_1["email"])

    return user_schema.dump(user)

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

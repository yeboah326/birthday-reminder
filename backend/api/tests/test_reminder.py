from api.reminder.models import Contact
from api.tests.setup import reset_db, create_one_test_user, create_multiple_contacts
from api.tests.data import valid_contacts, invalid_contact


def test_reminder_create_contact(client):
    # Reset the database
    reset_db()

    user = create_one_test_user(client)

    response = client.post(
        "api/reminder/contact",
        json=valid_contacts[0],
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    contact = Contact.query.filter_by(name=valid_contacts[0]["name"])

    assert response.status_code == 200
    assert response.json["message"] == "Contact created successfully"
    assert contact != None

    # Reset database
    reset_db()


def test_reminder_create_contact_bad_data(client):
    # Reset the database
    reset_db()

    user = create_one_test_user(client)

    response = client.post(
        "api/reminder/contact",
        json=invalid_contact[0],
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    assert response.status_code == 400
    assert response.json["message"] == "Bad data format"

    # Reset the database
    reset_db()

def test_reminder_get_all_contacts(client):
    # Reset the database
    reset_db()

    user = create_one_test_user(client)

    create_multiple_contacts(client, user)

    response = client.get(
        "/api/reminder/contact",
        headers={"Authorization": f"Bearer {user['token']}"}
    )

    assert response.status_code == 200
    assert len(response.json) == 4

    # Reset the database
    reset_db()

def test_reminder_get_all_upcoming_birthdays(client):
    # Reset the database
    reset_db()

    user = create_one_test_user(client)

    create_multiple_contacts(client, user)

    response = client.get(
        "/api/reminder/birthday/upcoming",
        headers={"Authorization": f"Bearer {user['token']}"}
    )
    print(response.json)
    assert 1 == 2

    # Reset the database
    # reset_db()

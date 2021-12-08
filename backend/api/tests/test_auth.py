from api.tests.data import (
    test_user_1,
    test_user_2
)
from api.tests.setup import (
    reset_db,
    create_one_test_user,
    create_two_test_users
)

def test_auth_hello(client):
    response = client.get(
        "api/auth/hello"
    )

    assert response.json['message'] == 'Auth blueprint is working'

def test_auth_create_new_user(client):

    # Reset the database before the test begins
    reset_db()

    response = client.post(
        "/api/auth/users",
        json=test_user_1
    )

    assert response.status_code == 200
    assert response.json

    # Reset the database after running all tests
    reset_db()

def test_auth_get_all_users(client):
    # Reset the database before the test begins
    reset_db()

    create_two_test_users(client)

    response = client.get(
        "/api/auth/users"
    )

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['email'] == test_user_1['email']
    assert response.json[1]['email'] == test_user_2['email']

    # Reset the database before the test begins
    reset_db()


def test_auth_get_user_by_id(client):
    # Reset the database before the test begins
    reset_db()

    user = create_one_test_user(client)

    response = client.get(
        f"/api/auth/users/{user['id']}"
    )

    assert response.status_code == 200
    assert response.json['id'] == user['id']
    assert response.json['email'] == user['email']
    assert response.json['name'] == user['name']

    # Reset the database before the test begins
    reset_db()

from api.tests.data import test_user_1, test_user_2
from api.tests.setup import (
    reset_db,
    create_super_user,
    create_one_test_user,
    create_two_test_users,
)


def test_auth_hello(client):
    response = client.get("api/auth/hello")

    assert response.json["message"] == "Auth blueprint is working"


def test_auth_create_new_user(client):

    # Reset the database before the test begins
    reset_db()

    response = client.post("/api/auth/users", json=test_user_1)

    assert response.status_code == 200
    assert response.json

    # Reset the database after running all tests
    reset_db()


def test_auth_login_user(client):

    # Reset the database before the test begins
    reset_db()

    # Create a single user
    create_one_test_user(client)

    response = client.post(
        "/api/auth/login",
        json={"email": test_user_1["email"], "password": test_user_1["password"]},
    )

    assert response.status_code == 200
    assert response.json["token"]
    assert response.json["user_type"] == "normal"


def test_auth_get_all_users(client):
    # Reset the database before the test begins
    reset_db()

    # Create super user
    super = create_super_user(client)

    create_two_test_users(client)

    response = client.get(
        "/api/auth/users", headers={"Authorization": f"Bearer {super['token']}"}
    )

    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json[1]["email"] == test_user_1["email"]
    assert response.json[2]["email"] == test_user_2["email"]

    # Reset the database before the test begins
    reset_db()


def test_auth_get_user_by_id(client):
    # Reset the database before the test begins
    reset_db()

    # Create super user
    super = create_super_user(client)
    print(super)
    user = create_one_test_user(client)

    response = client.get(
        f"/api/auth/users/{user['id']}",
        headers={"Authorization": f"Bearer {super['token']}"},
    )

    assert response.status_code == 200
    assert response.json["id"] == user["id"]
    assert response.json["email"] == user["email"]
    assert response.json["name"] == user["name"]

    # Reset the database before the test begins
    reset_db()

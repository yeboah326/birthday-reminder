from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from api.auth.models import User, UserSchema
from api import db

auth = Blueprint("auth", __name__, url_prefix="/api/auth")

# Schemas
user_schema = UserSchema(dump_only=["id"], unknown="EXCLUDE")
users_schema = UserSchema(many=True, dump_only=["id"], unknown="EXCLUDE")

@auth.get("/hello")
def auth_hello():
    return {"message": "Auth blueprint is working"}, 200


@auth.post("/users")
def auth_create_new_user():
    data = request.json

    # Load the user instance from the data
    new_user = user_schema.load(data)

    # Set the password for the user
    new_user.password = data['password']

    # Save data to the database
    db.session.add(new_user)
    db.session.commit()

    return {"message": f"New user {new_user.name} created"}, 200

@auth.post("/login")
def auth_login_user():
    # Collect data from the json post body
    data = request.json

    # Check whether user with given email exists
    user: User = User.find_by_email(data['email'])

    if user:
        password_correct = user.check_password(data['password'])
        if password_correct:
            token = create_access_token(identity=user.id)
            return {"token": token, "user_type": f"{user.type}"}, 200
        return {"message": "Wrong user credentials"}, 400
    return {"message": "A user with the given credentials does not exist"}, 404

@auth.get("/users")
@jwt_required()
def auth_get_all_users():
    all_users = User.query.all()
    return jsonify(users_schema.dump(all_users)), 200

@auth.get("/users/<id>")
@jwt_required()
def auth_get_user_by_id(id):
    user = User.find_by_id(id)
    return user_schema.dump(user), 200

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from api.auth.models import User, UserSchema

auth = Blueprint("auth", __name__, url_prefix="/api/auth")

# Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@auth.get("/hello")
def auth_hello():
    return {"message": "Auth blueprint working"}


@auth.post("/new_user")
def auth_create_new_user():
    pass

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
def get_all_users():
    all_users = User.all()
    return users_schema.dump(all_users)

@auth.get("/users/<id>")
def get_user_by_id(id):
    user = User.find_by_id(id)
    return user_schema.dump(user)
from flask import Blueprint

reminder = Blueprint("reminder", __name__, url_prefix="/api/reminder")

@reminder.get("/hello")
def reminder_hello():
    return {"message": "Reminder blueprint working"}
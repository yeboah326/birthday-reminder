from flask.cli import FlaskGroup
from api import create_app, db
from api.reminder.utils import get_all_users_contacts_birthdays

cli = FlaskGroup(create_app("BaseConfig"))

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

cli.command("check_birthdays")(get_all_users_contacts_birthdays)

if __name__ == "__main__":
    cli()
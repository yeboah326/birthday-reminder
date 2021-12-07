from flask.cli import FlaskGroup
from api import create_app, db

cli = FlaskGroup(create_app("BaseConfig"))

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()
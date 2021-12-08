import pytest
from api import create_app

# Change to use a development database for testing
@pytest.fixture
def app():
    flask_app = create_app("BaseConfig")
    flask_app.app_context().push()
    yield flask_app

@pytest.fixture
def client(app):
    yield app.test_client()
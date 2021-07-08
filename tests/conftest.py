import pytest
from api import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()

    from api.models import db

    with app.app.app_context():
        db.create_all()

    yield app


@pytest.fixture(scope="session")
def client(app):
    with app.app.test_client() as client:
        yield client

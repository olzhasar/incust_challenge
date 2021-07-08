import pytest
from api import create_app


@pytest.fixture(scope="session")
def app():
    connexion_app = create_app(testing=True)
    app = connexion_app.app

    from api.models import db

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    with app.test_client() as client:
        yield client

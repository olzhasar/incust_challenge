import pytest
from api import create_app
from api.models import User, db


@pytest.fixture(scope="session")
def app():
    connexion_app = create_app(testing=True)
    app = connexion_app.app

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    with app.test_client() as client:
        yield client


def _create_user(name: str, password: str):
    user = User(name=name)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture(scope="session")
def user_1():
    user = _create_user("user_1", "123qweasd")
    yield user


@pytest.fixture(scope="session")
def user_2():
    user = _create_user("user_2", "zxcasd123")
    yield user

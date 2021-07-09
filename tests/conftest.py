import pytest
from api import create_app
from api.models import User, db
from flask_jwt_extended import create_access_token


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


def _create_user(username: str, password: str, avatar_url: str = None):
    user = User(username=username, avatar_url=avatar_url)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture(scope="session")
def user_1():
    user = _create_user("user_1", "123qweasd", "http://example.com/avatar.jpg")
    yield user


@pytest.fixture(scope="session")
def user_2():
    user = _create_user("user_2", "zxcasd123", "http://example.com/avatar.jpg")
    yield user


@pytest.fixture(scope="session")
def as_user_1(app, user_1):
    token = create_access_token(identity=user_1)

    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        yield client

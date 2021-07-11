import os

import pytest
from api import create_app
from api.config import Config
from api.models import db
from flask_jwt_extended import create_access_token

from tests import factories


@pytest.fixture(scope="session", autouse=True)
def app():
    connexion_app = create_app(testing=True)
    app = connexion_app.app

    with app.app_context():
        yield app


@pytest.fixture(autouse=True)
def session(app):
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    with app.test_client() as client:
        yield client


def _create_user(username: str, password: str):
    avatar = f"{username}.jpg"

    user = factories.UserFactory(username=username)
    user.set_password("123qweasd")
    user.avatar = avatar

    filepath = os.path.join(Config.MEDIA_DIR, avatar)

    with open(filepath, "wb") as f:
        f.write(b"image")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def user():
    user = _create_user("user", "123qweasd")
    yield user


@pytest.fixture
def other_user():
    user = _create_user("other_user", "zxcasd123")
    yield user


@pytest.fixture
def as_user(app, user):
    token = create_access_token(identity=user)

    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        yield client


@pytest.fixture
def as_other_user(app, other_user):
    token = create_access_token(identity=other_user)

    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        yield client


@pytest.fixture
def product_list(user):
    obj = factories.ProductListFactory(user=user)

    db.session.add(obj)
    db.session.commit()

    return obj


@pytest.fixture
def product(product_list):
    obj = factories.ProductFactory(product_list=product_list)

    db.session.add(obj)
    db.session.commit()

    return obj


@pytest.fixture
def price(product):
    obj = factories.ProductPriceFactory(product=product)

    db.session.add(obj)
    db.session.commit()

    return obj

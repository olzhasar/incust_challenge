import pytest
from api import create_app
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


def _create_user(username: str, password: str, avatar_url: str = None):
    user = factories.UserFactory(username=username, avatar_url=avatar_url)
    user.set_password("123qweasd")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def user_1():
    user = _create_user("user_1", "123qweasd", "http://example.com/avatar.jpg")
    yield user


@pytest.fixture
def user_2():
    user = _create_user("user_2", "zxcasd123", "http://example.com/avatar.jpg")
    yield user


@pytest.fixture
def as_user_1(app, user_1):
    token = create_access_token(identity=user_1)

    with app.test_client() as client:
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        yield client


@pytest.fixture
def product_list(user_1):
    obj = factories.ProductListFactory(user=user_1)

    db.session.add(obj)
    db.session.commit()

    return obj


@pytest.fixture
def product(product_list):
    obj = factories.ProductFactory(product_list=product_list)

    db.session.add(obj)
    db.session.flush()

    prices = factories.ProductPriceFactory.create_batch(2, product=obj)

    db.session.add_all(prices)
    db.session.commit()

    return obj

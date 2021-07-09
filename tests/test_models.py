import pytest
from api.models import User, db

from tests import factories


@pytest.fixture
def user():
    user = factories.UserFactory()
    user.set_password("123qweasd")

    db.session.add(user)
    db.session.commit()

    return user


def test_user_persists(user):
    from_db = User.query.filter_by(username=user.username).one_or_none()

    assert from_db


def test_user_password(user):
    assert not user.check_password("zxcasd123")
    assert user.check_password("123qweasd")

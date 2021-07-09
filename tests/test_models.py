from api.models import User


def test_user(client, user_1):
    user = User.query.first()

    assert user == user_1
    assert not user.check_password("zxcasd123")
    assert user.check_password("123qweasd")

from api.models import User


class TestLogin:
    url = "/auth/login"

    def test_login_ok(self, client, user_1):
        response = client.post(
            self.url,
            json={
                "username": user_1.username,
                "password": "123qweasd",
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json

    def test_login_wrong_username(self, client, user_1):
        response = client.post(
            self.url,
            json={
                "username": "wrong_user",
                "password": "wrong_password",
            },
        )

        assert response.status_code == 401

    def test_login_wrong_password(self, client, user_1, user_2):
        response = client.post(
            self.url,
            json={
                "username": user_1.username,
                "password": "zxcasd123",
            },
        )

        assert response.status_code == 401


class TestSignup:
    url = "/auth/signup"

    def test_signup_ok(self, client):
        response = client.post(
            self.url,
            json={
                "username": "new_user",
                "password": "123qweasd",
            },
        )

        assert response.status_code == 201

        user = User.query.filter_by(username="new_user").first()
        assert user is not None
        assert user.check_password("123qweasd")

    def test_signup_username_taken(self, client, user_1):
        response = client.post(
            self.url,
            json={
                "username": user_1.username,
                "password": "123qweasd",
            },
        )

        assert response.status_code == 400
        assert response.json == {"msg": "Username is already taken"}

from api.models import User


class TestLogin:
    url = "/auth/login"

    def test_ok(self, client, user_1):
        response = client.post(
            self.url,
            json={
                "username": user_1.username,
                "password": "123qweasd",
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json

    def test_wrong_username(self, client, user_1):
        response = client.post(
            self.url,
            json={
                "username": "wrong_user",
                "password": "wrong_password",
            },
        )

        assert response.status_code == 401
        assert response.json["detail"] == "Invalid credentials"

    def test_wrong_password(self, client, user_1, user_2):
        response = client.post(
            self.url,
            json={
                "username": user_1.username,
                "password": "zxcasd123",
            },
        )

        assert response.status_code == 401
        assert response.json["detail"] == "Invalid credentials"


class TestSignup:
    url = "/auth/signup"

    def test_ok(self, client):
        response = client.post(
            self.url,
            json={
                "username": "new_user",
                "password": "123qweasd",
            },
        )

        assert response.status_code == 201

        user = User.query.filter_by(username="new_user").one_or_none()
        assert user is not None
        assert user.check_password("123qweasd")

    def test_username_taken(self, client, user_1):
        response = client.post(
            self.url,
            json={
                "username": user_1.username,
                "password": "123qweasd",
            },
        )

        assert response.status_code == 400
        assert response.json["detail"] == "Username is already taken"


class TestUpdate:
    url = "/auth/profile"

    def test_unauthorized(self, client):
        response = client.put(
            self.url,
            json={
                "username": "new_username",
                "password": "new_password",
            },
        )

        assert response.status_code == 401

    def test_ok(self, client, user_1, as_user_1):
        response = as_user_1.put(
            self.url,
            json={
                "username": "new_username",
                "avatar_url": "https://example.com/new_image.jpg",
            },
        )

        assert response.status_code == 200

        from_db = User.query.filter_by(username="new_username").one_or_none()

        assert from_db is not None
        assert from_db.username == "new_username"
        assert from_db.avatar_url == "https://example.com/new_image.jpg"

    def test_change_username_to_existing(self, client, user_1, user_2, as_user_1):
        response = as_user_1.put(
            self.url,
            json={
                "username": user_2.username,
                "avatar_url": "https://example.com/new_image.jpg",
            },
        )

        assert response.status_code == 400
        assert response.json["detail"] == "Username is already taken"

        from_db = User.query.filter_by(id=user_1.id).one_or_none()
        assert from_db.username != user_2.username

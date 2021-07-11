import os
from io import BytesIO

from api.models import User


class TestLogin:
    url = "/auth/login"

    def test_ok(self, client, user):
        response = client.post(
            self.url,
            json={
                "username": user.username,
                "password": "123qweasd",
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json

    def test_wrong_username(self, client, user):
        response = client.post(
            self.url,
            json={
                "username": "wrong_user",
                "password": "wrong_password",
            },
        )

        assert response.status_code == 401
        assert response.json["detail"] == "Invalid credentials"

    def test_wrong_password(self, client, user, other_user):
        response = client.post(
            self.url,
            json={
                "username": user.username,
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
            data={
                "username": "new_user",
                "password": "123qweasd",
                "avatar": (BytesIO(b"avatar.jpg"), "avatar.jpg"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 201

        user = User.query.filter_by(username="new_user").one_or_none()
        assert user is not None
        assert user.check_password("123qweasd")
        assert user.avatar == "avatar.jpg"

        assert response.json == {
            "id": user.id,
            "username": user.username,
            "avatar": "/media/avatar.jpg",
        }

        assert os.path.exists(user.avatar_filepath)

    def test_username_taken(self, client, user):
        response = client.post(
            self.url,
            data={
                "username": user.username,
                "password": "123qweasd",
                "avatar": (BytesIO(b"avatar.jpg"), "avatar.jpg"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 400
        assert response.json["detail"] == "Username is already taken"


class TestUpdate:
    url = "/auth/profile"

    def test_unauthorized(self, client):
        response = client.put(
            self.url,
            data={
                "username": "new_username",
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 401

    def test_ok(self, client, user, as_user):
        old_avatar_path = user.avatar_filepath
        assert os.path.exists(old_avatar_path)

        response = as_user.put(
            self.url,
            data={
                "username": "new_username",
                "avatar": (BytesIO(b"new_avatar.jpg"), "new_avatar.jpg"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 200

        from_db = User.query.filter_by(username="new_username").one_or_none()

        assert from_db is not None
        assert from_db.username == "new_username"
        assert from_db.avatar == "new_avatar.jpg"

        assert os.path.exists(from_db.avatar_filepath)
        assert not os.path.exists(old_avatar_path)

        assert response.json == {
            "id": from_db.id,
            "username": from_db.username,
            "avatar": "/media/new_avatar.jpg",
        }

    def test_change_username_to_existing(self, client, user, other_user, as_user):
        response = as_user.put(
            self.url,
            data={
                "username": other_user.username,
                "avatar": (BytesIO(b"new_avatar.jpg"), "new_avatar.jpg"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 400
        assert response.json["detail"] == "Username is already taken"

        from_db = User.query.filter_by(id=user.id).one_or_none()
        assert from_db.username != other_user.username

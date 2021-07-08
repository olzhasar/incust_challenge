def test_login(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "test",
            "password": "test",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json

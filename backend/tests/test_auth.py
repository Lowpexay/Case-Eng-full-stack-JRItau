def test_register_and_login(client):
    # Register
    resp = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "Secret@123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "testuser"

    # Login
    resp = client.post("/auth/login", json={
        "username": "testuser",
        "password": "Secret@123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_invalid_credentials(client):
    client.post("/auth/register", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "Pass@1234",
    })
    resp = client.post("/auth/login", json={
        "username": "user2",
        "password": "wrongpass",
    })
    assert resp.status_code == 401


def test_duplicate_username(client):
    client.post("/auth/register", json={
        "username": "dupeuser",
        "email": "dupe@example.com",
        "password": "Pass@1234",
    })
    resp = client.post("/auth/register", json={
        "username": "dupeuser",
        "email": "dupe2@example.com",
        "password": "Pass@1234",
    })
    assert resp.status_code == 400


def test_register_with_weak_password(client):
    resp = client.post("/auth/register", json={
        "username": "weakpassuser",
        "email": "weak@example.com",
        "password": "password123",
    })
    assert resp.status_code == 422
    payload = resp.json()
    assert payload["detail"] == "Erro de validação."
    assert any(error["field"] == "body.password" for error in payload["errors"])

import pytest


def _register_and_login(client, username="player1", email="player1@example.com", password="Pass@1234"):
    client.post("/auth/register", json={"username": username, "email": email, "password": password})
    resp = client.post("/auth/login", json={"username": username, "password": password})
    return resp.json()["access_token"]


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_start_game(client):
    token = _register_and_login(client, "gamer1", "gamer1@e.com")
    resp = client.post("/games/start", headers=_auth_headers(token))
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["max_attempts"] == 10


def test_submit_invalid_attempt(client):
    token = _register_and_login(client, "gamer2", "gamer2@e.com")
    resp = client.post("/games/start", headers=_auth_headers(token))
    game_id = resp.json()["id"]

    resp = client.post(f"/games/{game_id}/attempt", headers=_auth_headers(token), json={"guess": "XYZ"})
    # Pydantic rejects too-short guess with 422; service logic rejects invalid chars with 400
    assert resp.status_code in (400, 422)


def test_full_game_loss(client):
    """Player exhausts all attempts and loses."""
    token = _register_and_login(client, "gamer3", "gamer3@e.com")
    resp = client.post("/games/start", headers=_auth_headers(token))
    game_id = resp.json()["id"]

    for _ in range(10):
        r = client.post(f"/games/{game_id}/attempt", headers=_auth_headers(token), json={"guess": "AAAA"})
        assert r.status_code == 200

    data = r.json()
    assert data["is_finished"] is True


def test_attempt_on_finished_game(client):
    token = _register_and_login(client, "gamer4", "gamer4@e.com")
    resp = client.post("/games/start", headers=_auth_headers(token))
    game_id = resp.json()["id"]

    for _ in range(10):
        client.post(f"/games/{game_id}/attempt", headers=_auth_headers(token), json={"guess": "AAAA"})

    resp = client.post(f"/games/{game_id}/attempt", headers=_auth_headers(token), json={"guess": "BBBB"})
    assert resp.status_code == 400


def test_get_game_state(client):
    token = _register_and_login(client, "gamer5", "gamer5@e.com")
    resp = client.post("/games/start", headers=_auth_headers(token))
    game_id = resp.json()["id"]

    client.post(f"/games/{game_id}/attempt", headers=_auth_headers(token), json={"guess": "ABCD"})

    resp = client.get(f"/games/{game_id}", headers=_auth_headers(token))
    assert resp.status_code == 200
    data = resp.json()
    assert data["attempt_count"] == 1


def test_ranking(client):
    token = _register_and_login(client, "ranker1", "ranker1@e.com")
    resp = client.get("/ranking/", headers=_auth_headers(token))
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

import uuid


def unique_username(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def register_user(client, username: str, password: str = "123456"):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )


def login_user(client, username: str, password: str = "123456"):
    return client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )


def test_register_success(client):
    username = unique_username("test_register_success")

    response = register_user(client, username)

    assert response.status_code in (200, 201)

    data = response.json()
    assert data["username"] == username
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_username(client):
    username = unique_username("test_register_duplicate")

    first_response = register_user(client, username)
    second_response = register_user(client, username)

    assert first_response.status_code in (200, 201)
    assert second_response.status_code == 400


def test_login_success(client):
    username = unique_username("test_login_success")
    password = "123456"

    register_response = register_user(client, username, password)
    assert register_response.status_code in (200, 201)

    login_response = login_user(client, username, password)

    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"].lower() == "bearer"


def test_login_wrong_password(client):
    username = unique_username("test_login_wrong_password")

    register_response = register_user(client, username, "123456")
    assert register_response.status_code in (200, 201)

    login_response = login_user(client, username, "wrong-password")

    assert login_response.status_code == 401


def test_users_me_requires_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_users_me_with_token(client):
    username = unique_username("test_users_me")
    password = "123456"

    register_response = register_user(client, username, password)
    assert register_response.status_code in (200, 201)

    login_response = login_user(client, username, password)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == username
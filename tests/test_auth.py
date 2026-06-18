import uuid

from app.models.user import User


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


def promote_to_admin(db_session, username: str):
    user = db_session.query(User).filter(User.username == username).one()
    user.role = "ADMIN"
    db_session.commit()
    db_session.refresh(user)
    return user


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


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


def test_admin_can_list_request_logs(client, db_session):
    username = unique_username("test_admin_request_logs")

    register_response = register_user(client, username)
    assert register_response.status_code in (200, 201)

    promote_to_admin(db_session, username)

    login_response = login_user(client, username)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    users_me_response = client.get("/users/me", headers=auth_headers(token))
    assert users_me_response.status_code == 200

    response = client.get("/admin/request-logs", headers=auth_headers(token))

    assert response.status_code == 200
    logs = response.json()
    assert any(log["path"] == "/users/me" and log["user_id"] is not None for log in logs)


def test_login_bruteforce_creates_security_event(client, db_session):
    username = unique_username("test_bruteforce")
    admin_username = unique_username("test_bruteforce_admin")

    assert register_user(client, username, "correct-password").status_code in (200, 201)
    assert register_user(client, admin_username).status_code in (200, 201)
    promote_to_admin(db_session, admin_username)

    admin_login_response = login_user(client, admin_username)
    assert admin_login_response.status_code == 200
    admin_token = admin_login_response.json()["access_token"]

    for _ in range(5):
        response = login_user(client, username, "wrong-password")
        assert response.status_code == 401

    response = client.get("/admin/security-events", headers=auth_headers(admin_token))

    assert response.status_code == 200
    events = response.json()
    assert any(
        event["event_type"] == "LOGIN_BRUTE_FORCE"
        and event["risk_level"] == "MEDIUM"
        for event in events
    )

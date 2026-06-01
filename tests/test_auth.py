from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_register_login_and_me():
    register_response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret123"},
    )

    assert register_response.status_code == 201
    register_data = register_response.json()
    assert register_data["username"] == "alice"
    assert "password_hash" not in register_data

    duplicate_response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    assert duplicate_response.status_code == 400

    login_response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "secret123"},
    )

    assert login_response.status_code == 200
    token_data = login_response.json()
    assert token_data["token_type"] == "bearer"
    assert token_data["access_token"]

    me_response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token_data['access_token']}"},
    )

    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["username"] == "alice"
    assert me_data["is_active"] is True
    assert "password_hash" not in me_data


def test_login_rejects_wrong_password():
    client.post(
        "/auth/register",
        json={"username": "bob", "password": "secret123"},
    )

    response = client.post(
        "/auth/login",
        data={"username": "bob", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_me_rejects_missing_token():
    response = client.get("/users/me")

    assert response.status_code == 401

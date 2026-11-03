from datetime import datetime, timezone

import pytest
from fastapi import HTTPException
from jose import jwt

import auth


def test_hash_password_does_not_store_plain_text():
    hashed = auth.hash_password("unit-test-password")

    assert hashed != "unit-test-password"
    assert hashed.startswith("$2")


def test_verify_password_accepts_matching_password():
    hashed = auth.hash_password("unit-test-password")

    assert auth.verify_password("unit-test-password", hashed) is True


def test_verify_password_rejects_non_matching_password():
    hashed = auth.hash_password("unit-test-password")

    assert auth.verify_password("different-password", hashed) is False


def test_create_token_preserves_claims(monkeypatch):
    monkeypatch.setattr(auth, "SECRET_KEY", "unit-test-secret")

    token = auth.create_token({"user_id": 7, "username": "tester", "role": "Administrator"})
    payload = jwt.decode(token, "unit-test-secret", algorithms=[auth.ALGORITHM])

    assert payload["user_id"] == 7
    assert payload["username"] == "tester"
    assert payload["role"] == "Administrator"


def test_create_token_adds_future_expiration(monkeypatch):
    monkeypatch.setattr(auth, "SECRET_KEY", "unit-test-secret")

    token = auth.create_token({"user_id": 7})
    payload = jwt.decode(token, "unit-test-secret", algorithms=[auth.ALGORITHM])

    assert datetime.fromtimestamp(payload["exp"], timezone.utc) > datetime.now(timezone.utc)


def test_get_current_user_returns_token_identity(monkeypatch):
    monkeypatch.setattr(auth, "SECRET_KEY", "unit-test-secret")
    token = jwt.encode(
        {"user_id": 7, "username": "tester", "role": "Warehouse Staff"},
        "unit-test-secret",
        algorithm=auth.ALGORITHM,
    )

    assert auth.get_current_user(token) == {
        "user_id": 7,
        "username": "tester",
        "role": "Warehouse Staff",
    }


def test_get_current_user_rejects_token_without_user_id(monkeypatch):
    monkeypatch.setattr(auth, "SECRET_KEY", "unit-test-secret")
    token = jwt.encode({"username": "tester"}, "unit-test-secret", algorithm=auth.ALGORITHM)

    with pytest.raises(HTTPException) as error:
        auth.get_current_user(token)

    assert error.value.status_code == 401


def test_get_current_user_rejects_invalid_token():
    with pytest.raises(HTTPException) as error:
        auth.get_current_user("not-a-jwt")

    assert error.value.status_code == 403


@pytest.mark.parametrize(
    ("guard", "role"),
    [
        (auth.require_admin, "Administrator"),
        (auth.require_warehouse, "Administrator"),
        (auth.require_warehouse, "Warehouse Staff"),
        (auth.require_logistics, "Administrator"),
        (auth.require_logistics, "Logistics Staff"),
    ],
)
def test_role_guards_accept_authorized_roles(guard, role):
    current_user = {"user_id": 7, "username": "tester", "role": role}

    assert guard(current_user) is current_user


@pytest.mark.parametrize(
    ("guard", "role"),
    [
        (auth.require_admin, "Warehouse Staff"),
        (auth.require_warehouse, "Logistics Staff"),
        (auth.require_logistics, "Warehouse Staff"),
    ],
)
def test_role_guards_reject_unauthorized_roles(guard, role):
    with pytest.raises(HTTPException) as error:
        guard({"user_id": 7, "username": "tester", "role": role})

    assert error.value.status_code == 403


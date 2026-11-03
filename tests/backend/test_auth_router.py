from types import SimpleNamespace
from unittest.mock import Mock

import psycopg2
import pytest
from fastapi import HTTPException

from routers import auth as auth_router


def connection_with_user(user):
    cursor = Mock()
    cursor.fetchone.return_value = user
    connection = Mock()
    connection.cursor.return_value = cursor
    return connection, cursor


def test_login_returns_bearer_token_for_valid_credentials(monkeypatch):
    connection, cursor = connection_with_user((7, "tester", "stored-hash", "Administrator"))
    monkeypatch.setattr(auth_router, "get_connection", Mock(return_value=connection))
    monkeypatch.setattr(auth_router, "verify_password", Mock(return_value=True))
    create_token = Mock(return_value="signed-token")
    monkeypatch.setattr(auth_router, "create_token", create_token)

    result = auth_router.login(SimpleNamespace(username="tester", password="plain-password"))

    assert result == {"access_token": "signed-token", "token_type": "bearer"}
    create_token.assert_called_once_with(
        {"user_id": 7, "username": "tester", "role": "Administrator"}
    )
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_login_rejects_unknown_user(monkeypatch):
    connection, cursor = connection_with_user(None)
    monkeypatch.setattr(auth_router, "get_connection", Mock(return_value=connection))

    with pytest.raises(HTTPException) as error:
        auth_router.login(SimpleNamespace(username="missing", password="plain-password"))

    assert error.value.status_code == 401
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_login_rejects_wrong_password(monkeypatch):
    connection, _ = connection_with_user((7, "tester", "stored-hash", "Administrator"))
    monkeypatch.setattr(auth_router, "get_connection", Mock(return_value=connection))
    monkeypatch.setattr(auth_router, "verify_password", Mock(return_value=False))

    with pytest.raises(HTTPException) as error:
        auth_router.login(SimpleNamespace(username="tester", password="wrong-password"))

    assert error.value.status_code == 401


def test_login_translates_database_errors(monkeypatch):
    connection, cursor = connection_with_user(None)
    cursor.execute.side_effect = psycopg2.OperationalError("database unavailable")
    monkeypatch.setattr(auth_router, "get_connection", Mock(return_value=connection))

    with pytest.raises(HTTPException) as error:
        auth_router.login(SimpleNamespace(username="tester", password="plain-password"))

    assert error.value.status_code == 400
    assert "database unavailable" in error.value.detail


def test_get_me_returns_current_user():
    current_user = {"user_id": 7, "username": "tester", "role": "Administrator"}

    assert auth_router.get_me(current_user) is current_user


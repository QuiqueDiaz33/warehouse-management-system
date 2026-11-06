"""Pruebas para POST /sales-orders/lines (corrección de SOLineCreate)."""
from decimal import Decimal
from unittest.mock import Mock

import psycopg2
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pydantic import ValidationError

import auth as auth_core
from main import app
from routers import sales_orders
from schemas.sales_orders import SOLineCreate

VALID_LINE = {"so_id": 7, "item_id": 3, "quantity": 2, "unit_price": 15.5}
LOGISTICS_USER = {"user_id": 5, "username": "logistics", "role": "Logistics Staff"}


def mock_connection():
    cursor = Mock()
    connection = Mock()
    connection.cursor.return_value = cursor
    return connection, cursor


# --- Modelo -----------------------------------------------------------------

def test_so_line_model_accepts_fields_used_by_router():
    line = SOLineCreate(**VALID_LINE)

    assert (line.so_id, line.item_id) == (7, 3)
    assert (line.quantity, line.unit_price) == (Decimal("2"), Decimal("15.5"))


@pytest.mark.parametrize("missing", ["so_id", "item_id", "quantity", "unit_price"])
def test_so_line_model_rejects_missing_fields(missing):
    payload = {k: v for k, v in VALID_LINE.items() if k != missing}

    with pytest.raises(ValidationError):
        SOLineCreate(**payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("quantity", 0),
        ("quantity", -1),
        ("quantity", "0.001"),
        ("unit_price", -0.01),
        ("unit_price", "10.555"),
        ("item_id", "abc"),
    ],
)
def test_so_line_model_rejects_invalid_values(field, value):
    with pytest.raises(ValidationError):
        SOLineCreate(**{**VALID_LINE, field: value})


# --- Función del router -----------------------------------------------------

def test_add_so_line_calls_procedure_and_commits(monkeypatch):
    connection, cursor = mock_connection()
    monkeypatch.setattr(sales_orders, "get_connection", Mock(return_value=connection))

    result = sales_orders.add_so_line(SOLineCreate(**VALID_LINE), LOGISTICS_USER)

    cursor.execute.assert_called_once_with(
        "CALL sp_add_so_line(%s, %s, %s, %s)", (7, 3, Decimal("2"), Decimal("15.5"))
    )
    connection.commit.assert_called_once()
    assert result == {"message": "Line added and stock reserved successfully"}
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_add_so_line_rolls_back_and_returns_400_on_database_error(monkeypatch):
    connection, cursor = mock_connection()
    cursor.execute.side_effect = psycopg2.Error("insufficient stock")
    monkeypatch.setattr(sales_orders, "get_connection", Mock(return_value=connection))

    with pytest.raises(HTTPException) as error:
        sales_orders.add_so_line(SOLineCreate(**VALID_LINE), LOGISTICS_USER)

    assert error.value.status_code == 400
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


# --- HTTP: request -> FastAPI -> Pydantic -> router --------------------------

@pytest.fixture
def client():
    app.dependency_overrides[auth_core.require_logistics] = lambda: LOGISTICS_USER
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_http_add_line_returns_200_and_calls_procedure(client, monkeypatch):
    connection, cursor = mock_connection()
    monkeypatch.setattr(sales_orders, "get_connection", Mock(return_value=connection))

    response = client.post("/sales-orders/lines", json=VALID_LINE)

    assert response.status_code == 200
    assert response.json() == {"message": "Line added and stock reserved successfully"}
    cursor.execute.assert_called_once_with(
        "CALL sp_add_so_line(%s, %s, %s, %s)", (7, 3, Decimal("2"), Decimal("15.5"))
    )


@pytest.mark.parametrize(
    "payload",
    [
        {"so_id": 7, "item_id": 3},
        {**VALID_LINE, "quantity": 0},
        {**VALID_LINE, "quantity": 0.001},
        {**VALID_LINE, "unit_price": -1},
        {**VALID_LINE, "unit_price": 10.555},
    ],
    ids=["campos-faltantes", "cantidad-cero", "cantidad-3-decimales", "precio-negativo", "precio-3-decimales"],
)
def test_http_add_line_returns_422_without_touching_database(client, monkeypatch, payload):
    get_connection = Mock()
    monkeypatch.setattr(sales_orders, "get_connection", get_connection)

    response = client.post("/sales-orders/lines", json=payload)

    assert response.status_code == 422
    get_connection.assert_not_called()


def test_http_add_line_returns_400_on_database_error(client, monkeypatch):
    connection, cursor = mock_connection()
    cursor.execute.side_effect = psycopg2.Error("insufficient stock")
    monkeypatch.setattr(sales_orders, "get_connection", Mock(return_value=connection))

    response = client.post("/sales-orders/lines", json=VALID_LINE)

    assert response.status_code == 400
    connection.rollback.assert_called_once()


def test_http_add_line_requires_authentication():
    response = TestClient(app).post("/sales-orders/lines", json=VALID_LINE)

    assert response.status_code == 401

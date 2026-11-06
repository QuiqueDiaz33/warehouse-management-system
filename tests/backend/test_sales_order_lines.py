"""Pruebas para POST /sales-orders/lines (corrección de SOLineCreate)."""
from unittest.mock import Mock

import psycopg2
import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from routers import sales_orders
from schemas.sales_orders import SOLineCreate

VALID_LINE = {"so_id": 7, "item_id": 3, "quantity": 2, "unit_price": 15.5}


def mock_connection():
    cursor = Mock()
    connection = Mock()
    connection.cursor.return_value = cursor
    return connection, cursor


def test_so_line_model_accepts_fields_used_by_router():
    line = SOLineCreate(**VALID_LINE)

    assert (line.so_id, line.item_id, line.quantity, line.unit_price) == (7, 3, 2, 15.5)


@pytest.mark.parametrize("missing", ["so_id", "item_id", "quantity", "unit_price"])
def test_so_line_model_rejects_missing_fields(missing):
    payload = {k: v for k, v in VALID_LINE.items() if k != missing}

    with pytest.raises(ValidationError):
        SOLineCreate(**payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [("quantity", 0), ("quantity", -1), ("unit_price", -0.01), ("item_id", "abc")],
)
def test_so_line_model_rejects_invalid_values(field, value):
    with pytest.raises(ValidationError):
        SOLineCreate(**{**VALID_LINE, field: value})


def test_add_so_line_calls_procedure_and_commits(monkeypatch):
    connection, cursor = mock_connection()
    monkeypatch.setattr(sales_orders, "get_connection", Mock(return_value=connection))

    result = sales_orders.add_so_line(SOLineCreate(**VALID_LINE), {"role": "Logistics Staff"})

    cursor.execute.assert_called_once_with(
        "CALL sp_add_so_line(%s, %s, %s, %s)", (7, 3, 2, 15.5)
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
        sales_orders.add_so_line(SOLineCreate(**VALID_LINE), {"role": "Logistics Staff"})

    assert error.value.status_code == 400
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()

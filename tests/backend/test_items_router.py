from unittest.mock import Mock

import psycopg2
import pytest
from fastapi import HTTPException

from routers import items
from schemas.item import ItemCreate


def mock_connection():
    cursor = Mock()
    connection = Mock()
    connection.cursor.return_value = cursor
    return connection, cursor


def test_get_items_maps_database_rows(monkeypatch):
    connection, cursor = mock_connection()
    cursor.fetchall.return_value = [
        (1, "Box", "Cardboard box", 12.5, "EA", True),
        (2, "Tape", None, 5.0, "ROLL", False),
    ]
    monkeypatch.setattr(items, "get_connection", Mock(return_value=connection))

    result = items.get_items({"user_id": 7})

    assert result == [
        {
            "item_id": 1,
            "item_name": "Box",
            "description": "Cardboard box",
            "reorder_level": 12.5,
            "uom_symbol": "EA",
            "is_active": True,
        },
        {
            "item_id": 2,
            "item_name": "Tape",
            "description": None,
            "reorder_level": 5.0,
            "uom_symbol": "ROLL",
            "is_active": False,
        },
    ]
    cursor.execute.assert_called_once()
    assert cursor.close.call_count >= 1
    assert connection.close.call_count >= 1


def test_get_items_translates_database_errors(monkeypatch):
    connection, cursor = mock_connection()
    cursor.execute.side_effect = psycopg2.OperationalError("database unavailable")
    monkeypatch.setattr(items, "get_connection", Mock(return_value=connection))

    with pytest.raises(HTTPException) as error:
        items.get_items({"user_id": 7})

    assert error.value.status_code == 400


def test_create_item_commits_and_returns_created_item(monkeypatch):
    connection, cursor = mock_connection()
    cursor.fetchone.side_effect = [("EA",), (3, "Box", "Cardboard box", 10.0, True)]
    monkeypatch.setattr(items, "get_connection", Mock(return_value=connection))
    item = ItemCreate(
        item_name="Box",
        description="Cardboard box",
        reorder_level=10,
        uom_id=1,
    )

    result = items.create_item(item, {"role": "Administrator"})

    assert result == {
        "item_id": 3,
        "item_name": "Box",
        "description": "Cardboard box",
        "reorder_level": 10.0,
        "uom_symbol": "EA",
        "is_active": True,
    }
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()


def test_create_item_rejects_missing_uom(monkeypatch):
    connection, cursor = mock_connection()
    cursor.fetchone.return_value = None
    monkeypatch.setattr(items, "get_connection", Mock(return_value=connection))
    item = ItemCreate(item_name="Box", uom_id=999)

    with pytest.raises(HTTPException) as error:
        items.create_item(item, {"role": "Administrator"})

    assert error.value.status_code == 400
    connection.commit.assert_not_called()


def test_create_item_rolls_back_database_errors(monkeypatch):
    connection, cursor = mock_connection()
    cursor.fetchone.return_value = ("EA",)
    cursor.execute.side_effect = [None, psycopg2.IntegrityError("duplicate item")]
    monkeypatch.setattr(items, "get_connection", Mock(return_value=connection))
    item = ItemCreate(item_name="Box", uom_id=1)

    with pytest.raises(HTTPException) as error:
        items.create_item(item, {"role": "Administrator"})

    assert error.value.status_code == 400
    connection.rollback.assert_called_once()


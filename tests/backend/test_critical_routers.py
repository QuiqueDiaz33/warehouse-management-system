from unittest.mock import Mock

import psycopg2
import pytest
from fastapi import HTTPException

from routers import delivery_challans, grns, purchase_orders, sales_orders, stock


def mock_connection(rows):
    cursor = Mock()
    cursor.fetchall.return_value = rows
    connection = Mock()
    connection.cursor.return_value = cursor
    return connection, cursor


def test_get_stock_maps_inventory_status(monkeypatch):
    connection, cursor = mock_connection(
        [(1, "Box", "EA", 8, 2, 10, 5, False)]
    )
    monkeypatch.setattr(stock, "get_connection", Mock(return_value=connection))

    result = stock.get_stock({"role": "Warehouse Staff"})

    assert result == [{
        "item_id": 1,
        "item_name": "Box",
        "uom_symbol": "EA",
        "available_quantity": 8,
        "reserved_quantity": 2,
        "total_on_hand": 10,
        "reorder_level": 5,
        "is_low_stock": False,
    }]
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_get_grns_maps_receipts(monkeypatch):
    connection, cursor = mock_connection(
        [(4, 2, "warehouse", "Draft", "2026-11-03")]
    )
    monkeypatch.setattr(grns, "get_connection", Mock(return_value=connection))

    result = grns.get_grns({"role": "Warehouse Staff"})

    assert result == [{
        "grn_id": 4,
        "po_id": 2,
        "received_by": "warehouse",
        "status": "Draft",
        "received_at": "2026-11-03",
    }]
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_get_purchase_orders_maps_headers(monkeypatch):
    connection, cursor = mock_connection(
        [(3, "Supplier", "warehouse", "Pending", "2026-11-03")]
    )
    monkeypatch.setattr(
        purchase_orders, "get_connection", Mock(return_value=connection)
    )

    result = purchase_orders.get_purchase_orders({"role": "Warehouse Staff"})

    assert result == [{
        "po_id": 3,
        "supplier_name": "Supplier",
        "created_by": "warehouse",
        "status": "Pending",
        "created_at": "2026-11-03",
    }]
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_get_sales_orders_maps_headers(monkeypatch):
    connection, cursor = mock_connection(
        [(5, "Customer", "logistics", "Pending", "Unpaid", "2026-11-03")]
    )
    monkeypatch.setattr(
        sales_orders, "get_connection", Mock(return_value=connection)
    )

    result = sales_orders.get_sales_orders({"role": "Logistics Staff"})

    assert result == [{
        "so_id": 5,
        "customer_name": "Customer",
        "created_by": "logistics",
        "status": "Pending",
        "payment_status": "Unpaid",
        "created_at": "2026-11-03",
    }]
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_get_delivery_challans_maps_headers(monkeypatch):
    connection, cursor = mock_connection(
        [(6, 5, "Customer", "logistics", "Driver", "P-123", "Pending", "2026-11-03")]
    )
    monkeypatch.setattr(
        delivery_challans, "get_connection", Mock(return_value=connection)
    )

    result = delivery_challans.get_delivery_challans(
        {"role": "Logistics Staff"}
    )

    assert result == [{
        "dc_id": 6,
        "so_id": 5,
        "customer_name": "Customer",
        "created_by": "logistics",
        "driver_name": "Driver",
        "vehicle_number": "P-123",
        "status": "Pending",
        "created_at": "2026-11-03",
    }]
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@pytest.mark.parametrize(
    ("module", "function"),
    [
        (stock, stock.get_stock),
        (grns, grns.get_grns),
        (purchase_orders, purchase_orders.get_purchase_orders),
        (sales_orders, sales_orders.get_sales_orders),
        (delivery_challans, delivery_challans.get_delivery_challans),
    ],
)
def test_critical_lists_translate_database_errors(monkeypatch, module, function):
    connection, cursor = mock_connection([])
    cursor.execute.side_effect = psycopg2.OperationalError("database unavailable")
    monkeypatch.setattr(module, "get_connection", Mock(return_value=connection))

    with pytest.raises(HTTPException) as error:
        function({"role": "Administrator"})

    assert error.value.status_code == 400
    cursor.close.assert_called_once()
    connection.close.assert_called_once()

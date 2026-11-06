from decimal import Decimal

from pydantic import BaseModel, Field

class SalesOrderCreate(BaseModel):
    customer_id: int 
    created_by: int 
    
class SOLineCreate(BaseModel):
    # Campos que usa add_so_line en routers/sales_orders.py.
    # Decimal con 2 decimales, igual que NUMERIC(12,2) en sales_order_lines.
    so_id: int
    item_id: int
    quantity: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    unit_price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    
class SOAdvance(BaseModel):
    so_id: int
    
class SOCancel(BaseModel):
    so_id: int 

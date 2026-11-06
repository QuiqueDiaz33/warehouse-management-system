from pydantic import BaseModel, Field

class SalesOrderCreate(BaseModel):
    customer_id: int 
    created_by: int 
    
class SOLineCreate(BaseModel):
    # Campos que usa add_so_line en routers/sales_orders.py
    so_id: int
    item_id: int
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)
    
class SOAdvance(BaseModel):
    so_id: int
    
class SOCancel(BaseModel):
    so_id: int 

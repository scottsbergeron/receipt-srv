from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ReceiptItem(BaseModel):
    name: str
    quantity: float
    price: float
    total: float

class Receipt(BaseModel):
    merchant_name: str
    date: datetime
    total_amount: float
    items: List[ReceiptItem]
    tax: Optional[float] = None
    tip: Optional[float] = None
 
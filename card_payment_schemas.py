from pydantic import BaseModel
import datetime
from typing import Optional


class PaymentInitialization(BaseModel):
    card_number: int
    card_cvv:  int
    expiration_date: datetime.date
    user_name: str
    amount: float


class PaymentResultSchema(BaseModel):
    order_id: str
    status: str
    description: Optional[None | str] = None

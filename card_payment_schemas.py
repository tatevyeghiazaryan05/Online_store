from pydantic import BaseModel
import datetime


class PaymentInitialization(BaseModel):
    card_number: int
    card_cvv:  int
    expiration_date: datetime.date
    user_name: str
    amount: float


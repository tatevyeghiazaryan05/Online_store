from pydantic import BaseModel
import datetime


class UserOrdersSchema(BaseModel):
    quantity: int
    shipping_address: str
    drink_id: int
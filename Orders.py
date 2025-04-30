from fastapi import FastAPI, APIRouter, Depends
from Orders_schema import UserOrdersSchema
from security import get_current_user
import main
from fastapi.exceptions import HTTPException
import datetime


ordersrouter = APIRouter()


@ordersrouter.post("/api/orders/user")
def user_order(order_data: UserOrdersSchema, token=Depends(get_current_user)):
    user_id = token["id"]
    total_price = 0
    main.cursor.execute("SELECT price FROM drinks WHERE id = %s",
                        (order_data.drink_id,))
    drink_price = main.cursor.fetchone()

    if not drink_price:
        raise HTTPException(status_code=404, detail="Drink not found")

    drink_price = dict(drink_price).get("price")
    total_price += (drink_price * order_data.quantity)

    main.cursor.execute("INSERT INTO orders (user_id, drink_id, quantity, total_price, shipping_address) VALUES (%s, %s, %s, %s, %s)",
        (user_id, order_data.drink_id, order_data.quantity, total_price, order_data.shipping_address))

    main.conn.commit()

    message = f"New Order: User ID {user_id}, Drink ID {order_data.drink_id}, Qty {order_data.quantity}, Total ${total_price}"
    main.cursor.execute("INSERT INTO notifications (message, is_read) VALUES (%s, %s)",
                        (message, False))
    main.conn.commit()

    return "Order created successfully"

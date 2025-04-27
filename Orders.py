from fastapi import FastAPI, APIRouter, Depends
from Orders_schema import UserOrdersSchema, GetOrdersByDateSchema, GetOrdersByPriceSchema
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

    return "Order created successfully"


@ordersrouter.get("/api/orders/get/by/id/{order_id}")
def get_orders(order_id: int):
    main.cursor.execute("SELECT * FROM orders WHERE id=%s",
                        (order_id,))


@ordersrouter.get("/api/orders/get/by/date/{start_date}/{end_date}")
def get_order_by_date(start_date: datetime.date, end_date: datetime.date):

    main.cursor.execute("SELECT * FROM orders WHERE created_at >= %s AND created_at <= %s",
                        (start_date, end_date))
    orders = main.cursor.fetchall()

    return orders


@ordersrouter.get("/api/orders/get/by/price/{min_price}/{max_price}")
def get_order_by_date(min_price: float,  max_price: float):
    main.cursor.execute("SELECT * FROM orders WHERE total_price >= %s AND total_price <= %s",
                        (min_price, max_price))
    orders = main.cursor.fetchall()

    return orders

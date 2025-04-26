from fastapi import FastAPI, APIRouter, Depends
import main
from card_payment_schemas import PaymentInitialization, PaymentResultSchema
from security import get_current_user
from fastapi.responses import FileResponse


card_payments_router = APIRouter()


@card_payments_router.post("/api/payments/card/payment-start")
def card_payment_start(payments_data: PaymentInitialization, token=Depends(get_current_user)):
    user_id = token["id"]
    main.cursor.execute("INSERT INTO cardpayments (user_id,amount) VALUES (%s,%s)",
                        (user_id, payments_data.amount))
    main.conn.commit()
    link_URL= (f"https//bank.ameria.com/payments/cart_payment/init?amount={payments_data.amount}&user_name={payments_data.user_name}"
               f"&card_numbers={payments_data.card_number}&expiration_date={str(payments_data.expiration_date)}&card_cvv={payments_data.card_cvv}")

    return link_URL


@card_payments_router.post("/api/payments/card/payment-result")
def card_payment_result(payment_data: PaymentResultSchema):
    order_id = payment_data.order_id
    main.cursor.execute("UPDATE CardPayments SET status=%s WHERE order_id=%s",
                        (payment_data.status, order_id))
    main.conn.commit()
    return f"Description: {payment_data}"


@card_payments_router.get("/api/payments/card/payment-success")
def card_payment_success():
    return FileResponse("payments_success.html")


@card_payments_router.get("/api/payments/card/payment-fail")
def card_payment_fail():
    return FileResponse("payments_fail.html")


from fastapi import FastAPI, APIRouter, Depends
import main
from card_payment_schemas import PaymentInitialization
from security import get_current_user


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
def card_payment_result():
    pass


@card_payments_router.get("/api/payments/card/payment-success")
def card_payment_success():
    pass


@card_payments_router.get("/api/payments/card/payment-fail")
def card_payment_fail():
    pass


#todo end payments
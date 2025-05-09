from fastapi import APIRouter, Depends, HTTPException, status
import main
from schemas import UserNameChangeSchema, UserPasswordChangeSchema, AdminPasswordRecoverSchema, UserFeedbackSchema
from security import get_current_user, pwd_context
from pydantic import EmailStr
from email_service import send_verification_email
from datetime import datetime, timedelta
from models import ForgotPasswordCode


user_router = APIRouter()


@user_router.put("/api/user/change/name")
def change_user_name(data: UserNameChangeSchema, token=Depends(get_current_user)):
    print(token)
    user_id = token["id"]
    print(user_id)
    main.cursor.execute("UPDATE users SET name = %s WHERE id = %s", (data.name, user_id))
    main.conn.commit()
    return "Updated successfully!!"


@user_router.put("/api/user/change/password")
def change_user_password(data: UserPasswordChangeSchema, token=Depends(get_current_user)):
    user_id = token["id"]
    new_hashed_password = pwd_context.hash(data.password)
    main.cursor.execute("UPDATE users SET password = %s WHERE id = %s",
                        (new_hashed_password, user_id))
    main.conn.commit()
    return "Password updated successfully!!"


@user_router.get("/api/users/my-account-info")
def get_user_my_account_info(token=Depends(get_current_user)):
    user_id = token["id"]
    main.cursor.execute("SELECT email,name FROM users WHERE id=%s",
                        (user_id,))
    data = main.cursor.fetchall()
    return data


@user_router.get("/api/users/for/forgot/password/code/{email}")
def user_forgot_password_code(email: EmailStr):
    try:
        main.cursor.execute("SELECT * FROM users WHERE email=%s",
                            (email,))
        user = main.cursor.fetchone()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not such user!"

        )
    verification_code = send_verification_email(email)
    main.cursor.execute("INSERT INTO forgotpasswordcode (code,email) VALUES(%s,%s)",
                        (verification_code, email))

    main.conn.commit()


@user_router.post("/api/users/user/forgot/password")
def user_forgot_password(data: AdminPasswordRecoverSchema):
    code = data.code

    new_password = pwd_context.hash(data.new_password)

    try:
        main.cursor.execute("SELECT * FROM forgotpasswordcode WHERE code=%s",
                        (code,))
        data = main.cursor.fetchone()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        )

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code is incorrect!"

        )

    data = dict(data)
    created_at = data.get("created_at")
    expiration_time = created_at + timedelta(minutes=15)
    if datetime.now() > expiration_time:
        main.cursor.execute("DELETE FROM forgotpasswordcode WHERE code=%s", (code,))
        main.conn.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code has expired after 15 minutes."
        )

    main.cursor.execute("UPDATE users SET password =%s WHERE email=%s",
                        (new_password, data["email"]))

    main.conn.commit()

    main.cursor.execute("DELETE FROM forgotpasswordcode WHERE code = %s",
                        (code,))
    main.conn.commit()
    return "Change password successfully!!"


@user_router.put("/api/users/user/password/recovery")
def password_recovery(data: UserPasswordChangeSchema, token=Depends(get_current_user)):
    user_id = token["id"]
    new_password = pwd_context.hash(data.password)
    main.cursor.execute("UPDATE users SET password =%s WHERE id=%s",
                        (new_password, user_id))
    main.conn.commit()
    return "New password updated successfully!!"


@user_router.post("/api/users/feedback")
def user_feedback(feedback_data: UserFeedbackSchema):
    user_id = feedback_data.user_id
    comment = feedback_data.comment
    rating = feedback_data.rating

    main.cursor.execute("INSERT INTO feedback (user_id,comment,rating) VALUES (%s,%s,%s)",
                        (user_id, comment, rating))
    main.conn.commit()

    return "Feedback added successfully!!"


@user_router.get("/api/users/get/today/orders/total/price/{user_id}")
def get_today_orders_total_price(user_id: int):
    today = datetime.today().date()
    main.cursor.execute("SELECT SUM(total_price) FROM orders WHERE user_id = %s AND DATE(created_at) = %s",
                        (user_id, today))
    total_price = main.cursor.fetchone()
    return total_price


@user_router.get("/api/users/get/month/orders/total/price/{user_id}/{month_in_number}/{year}")
def get_month_orders_total_price(user_id: int, month_in_number: int, year: int):
    main.cursor.execute("SELECT SUM(total_price) FROM orders WHERE user_id = %s AND EXTRACT(MONTH FROM created_at)=%s "
                        "AND EXTRACT(YEAR FROM created_at) = %s",
                        (user_id, month_in_number, year))
    total_price = main.cursor.fetchone()
    return total_price


@user_router.get("/api/users/get/year/orders/total/price/{user_id}/{year}")
def get_year_orders_total_price(user_id: int, year: int):
    main.cursor.execute("SELECT SUM(total_price) FROM orders WHERE user_id = %s AND EXTRACT(YEAR FROM created_at) = %s",
                        (user_id, year))
    total_price = main.cursor.fetchone()
    return total_price

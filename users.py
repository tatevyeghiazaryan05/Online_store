from fastapi import APIRouter, Depends, HTTPException, status
import main
from schemas import UserNameChangeSchema, UserPasswordChangeSchema
from security import get_current_user, pwd_context
from pydantic import EmailStr
from email_service import send_verification_email



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
def user_forgot_password(email: EmailStr):
    try:
        main.cursor.execute("SELECT * FROM admins WHERE email=%s",
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


#TODO user forgot password (not log in)
#TODO user password recovery (log in)

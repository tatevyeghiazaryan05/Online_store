from fastapi import APIRouter, Depends
import main
from schemas import UserNameChangeSchema, UserPasswordChangeSchema
from security import get_current_user, pwd_context


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

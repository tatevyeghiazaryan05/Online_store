import main
from fastapi import APIRouter, HTTPException, status
from schemas import DrinkSchema, DrinkNameChangeSchema
from security import pwd_context, create_access_token


drink_router = APIRouter()


@drink_router.get("/api/get/drinks")
def get_drinks():
    main.cursor.execute("SELECT * FROM drinks")
    drinks = main.cursor.fetchall()
    return {"drinks": drinks}


@drink_router.get("/api/drinks/get/by-kind/{drink_kind}")
def get_drinks_by_kind(drink_kind: str):
    main.cursor.execute("SELECT * FROM drinks WHERE kind = %s",
                     (drink_kind,))
    drinks = main.cursor.fetchall()
    return drinks

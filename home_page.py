from fastapi import APIRouter, Depends
import main
from security import get_current_user, pwd_context
from fastapi import HTTPException, status

home_page_router = APIRouter()


@home_page_router.get("/api/home_page/get/drinks")  #TODO write using limit
def main_page():
    main.cursor.execute("SELECT * FROM drinks WHERE kind = 'alcoholic'")
    alcoholic = main.cursor.fetchall()

    main.cursor.execute("SELECT * FROM drinks WHERE kind = 'nonalcoholic'")
    nonalcoholic = main.cursor.fetchall()

    alcoholic_part = alcoholic[:5]
    nonalcoholic_part = nonalcoholic[:5]

    if len(alcoholic_part) < 5:
        nonalcoholic_extra = nonalcoholic[5:]
        nonalcoholic_part += nonalcoholic_extra[:10-len(alcoholic)+1]
    elif len(nonalcoholic_part) < 5:
        alcoholic_extra = alcoholic[5:]
        alcoholic_part += alcoholic_extra[:10-len(nonalcoholic)+1]

    combined = alcoholic_part + nonalcoholic_part
    return combined


@home_page_router.get("/api/home_page/filter/drinks/alcoholic")
def filter_alcoholic_drinks():
    main.cursor.execute("SELECT * FROM drinks WHERE kind = 'alcoholic'")
    drinks = main.cursor.fetchall()
    return drinks


@home_page_router.get("/api/home_page/filter/drinks/nonalcoholic")
def filter_nonalcoholic_drinks():
    main.cursor.execute("SELECT * FROM drinks WHERE kind = 'nonalcoholic'")
    drinks = main.cursor.fetchall()
    return drinks


@home_page_router.get("/api/home_page/filter/drinks/by/category/{drink_category}")
def filter_drinks_by_category(drink_category: str):
    main.cursor.execute("SELECT * FROM drinks WHERE category = %s",
                        (drink_category,))
    drinks = main.cursor.fetchall()
    return drinks


@home_page_router.get("/api/home_page/filter/drinks/by/price/{max_price}")
def filter_drinks_by_max_price(max_price: float):
    main.cursor.execute("SELECT * FROM drinks WHERE price <= %s",
                        (max_price,))
    drinks = main.cursor.fetchall()
    return drinks


@home_page_router.get("/api/home_page/filter/drinks/by/price/{min_price}")
def filter_drinks_by_max_price(min_price: float):
    main.cursor.execute("SELECT * FROM drinks WHERE price >= %s",
                        (min_price,))
    drinks = main.cursor.fetchall()
    return drinks



#TODO PRICE  LIMIT DRINKS  write in one function both min_price,max_price

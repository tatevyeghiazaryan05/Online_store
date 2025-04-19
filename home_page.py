from fastapi import APIRouter, Depends
import main
from security import get_current_user, pwd_context

home_page_router = APIRouter()


@home_page_router.get("/api/home_page/get/drinks")  #TODO write using limit +
def main_page():
    main.cursor.execute("SELECT * FROM drinks WHERE kind = 'alcoholic' LIMIT 5")
    alcoholic = main.cursor.fetchall()

    main.cursor.execute("SELECT * FROM drinks WHERE kind = 'nonalcoholic' LIMIT 5")
    nonalcoholic = main.cursor.fetchall()

    current_total = len(alcoholic) + len(nonalcoholic)

    if len(alcoholic) < 5:
        main.cursor.execute(
            "SELECT * FROM drinks WHERE kind = 'nonalcoholic' LIMIT %s OFFSET %s",
            (10-current_total, len(nonalcoholic))
        )
        nonalcoholic += main.cursor.fetchall()
    elif len(nonalcoholic) < 5:
        main.cursor.execute(
            "SELECT * FROM drinks WHERE kind = 'alcoholic' LIMIT %s OFFSET %s",
            (10 - nonalcoholic, len(alcoholic))
        )
        alcoholic += main.cursor.fetchall()

    result = nonalcoholic + alcoholic
    return result


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

#TODO user forgot password (not log in)
#TODO user password recovery (log in)

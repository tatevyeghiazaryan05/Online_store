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


@home_page_router.get("/api/home_page/filter/drinks/by/price")
def filter_drinks_by_price(min_price: float = None, max_price: float = None):
    if min_price is not None and max_price is not None:
        main.cursor.execute(
            "SELECT * FROM drinks WHERE price BETWEEN %s AND %s",
            (min_price, max_price)
        )
    elif min_price is not None:
        main.cursor.execute(
            "SELECT * FROM drinks WHERE price >= %s",
            (min_price,)
        )
    elif max_price is not None:
        main.cursor.execute(
            "SELECT * FROM drinks WHERE price <= %s",
            (max_price,)
        )
    else:
        main.cursor.execute("SELECT * FROM drinks")

    drinks = main.cursor.fetchall()
    return drinks


#TODO PRICE  LIMIT DRINKS  write in one function both min_price,max_price  +
#TODO user forgot password (not log in)
#TODO user password recovery (log in)

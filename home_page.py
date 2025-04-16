from fastapi import APIRouter, Depends
import main
from security import get_current_user, pwd_context

home_page_router = APIRouter()


@home_page_router.get("/api/home_page/get/drinks")
def main_page():
    main.cursor.execute("SELECT COUNT(id) FROM drinks")
    count = main.cursor.fetchone()



#TODO TAKE 5 NONALCHOHOLIC AND 5 ALCHOHOLIC AND ADD IN MAIN_PAGE

#TODO USER CAN FILTER AND SEE ONLY ALCHOHOLIC NONALCHOHOLIC,COULD SEE PRICE  LIMITE DRINKS, FILTER AS CATEGORY

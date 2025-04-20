from fastapi import FastAPI
from models import Base
from database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
from auth import authrouter
from users import user_router
from home_page import home_page_router
from Card_Payments import card_payments_router


Base.metadata.create_all(bind=engine)

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="password",
    database="online_store",
    cursor_factory=RealDictCursor
    )

cursor = conn.cursor()

app = FastAPI()
# app.mount("/images", StaticFiles(directory="uploads"), name="uploads")

app.include_router(authrouter)
app.include_router(user_router)
app.include_router(home_page_router)
app.include_router(card_payments_router)

from fastapi import FastAPI
from common.database.connection import create_db_and_tables


app = FastAPI()


@app.on_event("startup")
def on_startup():
    print("HELLO")
    create_db_and_tables()


@app.get("/")
async def main_route():
    return {"message": "Hello world!"}

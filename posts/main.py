from fastapi import FastAPI
from common.database.connection import SessionDep, create_db_and_tables
from common.database.models import Post
from sqlalchemy.exc import SQLAlchemyError


app = FastAPI()


@app.on_event("startup")
def on_startup():
    print("HELLO")
    create_db_and_tables()


@app.post("/posts", status_code=201)
async def create_post(post: Post, session: SessionDep):
    try:
        session.add(post)
        session.commit()
        session.refresh(post)
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Commit failed: {e}")

    return post

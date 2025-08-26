from fastapi import FastAPI, HTTPException
from common.database.connection import SessionDep, create_db_and_tables
from common.database.models import Post
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Field
from sqlmodel.main import uuid


app = FastAPI(
    title="Posts Service",
    description="APIs that the Posts Service support",
    version="0.0.1",
)


# refactor: Move to another file
class CreatePostPayload(BaseModel):
    author_id: uuid.UUID
    content: str


class EditPostPayload(BaseModel):
    content: str


# refactor: handle deprecation
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# refactor: create post logic
@app.post("/posts", status_code=201)
async def create_post(payload: CreatePostPayload, session: SessionDep):
    try:
        post = Post(**payload.model_dump())
        session.add(post)
        session.commit()
        session.refresh(post)

        return post
    except SQLAlchemyError as e:
        session.rollback()

        raise HTTPException(500, e._message())


# refactor: update post logic
@app.patch("/posts/{id}", status_code=200)
async def update_post(
    id: uuid.UUID, payload: EditPostPayload, session: SessionDep
):
    try:
        existing_post = session.get(Post, id)
        if not existing_post:
            raise HTTPException(404, "Post not found")

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(existing_post, key, value)

        session.add(existing_post)
        session.commit()
        session.refresh(existing_post)

        return existing_post
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(500, e._message())


# refactor: delete post logic
@app.delete("/posts/{id}", status_code=204)
async def delete_post(id: uuid.UUID, session: SessionDep):
    existing_post = session.get(Post, id)
    if not existing_post:
        raise HTTPException(404, "Post not found")

    session.delete(existing_post)
    session.commit()

    return None

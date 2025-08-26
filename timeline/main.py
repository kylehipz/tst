from typing import Optional
from datetime import datetime
from fastapi import FastAPI
from common.database.connection import SessionDep, create_db_and_tables
from pydantic import BaseModel
from sqlmodel import text
from sqlmodel.main import uuid


app = FastAPI(
    title="Timeline Service",
    description="APIs that the Timeline Service support",
    version="0.0.1",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


class PostWithAuthor(BaseModel):
    id: uuid.UUID
    author_id: uuid.UUID
    content: str
    created_at: datetime
    username: str
    email: str
    profile_picture: Optional[str] = None


@app.get("/timeline/{user_id}")
async def get_timeline(user_id: uuid.UUID, session: SessionDep):
    stmt = text(
        """
    SELECT p.*, u.username, u.email, u.profile_picture FROM post p
    JOIN "follow" f on f.followee_id = p.author_id
    JOIN "user" u on p.author_id = u.id
    WHERE f.follower_id = :current_user_id
    ORDER BY p.created_at DESC
    """
    )

    results = session.execute(stmt, {"current_user_id": user_id}).all()
    mappings = [row._mapping for row in results]

    return [PostWithAuthor(**row) for row in mappings]

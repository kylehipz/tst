from fastapi import FastAPI, HTTPException
from common.database.connection import SessionDep, create_db_and_tables
from common.database.models import Follow
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select


class FollowPayload(BaseModel):
    follower: str
    followee: str


class UnfollowPayload(BaseModel):
    follower: str
    followee: str


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/follow")
async def follow_user(payload: FollowPayload, session: SessionDep):
    try:
        follow_rel = Follow(**payload.model_dump())
        session.add(follow_rel)
        session.commit()
        session.refresh(follow_rel)

        return follow_rel
    except SQLAlchemyError as e:
        session.rollback()

        raise HTTPException(500, e._message())


@app.delete("/unfollow", status_code=204)
async def unfollow_user(payload: UnfollowPayload, session: SessionDep):
    stmt = select(Follow).where(
        Follow.follower == payload.follower,
        Follow.followee == payload.followee,
    )
    results = session.exec(stmt).all()
    if not results:
        raise HTTPException(
            404,
            f"User {payload.follower} doesn't follow user {payload.followee}",
        )

    follow_rel = results[0]

    session.delete(follow_rel)
    session.commit()

    return None

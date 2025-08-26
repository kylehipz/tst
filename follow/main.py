from fastapi import FastAPI, HTTPException
from common.database.connection import SessionDep, create_db_and_tables
from common.database.models import Follow
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.main import uuid

# INSERT INTO "user" ("id", "full_name", "email", "username")
# VALUES ('62b5e47a-ddc8-4243-9c38-9b467ff37728', 'Kyle Hipolito', 'kylehipolito2109@gmail.com', 'kylehipz'),
# ('c8875fc9-0dd8-494a-9f2c-bf798908be50', 'Myris Patosa', 'patosamyris@gmail.com', 'enmy')


class FollowPayload(BaseModel):
    follower_id: uuid.UUID
    followee_id: uuid.UUID


class UnfollowPayload(BaseModel):
    follower_id: uuid.UUID
    followee_id: uuid.UUID


app = FastAPI(
    title="Follow Service",
    description="APIs that the Follow Service support",
    version="0.0.1",
)


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
        Follow.follower_id == payload.follower_id,
        Follow.followee_id == payload.followee_id,
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

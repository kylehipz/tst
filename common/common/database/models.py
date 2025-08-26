from typing import List
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from sqlmodel.main import uuid
from datetime import datetime


class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    author: str = Field(index=True, nullable=False)
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    attachments: List["Attachment"] = Relationship(back_populates="post")


class Attachment(SQLModel, table=True):
    url: str = Field(primary_key=True)
    post_id: uuid.UUID = Field(index=True, foreign_key="post.id")
    created_at: datetime = Field(default_factory=datetime.now)

    post: Post = Relationship(back_populates="attachments")


class Follow(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    follower: str = Field(index=True, nullable=False)
    followee: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    __table_args__ = (
        UniqueConstraint("follower", "followee", name="uix_follower_followee"),
    )

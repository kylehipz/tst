from typing import List
from sqlalchemy import Nullable
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from sqlmodel.main import uuid
from datetime import datetime


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str
    email: str
    username: str
    profile_picture: str | None

    posts: List["Post"] = Relationship(back_populates="author")
    followers: List["Follow"] = Relationship(
        back_populates="followee",
        sa_relationship_kwargs={"foreign_keys": "[Follow.followee_id]"},
    )
    following: List["Follow"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"},
    )


class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    author_id: uuid.UUID = Field(
        foreign_key="user.id", index=True, nullable=False
    )
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    attachments: List["Attachment"] = Relationship(back_populates="post")
    author: User = Relationship(back_populates="posts")


class Attachment(SQLModel, table=True):
    url: str = Field(primary_key=True)
    post_id: uuid.UUID = Field(
        index=True, foreign_key="post.id", nullable=False
    )
    created_at: datetime = Field(default_factory=datetime.now)

    post: Post = Relationship(back_populates="attachments")


class Follow(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    follower_id: uuid.UUID = Field(
        foreign_key="user.id", index=True, nullable=False
    )
    followee_id: uuid.UUID = Field(
        foreign_key="user.id", index=True, nullable=False
    )
    created_at: datetime = Field(default_factory=datetime.now)

    follower: User = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"},
    )
    followee: User = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "[Follow.followee_id]"},
    )

    __table_args__ = (
        UniqueConstraint(
            "follower_id", "followee_id", name="uix_follower_id_followee_id"
        ),
    )

from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
import importlib
import os

importlib.import_module(".models", package="common.database")


db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

postgres_url = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

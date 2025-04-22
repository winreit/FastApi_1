import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import POSTGRES_DSN

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

engine = create_async_engine(POSTGRES_DSN)
session = async_sessionmaker(bind=engine, expire_on_commit=False)


class BaseModel(DeclarativeBase,AsyncAttrs):
    pass

class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unicue=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20),nullable=False)
    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[str]

    async def __init__(self, name, password):
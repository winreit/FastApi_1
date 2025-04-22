import datetime
from typing import Literal

from pydantic import BaseModel


class IdResponseBase(BaseModel):
    id: int

class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime.datetime
    updated_at: str
    author_id: int
    author_name: str
    price: int

class CreateAdvertisementResponse(IdResponseBase):
    pass

class UpdateAdvertisementResponse(IdResponseBase):
    pass


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int
    author_id: int


class UpdateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int
    author_id: int


class DeleteAdvertisementResponse(BaseModel):
    pass

class StatusResponse(BaseModel):
    status: Literal["deleted"]

class CreateUserRequest(BaseModel):
    name: str
    password: str

class CreateUserResponse(IdResponseBase):
    pass

class GetUserResponse(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: str

class UpdateUserRequest(BaseModel):
    name: str | None = None
    password: str | None = None


class UpdateUserResponse(IdResponseBase):
    pass

class DeleteUserResponse(BaseModel):
    pass
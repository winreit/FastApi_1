from pydantic import BaseModel
import datetime
from typing import Literal
import uuid


class IdResponseBase(BaseModel):
    id: int


class StatusResponse(BaseModel):
    status: Literal["deleted"]


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    created_at: datetime.datetime
    author_id: int


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int



class CreateAdvertisementResponse(IdResponseBase):
    pass


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None


class UpdateAdvertisementResponse(IdResponseBase):
    pass


class DeleteAdvertisementResponse(StatusResponse):
    pass

class BaseUserRequest(BaseModel):
    email: str
    password: str

class CreateUserRequest(BaseUserRequest):
    name: str


class CreateUserResponse(IdResponseBase):
    pass


class GetUserResponse(BaseModel):
    id: int
    name: str
    registration_time: datetime.datetime


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None


class UpdateUserResponse(IdResponseBase):
    pass


class DeleteUserResponse(StatusResponse):
    pass


class LoginRequest(BaseUserRequest):
    pass

class LoginResponse(BaseModel):
    token: uuid.UUID
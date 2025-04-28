from fastapi import FastAPI, Query, HTTPException
import uvicorn
from lifespan import lifespan
from models import Advert, User, Token
from dependency import SessionDependency, TokenDependency
import crud
from constants import STATUS_DELETED
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from auth import check_password, hash_password

from schema import (
    GetAdvertisementResponse,
    CreateAdvertisementResponse,
    CreateAdvertisementRequest,
    UpdateAdvertisementRequest,
    UpdateAdvertisementResponse,
    DeleteAdvertisementResponse,
    CreateUserResponse,
    CreateUserRequest,
    GetUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    DeleteUserResponse,
    LoginRequest,
    LoginResponse,
)


app = FastAPI(
    title="Advertisement API",
    version="0.1.0",
    description="API for advertisement",
    lifespan=lifespan,
)


@app.post(
    "/api/v1/advertisement",
    response_model=CreateAdvertisementResponse,
    tags=["advertisements"],
)
async def create_advertisement(
    advert_request: CreateAdvertisementRequest,
    session: SessionDependency,
    token: TokenDependency,
):
    advertisement_obj = Advert(
        title=advert_request.title,
        description=advert_request.description,
        price=advert_request.price,
        author_id=token.user_id,
    )
    await crud.add_advert(session, advertisement_obj)
    return advertisement_obj.id_dict


@app.patch(
    "/api/v1/advertisement/{advertisement_id}",
    response_model=UpdateAdvertisementResponse,
    tags=["advertisements"],
)
async def update_advertisement(
    advertisement_id: int,
    advertisement_request: UpdateAdvertisementRequest,
    session: SessionDependency,
    token: TokenDependency,
):

    advertisement_json = advertisement_request.model_dump(exclude_unset=True)
    advertisement = await crud.get_advert_by_id(session, Advert, advertisement_id)
    if advertisement.author_id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    for field, value in advertisement_json.items():
        setattr(advertisement, field, value)

    await crud.add_advert(session, advertisement)
    return advertisement.id_dict


@app.delete(
    "/api/v1/advertisement/{advertisement_id}",
    response_model=DeleteAdvertisementResponse,
    tags=["advertisements"],
)
async def delete_advertisement(
    advertisement_id: int, session: SessionDependency, token: TokenDependency
):
    advertisement = await crud.get_advert_by_id(session, Advert, advertisement_id)
    if advertisement.author_id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    await crud.delete_advert(advertisement, session)
    return STATUS_DELETED


@app.get(
    "/api/v1/advertisement/{advertisement_id}",
    response_model=GetAdvertisementResponse,
    tags=["advertisements"],
)
async def get_advertisement(session: SessionDependency, advertisement_id: int):
    advertisement_obj = await crud.get_advert_by_id(session, Advert, advertisement_id)
    return advertisement_obj.dict


@app.get(
    "/api/v1/advertisement",
    response_model=list[GetAdvertisementResponse],
    tags=["advertisements"],
)
async def get_advertisement_by_qs(
    session: SessionDependency,
    title: str = Query(None),
    description: str = Query(None),
    price: int = Query(None),
    author_id: int = Query(None),
):
    query_string = {}
    if title:
        query_string["title"] = title
    if description:
        query_string["description"] = description
    if price:
        query_string["price"] = price
    if author_id:
        query_string["author_id"] = author_id

    advertisement_obj = await crud.get_advert_by_qs(session, Advert, **query_string)
    advertisement_list = [
        advert.dict for advert in advertisement_obj.unique().scalars().all()
    ]
    return advertisement_list


@app.post("/api/v1/user", response_model=CreateUserResponse, tags=["users"])
async def create_user(user_request: CreateUserRequest, session: SessionDependency):
    user_request_dict = user_request.dict()
    user_request_dict["password"] = hash_password(user_request_dict["password"])

    user_obj = User(**user_request_dict)
    await crud.add_user(session, user_obj)
    return user_obj.id_dict


@app.get("/api/v1/user/{user_id}", response_model=GetUserResponse, tags=["users"])
async def get_user(session: SessionDependency, user_id: int):
    user_obj = await crud.get_user_by_id(session, User, user_id)
    return user_obj.dict


@app.patch("/api/v1/user/{user_id}", response_model=UpdateUserResponse, tags=["users"])
async def update_user(
    user_id: int,
    user_request: UpdateUserRequest,
    session: SessionDependency,
    token: TokenDependency,
):

    user_json = user_request.model_dump(exclude_unset=True)
    user = await crud.get_user_by_id(session, User, user_id)
    if user.id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    for field, value in user_json.items():
        setattr(user, field, value)

    await crud.add_user(session, user)
    return user.id_dict


@app.delete("/api/v1/user/{user_id}", response_model=DeleteUserResponse, tags=["users"])
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    user = await crud.get_user_by_id(session, User, user_id)
    if user.id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    await crud.delete_user(user, session)
    return STATUS_DELETED


@app.post("/api/v1/login", response_model=LoginResponse, tags=["user"])
async def login(login_request: LoginRequest, session: SessionDependency):
    user_query = select(User).where(User.email == login_request.email)
    user = await session.scalar(user_query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not check_password(login_request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    token = Token(user_id=user.id)
    await crud.add_token(session, token)
    return token.dict


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
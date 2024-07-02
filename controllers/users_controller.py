from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from services.users_service import UsersService
from utils.connectors import db_conn

users_service = UsersService(db_conn)
router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None


class UserCreateResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    created_on: datetime
    role_id: int


class UserRetrieveResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    role_name: str


class UserUpdateResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    updated_on: datetime
    role_id: int


class UserValidate(BaseModel):
    email: EmailStr
    password: str


@router.post("/user", response_model=UserCreateResponse)
def create_user(user: UserCreate):
    try:
        created_user = users_service.create(user.model_dump())
        if not created_user:
            raise HTTPException(
                status_code=500, detail="Failed to create user")
        return UserCreateResponse(**created_user.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}", response_model=UserRetrieveResponse)
def read_user(user_id: int = Path(..., gt=0)):
    try:
        user = users_service.read_with_role(user_id)
        user_ = user.fetchone()
        if user_ is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRetrieveResponse(**user_)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/user/{user_id}", response_model=UserUpdateResponse)
def update_user(user_id: int, user: UserUpdate):
    try:
        updated_user = users_service.update(
            user.model_dump(exclude_unset=True), {"user_id": user_id})
        updated_user_ = updated_user.fetchone()
        if updated_user_ is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserUpdateResponse(**updated_user_)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/user/{user_id}", response_model=dict)
def delete_user(user_id: int = Path(..., gt=0)):
    try:
        result = users_service.delete({"user_id": user_id})
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/user/login", response_model=UserRetrieveResponse)
async def login(user: UserValidate):
    try:
        try_user = users_service.read(conditions=user.model_dump())
        try_user_ = try_user.fetchone()
        if try_user_ is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user_details = users_service.read_with_role(try_user_["user_id"])
        return UserRetrieveResponse(**user_details.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

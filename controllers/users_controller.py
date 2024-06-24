from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from services.users_service import UsersService
from connectors import db_conn

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


class UserCreateResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    created_on: datetime
    updated_at: datetime
    role_id: int


@router.post("/user", response_model=UserCreateResponse)
def create_user(user: UserCreate):
    try:
        created_user = users_service.create('user', user.model_dump())
        if not created_user:
            raise HTTPException(
                status_code=500, detail="Failed to create user")

        return created_user.one()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}")
def read_user(user_id: int):
    conditions = {"user_id": user_id}
    try:
        user = users_service.read('user', conditions=conditions)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user.one()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/user/{user_id}", response_model=dict)
def update_user(user_id: int, user: UserUpdate):
    conditions = {"user_id": user_id}
    try:
        updated_user = users_service.update(
            'user', user.model_dump(exclude_none=True), conditions)
        if not updated_user:
            raise HTTPException(
                status_code=500, detail="User not updated")
        return updated_user.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/user/{user_id}", response_model=dict)
def delete_user(user_id: int):
    conditions = {"user_id": user_id}
    try:
        result = users_service.delete('user', conditions=conditions)
        if not result:
            raise HTTPException(500, "Failed to delete user")
        return {"message": f"User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
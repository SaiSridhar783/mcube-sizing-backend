from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from services.role_service import RolesService
from connectors import db_conn

role_service = RolesService(db_conn)
router = APIRouter()


class RoleCreate(BaseModel):
    name: str


class RoleReturn(BaseModel):
    role_id: int
    name: str


@router.post("/role", response_model=RoleReturn)
def create_role(role: rolecreate):
    try:
        created_role = role_service.create(role.model_dump())
        if not created_role:
            raise (HTTPException(status_code=500, detail="Failed to create role"))
        return created_role.one()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/roles", response_model=RoleReturn)
def get_roles():
    try:
        roles = role_services.read_all()
        if not role:
            raise HTTPException(status_code=404, detail="roles not found")

        return roles.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/role/{role_id}")
def del_role(role_id: int):
    conditions = {"role_id": role_id}
    try:
        del_rol = role_service.delete(conditions=conditions)
        if not result:
            raise HTTPException(500, "Failed to delete user")
        return {"message": f"Role deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

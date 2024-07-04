from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.role_service import RoleService
from utils.connectors import db_conn

role_service = RoleService(db_conn)
router = APIRouter()


class RoleCreate(BaseModel):
    name: str


class RoleReturn(BaseModel):
    id: int
    name: str


@router.post("/role", response_model=RoleReturn)
def create_role(role: RoleCreate):
    try:
        created_role = role_service.create(role.model_dump())
        if not created_role:
            raise HTTPException(
                status_code=500, detail="Failed to create role")
        return RoleReturn(**created_role.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/roles", response_model=List[RoleReturn])
def get_roles():
    try:
        roles = role_service.read_all()
        return [RoleReturn(**role) for role in roles.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/role/{id}", response_model=dict)
def delete_role(id: int):
    try:
        result = role_service.delete(conditions={"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Role not found")
        return {"message": "Role deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

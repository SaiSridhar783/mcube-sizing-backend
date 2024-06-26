from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.role_service import RoleService
from utils.connectors import db_conn

target_service = DeploymentTargetService(db_conn)
router = APIRouter()


class TargetCreate(BaseModel):
    target_name: str
    target_type: str


class TargetReturn(BaseModel):
    id: int
    target_name: str
    target_type: str


@router.post("/deployment_target", response_model=TargetReturn)
def create_target(role: TargetCreate):
    try:
        created_target = target_service.create(table= "deployment_target", data = TargetCreate)
        if not created_role:
            raise HTTPException(
                status_code=500, detail="Failed to create deployment_target")
        return TargetReturn(**created_target.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/deployment_targets", response_model=List[TargetReturn])
def get_roles():
    try:
        targets = target_service.read_all(table = "deployment_target")
        return [TargetReturn(**target) for target in targets.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/deployment_target/{id}", response_model=dict)
def delete_role(id: int):
    try:
        result = target_service.delete(table = "deployment_target", conditions = {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="target not found")
        return {"message": "Deployment Target deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

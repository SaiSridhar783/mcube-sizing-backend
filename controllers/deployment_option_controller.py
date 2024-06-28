from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.deployment_option_service import DeploymentTargetService
from utils.connectors import db_conn

target_service = DeploymentOptionService(db_conn)
router = APIRouter()


class TargetCreate(BaseModel):
    target_name: str
    target_type: str


class TargetReturn(BaseModel):
    id: int
    target_name: str
    target_type: str


@router.post("/", response_model=TargetReturn)
def create_target(data: TargetCreate):
    try:
        created_target = target_service.create(
            table="deployment_option", data=data.model_dump())
        if not created_target:
            raise HTTPException(
                status_code=500, detail="Failed to create deployment_option")
        return TargetReturn(**created_target.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TargetReturn])
def get_targets():
    try:
        targets = target_service.read_all(table="deployment_option")
        return [TargetReturn(**target) for target in targets.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", response_model=dict)
def delete_target(id: int):
    try:
        result = target_service.delete(
            table="deployment_option", conditions={"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="target not found")
        return {"message": "Deployment Option deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

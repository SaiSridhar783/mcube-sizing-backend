# mcube_component_controller.py

from fastapi import APIRouter, HTTPException, Path, FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from services.mcube_component_service import McubeComponent
from utils.connectors import db_conn


mcube_component_service = McubeComponent(db_conn)
router = APIRouter()


class McubeComponentBase(BaseModel):
    component_name: str
    component_ver: str
    component_category: str


class McubeComponentResponse(BaseModel):
    id: int
    mcube_ver: str
    component_name: str
    component_ver: str
    component_category: str
    created_on: datetime


class McubeResponsePost(BaseModel):
    id: int
    mcube_ver: str
    component_name: str
    component_ver: str
    component_category: str


class McubeComponentBasepatch(BaseModel):
    component_name: Optional[str] = None
    component_ver: Optional[str] = None
    component_category: Optional[str] = None


@router.get("/mcube_component/{id}/{mcube_ver}", response_model=McubeComponentBase)
def read_mcube_component(id: int = Path(..., description="Id of the mcube_component", gt=0), mcube_ver: str = Path(..., description="Version of the mcube_component")):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        mcube_components = mcube_component_service.read(
            table="mcube_component", conditions=conditions)
        if not mcube_components:
            raise HTTPException(
                status_code=404, detail="mcube_component not found")

        return [McubeComponentBase(**mcube_components.one())]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/mcube_component", response_model=McubeResponsePost)
def create_mcube_component(component: McubeResponsePost):
    try:
        created_component = mcube_component_service.create(
            "mcube_component", data=component.model_dump())
        return McubeComponentResponse(**created_component.one())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/mcube_component/{id}/{mcube_ver}", response_model=McubeComponentResponse)
def update_mcube_component(id: int, mcube_ver: str, component: McubeComponentBasepatch):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        updated_component = mcube_component_service.update(
            table="mcube_component", conditions=conditions,
            data=component.model_dump(exclude_unset=True))
        if not updated_component:
            raise HTTPException(
                status_code=404, detail="mcube_component not found")

        return McubeComponentBasepatch(**updated_component.one())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/mcube_component/{id}/{mcube_ver}", response_model=dict)
def delete_mcube_component(id: int, mcube_ver: str):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        result = mcube_component_service.delete(
            table="mcube_component", conditions=conditions)
        if not result:
            raise HTTPException(
                status_code=404, detail="mcube_component not found")

        return {"message": "mcube_component deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from services.mcube_component_service import McubeComponentService
from utils.connectors import db_conn

mcube_component_service = McubeComponentService(db_conn)
router = APIRouter()


class McubeComponentBase(BaseModel):
    mcube_ver: str
    component_name: str | None
    component_ver: str
    component_category: str


class McubeComponentCreate(McubeComponentBase):
    id: int


class McubeComponentUpdate(BaseModel):
    component_name: Optional[str] = None
    component_ver: Optional[str] = None
    component_category: Optional[str] = None


@router.post("/", response_model=McubeComponentCreate)
def create_mcube_component(component: McubeComponentCreate):
    try:
        created_component = mcube_component_service.create(
            "mcube_component", data=component.model_dump())
        return McubeComponentCreate(**created_component.one())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}/{mcube_ver}", response_model=McubeComponentCreate)
def read_mcube_component(
    id: int = Path(..., description="Id of the mcube_component", gt=0),
    mcube_ver: str = Path(..., description="Version of the mcube_component")
):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        mcube_component = mcube_component_service.read(
            table="mcube_component", conditions=conditions)
        if not mcube_component:
            raise HTTPException(
                status_code=404, detail="mcube_component not found")
        return McubeComponentCreate(**mcube_component.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{id}/{mcube_ver}", response_model=McubeComponentCreate)
def update_mcube_component(
    id: int,
    mcube_ver: str,
    component: McubeComponentUpdate
):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        updated_component = mcube_component_service.update(
            table="mcube_component",
            conditions=conditions,
            data=component.model_dump(exclude_unset=True)
        )
        if not updated_component:
            raise HTTPException(
                status_code=404, detail="mcube_component not found")
        return McubeComponentCreate(**updated_component.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}/{mcube_ver}", response_model=dict)
def delete_mcube_component(id: int, mcube_ver: str):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        result = mcube_component_service.delete(
            table="mcube_component", conditions=conditions)
        if not result:
            raise HTTPException(
                status_code=404, detail="mcube_component not found")
        return {"message": "mcube_component deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{category}", response_model=List[McubeComponentCreate])
def get_components_by_category(category: str):
    try:
        mcube_components = mcube_component_service.read(
            table="mcube_component", conditions={"component_category": category})
        if not mcube_components:
            raise HTTPException(
                status_code=404, detail="mcube_component not found")
        return [McubeComponentCreate(**mcube_component) for mcube_component in mcube_components.all()]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

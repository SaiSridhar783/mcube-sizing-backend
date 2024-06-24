# mcube_component_controller.py

from fastapi import APIRouter, HTTPException, Path, FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from services.mcube_component_service import McubeComponent
from connectors import db_conn


mcube_component_service = McubeComponent(db_conn)
router = APIRouter()

class McubeComponentBase(BaseModel):
    mcube_ver: str
    component_name: str
    component_ver: str
    component_category: str

class McubeComponentResponse(McubeComponentBase):
    user_id: int
    created_on: datetime
@router.get("/mcube_component/{id}/{mcube_ver}", response_model=List[McubeComponentResponse])
def read_mcube_component(id: int = Path(..., description="Id of the mcube_component", gt=0), mcube_ver: str = Path(..., description="Version of the mcube_component")):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        mcube_components = mcube_component_service.read(conditions=conditions)
        if not mcube_components:
            raise HTTPException(status_code=404, detail="mcube_component not found")
        
        return mcube_components
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/mcube_component", response_model=McubeComponentResponse)
def create_mcube_component(component: McubeComponentBase):
    try:
        created_component = mcube_component_service.create(component.dict())
        return created_component
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/mcube_component/{id}/{mcube_ver}", response_model=McubeComponentResponse)
def update_mcube_component(id: int, mcube_ver: str, component: McubeComponentBase):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        updated_component = mcube_component_service.update(conditions=conditions, data=component.dict())
        if not updated_component:
            raise HTTPException(status_code=404, detail="mcube_component not found")
        
        return updated_component
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/mcube_component/{id}/{mcube_ver}", response_model=dict)
def delete_mcube_component(id: int, mcube_ver: str):
    conditions = {"id": id, "mcube_ver": mcube_ver}
    try:
        result = mcube_component_service.delete(conditions=conditions)
        if not result:
            raise HTTPException(status_code=404, detail="mcube_component not found")
        
        return {"message": "mcube_component deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

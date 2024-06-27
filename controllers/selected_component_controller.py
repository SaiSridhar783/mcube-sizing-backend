from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.selected_component_service import ComponentService
from utils.connectors import db_conn

component_service = ComponentService(db_conn)
router = APIRouter()

class SelectedCompResponse(BaseModel):
    id : int
    estimation_id : int
    size_slab_id : int
    provided_by : int

class CompUpdate(BaseModel):
    estimation_id : Optional[int] = None
    size_slab_id : Optional[int] = None
    provided_by : Optional[int] = None

class CompBody(BaseModel):
    estimation_id : int
    size_slab_id : int
    provided_by : int

@router.get("/selected-components/{estimation_id}", response_model = List[SelectedCompResponse])
def compget(estimation_id : int):
    conditions = {"estimation_id" : estimation_id}
    try:
        selectcomponent_read = component_service.read(table = "selected_component", conditions = conditions)
        if not selectcomponent_read:
            raise HTTPException(
                status_code=404, detail="Failed to read selected component")
        return [SelectedCompResponse(**select) for select in selectcomponent_read.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/selected-components", response_model = SelectedCompResponse)
def compcreate(creating_component : CompBody):
    try:
        create_selectcomp = component_service.create(table = "selected_component", data = creating_component.model_dump())
        if not create_selectcomp:
            raise HTTPException(status_code = 500, detail = "coudn't create selected component")
        return SelectedCompResponse(**create_selectcomp.one())
    except Exception as e:
        raise HTTPException(status_code=400, detail = str(e))
    
@router.put("/selected-components/{id}", response_model = SelectedCompResponse)
def updatecompselect(id : int, updating_component : CompUpdate):
    conditions = {"id" : id}
    try:
        update_selectcomp = component_service.update(table = "selected_component", conditions = conditions, data = updating_component.model_dump(exclude_none=True))
        if not update_selectcomp:
            raise HTTPException(status_code = 500, detail = "coudn't update component for selected id")
        return SelectedCompResponse(**update_selectcomp.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail = str(e))

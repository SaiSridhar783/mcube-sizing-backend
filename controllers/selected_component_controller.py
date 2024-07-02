from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.selected_component_service import SelectedComponentService
from utils.connectors import db_conn

selected_component_service = SelectedComponentService(db_conn)
router = APIRouter()


class SelectedComponentResponse(BaseModel):
    id: int
    estimation_id: int
    size_slab_id: int
    provided_by: int
    component_name: Optional[str] = None


class SelectedComponentUpdate(BaseModel):
    estimation_id: Optional[int] = None
    size_slab_id: Optional[int] = None
    provided_by: Optional[int] = None


class SelectedComponentCreate(BaseModel):
    estimation_id: int
    size_slab_id: int
    provided_by: int


@router.get("/{estimation_id}", response_model=List[SelectedComponentResponse])
def get_selected_components(estimation_id: int):
    conditions = {"estimation_id": estimation_id}
    try:
        selected_components = selected_component_service.read_with_component_name(
            table="selected_component", conditions=conditions)
        if not selected_components:
            raise HTTPException(
                status_code=404, detail="No selected components found for this estimation")
        return [SelectedComponentResponse(**component) for component in selected_components.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create", response_model=SelectedComponentResponse)
def create_selected_component(component: SelectedComponentCreate):
    try:
        created_component = selected_component_service.create(
            table="selected_component", data=component.model_dump())
        if not created_component:
            raise HTTPException(
                status_code=500, detail="Failed to create selected component")
        return SelectedComponentResponse(**created_component.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=SelectedComponentResponse)
def update_selected_component(id: int, component: SelectedComponentUpdate):
    conditions = {"id": id}
    try:
        updated_component = selected_component_service.update(
            table="selected_component", conditions=conditions, data=component.model_dump(exclude_none=True))
        if not updated_component:
            raise HTTPException(
                status_code=500, detail="Failed to update selected component")
        return SelectedComponentResponse(**updated_component.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

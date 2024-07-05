from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.selected_component_service import SelectedComponentService
from utils.connectors import db_conn

selected_component_service = SelectedComponentService(db_conn)
router = APIRouter()


class MCubeComponentResponse(BaseModel):
    id: int
    mcube_ver: str
    component_name: str | None
    component_category: str
    component_ver: str


class SizeSlab(BaseModel):
    id: int
    price_model_name: str
    storage_range: str | None
    storage_gb: int | None
    cpu_range: str | None
    cpu_cores: int | None
    gpu_range: str | None
    gpu_gb: int | None
    memory_range: str | None
    memory_gb: int | None
    node_range: str | None
    node_count: int | None


class SelectedComponentResponse(BaseModel):
    id: int
    estimation_id: int
    size_slab_id: int
    provided_by: int


class SelectedComponentDetailResponse(BaseModel):
    selected_component: SelectedComponentResponse
    mcube_component: MCubeComponentResponse
    size_slab: SizeSlab


class SelectedComponentUpdate(BaseModel):
    provided_by: int


class SelectedComponentCreate(BaseModel):
    estimation_id: int
    size_slab_id: int
    provided_by: int


@router.get("/{estimation_id}", response_model=List[SelectedComponentDetailResponse])
def get_selected_components(estimation_id: int):
    try:
        selected_components = selected_component_service.read_with_details(
            estimation_id)
        if not selected_components:
            raise HTTPException(
                status_code=404, detail="No selected components found for this estimation")
        return selected_components
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/save/{estimation_id}/{size_slab_id}", response_model=SelectedComponentDetailResponse)
def upsert_selected_component(estimation_id: int, size_slab_id: int, component: SelectedComponentUpdate):
    try:
        upserted_component = selected_component_service.upsert(
            estimation_id, size_slab_id, component.model_dump())
        if not upserted_component:
            raise HTTPException(
                status_code=500, detail="Failed to upsert selected component")
        return SelectedComponentDetailResponse(**upserted_component)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create", response_model=SelectedComponentDetailResponse)
def create_selected_component(component: SelectedComponentCreate):
    try:
        created_component = selected_component_service.upsert(
            component.estimation_id, component.size_slab_id, component.model_dump())
        if not created_component:
            raise HTTPException(
                status_code=500, detail="Failed to create selected component")
        return SelectedComponentDetailResponse(**created_component)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{id}", response_model=SelectedComponentDetailResponse)
def update_selected_component(id: int, component: SelectedComponentUpdate):
    try:
        updated_component = selected_component_service.read(
            table="selected_component", conditions={"id": id}).one()
        if not updated_component:
            raise HTTPException(
                status_code=404, detail="Selected component not found")
        upserted_component = selected_component_service.upsert(
            updated_component["estimation_id"], updated_component["size_slab_id"], component.model_dump())
        if not upserted_component:
            raise HTTPException(
                status_code=500, detail="Failed to update selected component")
        return SelectedComponentDetailResponse(**upserted_component)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

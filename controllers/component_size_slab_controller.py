from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from services.component_size_slab_service import MCubeSizeSlabService
from utils.connectors import db_conn

size_slab_service = MCubeSizeSlabService(db_conn)
router = APIRouter()


class MCubeSizeSlabCreate(BaseModel):
    component_id: int
    price_model_name: Literal["basic", "standard", "premium"]
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


class MCubeSizeSlabResponse(BaseModel):
    id: int
    component_id: int
    price_model_name: Literal["basic", "standard", "premium"]
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


@router.post("/", response_model=MCubeSizeSlabResponse)
def create_size_slab(data: MCubeSizeSlabCreate):
    try:
        new_slab = size_slab_service.create_size_slab(
            table="mcube_component_size_slab", data=data.model_dump())
        if not new_slab:
            raise HTTPException(
                status_code=400, detail="Failed to create mCube component size slab")
        return MCubeSizeSlabResponse(**new_slab.one())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{slab_id}", response_model=MCubeSizeSlabResponse)
def get_size_slab(slab_id: int):
    try:
        slab = size_slab_service.get_size_slab(
            table="mcube_component_size_slab", conditions={"id": slab_id})
        if not slab:
            raise HTTPException(status_code=404, detail="Size slab not found")
        return MCubeSizeSlabResponse(**slab.one())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{slab_id}", response_model=MCubeSizeSlabResponse)
def update_size_slab(slab_id: int, data: MCubeSizeSlabCreate):
    try:
        updated_slab = size_slab_service.update_size_slab(
            table="mcube_component_size_slab", conditions={"id": slab_id}, data=data.model_dump())
        if not updated_slab:
            raise HTTPException(status_code=404, detail="Size slab not found")
        return MCubeSizeSlabResponse(**updated_slab.one())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{slab_id}", response_model=dict)
def delete_size_slab(slab_id: int):
    try:
        conditions = {"id": slab_id}
        deleted = size_slab_service.delete_size_slab(
            table="mcube_component_size_slab", conditions=conditions)
        if not deleted:
            raise HTTPException(status_code=404, detail="Size slab not found")
        return {"message": "mCube component size slab successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-component/{component_id}/{price_model_name}", response_model=List[MCubeSizeSlabResponse])
def get_size_slabs_by_component(component_id: int, price_model_name: Literal["basic", "standard", "premium"]):
    try:
        slabs = size_slab_service.get_size_slabs(table="mcube_component_size_slab", conditions={
            "component_id": component_id, "price_model_name": price_model_name})
        if not slabs:
            raise HTTPException(
                status_code=404, detail="No matching size slabs found")
        return [MCubeSizeSlabResponse(**slab) for slab in slabs.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

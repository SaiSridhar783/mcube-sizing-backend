from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
from services.component_size_slab_service import SizeSlabService
from utils.connectors import db_conn

slab_service = SizeSlabService(db_conn)
router = APIRouter()

class slabbody(BaseModel):
    component_id: int
    price_model_name: Literal["basic" | "standard" | "premium"]
    storage_range: str
    storage: int
    cpu_range: str
    cpu: int
    memory_range: str
    memory: int
    node_range: str
    node_count: int

class slabReturn(BaseModel):
    id : int
    component_id: int
    price_model_name: Literal["basic" | "standard" | "premium"]
    storage_range: str
    storage: int
    cpu_range: str
    cpu: int
    memory_range: str
    memory: int
    node_range: str
    node_count: int

@router.post("/", response_model = slabReturn)
def slab_add(data : slabbody):
    try: 
        new_slab = slab_service.SlabAdd(table = "mcube_component_size_slab", data = data.model_dump())
        if not new_sab:
            raise HTTPException(status_code=400, detail = "failed to create a component size slab")
        return slabReturn(**new_slab.one())
    except Exception as e:
        raise HTTPException(status_code=440, detail=str(e))

@router.get("/{id}", response_model = slabReturn)
def get_slab(id : int):
    try:
        read_slab = slab_service.ReadSlab(table="mcube_component_size_slab", conditions = {"id" : id})
        if not read_slab:
            raise HTTPException(status_code=400, detail="Failed to read")
        return slabReturn(**read_slab.one())
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
@router.patch("/{id}", response_model = slabReturn)
def patch_slab(id : int, data : slabbody):
    try:
        upated_slab = slab_service.SlabUpdate(table="mcube_component_size_slab", conditions = {"id" : id}, data = data.mode_dump())
        if not patch_slab:
            raise HTTPException(status_code=400, detail="failed to update")
        return slabReturn(**updated_slab.one())
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

@router.delete("/{id}", response_model = slabReturn)
def del_slab(id : int):
    try:
        conditions = {"id" : id}
        deleted_slab = slab_service.Slabdelete(table = "mcube_component_size_slab", conditions=conditions)
        if not patch_slab:
            raise HTTPException(status_code=400, detail="failed to update")
        return {"message" : "successfully deleted slab size"}
    except Exception as e:
        raise HTTPException(status_code=440, detail=str(e))

@router.get("/{component_id}/{price_model_name}", response_model = List[slabReturn])
def get_slab_byestimation(component_id : int, price_model_name : Literal["basic" | "standard" | "premium"]):
    try:
        read_slab = slab_service.ReadSlab(table="mcube_component_size_slab", conditions = {"component_id" : component_id, "price_model_name" : price_model_name})
        if not read_slab:
            raise HTTPException(status_code=400, detail="Failed to read")
        return [slabReturn(**read_slab) for read_slab in read_slab.fetchall()]
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
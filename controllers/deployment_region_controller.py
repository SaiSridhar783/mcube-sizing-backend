from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from services.deployment_region_service import RegionService
from utils.connectors import db_conn

region_service = RegionService(db_conn)
router = APIRouter()

class RegionPatch(BaseModel):
    region_name : str
    region_code : str

class RegionCreate(RegionPatch):
    deployment_option_id : int

class RegionResponse(BaseModel):
    id : int
    region_name : str
    region_code : str
    deployment_option_id : int

@router.post("/regions", response_model = RegionResponse)
def add_region(data :RegionCreate):
    try:
        new_region = region_service.regionadd(table = "deployment_region", data = data.model_dump())
        if not new_region:
            raise HTTPException(status_code=400, detail="Failed to add new region")
        return RegionResponse(**new_region.one())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/regions/{id}")
def delete_region( id : int):
    try:
        del_region = region_service.regiondelete(table = "deployment_region", conditions = {"id" : id})
        if not del_region:
            raise HTTPException(status_code=400, detail="coudn't delete region")
        return {"message" : "Region deleted Successfully"}
    except Exception as e:
        raise HTTPException(status_code=440, detail=str(e))

@router.get("/deployment_options/{deployment_option_id}/regions", response_model = List[RegionResponse])
def read_region(deployment_option_id : int):
    try: 
        reading_region = region_service.regionread(table = "deployment_region", conditions={"deployment_option_id" : deployment_option_id})
        if not reading_region:
            raise HTTPException(status_code=400, detail = "coudn't read region")
        return [RegionResponse(**r) for r in reading_region.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=440, detail = str(e))

@router.patch("/regions/{id}")
def update_region(id : int, data : RegionPatch):
    try: 
        updated_region = region_service.regionupdate(table = "deployment_region", data = data.model_dump(), conditions = {"id" : id})
        if not updated_region:
            raise HTTPException(status_code=400, detail="Coudn't update region")
        return RegionResponse(**updated_region.one())
    except Exception as e:
        raise HTTPException(status_code=440, detail = str(e))


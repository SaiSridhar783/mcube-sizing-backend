import fastapi
from fastapi import FastAPI, HTTPException, APIRouter, Path
from typing import Optional, List
from services.sizing_req_service import SizingRequirement
from pydantic import BaseModel
from connectors import db_conn

sizing_req_service = SizingRequirement(db_conn)
router = APIRouter()

class SizingCreate(BaseModel):
    data_vol : int
    tps_qps : int
    concurrent_users : int
    data_retention_period : int
    max_job_count : int #count
    max_report_count : int #count
    ai_ml_model : int
    high_availability : bool
    deployment_type : int
    location : str
    provided_by : int

class SizingUpdate(BaseModel):
    data_vol : Optional[int] = None
    tps_qps : Optional[int] = None
    concurrent_users : Optional[int] = None
    data_retention_period : Optional[int] = None
    max_job_count : Optional[int] = None #count
    max_report_count : Optional[int] = None #count
    ai_ml_model : Optional[int] = None
    high_availability : Optional[bool] = None
    deployment_type : Optional[int] = None
    location : Optional[str] = None
    provided_by : Optional[int] = None

class SizingResponse(BaseModel):
    id : int
    estimation_id : int
    data_vol: int 
    concurrent_users : int
    data_retention_period : int
    max_job_count : int #count
    max_report_count : int #count
    ai_ml_model : int
    high_availability : bool
    deployment_type : int
    location : str
    provided_by : int

class SizingResponse2(BaseModel):
    data_vol : int
    tps_qps : int
    concurrent_users : int
    data_retention_period : int
    max_job_count : int #count
    max_report_count : int #count
    ai_ml_model : int
    high_availability : bool
    deployment_type : int
    location : str
    provided_by : int


@router.get("/requirements/{estimation_id}", response_model=List[SizingResponse])
def read_sizing(estimation_id: int):
    conditions = {"estimation_id": estimation_id}
    try:
        sizing_params = sizing_req_service.read(table="sizing_requirement", conditions=conditions)
        if not sizing_params:
            raise HTTPException(status_code=404, detail="Estimation not found")
        return [SizingResponse(**t) for t in sizing_params.all()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update_requirement/{estimation_id}", response_model=SizingResponse)
def update_sizing(estimation_id: int, sizing: SizingUpdate):
    conditions = {"estimation_id": estimation_id}
    try:
        updated_sizing = sizing_req_service.update(table="sizing_requirement",data = sizing.model_dump(exclude_none=True), conditions = conditions)
        if not updated_sizing:
            raise HTTPException(
                status_code=500, detail="Sizing not updated")
        return SizingResponse(**updated_sizing.one())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{sizing_id}", response_model=dict)
def delete_sizing(sizing_id: int):
    conditions = {"id": sizing_id}
    try:
        result = sizing_req_service.delete(table="sizing_requirement", conditions=conditions)
        if not result:
            raise HTTPException(500, "Failed to delete sizing")
        return {"message": f"Sizing deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/save-requirements/{estimation_id}", response_model=SizingResponse2)
def create_sizing(sizing: SizingCreate, estimation_id : int):
    try:
        create_sizing = sizing_req_service.create(table = "sizing_requirement", data = sizing.model_dump(), condition_value = estimation_id)
        if not create_sizing:
            raise HTTPException(500, "Falied to create user")

        return SizingResponse2(**create_sizing.one())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

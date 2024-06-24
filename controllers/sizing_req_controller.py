import fastapi
from fastapi import FastAPI, HTTPException, APIRouter, Path
from typing import Optional, List
from services.sizing_req_service import SizingRequirement
from pydantic import BaseModel
from connectors import db_conn

sizing_req_service = SizingRequirement(db_conn)
router = APIRouter()

class SizingCreate(BaseModel):
    estimation_id : int
    data_vol : int
    TPS_QPS : int
    conc_unsers : int
    ret_period : int
    max_job : int #count
    max_report : int #count
    ai_ml : int
    high_availability : bool
    deploy_type : int
    provided_by : int

class SizingUpdate(BaseModel):
    estimation_id : Optional[int] = None
    data_vol : Optional[int] = None
    TPS_QPS : Optional[int] = None
    conc_unsers : Optional[int] = None
    ret_period : Optional[int] = None
    max_job : Optional[int] = None #count
    max_report : Optional[int] = None #count
    ai_ml : Optional[int] = None
    high_availability : Optional[bool] = None
    deploy_type : Optional[int] = None
    provided_by : Optional[int] = None

class SizingResponse(BaseModel):
    sizing_id : int
    estimation_id : int
    data_vol : int
    TPS_QPS : int
    conc_unsers : int
    ret_period : int
    max_job : int #count
    max_report : int #count
    ai_ml : int
    high_availability : bool
    deploy_type : int
    provided_by : int

@router.get("/requirements/{estimation_id}", response_model=List[dict])
def read_sizing(estimation_id: int):
    conditions = {"estimation_id": estimation_id}
    try:
        sizing_params = sizing_req_service.read(conditions=conditions)
        if not sizing_params:
            raise HTTPException(status_code=404, detail="User not found")

        return sizing_params.one()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{sizing_id}", response_model=dict)
def update_sizing(user_id: int, sizing: SizingUpdate):
    conditions = {"sizing_id": sizing_id}
    try:
        updated_sizing = sizing_req_service.update('sizing_requirements',sizing.model_dump(exclude_none=True), conditions)
        if not updated_user:
            raise HTTPException(
                status_code=500, detail="Sizing not updated")
        return {"message": "Sizing updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{sizing_id}", response_model=dict)
def delete_sizing(sizing_id: int):
    conditions = {"sizing_id": sizing_id}
    try:
        result = sizing_req_service_service.delete(conditions=conditions)
        if not result:
            raise HTTPException(500, "Failed to delete sizing")
        return {"message": f"Sizing deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/save-requirements/{estimation_id}", response_model=dict)
def create_sizing(sizing: SizingCreate, estimation_id : int):
    conditions = {"estimation_id" : estimation_id}
    try:
        create_sizing = sizing_req_service.create(sizing.model_dump(), condition_key = 'estimation_id', condition_value = estimation_id)
        if not create_sizing:
            raise HTTPException(500, "Falied to create user")

        return create_sizing.one()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

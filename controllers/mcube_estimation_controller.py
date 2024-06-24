import fastapi
from datetime import datetime
from fastapi import FastAPI, HTTPException, APIRouter, Path
from typing import Optional, List
from services.mcube_estimation_service import McubeEstimationService
from pydantic import BaseModel
from connectors import db_conn

mcube_estimation_service = McubeEstimationService(db_conn)
router = APIRouter()

class EstimationCreate(BaseModel):
    name : str
    created_by : int
    customer_name : str
    subitted : bool

class EstimationUpdate(BaseModel):
    name : Optional[str] = None
    created_by : Optional[int] = None
    customer_name : Optional[str] = None
    submitted : Optional[bool] = None

class EstimationResponse(BaseModel):
    estim_id : int
    name : str
    created_by : int
    customer_name : str
    subitted : bool

class EstimationResponse_time(BaseModel):
    estim_id : int
    name : str
    created_by : int
    customer_name : str
    subitted : bool
    created_on : datetime

class EstimationResponse_time2(BaseModel):
    estim_id : int
    name : str
    created_by : int
    customer_name : str
    subitted : bool
    created_on : datetime
    updated_on : datetime

@router.get("/get-submitted-estimations", response_model = EstimationResponse)
def read_estimations():
    try:
        return mcube_estimation_service.read_all('Mcube_Estimation')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get-estimation/{created_by}", response_model = EstimationResponse)
def read_estimation(created_by : int = Path(..., description = "Id for showing the requested", gt = 0)):
    conditions = {"created_by" : created_by}
    try: 
        if estimation_id not in mcube_estimation_service:
            raise HTTPException(status_code=404, detail="Estimation not found")

        estim = mcube_estimation_service.read( 'Mcube_Estimation', conditions = condition)
        return estim.one()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create_estimation", response_model = EstimationResponse_time)
def create_estimation(Estimation : EstimationCreate):
    try:
        create_estimation = mcube_estimation_service.create('Mcube_Estimation', Estimation.model_dump())
        if estimation_id in mcube_estimation_service:
            raise HTTPException(500, "Id already exists")
        return create_estimation.one()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update_estimation/{estimation_id}", response_model = EstimationResponse_time2)
def update_estimation(Estimation : EstimationUpdate, estimation_id : int):
    conditions = {"estimation_id" : estimation_id}
    try:
        update_estimation = mcube_estimation_service.update('Mcube_Estimation', Estimation.model_dump(exclude_none=True), conditions)
        if not update_estimation:
            raise HTTPException(
                status_code=500, detail="Estimation not updated")
        return update_estimation.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/estimation/{estimation_id}", response_model = dict)
def delete_estimation(estimation_id : int):
    conditions = {"estimation_id" : estimation_id}
    try:
        result = mcube_estimation_service.delete(conditions=conditions)
        if not result:
            raise HTTPException(500, "Failed to delete Estimation")
        return {"message": f"Estimation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
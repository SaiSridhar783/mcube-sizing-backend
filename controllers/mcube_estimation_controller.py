from fastapi import APIRouter, HTTPException, Path
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from services.mcube_estimation_service import McubeEstimationService
from utils.connectors import db_conn

mcube_estimation_service = McubeEstimationService(db_conn)
router = APIRouter()


class EstimationBase(BaseModel):
    estimation_name: str
    customer_name: str


class EstimationCreate(EstimationBase):
    created_by: int


class EstimationUpdate(BaseModel):
    estimation_name: Optional[str] = None
    customer_name: Optional[str] = None
    submitted: Optional[bool] = None


class EstimationResponse(EstimationBase):
    id: int
    created_by: int
    submitted: bool


class EstimationResponseWithTime(EstimationResponse):
    created_on: datetime


class EstimationResponseWithUpdateTime(EstimationResponseWithTime):
    updated_on: datetime


@router.get("/get-estimations-by-user/{user_id}", response_model=List[EstimationResponse])
def get_estimations_by_user(user_id: int = Path(..., gt=0)):
    try:
        estimations = mcube_estimation_service.read(
            'mcube_estimation', conditions={"created_by": user_id})
        return [EstimationResponse(**estimation) for estimation in estimations.all()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-estimation", response_model=EstimationResponseWithTime)
def create_estimation(estimation: EstimationCreate):
    try:
        created_estimation = mcube_estimation_service.create(
            'mcube_estimation', estimation.model_dump())
        return EstimationResponseWithTime(**created_estimation.one())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/estimation/{estimation_id}", response_model=dict)
def delete_estimation(estimation_id: int = Path(..., gt=0)):
    try:
        result = mcube_estimation_service.delete(
            'mcube_estimation', conditions={"id": estimation_id})
        if not result:
            raise HTTPException(status_code=404, detail="Estimation not found")
        return {"message": "Estimation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/estimation/{estimation_id}", response_model=EstimationResponseWithUpdateTime)
def update_estimation(estimation_id: int, estimation: EstimationUpdate):
    try:
        updated_estimation = mcube_estimation_service.update(
            'mcube_estimation', estimation.model_dump(exclude_unset=True), conditions={"id": estimation_id})
        if not updated_estimation:
            raise HTTPException(status_code=404, detail="Estimation not found")
        return EstimationResponseWithUpdateTime(**updated_estimation.one())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get-all-estimations", response_model=List[EstimationResponse])
def get_all_estimations():
    try:
        estimations = mcube_estimation_service.read('mcube_estimation')
        return [EstimationResponse(**estimation) for estimation in estimations.all()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get-submitted-estimations", response_model=List[EstimationResponse])
def get_submitted_estimations():
    try:
        estimations = mcube_estimation_service.read(
            'mcube_estimation', conditions={"submitted": True})
        return [EstimationResponse(**estimation) for estimation in estimations.all()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import HTTPException, APIRouter
from typing import Optional, List
from services.sizing_requirement_service import SizingRequirementService
from pydantic import BaseModel
from utils.connectors import db_conn

sizing_req_service = SizingRequirementService(db_conn)
router = APIRouter()


class SizingRequirementCreate(BaseModel):
    data_vol_gb: int
    tps_qps: int
    concurrent_users: int
    data_retention_period_months: int
    max_job_count: int
    max_report_count: int
    ai_ml_model: int
    high_availability: bool
    deployment_type: int
    deployment_region: int
    provided_by: int


class SizingRequirementUpdate(BaseModel):
    data_vol_gb: Optional[int] = None
    tps_qps: Optional[int] = None
    concurrent_users: Optional[int] = None
    data_retention_period_months: Optional[int] = None
    max_job_count: Optional[int] = None
    max_report_count: Optional[int] = None
    ai_ml_model: Optional[int] = None
    high_availability: Optional[bool] = None
    deployment_type: Optional[int] = None
    deployment_region: Optional[int] = None
    provided_by: Optional[int] = None


class SizingRequirementResponse(BaseModel):
    id: int
    estimation_id: int
    data_vol_gb: int
    tps_qps: int
    concurrent_users: int
    data_retention_period_months: int
    max_job_count: int
    max_report_count: int
    ai_ml_model: int
    high_availability: bool
    deployment_type: int
    deployment_region: int
    provided_by: int


@router.get("/requirements/{estimation_id}", response_model=SizingRequirementResponse)
def get_sizing_requirements(estimation_id: int):
    conditions = {"estimation_id": estimation_id}
    try:
        sizing_params = sizing_req_service.read(
            table="sizing_requirement", conditions=conditions)
        sizing_params_ = sizing_params.fetchone()
        if sizing_params_ is None:
            raise HTTPException(
                status_code=404, detail="Sizing Requirements not found")
        return SizingRequirementResponse(**sizing_params_)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update-requirement/{estimation_id}", response_model=SizingRequirementResponse)
def update_sizing_requirement(estimation_id: int, sizing: SizingRequirementUpdate):
    conditions = {"estimation_id": estimation_id}
    try:
        updated_sizing = sizing_req_service.update(
            table="sizing_requirement", data=sizing.model_dump(exclude_none=True), conditions=conditions)
        updated_sizing_ = updated_sizing.fetchone()
        if updated_sizing_ is None:
            raise HTTPException(
                status_code=404, detail="Sizing requirement not found")
        return SizingRequirementResponse(**updated_sizing_)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/requirement/{sizing_id}", response_model=dict)
def delete_sizing_requirement(sizing_id: int):
    conditions = {"id": sizing_id}
    try:
        result = sizing_req_service.delete(
            table="sizing_requirement", conditions=conditions)
        if not result:
            raise HTTPException(404, "Sizing requirement not found")
        return {"message": f"Sizing requirement deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/save-requirements/{estimation_id}", response_model=SizingRequirementResponse)
def create_sizing_requirement(sizing: SizingRequirementCreate, estimation_id: int):
    try:
        created_sizing = sizing_req_service.create(
            table="sizing_requirement", data=sizing.model_dump(), condition_value=estimation_id)
        created_sizing_ = created_sizing.fetchone()
        if created_sizing_ is None:
            raise HTTPException(500, "Failed to create sizing requirement")
        return SizingRequirementResponse(**created_sizing_)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

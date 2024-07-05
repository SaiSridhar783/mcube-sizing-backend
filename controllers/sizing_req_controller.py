from fastapi import HTTPException, APIRouter
from typing import Optional
from pydantic import BaseModel
from services.sizing_requirement_service import SizingRequirementService
from utils.connectors import db_conn

sizing_req_service = SizingRequirementService(db_conn)
router = APIRouter()


class DeploymentOption(BaseModel):
    id: int
    target_name: str
    target_type: str


class DeploymentRegion(BaseModel):
    id: int
    region_name: str
    region_code: str


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


class SizingRequirementDetailResponse(BaseModel):
    sizing_requirement: SizingRequirementResponse
    deployment_option: DeploymentOption
    deployment_region: DeploymentRegion


class SizingRequirementUpdate(BaseModel):
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


@router.get("/requirements/{estimation_id}", response_model=SizingRequirementDetailResponse)
def get_sizing_requirements(estimation_id: int):
    try:
        sizing_params = sizing_req_service.read_with_details(estimation_id)
        if sizing_params is None:
            raise HTTPException(
                status_code=404, detail="Sizing Requirements not found")
        return SizingRequirementDetailResponse(**sizing_params)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/save/{estimation_id}", response_model=SizingRequirementDetailResponse)
def upsert_sizing_requirement(estimation_id: int, sizing: SizingRequirementUpdate):
    try:
        upserted_sizing = sizing_req_service.upsert(
            estimation_id, sizing.model_dump())
        if upserted_sizing is None:
            raise HTTPException(
                status_code=500, detail="Failed to upsert sizing requirement")
        return SizingRequirementDetailResponse(**upserted_sizing)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/requirement/{sizing_id}", response_model=dict)
def delete_sizing_requirement(sizing_id: int):
    conditions = {"id": sizing_id}
    try:
        result = sizing_req_service.delete(
            conditions=conditions)
        if not result:
            raise HTTPException(404, "Sizing requirement not found")
        return {"message": f"Sizing requirement deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

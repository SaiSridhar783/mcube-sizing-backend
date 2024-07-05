from fastapi import HTTPException, APIRouter, Path
from typing import List, Optional, Literal
from services.deployment_spec_service import DeploymentSpecService
from pydantic import BaseModel
from utils.connectors import db_conn

spec_service = DeploymentSpecService(db_conn)
router = APIRouter()


class MCubeComponentResponse(BaseModel):
    id: int
    mcube_ver: str
    component_name: str | None
    component_category: str
    component_ver: str


class DeploymentSpecResponse(BaseModel):
    id: int
    estimation_id: int
    node_id: Optional[int]
    node_name: str
    node_type: Literal['driver', 'worker', 'executor',
                       'master', 'slave', 'data', 'broker', 'compute', 'storage']
    cpu: int
    gpu: int
    memory: int
    storage: int
    target_id: Optional[int]
    cost: Optional[float]


class SizeSlab(BaseModel):
    id: int
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


class DeploymentSpecDetailResponse(BaseModel):
    deployment_spec: DeploymentSpecResponse
    mcube_component: MCubeComponentResponse
    size_slab: SizeSlab


class DeploymentSpecCreate(BaseModel):
    node_name: str
    node_type: Literal['driver', 'worker', 'executor',
                       'master', 'slave', 'data', 'broker', 'compute', 'storage']
    cpu: int
    gpu: int
    memory: int
    storage: int


class DeploymentSpecUpdate(BaseModel):
    node_name: Optional[str] = None
    node_type: Optional[Literal['driver', 'worker', 'executor',
                                'master', 'slave', 'data', 'broker', 'compute', 'storage']] = None
    cpu: Optional[int] = None
    gpu: Optional[int] = None
    memory: Optional[int] = None
    storage: Optional[int] = None
    target_id: Optional[int] = None
    cost: Optional[float] = None


class DeploymentSpecSave(BaseModel):
    node_name: str
    node_type: Literal['driver', 'worker', 'executor',
                       'master', 'slave', 'data', 'broker', 'compute', 'storage']
    cpu: int
    gpu: int
    memory: int
    storage: int
    target_id: Optional[int] = None
    cost: Optional[float] = None


@router.get("/{estimation_id}", response_model=List[DeploymentSpecDetailResponse])
def get_deployment_specs(estimation_id: int = Path(..., description="Retrieve the detailed deployment specifications for a given estimation ID")):
    try:
        specs = spec_service.get_specs_with_details(estimation_id)
        if not specs:
            raise HTTPException(
                status_code=404, detail="No specifications found for this estimation ID")
        return [DeploymentSpecDetailResponse(**spec) for spec in specs]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save/{estimation_id}/{size_slab_id}", response_model=DeploymentSpecDetailResponse)
def save_deployment_spec(estimation_id: int, size_slab_id: int, data: DeploymentSpecSave):
    try:
        saved_spec = spec_service.upsert_spec(
            estimation_id, size_slab_id, data.model_dump(exclude_none=True))
        if not saved_spec:
            raise HTTPException(
                status_code=400, detail="Failed to save specification")
        return DeploymentSpecDetailResponse(**saved_spec)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{estimation_id}/{slab_id}", status_code=204)
def delete_deployment_spec(estimation_id: int, slab_id: int):
    try:
        deleted = spec_service.delete_spec(estimation_id, slab_id)
        if not deleted:
            raise HTTPException(
                status_code=404, detail="Specification not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

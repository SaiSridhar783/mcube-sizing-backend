from fastapi import HTTPException, APIRouter, Path
from typing import List, Optional
from services.deployment_spec_service import DeploymentSpecService
from pydantic import BaseModel
from utils.connectors import db_conn

spec_service = DeploymentSpecService(db_conn)
router = APIRouter()


class MCubeComponentResponse(BaseModel):
    id: int
    mcube_ver: str
    component_name: str
    component_category: str
    component_ver: str


class DeploymentSpecResponse(BaseModel):
    id: int
    node_id: int | None
    node_name: str
    node_type: str
    cpu: int
    memory: int
    storage: int
    target_id: int | None
    cost: float | None
    mcube_component: MCubeComponentResponse


class DeploymentSpecCreate(BaseModel):
    node_name: str
    node_type: str
    cpu: int
    memory: int
    storage: int


class DeploymentSpecUpdate(BaseModel):
    node_name: Optional[str] = None
    node_type: Optional[str] = None
    cpu: Optional[int] = None
    memory: Optional[int] = None
    storage: Optional[int] = None
    target_id: Optional[int] = None
    cost: Optional[float] = None


@router.get("/{estimation_id}", response_model=List[DeploymentSpecResponse])
def get_deployment_specs(estimation_id: int = Path(..., description="Retrieve the deployment specifications for a given estimation ID")):
    try:
        specs = spec_service.get_specs_with_component(estimation_id)
        if not specs:
            raise HTTPException(
                status_code=404, detail="No specifications found for this estimation ID")
        return [DeploymentSpecResponse(**spec) for spec in specs]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{estimation_id}/{size_slab_id}", response_model=DeploymentSpecResponse)
def create_deployment_spec(estimation_id: int, size_slab_id: int, data: DeploymentSpecCreate):
    try:
        new_spec = spec_service.create_spec(
            estimation_id, size_slab_id, data.model_dump())
        if not new_spec:
            raise HTTPException(
                status_code=400, detail="Failed to create new specification")
        return DeploymentSpecResponse(**new_spec)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{estimation_id}/{slab_id}", response_model=DeploymentSpecResponse)
def update_deployment_spec(estimation_id: int, slab_id: int, data: DeploymentSpecUpdate):
    try:
        updated_spec = spec_service.update_spec(
            estimation_id, slab_id, data.model_dump(exclude_none=True))
        if not updated_spec:
            raise HTTPException(
                status_code=404, detail="Specification not found")
        return DeploymentSpecResponse(**updated_spec)
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

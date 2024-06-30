from fastapi import HTTPException, APIRouter, Path
from typing import List
from services.deployment_spec_service import SpecService
from pydantic import BaseModel, condecimal
from utils.connectors import db_conn
from decimal import Decimal

spec_service = SpecService(db_conn)
router = APIRouter()

class componentresponse(BaseModel):
    id : int
    mcube_ver : str
    component_name : str
    component_category : str
    component_ver : str

class specgetresponse(BaseModel):
    id : int
    node_id : int
    node_name : str
    node_type : str
    cpu : int
    memory : int
    storage : int
    target_id : int
    cost: condecimal(max_digits=10, decimal_places=2)
    mcube_component : componentresponse

class specbody(BaseModel):
    node_name : str
    mcube_component_id : int
    node_type : str
    cpu : int
    memory : int
    storage : int

class specpatchbody(BaseModel):
    node_name : str
    node_type : str
    cpu : int
    memory : int
    storage : int
    target_id : int
    cost : condecimal(max_digits=10, decimal_places=2)

class specresponse(specpatchbody):
    id : int
    mcube_component_id : int


@router.get("/{estimation_id}", response_model = specgetresponse)
def get_specification(estimation_id : int = Path(..., description="Retrieve the deployment specifications for a given estimation ID")):
    conditions = {"estimation_id" : estimation_id}
    try:
        specification_on_estimation = spec_service.read_with_component(estimation_id)
        if not specification_on_estimation:
            raise HTTPException(status_code=404, detail = "specification not found")
        return specgetresponse(**specification_on_estimation.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.patch("/{estimation_id}/{component_id}", response_model = specresponse)
def spec_update(estimation_id : int, mcube_component_id : int, data : specpatchbody):
    conditions = {"estimation_id" : estimation_id, "mcube_component_id" : mcube_component_id}
    try:
        updated_spec = spec_service.specupdate(table = "deployment_spec", conditions = conditions, data = data.model_dump(exclude_unset=True))
        if not updated_spec:
            raise HTTPException(status_code=404, detail="Specification not found")
        return specresponse(**updated_spec.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/estimation_id", response_model = specresponse) 
def spec_post(estimation_id : int, data :  specbody):
    conditions = {"estimation_id" : estimation_id}
    try: 
        new_spec = spec_service.specadd(table = "deployment_spec", conditions = conditions, data = data.model_dump(exclude_none=True))
        if not new_spec:
            raise HTTPException(status_code=404, detail="failed to create new user")
        return specresponse(**new_spec.one())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{estimation_id}/{spec_id}")
def spec_delete(estimation_id : int, spec_id : int):
    conditions = {"estimation_id" : estimation_id, "id" : spec_id}
    try:
        deleted_spec = spec_service.specdelete(table="deployment_spec", conditions=conditions)
        if not deleted_spec:
            raise HTTPException(status_code=404, detail = "Non suitable found") 
        return {"message": "HTTP 204 No content"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

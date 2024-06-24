import fastapi
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

class EstimationUpdate(BaseModel):
    name : Optional[str] = None
    created_by : Optional[int] = None
    customer_name : Optional[str] = None

@router.get("/get-estimation", response_model = List[dict])
def read_estimations():
    try:
        return mcube_estimation_service.read_all('Mcube_Estimation')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get-estimation/{estimation_id}", response_model = List[dict])
def read_estimation(estimation_id : int = Path(..., description = "Id for showing the requested", gt = 0)):
    conditions = {"estimation_id" : estimation_id}
    try: 
        if estimation_id not in mcube_estimation_service:
            raise HTTPException(status_code=404, detail="Estimation not found")
        return mcube_estimation_service.read( 'Mcube_Estimation', conditions = condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/create_estimation/{estimation_id}", response_model = dict)
def create_estimation(Estimation : EstimationCreate):
    try:
        create_estimation = mcube_estimation_service.create('Mcube_Estimation', Estimation.model_dump())
        if estimation_id in mcube_estimation_service:
            raise HTTPException(500, "Id alreaady exists")
        return {"message": f"Estimation created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.put("/update_estimation/{estimation_id}", response_model = dict)
def update_estimation(Estimation : EstimationUpdate, estimation_id : int):
    conditions = {"estimation_id" : estimation_id}
    try:
        update_estimation = mcube_estimation_service.update('Mcube_Estimation', Estimation.model_dump(exclude_none=True), conditions)
        if not update_estimation:
            raise HTTPException(
                status_code=500, detail="User not updated")
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete_estimation/{estimation_id}", response_model = dict)
def delete_estimation(estimation_id : int):
    conditions = {"estimation_id" : estimation_id}
    try:
        result = mcube_estimation_service.delete('user', conditions=conditions)
        if not result:
            raise HTTPException(500, "Failed to delete user")
        return {"message": f"User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
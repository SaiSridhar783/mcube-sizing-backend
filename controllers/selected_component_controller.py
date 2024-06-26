from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.selected_component_service import ComponentService
from utils.connectors import db_conn

comp_service = ComponentServiceService(db_conn)
router = APIRouter()

class SelectedCompResponse(BaseModel):
    id : int
    estimation_id : int
    size_slab_id : int
    provided_by : int

class CompuUpdate(BaseModel):
    estimation_id : Optional[int] = None
    size_slab_id : Optional[int] = None
    provided_by : Optional[int] = None

class CompBody(BaseModel):
    estimation_id : int
    size_slab_id : int
    provided_by : int

@router.get(" /selected-components/{estimation_id}")
def compget(estimation_id : int, response_model = SelectedCompResponse):
    conditions = {"estimation_id" : estimation_id}
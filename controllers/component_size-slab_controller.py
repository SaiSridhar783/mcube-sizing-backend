from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
from services.component_size_slab_service import SizeSlabService
from utils.connectors import db_conn

slab_service = SizeSlabService(db_conn)
router = APIrouter()

def slabbody(BaseModel):
    component_id: int
    price_model_name: "basic" | "standard" | "premium"
    storage_range: str
    storage: int
    cpu_range: str
    cpu: int
    memory_range: str
    memory: int
    node_range: str
    node_count: int
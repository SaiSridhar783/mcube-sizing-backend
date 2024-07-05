from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from services.suggest_service import SuggestService
from utils.connectors import db_conn

router = APIRouter()
sizings = SuggestService(db_conn)

class SuggestResponse(BaseModel):
    id : int
    node_type : str
    cpu : int 
    memory : int
    storage : int

class SuggestNodes(BaseModel):
    n_data_nodes : int
    n_master_nodes : int
    cpu : int
    n_disk_storage : int
    n_memory_ram : int

class SizingRequest(BaseModel):
    rawdata: int
    scale_factor: float
    indep_tasks: int = 0
    tot_tasks: int = 0
    max_cpus_per_task: int = 0
    node_class: str = None
    mem_data_ratio: float = 30
    ret_lc: float = 1.0
    ncop: int = 1
    indexing_comp_ratio: float = 1.5
    lake_ratio: float = 0.5

@router.get("/suggested_estimations/{sizing_id}",response_model = List[SuggestResponse])
def read_suggestion(sizing_id : int):
    input_suggestion = sizings.read_sizing(conditions = {"id" : sizing_id})
    fetched_data = input_suggestion[0]
    input_params = {
        "rawdata": fetched_data["data_vol_gb"],
        "scale_factor": fetched_data("scale_factor", 1.25),
        "indep_tasks": fetched_data["max_job_count"],
        "tot_tasks": fetched_data["max_report_count"],
        "node_class": fetched_data.get("node_class", None),
        "mem_data_ratio": fetched_data.get("mem_data_ratio", 0),
        "ret_lc": fetched_data["data_retention_period_months"]*30*24,
        "ncop": 1,
        "indexing_comp_ratio": fetched_data.get("indexing_comp_ratio", 0.7),
        "lake_ratio": fetched_data.get("lake_ratio", 0.5)
    }
    try:
        result = sizings.get_sizing_requirements(**input_params)

    # Create an instance of SuggestNodes
        suggestion_out = SuggestNodes(
            n_data_nodes=result["data_node"],
            n_master_nodes=result["master_node"],
            cpu=result["cpu_cores"]/result["node_count"],
            n_disk_storage=result["memory_gb"]/result["data_node"],
            n_memory_ram=result["ram_per_node"] 
        )
        Node_types = ["data", "master"]

        suggestions = sizings.add_suggest_response(suggestion_out = suggestion_out, Node_types = Node_types)

        return [SuggestResponse(**suggestion) for suggestion in suggestions.all()]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


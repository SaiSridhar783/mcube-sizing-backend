from elasticsearch import ESClusterEstimator, EstimatorResult
from utils.db_connector import DBConnector
from typing import Optional, List

class SuggestService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.table = 'sizing_requirement'

    async def get_sizing_requirements(
    rawdata: int,
    scale_factor: float,
    indep_tasks: int = 0,
    tot_tasks: int = 0,
    node_class: Optional[str] = None,
    mem_data_ratio: float = 30,
    ret_lc: float = 1.0,
    ncop: int = 1,
    indexing_comp_ratio: float = 1.5,
    lake_ratio: float = 0.5
    ) -> EstimatorResult:
        estimator = ESClusterEstimator(rawdata, scale_factor, indep_tasks, tot_tasks, node_class, mem_data_ratio)
        result: EstimatorResult = estimator.mapping_scenario(ret_lc, ncop, indexing_comp_ratio, lake_ratio)
        return result

    def read_sizing(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def add_suggest_response(suggestion_out : List[dict], Node_types : List[str]):
        suggestions = []
        for suggestion_out in suggestion_out:
                #for data_node
            idx = max(suggestions.id)+1
            for t in Node_types:
                    
                while(i < range(suggestion_out[f'n_{t}_nodes'])):
                    suggestion = SuggestResponse(
                        id = idx + i,
                        node_type = t.capitalize(),
                        cpu = suggestion_out.cpu,
                        memory = suggestion_out.n_memory_ram,
                        storage = suggestion_out.n_disk_storage
                    )
                    i += 1
                    suggestions.append(suggestion)

        return suggestions



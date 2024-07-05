from utils.db_connector import DBConnector
from elasticsearch import ESClusterEstimator

class DeploymentSpecService:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def create_spec(self, estimation_id: int, size_slab_id: int, data: dict):
        data['estimation_id'] = estimation_id
        data['size_slab_id'] = size_slab_id
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO deployment_spec ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        return self.get_spec(last_inserted_id)

    #def suggest(self, estimation_id : int, component_id : int):
        

    def get_spec(self, slab_id: int, estimation_id: int):
        query = """
        SELECT 
            ds.id, ds.estimation_id, ds.node_id, ds.node_name, ds.node_type,
            ds.cpu, ds.memory, ds.storage, ds.target_id, ds.cost,
            mc.id as mc_id, mc.mcube_ver, mc.component_name, 
            mc.component_category, mc.component_ver
        FROM deployment_spec ds
        JOIN mcube_component_size_slab mcss ON ds.size_slab_id = mcss.id
        JOIN mcube_component mc ON mcss.component_id = mc.id
        WHERE ds.size_slab_id = :slab_id AND ds.estimation_id = :estimation_id
        """
        result = self.connector.execute(
            query, {'slab_id': slab_id, 'estimation_id': estimation_id})
        row = result.fetchone()
        if row:
            return self._format_spec_result(row)
        return None

    def get_specs_with_component(self, estimation_id: int):
        query = """
        SELECT 
            ds.id, ds.estimation_id, ds.node_id, ds.node_name, ds.node_type,
            ds.cpu, ds.memory, ds.storage, ds.target_id, ds.cost,
            mc.id as mc_id, mc.mcube_ver, mc.component_name, 
            mc.component_category, mc.component_ver
        FROM deployment_spec ds
        JOIN mcube_component_size_slab mcss ON ds.size_slab_id = mcss.id
        JOIN mcube_component mc ON mcss.component_id = mc.id
        WHERE ds.estimation_id = :estimation_id
        """
        result = self.connector.execute(
            query, {"estimation_id": estimation_id})
        return [self._format_spec_result(row) for row in result.fetchall()]

    def _format_spec_result(self, row: dict):
        return {
            "id": row["id"],
            "node_id": row["node_id"],
            "node_name": row["node_name"],
            "node_type": row["node_type"],
            "cpu": row["cpu"],
            "memory": row["memory"],
            "storage": row["storage"],
            "target_id": row["target_id"],
            "cost": row["cost"],
            "mcube_component": {
                "id": row["mc_id"],
                "mcube_ver": row["mcube_ver"],
                "component_name": row["component_name"],
                "component_category": row["component_category"],
                "component_ver": row["component_ver"]
            }
        }

    def update_spec(self, estimation_id: int, slab_id: int, data: dict):
        updates = ', '.join([f"{k} = :{k}" for k in data.keys()])
        query = f"""
        UPDATE deployment_spec 
        SET {updates} 
        WHERE size_slab_id = :slab_id AND estimation_id = :estimation_id
        """
        self.connector.execute(
            query, {**data, 'slab_id': slab_id, 'estimation_id': estimation_id})
        return self.get_spec(slab_id, estimation_id)

    def delete_spec(self, estimation_id: int, slab_id: int):
        query = 'DELETE FROM deployment_spec WHERE size_slab_id = :slab_id AND estimation_id = :estimation_id'
        result = self.connector.execute(
            query, {'slab_id': slab_id, 'estimation_id': estimation_id})
        return result

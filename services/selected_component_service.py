from utils.db_connector import DBConnector


class SelectedComponentService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.table = 'selected_component'

    def create(self, data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {self.table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created = self.read(conditions={"id": last_inserted_id})
        return created

    def read(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        rd = self.connector.execute(query, params)
        return rd

    def read_with_details(self, estimation_id: int):
        query = '''
        SELECT 
            sc.id, sc.estimation_id, sc.size_slab_id, sc.provided_by,
            mc.id as component_id, mc.mcube_ver, mc.component_name, 
            mc.component_category, mc.component_ver,
            mcss.id as slab_id, mcss.price_model_name, mcss.storage_range,
            mcss.storage_gb, mcss.cpu_range, mcss.cpu_cores, mcss.gpu_range, mcss.gpu_gb, mcss.memory_range,
            mcss.memory_gb, mcss.node_range, mcss.node_count
        FROM selected_component sc
        JOIN mcube_component_size_slab mcss ON sc.size_slab_id = mcss.id
        JOIN mcube_component mc ON mcss.component_id = mc.id
        WHERE sc.estimation_id = :estimation_id
        '''
        result = self.connector.execute(
            query, {'estimation_id': estimation_id})
        return [self._format_component_with_details(row) for row in result.fetchall()]

    def _format_component_with_details(self, row: dict):
        return {
            "selected_component": {
                "id": row["id"],
                "estimation_id": row["estimation_id"],
                "size_slab_id": row["size_slab_id"],
                "provided_by": row["provided_by"]
            },
            "mcube_component": {
                "id": row["component_id"],
                "mcube_ver": row["mcube_ver"],
                "component_name": row["component_name"],
                "component_category": row["component_category"],
                "component_ver": row["component_ver"]
            },
            "size_slab": {
                "id": row["slab_id"],
                "price_model_name": row["price_model_name"],
                "storage_range": row["storage_range"],
                "storage_gb": row["storage_gb"],
                "cpu_range": row["cpu_range"],
                "cpu_cores": row["cpu_cores"],
                "gpu_range": row["gpu_range"],
                "gpu_gb": row["gpu_gb"],
                "memory_range": row["memory_range"],
                "memory_gb": row["memory_gb"],
                "node_range": row["node_range"],
                "node_count": row["node_count"]
            }
        }

    def upsert(self, estimation_id: int, size_slab_id: int, data: dict):
        query = '''
        INSERT INTO selected_component (estimation_id, size_slab_id, provided_by)
        VALUES (:estimation_id, :size_slab_id, :provided_by)
        ON DUPLICATE KEY UPDATE
        provided_by = :provided_by
        '''
        self.connector.execute(query, {
            "estimation_id": estimation_id,
            "size_slab_id": size_slab_id,
            **data
        })
        return self.get_component_with_details(estimation_id, size_slab_id)

    def get_component_with_details(self, estimation_id: int, size_slab_id: int):
        query = '''
        SELECT 
            sc.id, sc.estimation_id, sc.size_slab_id, sc.provided_by,
            mc.id as component_id, mc.mcube_ver, mc.component_name, 
            mc.component_category, mc.component_ver,
            mcss.id as slab_id, mcss.price_model_name, mcss.storage_range,
            mcss.storage_gb, mcss.cpu_range, mcss.cpu_cores, mcss.gpu_range, mcss.gpu_gb, mcss.memory_range,
            mcss.memory_gb, mcss.node_range, mcss.node_count
        FROM selected_component sc
        JOIN mcube_component_size_slab mcss ON sc.size_slab_id = mcss.id
        JOIN mcube_component mc ON mcss.component_id = mc.id
        WHERE sc.estimation_id = :estimation_id AND sc.size_slab_id = :size_slab_id
        '''
        result = self.connector.execute(query, {
            'estimation_id': estimation_id,
            'size_slab_id': size_slab_id
        })
        row = result.fetchone()
        if row:
            return self._format_component_with_details(row)
        return None

from utils.db_connector import DBConnector

class SpecService:
    def __init__(self, connector : DBConnector):
        self.connector = connector

    def specadd(self,table : str, data : dict = None, conditions : dict = None):
        data.update(conditions)
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created_spec = self.specread(
            table, conditions={"id": last_inserted_id})
        return created_spec
    
    def specread(self, table : str, columns = '*', conditions : dict = None):
        query = f'SELECT {columns} from {table}'
        params = {}
        if conditions:
            query += f' WHERE {"AND".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def read_with_component(self, estimation_id: int):
        query = """
        SELECT 
            n.id, n.estimation_id, n.node_id, n.node_name, n.node_type, n.cpu, n.memory, 
            n.storage, n.target_id, n.cost, 
            mc.id as mcube_component_id, mc.mcube_ver, mc.component_name, 
            mc.component_category, mc.component_ver
        FROM deployment_spec n
        JOIN mcube_component mc ON n.mcube_component_id = mc.id
        WHERE n.estimation_id = :estimation_id
        """
        result = self.connector.execute(query, {"estimation_id": estimation_id})
        return result

    def specupdate(self, table : str, conditions : dict = None, data : dict = None):
        conds = 'AND'.join([f"{k} = :{k}" for k in conditions.keys()])
        updates = ', '.join([f"{k} = :{k}" for k in data.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {conds}'
        self.connector.execute(query, {**data, **conditions})
        updated_spec = self.specread(table, conditions = {"id" : last_inserted_id})
        return updated_spec

    def specdelete(self, table : str, conditions : dict = None):
        conds = 'AND'.join([f"{k} = :{k}" for k in conditions.keys()])
        query = f'DELETE FROM {table} WHERE {conds}'
        return self.connector.execute(query, conds)
    


from utils.db_connector import DBConnector


class DeploymentOptionService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.table = 'deployment_option'

    def create(self, data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {self.table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created_target = self.read(conditions={"id": last_inserted_id})
        return created_target

    def read_all(self):
        return self.read()

    def read(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def delete(self, conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {self.table} WHERE {conds}'
        return self.connector.execute(query, conditions)

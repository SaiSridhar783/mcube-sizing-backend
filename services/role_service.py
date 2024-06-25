from db_connector import DBConnector

class RolesService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
    
    def create(self, table: str, data : dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        created_role = self.read(table, conditions=data)
        return created_role

    def read_all(self, table: str):
        return self.read(table)

    def read(self, table: str, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def delete(self, table: str, conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {table} WHERE {conds}'
        deleted_role = self.connector.execute(query, conditions)
        return deleted_role
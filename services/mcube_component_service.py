from utils.db_connector import DBConnector


class McubeComponentService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.table = 'mcube_component'

    def create(self, data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {self.table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        created_component = self.read(
            conditions={"id": data['id'], "mcube_ver": data['mcube_ver']})
        return created_component

    def read(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def read_all(self):
        return self.read()

    def update(self, data: dict, conditions: dict):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {self.table} SET {updates} WHERE {conds}'
        self.connector.execute(query, {**data, **conditions})
        updated_component = self.read(conditions=conditions)
        return updated_component

    def delete(self, conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {self.table} WHERE {conds}'
        return self.connector.execute(query, conditions)

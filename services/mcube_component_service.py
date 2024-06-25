from utils.db_connector import DBConnector


class McubeComponent:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def create(self, table: str, data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        creared_component = self.read(table, conditions=data)
        return created_component

    def read(self, table: str, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def read_all(self, table='mcube_component'):
        return self.read(table)

    def update(self, table: str, data: dict, conditions: dict):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {conds}'
        self.connector.execute(query, {**data, **conditions})
        updated_component = self.read(table, conditions=conditions)
        return updated_component

    def delete(self, *, table='mcube_component', conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {table} WHERE {conds}'
        return self.connector.execute(query, conditions)

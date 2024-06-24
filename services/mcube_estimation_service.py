from db_connector import DBConnector

class McubeEstimationService:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def create(self, * ,table = 'Mcube_Estimation', data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        created_user = self.connector.execute(query, data)
        return created_user

    def read(self, table = 'Mcube_Estimation', columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def read_all(self, table = 'Mcube_Estimation'):
        return self.read(table)

    def update(self, * ,table = 'Mcube_Estimation', data: dict, conditions: dict):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE Mcube_Estimation SET {updates} WHERE {conds}'
        updated_user = self.connector.execute(query, {**data, **conditions})
        return updated_user

    def delete(self, * ,table = 'Mcube_Estimation', conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {table} WHERE {conds}'
        deleted_user = self.connector.execute(query, conditions)
        return deleted_user

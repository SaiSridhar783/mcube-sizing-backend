from db_connector import DBConnector


class McubeComponent:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def get_id(self) -> int:
        return max(self.users.keys(), default=0)

    def create(self, * ,table = 'mcube_component', data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        created_sizing = self.connector.execute(query, data)
        #created_sizing['id'] = self.get_id() + 1
        return created_sizing

    def read(self, table = 'mcube_component', columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def read_all(self, table = 'mcube_component'):
        return self.read(table)

    def update(self, *,table = 'mcube_component', data: dict, conditions: dict):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {conds}'
        updated_sizing = self.connector.execute(query, {**data, **conditions})
        return updated_sizing

    def delete(self, *,table = 'mcube_component', conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {table} WHERE {conds}'
        deleted_sizing = self.connector.execute(query, conditions)
        return deleted_sizing

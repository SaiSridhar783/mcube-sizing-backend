from db_connector import DBConnector


class SizingRequirement:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def create(self, *, table='sizing_requirements', data: dict, condition_key : str, condition_value):
    
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        data[condition_key] = condition_value
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
    
        self.connector.execute(query, data)

        created_sizing = self.read(table, conditions = data)
        return created_sizing

    def read(self, table = 'sizing_requirements', columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def read_all(self, table = 'sizing_requirements'):
        return self.read(table)

    def update(self, *,table = 'sizing_requirements', data: dict, conditions: dict):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {conds}'
        self.connector.execute(query, {**data, **conditions})
        updated_sizing = self.read(table, conditions=data)
        return updated_sizing

    def delete(self, *,table = 'sizing_requirements', conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {table} WHERE {conds}'
        deleted_sizing = self.connector.execute(query, conditions)
        return deleted_sizing
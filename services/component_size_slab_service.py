from utils.db_connector import DBConnector


class MCubeSizeSlabService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.table = 'mcube_component_size_slab'

    def create_size_slab(self, data: dict = None):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{k}" for k in data.keys()])
        query = f'INSERT INTO {self.table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        added_slab = self.get_size_slab(
            conditions={"id": last_inserted_id})
        return added_slab

    def get_size_slab(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def get_all_size_slabs(self):
        return self.get_size_slab()

    def update_size_slab(self, data: dict, conditions: dict = None):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        where_clause = 'AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {self.table} SET {updates} WHERE {where_clause}'
        self.connector.execute(query, {**data, **conditions})
        updated = self.get_size_slab(self.table, conditions=conditions)
        return updated

    def delete_size_slab(self, conditions: dict):
        where_clause = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f"DELETE FROM {self.table} WHERE {where_clause}"
        return self.connector.execute(query, conditions)

    def get_size_slabs(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

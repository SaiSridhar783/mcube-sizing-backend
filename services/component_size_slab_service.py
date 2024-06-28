from utils.db_connector import DBConnector


class MCubeSizeSlabService:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def create_size_slab(self, table: str, data: dict = None):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{k}" for k in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        added_slab = self.get_size_slab(
            table, conditions={"id": last_inserted_id})
        return added_slab

    def get_size_slab(self, table: str, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def get_all_size_slabs(self, table: str):
        return self.get_size_slab(table)

    def update_size_slab(self, table: str, data: dict, conditions: dict = None):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        where_clause = 'AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {where_clause}'
        self.connector.execute(query, {**data, **conditions})
        updated = self.get_size_slab(table, conditions=conditions)
        return updated

    def delete_size_slab(self, table: str, conditions: dict):
        where_clause = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return self.connector.execute(query, conditions)

    def get_size_slabs(self, table: str, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

from utils.db_connector import DBConnector


class SelectedComponentService:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def create(self, table: str, data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created = self.read(table, conditions={"id": last_inserted_id})
        return created

    def read(self, table: str, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        rd = self.connector.execute(query, params)
        return rd

    def read_all(self, table: str):
        return self.read(table)

    def update(self, table: str, data: dict, conditions: dict = None):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        changes = 'AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {changes}'
        self.connector.execute(query, {**data, **conditions})
        updated = self.read(table, conditions=conditions)
        return updated

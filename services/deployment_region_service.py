from utils.db_connector import DBConnector


class RegionService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.table = 'deployment_region'

    def region_add(self, data: dict = None):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {self.table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created_target = self.region_read(
            conditions={"id": last_inserted_id})
        return created_target

    def region_read(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def region_update(self, data: dict, conditions: dict = None):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        where_clause = 'AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {self.table} SET {updates} WHERE {where_clause}'
        self.connector.execute(query, {**data, **conditions})
        updated = self.region_read(conditions=conditions)
        return updated

    def region_delete(self, conditions: dict):
        where_clause = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f"DELETE FROM {self.table} WHERE {where_clause}"
        return self.connector.execute(query, conditions)

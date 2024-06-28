from utils.db_connector import DBConnector

class RegionService:
    def __init__(self, connector : DBConnector):
        self.connector = connector

    def regionadd(self, table : str, data : dict = None):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created_target = self.regionread(table, conditions={"id": last_inserted_id})
        return created_target

    def regionread(self, *,columns = '*', table : str, conditions : dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def regionupdate(self, data : dict, table : str, conditions : dict = None):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        where_clause = 'AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {where_clause}'
        self.connector.execute(query, {**data, **conditions})
        updated = self.regionread(table, conditions=conditions)
        return updated

    def regiondelete(self, table:str, conditions : dict):
        where_clause = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return self.connector.execute(query, conditions)
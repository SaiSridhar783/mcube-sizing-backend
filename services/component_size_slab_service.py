from utils.db_connector import DBConnector

class SizeSlabService:
    def __init__(self, connector : DBConnector):
        self.connector = connector

    def SlabAdd(self, table : str, data : dict = None):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{k}" for k in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        self.connector.execute(query, data)
        added_slab = self.ReadSlab(table, conditions = {"id" : last_inserted_id})
        return added_slab

    def ReadSlab(self, table:str, columns = '*', conditions : dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        rd = self.connector.execute(query, params)
        return rd

    def read_all(self, table: str):
        return self.ReadSlab(table)

    def SlabUpdate(self, table : str, data : dict, conditions : dict = None):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        changes = 'AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {changes}'
        self.connector.execute(query, {**data, **conditions})
        updated = self.ReadSlab(table, conditions = conditions)
        return updated

    def Slabdelete(slef, table : str, conditions : dict):
        conds = ', '.join([f'{k} = :{k}' for k in conditions.keys()])
        deleted = f"DELETE FROM {table} WHERE {conds}"
        return self.connector.execute(query, conds)
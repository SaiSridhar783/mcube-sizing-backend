from utils.db_connector import DBConnector

class SizeSlabService:
    def __init__(slef, connector : DBConnector):
        self.connector = connector

    def SlabAdd(self, table : str, data : dict = None):
        keys = ', '.join(data.keys())
        values = ', '.join([f"{k} for k in data.keys()"])
        query = f'INSERT INTO {table} ({keys} VALUES {values})'
        last_inserted_id = self.connector.execute(f"LAST_INSERTE_ID() as id").first()["id"]
        self.connector.execute(query, data)
        added_slab = self.read(table, conditions = {"id" : last_inserted_id})
        return added_slab

    def ReadSlab(self, table:str, columns = '*', conditions : dict = None):
        keys = ', '.join(conditions.keys())
        query = ', '.join()
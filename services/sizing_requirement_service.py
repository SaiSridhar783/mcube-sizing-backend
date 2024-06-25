from utils.db_connector import DBConnector


class SizingRequirementService:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def create(self, table: str, data: dict, condition_value: int):
        data["estimation_id"] = condition_value
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'

        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created_sizing = self.read(table, conditions={"id": last_inserted_id})
        return created_sizing

    def read(self, table: str, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def update(self, table: str, data: dict, conditions: dict):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {conds}'
        self.connector.execute(query, {**data, **conditions})
        updated_sizing = self.read(table, conditions=data)
        return updated_sizing

    def delete(self, table: str, conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {table} WHERE {conds}'
        deleted_sizing = self.connector.execute(query, conditions)
        return deleted_sizing

from utils.db_connector import DBConnector


class SizingRequirementService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.table = 'sizing_requirement'

    def create(self, data: dict, condition_value: int):
        data["estimation_id"] = condition_value
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {self.table} ({keys}) VALUES ({values})'

        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created_sizing = self.read(conditions={"id": last_inserted_id})
        return created_sizing

    def read(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def update(self, data: dict, conditions: dict):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {self.table} SET {updates} WHERE {conds}'
        self.connector.execute(query, {**data, **conditions})
        updated_sizing = self.read(conditions=data)
        return updated_sizing

    def delete(self, conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {self.table} WHERE {conds}'
        deleted_sizing = self.connector.execute(query, conditions)
        return deleted_sizing

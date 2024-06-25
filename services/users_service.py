from utils.db_connector import DBConnector


class UsersService:
    def __init__(self, connector: DBConnector):
        self.connector = connector

    def create(self, table: str, data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        created_user = self.read(table, conditions=data)
        return created_user

    def read(self, table: str, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        return self.connector.execute(query, params)

    def read_with_role(self, user_id: int):
        query = """
        SELECT u.user_id, u.name, u.email, r.name as role_name
        FROM user u
        JOIN role r ON u.role_id = r.id
        WHERE u.user_id = :user_id
        """
        result = self.connector.execute(query, {"user_id": user_id})
        return result

    def update(self, table: str, data: dict, conditions: dict):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {table} SET {updates} WHERE {conds}'
        self.connector.execute(query, {**data, **conditions})
        updated_user = self.read(table, conditions=conditions)
        return updated_user

    def delete(self, table: str, conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {table} WHERE {conds}'
        return self.connector.execute(query, conditions)

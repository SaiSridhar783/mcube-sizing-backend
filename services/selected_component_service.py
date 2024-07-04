from utils.db_connector import DBConnector


class SelectedComponentService:
    def __init__(self, connector: DBConnector):
        self.connector = connector
        self.table = 'selected_component'

    def create(self, data: dict):
        keys = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        query = f'INSERT INTO {self.table} ({keys}) VALUES ({values})'
        self.connector.execute(query, data)
        last_inserted_id = self.connector.execute(
            "SELECT LAST_INSERT_ID() AS id").first()["id"]
        created = self.read(conditions={"id": last_inserted_id})
        return created

    def read(self, columns='*', conditions: dict = None):
        query = f'SELECT {columns} FROM {self.table}'
        params = {}
        if conditions:
            query += f' WHERE {" AND ".join([f"{k} = :{k}" for k in conditions.keys()])}'
            params = conditions
        rd = self.connector.execute(query, params)
        return rd

    def read_with_component_name(self, columns='*', conditions: dict = None):
        query = f"""
        SELECT sc.*, mc.component_name
        FROM {self.table} sc
        JOIN mcube_component_size_slab mcss ON sc.size_slab_id = mcss.id
        JOIN mcube_component mc ON mcss.component_id = mc.id
        """

        params = {}
        if conditions:
            where_clause = " AND ".join(
                [f"{k} = :{k}" for k in conditions.keys()])
            query += f' WHERE {where_clause}'
            params = conditions

        rd = self.connector.execute(query, params)
        return rd

    def read_all(self):
        return self.read()

    def update(self, data: dict, conditions: dict = None):
        updates = ', '.join([f'{k} = :{k}' for k in data.keys()])
        changes = 'AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'UPDATE {self.table} SET {updates} WHERE {changes}'
        self.connector.execute(query, {**data, **conditions})
        updated = self.read(conditions=conditions)
        return updated

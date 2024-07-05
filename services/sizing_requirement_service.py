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

    def read_with_details(self, estimation_id: int):
        query = '''
        SELECT 
            sr.*,
            do.target_name, do.target_type,
            dr.region_name, dr.region_code
        FROM sizing_requirement sr
        JOIN deployment_option do ON sr.deployment_type = do.id
        JOIN deployment_region dr ON sr.deployment_region = dr.id
        WHERE sr.estimation_id = :estimation_id
        '''
        result = self.connector.execute(
            query, {'estimation_id': estimation_id})
        row = result.fetchone()
        if row:
            return self._format_sizing_requirement_with_details(row)
        return None

    def _format_sizing_requirement_with_details(self, row: dict):
        return {
            "sizing_requirement": {
                "id": row["id"],
                "estimation_id": row["estimation_id"],
                "data_vol_gb": row["data_vol_gb"],
                "tps_qps": row["tps_qps"],
                "concurrent_users": row["concurrent_users"],
                "data_retention_period_months": row["data_retention_period_months"],
                "max_job_count": row["max_job_count"],
                "max_report_count": row["max_report_count"],
                "ai_ml_model": row["ai_ml_model"],
                "high_availability": row["high_availability"],
                "deployment_type": row["deployment_type"],
                "deployment_region": row["deployment_region"],
                "provided_by": row["provided_by"]
            },
            "deployment_option": {
                "id": row["deployment_type"],
                "target_name": row["target_name"],
                "target_type": row["target_type"]
            },
            "deployment_region": {
                "id": row["deployment_region"],
                "region_name": row["region_name"],
                "region_code": row["region_code"]
            }
        }

    def upsert(self, estimation_id: int, data: dict):
        query = '''
        INSERT INTO sizing_requirement 
        (estimation_id, data_vol_gb, tps_qps, concurrent_users, data_retention_period_months, 
        max_job_count, max_report_count, ai_ml_model, high_availability, deployment_type, 
        deployment_region, provided_by)
        VALUES 
        (:estimation_id, :data_vol_gb, :tps_qps, :concurrent_users, :data_retention_period_months, 
        :max_job_count, :max_report_count, :ai_ml_model, :high_availability, :deployment_type, 
        :deployment_region, :provided_by)
        ON DUPLICATE KEY UPDATE
        data_vol_gb = :data_vol_gb,
        tps_qps = :tps_qps,
        concurrent_users = :concurrent_users,
        data_retention_period_months = :data_retention_period_months,
        max_job_count = :max_job_count,
        max_report_count = :max_report_count,
        ai_ml_model = :ai_ml_model,
        high_availability = :high_availability,
        deployment_type = :deployment_type,
        deployment_region = :deployment_region,
        provided_by = :provided_by
        '''
        self.connector.execute(query, {"estimation_id": estimation_id, **data})
        return self.read_with_details(estimation_id)

    def delete(self, conditions: dict):
        conds = ' AND '.join([f'{k} = :{k}' for k in conditions.keys()])
        query = f'DELETE FROM {self.table} WHERE {conds}'
        deleted_sizing = self.connector.execute(query, conditions)
        return deleted_sizing

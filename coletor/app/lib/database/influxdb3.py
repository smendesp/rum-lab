from influxdb_client_3 import InfluxDBClient3
from app.config.settings import settings

# Authorization: Bearer apiv3_ycTA5tXFXZBpqjJFzqInhF3FgAj49Ag_HblCuX90R-5s1HPUTyNu1_wf1UNbhI_iSwIOXf_hi0OQx5lRNaaHCg

class InfluxDB:
    def __init__(self, host : str = '', database: str = '', token: str = ''):
        self.influxdb = InfluxDBClient3(
            host=str(settings.INFLUXDB_URL) if host == '' else host,
            database=str(settings.INFLUXDB_DATABASE) if database == '' else database,
            token=str(settings.INFLUXDB_TOKEN) if token == '' else token,
        )

    def get_client(self):
        return self.influxdb
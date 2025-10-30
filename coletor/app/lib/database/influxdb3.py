from influxdb_client_3 import InfluxDBClient3, WriteOptions
from app.config.settings import settings

# Authorization: Bearer apiv3_ycTA5tXFXZBpqjJFzqInhF3FgAj49Ag_HblCuX90R-5s1HPUTyNu1_wf1UNbhI_iSwIOXf_hi0OQx5lRNaaHCg


class InfluxDB:
    def __init__(self, host: str = '', database: str = '', token: str = ''):

        write_options = WriteOptions(
            batch_size=1000,
            flush_interval=10_000,
            jitter_interval=2_000,
            retry_interval=5_000,
            max_retries=3,
            max_retry_delay=30_000,
        )

        self.influxdb = InfluxDBClient3(
            host=str(settings.INFLUXDB_URL) if host == '' else host,
            database=str(settings.INFLUXDB_DATABASE)
            if database == ''
            else database,
            token=str(settings.INFLUXDB_TOKEN) if token == '' else token,
            write_options=write_options,
        )

    def get_client(self):
        return self.influxdb

from influxdb_client_3 import Point, WriteOptions
from app.lib.database.influxdb3 import InfluxDB
from app.lib.logger import Logger
from app.config.settings import settings
from datetime import datetime, timezone
import uuid


class TimeSeries:
    def __init__(self):

        self.log = Logger()
        ifx_db = InfluxDB()
        self.timeseries = ifx_db.get_client()

    def get_timestamp(self, timestamp: str = ''):
        if str(settings.TS_ORIGIN) == 'COLETOR':
            return int(datetime.now(timezone.utc))
        elif str(settings.TS_ORIGIN) == 'AGENTE':
            return timestamp
        elif str(settings.TS_ORIGIN) == 'DATABASE':
            return None

    def get_id(self):
        return str(uuid.uuid4())

from influxdb_client_3 import Point, WriteOptions
from app.lib.database.influxdb3 import InfluxDB
from app.lib.logger import Logger
import uuid


class TimeSeries:
    def __init__(self):

        self.log = Logger()
        ifx_db = InfluxDB()
        self.timeseries = ifx_db.get_client()

    def get_id(self):
        return str(uuid.uuid4())

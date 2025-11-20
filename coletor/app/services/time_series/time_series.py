from influxdb_client_3 import Point, WriteOptions
from app.lib.database.influxdb3 import InfluxDB
from app.lib.logger import Logger
from app.lib.utils import Utils

import uuid


class TimeSeries:
    def __init__(self):

        self.log = Logger()
        ifx_db = InfluxDB()
        self.timeseries = ifx_db.get_client()
        self.utils = Utils()  

    def get_id(self):
        return str(uuid.uuid4())

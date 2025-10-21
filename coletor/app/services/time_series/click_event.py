from influxdb_client_3 import Point, WriteOptions
from app.lib.database.influxdb3 import InfluxDB
from app.lib.logger import Logger


class ClickEvent:
    def __init__(self):

        self.logger = Logger()

        ifx_db = InfluxDB(database='rum')

        self.timeseries = ifx_db.get_client()

    def set_click_events(self, events: list):

        print(f'Events to write: {events}')

        data_points: list = []

        for event in events:
            data_point = (
                Point('click-event')
                .tag('appKey', event['appKey'])
                .tag('eventType', event['eventType'])
                .tag('sessionId', event['sessionId'])
                .tag('tuserIdext', event['userId'])
                .tag('pageUrl', event['pageUrl'])
                .tag('userAgent', event['userAgent'])
                .tag('clickElement', event['clickElement'])
                .tag('clickText', event['clickText'])
                .tag('clickX', event['clickX'])
                .tag('clickY', event['clickY'])
                .field('count', 1)
                .time(event['timestamp'])
            )
            data_points.append(data_point)

            # self.logger.logger.debug(f'++++++++++++: {data_point.to_line_protocol()}')

        self.timeseries.write(record=data_points)

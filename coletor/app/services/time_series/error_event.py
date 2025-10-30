from influxdb_client_3 import Point
from app.services.time_series.time_series import TimeSeries


class ErrorEvent(TimeSeries):
    def __init__(self):
        super().__init__()

    def set_events(self, events: list):

        data_points: list = []

        for event in events:
            data_point = (
                Point('error_event')
                .tag('id', self.get_id())
                .tag('app_key', event['app_key'])
                .tag('event_type', event['event_type'])
                .tag('session_id', event['session_id'])
                .tag('user_id', event['user_id'])
                .tag('page_url', event['page_url'])
                .tag('user_agent', event['user_agent'])
                .tag('message', event['message'])
                .tag('stack', event['stack'])
                .tag('filename', event['filename'])
                .tag('lineno', event['lineno'])
                .tag('colno', event['colno'])
                .field('count', 1)
                .time(self.get_timestamp(event['timestamp']))
            )
            data_points.append(data_point)

        try:
            self.timeseries.write(record=data_points)
            self.log.logger.info(
                f'Successfully wrote {len(data_points)} without error events to time series database.'
            )
        except Exception as e:
            self.log.logger.error(
                f'Error writing error events to time series database: {e}'
            )
            raise e

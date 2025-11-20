from influxdb_client_3 import Point
from app.services.time_series.time_series import TimeSeries


class PerformanceEvent(TimeSeries):
    def __init__(self):
        super().__init__()

    def set_events(self, events: list):
        data_points: list = []
        fields: list = [
            'first_paint',
            'first_contentful_paint',
            'dom_content_loaded',
            'load_time',
        ]
        for event in events:
            if event in events:
                for field in fields:
                    data_point = (
                        Point('performance_event')
                        .tag('id', self.get_id())
                        .tag('app_key', event['app_key'])
                        .tag('event_type', event['event_type'])
                        .tag('session_id', event['session_id'])
                        .tag('user_id', event['user_id'])
                        .tag('page_url', event['page_url'])
                        .tag('user_agent', event['user_agent'])
                        .tag('metric', field)
                        .field('value', int(event[field]))
                        .time(self.utils.get_timestamp(event['timestamp']))
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
            raise ValueError(e)

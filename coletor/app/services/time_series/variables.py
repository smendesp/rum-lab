from influxdb_client_3 import Point
import pandas as pd

from app.services.time_series.time_series import TimeSeries
from app.lib.utils import Utils


class Variables(TimeSeries):
    def __init__(self):
        super().__init__()

    def prepare_df(self, data_frame):
        data = {
            'event_type': data_frame['event_type'],
            'session_id': data_frame['session_id'],
            'user_id': data_frame['user_id'],
            'page_url': data_frame['page_url'],
            'user_agent': data_frame['user_agent'],
            'element': data_frame['element'],
            'text': data_frame['text'],
            'time': data_frame['time'],
        }

        df = pd.DataFrame(data)

        return df

    def set_data(self, data_list: list):
        fields = [
            'event_type',
            'session_id',
            'user_id',
            'page_url',
            'user_agent',
            'element',
            'text',
        ]

        df = self.prepare_df(data_list)

        try:
            self.timeseries.write(
                record=df,
                data_frame_measurement_name='variables',
                data_frame_field_columns=fields,
                data_frame_timestamp_column='time',
                write_precision='s',  # Precisão: 'ns', 'us', 'ms', 's'
            )

            self.log.logger.info(
                f'Successfully wrote {len(df)} without error events to time series database.'
            )
        except Exception as e:
            self.log.logger.error(
                f'Error writing error events to time series database: {e}'
            )
            raise ValueError(e)

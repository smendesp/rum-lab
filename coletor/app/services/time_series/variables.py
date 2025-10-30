from influxdb_client_3 import Point
import pandas as pd


from app.services.time_series.time_series import TimeSeries
from datetime import datetime, timezone


class Variables(TimeSeries):
    def __init__(self):
        super().__init__()

    def prepare_df(self, data_list: list):

        data = {
            'event_type': [data['event_type'] for data in data_list],
            'session_id': [data['session_id'] for data in data_list],
            'user_id': [data['user_id'] for data in data_list],
            'page_url': [data['page_url'] for data in data_list],
            'user_agent': [data['user_agent'] for data in data_list],
            'element': [data['element'] for data in data_list],
            'text': [data['text'] for data in data_list],
            'time': (datetime.now(timezone.utc)),
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
                # data_frame_timestamp_timezone='UTC',  # Timezone
                write_precision='s',  # Precisão: 'ns', 'us', 'ms', 's'
            )

            self.log.logger.info(
                f'Successfully wrote {len(df)} without error events to time series database.'
            )
        except Exception as e:
            self.log.logger.error(
                f'Error writing error events to time series database: {e}'
            )
            raise e

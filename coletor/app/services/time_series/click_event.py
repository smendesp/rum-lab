from influxdb_client_3 import Point
import pandas as pd
from datetime import datetime, timezone

from app.services.time_series.time_series import TimeSeries
from app.services.time_series.variables import Variables


class ClickEvent(TimeSeries):
    def __init__(self):
        super().__init__()

    def set_events(self, events: list):
        variables = Variables()
        data_points: list = []
        # variables_data: list = []

        fields_tags = [
            'id',
            'app_key',
            'event_type',
            'session_id',
            'user_id',
            'page_url',
            'user_agent',
            'element',
            'text',
            'x',
            'y',
        ]

        # TODO: Corrigir time está fixado pelo coletor
        data_tag = {
            'id': [self.get_id() for data in events],
            'app_key': [data['app_key'] for data in events],
            'event_type': [data['event_type'] for data in events],
            'session_id': [data['session_id'] for data in events],
            'user_id': [data['user_id'] for data in events],
            'page_url': [data['page_url'] for data in events],
            'user_agent': [data['user_agent'] for data in events],
            'element': [data['element'] for data in events],
            'text': [data['text'] for data in events],
            'x': [data['x'] for data in events],
            'y': [data['y'] for data in events],
            'time': [datetime.now(timezone.utc) for data in events],
        }

        data_field = {
            'element_group': [data['element'] for data in events],
            'count': [data['text'] for data in events],
        }

        # separo tags de fields
        df_tag = pd.DataFrame(data_tag)
        df_field = pd.DataFrame(data_field)

        # agrupo e sumarizo/totalizo
        df_field_group = df_field.groupby(['element_group', 'count'])
        df_field_sumarizado = df_field_group[['count']].count()

        # Indexação
        df_tag_reset = df_tag.reset_index(drop=True)
        df_field_reset = df_field_sumarizado.reset_index(drop=True)

        # merge
        df_merged = pd.concat([df_tag_reset, df_field_reset], axis=1)

        # removo campos em bracos resultantes do mege vs sumarização
        df = df_merged.dropna()

        # tranform o valor em inteiro
        # TODO
        # A value is trying to be set on a copy of a slice from a DataFrame.
        # Try using .loc[row_indexer,col_indexer] = value instead
        # See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
        # df['count'] = pd.to_numeric(df['count'], downcast='integer')

        # df['count'] = pd.to_numeric(df['count'], downcast='integer')
        df['count'] = df['count'].astype(int)
        # print(df.loc[['count']])
        #df.loc[:, 'count'] = df.loc[:, 'count'].astype(int)

        print(df_merged.head())
        
        try:
            self.timeseries.write(
                record=df,
                data_frame_measurement_name='click_event',
                data_frame_tag_columns=fields_tags,
                data_frame_field_columns=['count'],
                data_frame_timestamp_column='time',
                # data_frame_timestamp_timezone='UTC',  # Timezone
                write_precision='ms',  # Precisão: 'ns', 'us', 'ms', 's'
            )

            variables.set_data(events)

            self.log.logger.info(
                f'Successfully wrote {len(data_points)} without error events to time series database.'
            )
        except Exception as e:
            self.log.logger.error(
                f'Error writing error events to time series database: {e}'
            )
            raise e

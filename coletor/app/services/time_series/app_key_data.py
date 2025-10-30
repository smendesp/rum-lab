from influxdb_client_3 import Point
from app.services.time_series.time_series import TimeSeries


class AppKeyData(TimeSeries):
    def __init__(self):
        super().__init__()

    def set_data(self, data_list: list):

        data_points: list = []
        print(data_list)
        for data in data_list:
            data_point = (
                Point('app_key')
                .tag('id', self.get_id())
                .tag('description', data['description'])
                .field('app_key', data['app_key'])
            )
            print(data_point)
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

from datetime import datetime, timezone


class Utils:
    def get_timestamp(self, timestamp: str = ''):
        if timestamp == '':
            return datetime.now(timezone.utc)
        else:
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)

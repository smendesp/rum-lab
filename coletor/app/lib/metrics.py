from opentelemetry import metrics


class Metrics:
    def __init__(self, identifier: str = 'application metrics'):
        self.meter = metrics.get_meter(identifier)

    def get_meter(self):
        return self.meter

    def counter(self, name: str, description: str = ''):
        return self.meter.create_counter(name, description=description)

    def gauge(self, name: str, description: str = '', unit: str = 'unitless'):
        return self.meter.create_gauge(
            name, description=description, unit=unit
        )

    def histogram(self, name: str, description: str = '', unit: str = 'ms'):
        return self.meter.create_histogram(
            name, description=description, unit=unit
        )

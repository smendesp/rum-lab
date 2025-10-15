from opentelemetry import metrics


class Metrics:
    def __init__(self, identifier: str = 'application metrics'):
        self.meter = metrics.get_meter(identifier)

    def get_meter(self):
        return self.meter

    def counter(self, name: str, description: str = ''):
        return self.meter.create_counter(name, description=description)

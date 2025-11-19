from app.services.time_series.performance_event import PerformanceEvent


class PerformanceEventUseCase:
    def __init__(self):
        ...

    def set_events(self, events):
        performance_event = PerformanceEvent()
        performance_event.set_events(events)

from app.services.time_series.error_event import ErrorEvent


class ErrorEventUseCase:
    def __init__(self):
        ...

    def set_events(self, events):
        error_event = ErrorEvent()
        error_event.set_events(events)

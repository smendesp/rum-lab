from app.services.time_series.webvitals_event import WebVitalsEvent


class WebvitalsEventUseCase:
    def __init__(self):
        ...

    def set_events(self, events):
        webvitals_event = WebVitalsEvent()
        webvitals_event.set_events(events)

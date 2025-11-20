from app.services.time_series.resource_event import ResourceEvent


class ResourceEventUseCase:
    def __init__(self):
        ...

    def set_events(self, events):
        resource_event = ResourceEvent()
        resource_event.set_events(events)

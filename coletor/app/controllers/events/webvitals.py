from app.models.events import RumWebvitalsEvent, RumWebvitalsEventData

from app.use_cases.webvitals_event import WebvitalsEventUseCase

from app.lib.logger import Logger
from app.lib.metrics import Metrics

class WebvitalsEventController:
    def __init__(self):
        self.log = Logger()
        self.metrics = Metrics()
        self.webvitals_event_uses_case = WebvitalsEventUseCase()

    def set_events(self, data: list):

        events: list = []

        for event in data:
            if event['type'] != 'web-vitals':
                raise ValueError(f'Error: is not a webvitals event') 

            rum_webvitals_event_count = self.metrics.counter(
                name='rum.webvitals.events.count',
                description='Count of RUM events',
            )

            try:
                rum_webvitals_event = RumWebvitalsEvent(
                    app_key=event['appKey'],
                    type=event['type'],
                    timestamp=event['timestamp'],
                    session_id=event['sessionId'],
                    user_id=event['userId'],
                    page_url=event['pageUrl'],
                    user_agent=event['userAgent'],
                    data=RumWebvitalsEventData(
                        id=event['data']['id'],
                        name=event['data']['name'],
                        value=event['data']['value']
                    ),
                )

            except Exception as e:
                raise f'Invalid RUM Error Event data: {e}'

            events.append(
                rum_webvitals_event.to_dict()
            )

            rum_webvitals_event_count.add(
                1, attributes=rum_webvitals_event.to_dict()
            )

            events.append(rum_webvitals_event.to_dict())


        self.webvitals_event_uses_case.set_events(events=events)

from app.models.events import RumResourceEvent, RumResourceEventData

from app.use_cases.resource_event import ResourceEventUseCase

from app.lib.logger import Logger
from app.lib.metrics import Metrics

class ResourceEventController:
    def __init__(self):
        self.log = Logger()
        self.metrics = Metrics()
        self.resource_event_uses_case = ResourceEventUseCase()

    def set_events(self, data: list):

        events: list = []

        for event in data:
            if event['type'] != 'resource':
                raise ValueError(f'Error: is not a resource event') 

            rum_resource_event_count = self.metrics.counter(
                name='rum.resource.events.count',
                description='Count of RUM events',
            )

            try:
                rum_resource_event = RumResourceEvent(
                    app_key=event['appKey'],
                    type=event['type'],
                    timestamp=event['timestamp'],
                    session_id=event['sessionId'],
                    user_id=event['userId'],
                    page_url=event['pageUrl'],
                    user_agent=event['userAgent'],
                    data=RumResourceEventData(
                        duration=event['data']['duration'] if 'duration' in event['data'] else 0,
                        name=event['data']['name'] if 'name' in event['data'] else '',
                        size=event['data']['size'] if 'size' in event['data'] else 0,
                        success=event['data']['success'] if 'success' in event['data'] else False,
                        type=event['data']['type'] if 'type' in event['data'] else '',
                    ),
                )

            except Exception as e:
                raise ValueError(f'Invalid RUM Error Event data: {e}')

            events.append(
                rum_resource_event.to_dict()
            )

            rum_resource_event_count.add(
                1, attributes=rum_resource_event.to_dict()
            )

            events.append(rum_resource_event.to_dict())


        self.resource_event_uses_case.set_events(events=events)

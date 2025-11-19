from app.models.events import RumPerformanceEvent, RumPerformanceEventData

from app.use_cases.performance_event import PerformanceEventUseCase

from app.lib.logger import Logger
from app.lib.metrics import Metrics


class PerformanceEventController:
    def __init__(self):
        self.log = Logger()
        self.metrics = Metrics()
        self.performance_event_uses_case = PerformanceEventUseCase()

    def set_events(self, data: list):

        events: list = []

        for event in data:
            if event['type'] != 'performance':
                raise ValueError(f'Error: is not a performance event')

            rum_performance_event_count = self.metrics.counter(
                name='rum.performance.events.count',
                description='Count of RUM events',
            )

            try:
                rum_performance_event = RumPerformanceEvent(
                    app_key=event['appKey'],
                    type=event['type'],
                    timestamp=event['timestamp'],
                    session_id=event['sessionId'],
                    user_id=event['userId'],
                    page_url=event['pageUrl'],
                    user_agent=event['userAgent'],
                    data=RumPerformanceEventData(
                        first_paint=event['data']['firstPaint'],
                        first_contentful_paint=event['data']['firstContentfulPaint'],
                        dom_content_loaded=event['data']['domContentLoaded'],
                        load_time=event['data']['loadTime'],
                    ),
                )

            except Exception as e:
                raise f'Invalid RUM Error Event data: {e}'

            events.append(
                rum_performance_event.to_dict()
            )

            rum_performance_event_count.add(
                1, attributes=rum_performance_event.to_dict()
            )

            events.append(rum_performance_event.to_dict())

        self.performance_event_uses_case.set_events(events=events)

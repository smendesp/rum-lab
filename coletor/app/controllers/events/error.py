from app.models.events import RumErrorEvent, RumErrorEventData

from app.use_cases.error_event import ErrorEventUseCase

from app.lib.logger import Logger
from app.lib.metrics import Metrics

class ErrorEventController:
    def __init__(self):
        self.log = Logger()
        self.metrics = Metrics()
        self.error_event_uses_case = ErrorEventUseCase()

    def set_events(self, data: list):

        events: list = []

        for event in data:
            if event['type'] != 'error':
                raise ValueError(f'Error: is not a error event') 

            rum_error_event_count = self.metrics.counter(
                name='rum.error.events.count',
                description='Count of RUM events',
            )

            try:
                rum_error_event = RumErrorEvent(
                    app_key=event['appKey'],
                    type=event['type'],
                    timestamp=event['timestamp'],
                    session_id=event['sessionId'],
                    user_id=event['userId'],
                    page_url=event['pageUrl'],
                    user_agent=event['userAgent'],
                    data=RumErrorEventData(
                        filename=event['data']['filename'] if 'filename' in event['data'] else '',
                        colno=event['data']['colno'] if 'colno' in event['data'] else 0,
                        lineno=event['data']['lineno'] if 'lineno' in event['data'] else 0,
                        message=event['data']['message'] if 'message' in event['data'] else '',
                        stack=event['data']['stack'] if 'stack' in event['data'] else '',
                    ),
                )

            except Exception as e:
                raise ValueError(f'Invalid RUM Error Event data: {e}')

            events.append(
                rum_error_event.to_dict()
            )

            rum_error_event_count.add(
                1, attributes=rum_error_event.to_dict()
            )

            events.append(rum_error_event.to_dict())


        self.error_event_uses_case.set_events(events=events)

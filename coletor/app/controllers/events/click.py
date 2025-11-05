from app.models.events import RumClickEvent, RumClickEventData

from app.use_cases.click_event import ClickEventUseCase

from app.lib.logger import Logger
from app.lib.metrics import Metrics


class ClickEventController:
    def __init__(self):
        self.log = Logger()
        self.metrics = Metrics()
        self.click_event_uses_case = ClickEventUseCase()

    def set_events(self, data: list):

        events: list = []

        for event in data:
            if event['type'] != 'click':
                raise f'Error: is not a click event'

            rum_click_event_count = self.metrics.counter(
                name='rum.click.events.count',
                description='Count of RUM Click events',
            )
            try:
                rum_click_event = RumClickEvent(
                    app_key=event['appKey'],
                    type=event['type'],
                    timestamp=event['timestamp'],
                    session_id=event['sessionId'],
                    user_id=event['userId'],
                    page_url=event['pageUrl'],
                    user_agent=event['userAgent'],
                    data=RumClickEventData(
                        x=event['data']['x'],
                        y=event['data']['y'],
                        element=event['data']['element'],
                        text=event['data']['text'],
                    ),
                )

            except Exception as e:
                raise f'Invalid RUM Click Event data: {e}'

            rum_click_event_count.add(1, attributes=rum_click_event.to_dict())
            events.append(rum_click_event.to_dict())

        self.click_event_uses_case.set_events(events=events)

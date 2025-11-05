import json
from collections import defaultdict

from app.models.events import (
    RumClickEvent,
    RumClickEventData,
    RumErrorEvent,
    RumErrorEventData,
    RumPerformanceEvent,
    RumPerformanceEventData,
    RumWebVitalsEvent,
    RumWebVitalsEventData,
    RumResourceEvent,
    RumResourceEventData,
)

from app.lib.logger import Logger
from app.lib.custom_response import generate_json_response
from app.lib.metrics import Metrics

from app.services.time_series import (
    ClickEvent,
    WebVitalsEvent,
    ErrorEvent,
    ResourceEvent,
    PerformanceEvent,
)

from app.controllers.events import ClickEventController
from app.use_cases.click_event import ClickEventUseCase


class RumEventController:
    def __init__(self):
        self.log = Logger()
        self.metrics = Metrics()
        self.click_event = ClickEvent()
        self.web_vitals_event = WebVitalsEvent()
        self.error_event = ErrorEvent()
        self.resource_event = ResourceEvent()
        self.performance_event = PerformanceEvent()

    def rum(self, data: list):

        try:
            if 'appKey' not in data[0] or data[0]['appKey'] == '':
                self.log.logger.error('appKey is missing in the RUM data')
                raise 'appKey is required'

            click_event_controller = ClickEventController()

            group_by_event = defaultdict(list)

            for item in data:
                group_by_event[item['type']].append(item)

            rum_event_click_list: list = group_by_event['click']
            rum_event_web_vitals_list: list = group_by_event['web-vitals']
            rum_event_performance_list: list = group_by_event['performance']
            rum_event_error_list: list = group_by_event['error']
            rum_event_resource_list: list = group_by_event['resource']

            res = {
                'click': len(rum_event_click_list),
                'error': len(rum_event_error_list),
                'resource': len(rum_event_resource_list),
                'performance': len(rum_event_performance_list),
                'web_vitals': len(rum_event_web_vitals_list),
            }

            click_event_controller.set_events(data=rum_event_click_list)

            return rum_event_click_list

            # for event in data:

            #     if event['type'] == 'resource':
            #         rum_resource_event_count = self.metrics.counter(
            #             name='rum.resource.events.count',
            #             description='Count of RUM Resourceevents',
            #         )

            #         try:
            #             rum_resource_event = RumResourceEvent(
            #                 app_key=event['appKey'],
            #                 type=event['type'],
            #                 timestamp=event['timestamp'],
            #                 session_id=event['sessionId'],
            #                 user_id=event['userId'],
            #                 page_url=event['pageUrl'],
            #                 user_agent=event['userAgent'],
            #                 data=RumResourceEventData(
            #                     name=event['data']['name'],
            #                     type=event['data']['type'],
            #                     duration=event['data']['duration'],
            #                     success=event['data']['success'],
            #                     size=event['data']['size'],
            #                 ),
            #             )

            #         except Exception as e:
            #             raise f'Invalid RUM Resource Event data: {e}'

            #         rum_event_resource_list.append(
            #             rum_resource_event.to_dict()
            #         )
            #         rum_resource_event_count.add(
            #             1, attributes=rum_resource_event.to_dict()
            #         )

            #         self.log.logger.info(
            #             f'RUM Resource Event Received: {json.dumps(event)}'
            #         )

            #         res['resource'] = res['resource'] + 1

            #     elif event['type'] == 'click':
            #         rum_click_event_count = self.metrics.counter(
            #             name='rum.click.events.count',
            #             description='Count of RUM Click events',
            #         )
            #         try:
            #             click_event_controller = ClickEventController()
            #             click_event_controller.set_events(event)

            #             rum_click_event = RumClickEvent(
            #                 app_key=event['appKey'],
            #                 type=event['type'],
            #                 timestamp=event['timestamp'],
            #                 session_id=event['sessionId'],
            #                 user_id=event['userId'],
            #                 page_url=event['pageUrl'],
            #                 user_agent=event['userAgent'],
            #                 data=RumClickEventData(
            #                     x=event['data']['x'],
            #                     y=event['data']['y'],
            #                     element=event['data']['element'],
            #                     text=event['data']['text'],
            #                 ),
            #             )

            #         except Exception as e:
            #             raise f'Invalid RUM Click Event data: {e}'

            #         rum_click_event_count.add(
            #             1, attributes=rum_click_event.to_dict()
            #         )
            #         rum_event_click_list.append(rum_click_event.to_dict())
            #         # log.logger.info(
            #         #     f'RUM Click Event Received: {json.dumps(event)}'
            #         # )
            #         res['click'] = res['click'] + 1

            #     elif event['type'] == 'error':
            #         rum_error_event_count = self.metrics.counter(
            #             name='rum.error.events.count',
            #             description='Count of RUM Error events',
            #         )

            #         try:
            #             rum_error_event = RumErrorEvent(
            #                 app_key=event['appKey'],
            #                 type=event['type'],
            #                 timestamp=event['timestamp'],
            #                 session_id=event['sessionId'],
            #                 user_id=event['userId'],
            #                 page_url=event['pageUrl'],
            #                 user_agent=event['userAgent'],
            #                 data=RumErrorEventData(
            #                     message=event['data']['message'],
            #                     stack=event['data']['stack'],
            #                     filename=event['data']['filename'],
            #                     lineno=event['data']['lineno'],
            #                     colno=event['data']['colno'],
            #                 ),
            #             )

            #         except Exception as e:
            #             raise f'Invalid RUM Error Event data: {e}'

            #         rum_event_error_list.append(rum_error_event.to_dict())

            #         rum_error_event_count.add(
            #             1, attributes=rum_error_event.to_dict()
            #         )

            #         self.log.logger.info(
            #             f'RUM Error Event Received: {json.dumps(event)}'
            #         )
            #         res['error'] = res['error'] + 1

            #     elif event['type'] == 'performance':
            #         rum_performance_event_count = self.metrics.counter(
            #             name='rum.performance.events.count',
            #             description='Count of RUM events',
            #         )

            #         try:
            #             rum_performance_event = RumPerformanceEvent(
            #                 app_key=event['appKey'],
            #                 type=event['type'],
            #                 timestamp=event['timestamp'],
            #                 session_id=event['sessionId'],
            #                 user_id=event['userId'],
            #                 page_url=event['pageUrl'],
            #                 user_agent=event['userAgent'],
            #                 data=RumPerformanceEventData(
            #                     first_paint=[
            #                         item['data']['firstPaint']
            #                         for item in event['data']
            #                     ],
            #                     first_contentful_paint=[
            #                         item['data']['firstContentfulPaint']
            #                         for item in event['data']
            #                     ],
            #                     dom_content_loaded=[
            #                         item['data']['domContentLoaded']
            #                         for item in event['data']
            #                     ],
            #                     load_time=[
            #                         item['data']['loadTime']
            #                         for item in event['data']
            #                     ],
            #                 ),
            #             )

            #         except Exception as e:
            #             raise f'Invalid RUM Error Event data: {e}'

            #         rum_event_performance_list.append(
            #             rum_performance_event.to_dict()
            #         )

            #         rum_performance_event_count.add(
            #             1, attributes=rum_performance_event.to_dict()
            #         )

            #         self.log.logger.info(
            #             f'RUM Performance Event Received: {json.dumps(event)}'
            #         )

            #         res['performance'] = res['performance'] + 1

            #     elif event['type'] == 'web-vitals':
            #         rum_web_vitals_event_gauge = self.metrics.gauge(
            #             name='rum.webvitals.events.gauge',
            #             description='Count of RUM events',
            #         )

            #         try:
            #             rum_web_vitals_event = RumWebVitalsEvent(
            #                 app_key=event['appKey'],
            #                 type=event['type'],
            #                 timestamp=event['timestamp'],
            #                 session_id=event['sessionId'],
            #                 user_id=event['userId'],
            #                 page_url=event['pageUrl'],
            #                 user_agent=event['userAgent'],
            #                 data=RumWebVitalsEventData(
            #                     id=event['data']['id'],
            #                     name=event['data']['name'],
            #                     value=event['data']['value'],
            #                 ),
            #             )

            #         except Exception as e:
            #             raise f'Invalid RUM Error Event data: {e}'

            #         rum_web_vitals_event_gauge.set(
            #             event['data']['value'],
            #             attributes=rum_web_vitals_event.to_dict(),
            #         )

            #         rum_event_web_vitals_list.append(
            #             rum_web_vitals_event.to_dict()
            #         )

            #         self.log.logger.info(
            #             f'RUM Web Vitals Event Received: {json.dumps(event)}'
            #         )

            #         res['web_vitals'] = res['web_vitals'] + 1

            # click_event_use_case = ClickEventUseCase()
            # click_event_use_case.apply(events=rum_event_click_list)

            # # click_event.set_events(events=rum_event_click_list)
            # self.web_vitals_event.set_events(events=rum_event_web_vitals_list)
            # self.error_event.set_events(events=rum_event_error_list)
            # self.performance_event.set_events(
            #     events=rum_event_performance_list
            # )
            # self.resource_event.set_events(events=rum_event_resource_list)

            # return res

        except Exception as e:
            raise e

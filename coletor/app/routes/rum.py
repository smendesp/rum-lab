from fastapi import Body, APIRouter, HTTPException, Path
from typing import Annotated
import json

from app.models.events.rum_click_event import RumClickEvent, RumClickEventData
from app.models.events.rum_error_event import RumErrorEvent, RumErrorEventData
from app.models.events.rum_performance_event import (
    RumPerformanceEvent,
    RumPerformanceEventData,
)
from app.models.events.rum_webvitals_event import (
    RumWebVitalsEvent,
    RumWebVitalsEventData,
)
from app.models.events.rum_resource_event import (
    RumResourceEvent,
    RumResourceEventData,
)

from app.lib.logger import Logger
from app.lib.custom_response import generate_json_response
from app.lib.metrics import Metrics

from app.services.time_series.click_event import ClickEvent

log = Logger()
router = APIRouter()
metrics = Metrics()
# click_event = ClickEvent()


@router.post('/v1/rum')
# async def user_account_add(data: Annotated[UserAccountModel, Body(embed=False)]):
async def rum(data: Annotated[list, Body(embed=False)]):
    try:

        if 'appKey' not in data[0] or data[0]['appKey'] == '':
            log.logger.error('appKey is missing in the RUM data')
            raise HTTPException(status_code=400, detail='appKey is required')

        res = {
            'click': 0,
            'error': 0,
            'resource': 0,
            'performance': 0,
            'web_vitals': 0,
        }
        rum_event_click_list: list = []

        for event in data:

            if event['type'] == 'resource':
                rum_resource_event_count = metrics.counter(
                    name='rum.resource.events.count',
                    description='Count of RUM Resourceevents',
                )

                attributes = {
                    'appKey': event['appKey']
                    if 'appKey' in event
                    else 'unknown',
                    'timestamp': event['timestamp']
                    if 'timestamp' in event
                    else 0,
                    'eventType': event['type']
                    if 'type' in event
                    else 'unknown',
                    'sessionId': event['sessionId']
                    if 'sessionId' in event
                    else 'unknown',
                    'userId': event['userId']
                    if 'userId' in event
                    else 'unknown',
                    'pageUrl': event['pageUrl']
                    if 'pageUrl' in event
                    else 'unknown',
                    'userAgent': event['userAgent']
                    if 'userAgent' in event
                    else 'unknown',
                    'resourceName': event['data']['name']
                    if 'name' in event['data']
                    else 'unknown',
                    'resourceType': event['data']['type']
                    if 'type' in event['data']
                    else 'unknown',
                    'resourceSuccess': event['data']['success']
                    if 'success' in event['data']
                    else 'unknown',
                    'resourceSize': event['data']['size']
                    if 'size' in event['data']
                    else 'unknown',
                    'resourceDuration': event['data']['duration']
                    if 'duration' in event['data']
                    else 'unknown',
                }
                rum_resource_event_count.add(1, attributes=attributes)

                log.logger.info(
                    f'RUM Resource Event Received: {json.dumps(event)}'
                )

                res['resource'] = res['resource'] + 1
            # rum_event_count.add(1)
            elif event['type'] == 'click':
                rum_click_event_count = metrics.counter(
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
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid RUM Click Event data: {e}',
                    )

                rum_click_event_count.add(
                    1, attributes=rum_click_event.to_dict()
                )
                rum_event_click_list.append(rum_click_event.to_dict())
                # log.logger.info(
                #     f'RUM Click Event Received: {json.dumps(event)}'
                # )
                res['click'] = res['click'] + 1

            elif event['type'] == 'error':
                rum_error_event_count = metrics.counter(
                    name='rum.error.events.count',
                    description='Count of RUM Error events',
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
                            error_message=event['data']['message'],
                            error_stack=event['data']['stack'],
                            error_filename=event['data']['filename'],
                            error_lineno=event['data']['lineno'],
                            error_colno=event['data']['colno'],
                        ),
                    )

                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid RUM Error Event data: {e}',
                    )

                rum_error_event_count.add(
                    1, attributes=rum_error_event.to_dict()
                )

                log.logger.info(
                    f'RUM Error Event Received: {json.dumps(event)}'
                )
                res['error'] = res['error'] + 1

            elif event['type'] == 'performance':
                rum_performance_event_count = metrics.counter(
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
                            first_contentful_paint=event['data'][
                                'firstContentfulPaint'
                            ],
                            performance_dom_content_loaded=event['data'][
                                'domContentLoaded'
                            ],
                            performance_load_time=event['data']['loadTime'],
                        ),
                    )

                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid RUM Error Event data: {e}',
                    )

                rum_performance_event_count.add(
                    1, attributes=rum_performance_event.to_dict()
                )

                log.logger.info(
                    f'RUM Performance Event Received: {json.dumps(event)}'
                )

                res['performance'] = res['performance'] + 1

            elif event['type'] == 'web-vitals':
                rum_web_vitals_event_gauge = metrics.gauge(
                    name='rum.webvitals.events.gauge',
                    description='Count of RUM events',
                )

                try:
                    rum_web_vitals_event = RumWebVitalsEvent(
                        app_key=event['appKey'],
                        type=event['type'],
                        timestamp=event['timestamp'],
                        session_id=event['sessionId'],
                        user_id=event['userId'],
                        page_url=event['pageUrl'],
                        user_agent=event['userAgent'],
                        data=RumWebVitalsEventData(
                            id=event['data']['id'],
                            name=event['data']['name'],
                            value=event['data']['value'],
                        ),
                    )

                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid RUM Error Event data: {e}',
                    )

                rum_web_vitals_event_gauge.set(
                    event['data']['value'],
                    attributes=rum_web_vitals_event.to_dict(),
                )

                log.logger.info(
                    f'RUM Web Vitals Event Received: {json.dumps(event)}'
                )

                res['web_vitals'] = res['web_vitals'] + 1

            elif event['type'] == 'resource':
                rum_resource_event_histogram = metrics.histogram(
                    name='rum.resource.events.histogram',
                    description='Histogram of RUM resource events',
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
                            name=event['data']['id'],
                            type=event['data']['name'],
                            duration=event['data']['duration'],
                            success=event['data']['success'],
                            size=event['data']['size'],
                        ),
                    )

                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid RUM Error Event data: {e}',
                    )

                rum_resource_event_histogram.record(
                    event['data']['duration'],
                    attributes=rum_resource_event.to_dict(),
                )

                log.logger.info(
                    f'RUM Web Vitals Event Received: {json.dumps(event)}'
                )

                res['web_vitals'] = res['web_vitals'] + 1
        # click_event.set_click_events(events=rum_event_click_list)

        return generate_json_response(response_data={'data': res})

    except HTTPException as http_error:
        log.logger.error(
            f'HTTP error processing RUM data: {http_error.detail}'
        )
        raise http_error

    except Exception as error:
        log.logger.error(f'Error processing RUM data: {error}')
        raise HTTPException(status_code=418, detail=error)

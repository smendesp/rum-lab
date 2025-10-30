from fastapi import Body, APIRouter, HTTPException, Path
from typing import Annotated
import json

from app.models.entities import AppKeyEntity
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
    AppKeyData,
)

# from app.services.time_series import WebVitalsEvent

log = Logger()
router = APIRouter()
metrics = Metrics()
click_event = ClickEvent()
web_vitals_event = WebVitalsEvent()
error_event = ErrorEvent()
resource_event = ResourceEvent()
performance_event = PerformanceEvent()
app_key_data = AppKeyData()


@router.post('/v1/app-key')
# async def user_account_add(data: Annotated[UserAccountModel, Body(embed=False)]):
async def app_key(data: Annotated[list, Body(embed=False)]):
    try:

        if 'appKey' not in data[0] or data[0]['appKey'] == '':
            log.logger.error('appKey is missing in the RUM data')
            raise HTTPException(status_code=400, detail='appKey is required')

        res = {
            'app-key': 0,
        }
        rum_app_key_list: list = []

        for item in data:
            try:
                rum_app_key = AppKeyEntity(
                    app_key=item['appKey'],
                    description=item['description'],
                    timestamp=item['timestamp'],
                )

            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f'Invalid RUM Resource Event data: {e}',
                )

            rum_app_key_list.append(rum_app_key.to_dict())

            log.logger.info(f'RUM App Key Event Received: {json.dumps(item)}')

            res['app-key'] = res['app-key'] + 1

        app_key_data.set_data(data_list=rum_app_key_list)

        return generate_json_response(response_data={'data': res})

    except HTTPException as http_error:
        log.logger.error(
            f'HTTP error processing RUM data: {http_error.detail}'
        )
        raise HTTPException(status_code=418, detail=http_error.detail)

    except Exception as error:
        log.logger.error(f'Error processing RUM data: {error}')
        raise HTTPException(status_code=418, detail=error.__str__())


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
        rum_event_web_vitals_list: list = []
        rum_event_performance_list: list = []
        rum_event_error_list: list = []
        rum_event_resource_list: list = []

        for event in data:

            if event['type'] == 'resource':
                rum_resource_event_count = metrics.counter(
                    name='rum.resource.events.count',
                    description='Count of RUM Resourceevents',
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
                            name=event['data']['name'],
                            type=event['data']['type'],
                            duration=event['data']['duration'],
                            success=event['data']['success'],
                            size=event['data']['size'],
                        ),
                    )

                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid RUM Resource Event data: {e}',
                    )

                rum_event_resource_list.append(rum_resource_event.to_dict())
                rum_resource_event_count.add(
                    1, attributes=rum_resource_event.to_dict()
                )

                log.logger.info(
                    f'RUM Resource Event Received: {json.dumps(event)}'
                )

                res['resource'] = res['resource'] + 1

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
                            message=event['data']['message'],
                            stack=event['data']['stack'],
                            filename=event['data']['filename'],
                            lineno=event['data']['lineno'],
                            colno=event['data']['colno'],
                        ),
                    )

                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid RUM Error Event data: {e}',
                    )

                rum_event_error_list.append(rum_error_event.to_dict())

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
                            first_paint=[
                                item['data']['firstPaint']
                                for item in event['data']
                            ],
                            first_contentful_paint=[
                                item['data']['firstContentfulPaint']
                                for item in event['data']
                            ],
                            dom_content_loaded=[
                                item['data']['domContentLoaded']
                                for item in event['data']
                            ],
                            load_time=[
                                item['data']['loadTime']
                                for item in event['data']
                            ],
                        ),
                    )

                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Invalid RUM Error Event data: {e}',
                    )

                rum_event_performance_list.append(
                    rum_performance_event.to_dict()
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

                rum_event_web_vitals_list.append(
                    rum_web_vitals_event.to_dict()
                )

                log.logger.info(
                    f'RUM Web Vitals Event Received: {json.dumps(event)}'
                )

                res['web_vitals'] = res['web_vitals'] + 1

        click_event.set_events(events=rum_event_click_list)
        web_vitals_event.set_events(events=rum_event_web_vitals_list)
        error_event.set_events(events=rum_event_error_list)
        performance_event.set_events(events=rum_event_performance_list)
        resource_event.set_events(events=rum_event_resource_list)

        return generate_json_response(response_data={'data': res})

    except HTTPException as http_error:
        log.logger.error(
            f'HTTP error processing RUM data: {http_error.detail}'
        )
        raise HTTPException(status_code=418, detail=http_error.detail)

    except Exception as error:
        log.logger.error(f'Error processing RUM data: {error}')
        raise HTTPException(status_code=418, detail=error.__str__())

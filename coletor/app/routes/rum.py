from fastapi import Body, APIRouter, HTTPException, Path
from typing import Annotated
import json

from app.models.request.user_account import UserAccountModel
from app.lib.logger import Logger
from app.lib.custom_response import generate_json_response
from app.lib.metrics import Metrics

from app.services.time_series.click_event import ClickEvent


log = Logger()
router = APIRouter()
metrics = Metrics()
click_event = ClickEvent()


@router.post('/rum')
# async def user_account_add(data: Annotated[UserAccountModel, Body(embed=False)]):
async def user_account_add(data: Annotated[dict, Body(embed=False)]):
    try:
        # user_account_service = UserAccountService()
        # user_account_service.add(data)

        # return generate_json_response(response_data={"data": {"operation": "Ok"}})

        rum_event_count = metrics.counter(
            name='rum.events.count',
            description='Count of RUM events',
        )

        if 'appKey' not in data or data['appKey'] == '':
            log.logger.error('appKey is missing in the RUM data')
            raise HTTPException(status_code=400, detail='appKey is required')

        attributes = {
            'appKey': data['appKey'] if 'appKey' in data else 'unknown',
            'eventType': data['eventType']
            if 'eventType' in data
            else 'unknown',
            'timestamp': data['timestamp'] if 'timestamp' in data else 0,
            'tagName': data['element']['tagName']
            if 'element' in data and 'tagName' in data['element']
            else 'unknown',
            'text': data['element']['text']
            if 'element' in data and 'text' in data['element']
            else 'unknown',
            'href': data['element']['href']
            if 'element' in data and 'href' in data['element']
            else 'unknown',
            'x': data['position']['x']
            if 'position' in data and 'x' in data['position']
            else 0,
            'y': data['position']['y']
            if 'position' in data and 'y' in data['position']
            else 0,
            'pageUrl': data['page']['url']
            if 'page' in data and 'url' in data['page']
            else 'unknown',
            'pageTitle': data['page']['title']
            if 'page' in data and 'title' in data['page']
            else 'unknown',
            'pageReferrer': data['page']['referrer']
            if 'page' in data and 'referrer' in data['page']
            else 'unknown',
            'userAgent': data['user']['agent']
            if 'user' in data and 'agent' in data['user']
            else 'unknown',
            'useLanguage': data['user']['language']
            if 'user' in data and 'language' in data['user']
            else 'unknown',
            'userTimezone': data['user']['timezone']
            if 'user' in data and 'timezone' in data['user']
            else 'unknown',
            'appVersion': data['metadata']['appVersion']
            if 'metadata' in data and 'appVersion' in data['metadata']
            else 'unknown',
            'environment': data['metadata']['environment']
            if 'metadata' in data and 'environment' in data['metadata']
            else 'unknown',
        }
        rum_event_count.add(1, attributes=attributes)
        # rum_event_count.add(1)

        log.logger.info(f'RUM Data Received: {json.dumps(data)}')
        return generate_json_response(response_data={'data': data})

    except HTTPException as http_error:
        log.logger.error(
            f'HTTP error processing RUM data: {http_error.detail}'
        )
        raise http_error

    except Exception as error:
        log.logger.error(f'Error processing RUM data: {error}')
        raise HTTPException(status_code=418, detail=error)


@router.post('/v1/rum')
# async def user_account_add(data: Annotated[UserAccountModel, Body(embed=False)]):
async def rum(data: Annotated[list, Body(embed=False)]):
    try:

        if 'appKey' not in data[0] or data[0]['appKey'] == '':
            log.logger.error('appKey is missing in the RUM data')
            raise HTTPException(status_code=400, detail='appKey is required')

        res = {'click': 0, 'error': 0, 'resource': 0, 'performance': 0}
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
                    'clickElement': event['data']['element']
                    if 'element' in event['data']
                    else 'unknown',
                    'clickText': event['data']['text']
                    if 'text' in event['data']
                    else 'unknown',
                    'clickX': event['data']['x']
                    if 'x' in event['data']
                    else 'unknown',
                    'clickY': event['data']['y']
                    if 'y' in event['data']
                    else 'unknown',
                }
                rum_click_event_count.add(1, attributes=attributes)
                rum_event_click_list.append(attributes)
                # log.logger.info(
                #     f'RUM Click Event Received: {json.dumps(event)}'
                # )
                res['click'] = res['click'] + 1

            elif event['type'] == 'error':
                rum_error_event_count = metrics.counter(
                    name='rum.error.events.count',
                    description='Count of RUM Error events',
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
                    'errorMessage': event['data']['message']
                    if 'message' in event['data']
                    else 'unknown',
                    'errorStack': event['data']['stack']
                    if 'stack' in event['data']
                    else 'unknown',
                    'errorFilename': event['data']['filename']
                    if 'filename' in event['data']
                    else 'unknown',
                    'errorLineno': event['data']['lineno']
                    if 'lineno' in event['data']
                    else 'unknown',
                    'errorColno': event['data']['colno']
                    if 'colno' in event['data']
                    else 'unknown',
                }
                rum_error_event_count.add(1, attributes=attributes)

                log.logger.info(
                    f'RUM Error Event Received: {json.dumps(event)}'
                )
                res['error'] = res['error'] + 1

            elif event['type'] == 'performance':
                rum_performance_event_count = metrics.counter(
                    name='rum.performance.events.count',
                    description='Count of RUM events',
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
                    'clickElement': event['data']['element']
                    if 'element' in event['data']
                    else 'unknown',
                    'performanceText': event['data']['loadTime']
                    if 'loadTime' in event['data']
                    else 'unknown',
                    'performanceDomContentLoaded': event['data'][
                        'domContentLoaded'
                    ]
                    if 'domContentLoaded' in event['data']
                    else 'unknown',
                }
                rum_performance_event_count.add(1, attributes=attributes)

                log.logger.info(
                    f'RUM Performance Event Received: {json.dumps(event)}'
                )

                res['performance'] = res['performance'] + 1
                

        click_event.set_click_events(events=rum_event_click_list)
        
        return generate_json_response(response_data={'data': res})

    except HTTPException as http_error:
        log.logger.error(
            f'HTTP error processing RUM data: {http_error.detail}'
        )
        raise http_error

    except Exception as error:
        log.logger.error(f'Error processing RUM data: {error}')
        raise HTTPException(status_code=418, detail=error)

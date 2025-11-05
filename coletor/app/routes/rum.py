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

from app.controllers.rum import RumEventController
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

from app.use_cases.click_event import ClickEventUseCase

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
        rum_event_controller = RumEventController()

        res = rum_event_controller.rum(data=data)

        return generate_json_response(response_data={'data': res})

    except HTTPException as http_error:
        log.logger.error(
            f'HTTP error processing RUM data: {http_error.detail}'
        )
        raise HTTPException(status_code=418, detail=http_error.detail)

    except Exception as error:
        log.logger.error(f'Error processing RUM data: {error}')
        raise HTTPException(status_code=418, detail=error.__str__())

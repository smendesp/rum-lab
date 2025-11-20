import json
from collections import defaultdict

from app.models.events import (
    RumClickEvent,
    RumClickEventData,
    RumErrorEvent,
    RumErrorEventData,
    RumPerformanceEvent,
    RumPerformanceEventData,
    RumWebvitalsEvent,
    RumWebvitalsEventData,
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

from app.controllers.events import ( 
    ClickEventController, 
    PerformanceEventController, 
    WebvitalsEventController,
    ResourceEventController,
    ErrorEventController,
)



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
                raise ValueError('appKey is required')

            group_by_event = defaultdict(list)

            for item in data:
                group_by_event[item['type']].append(item)

            rum_event_click_list: list = group_by_event['click']
            rum_event_performance_list: list = group_by_event['performance']
            rum_event_webvitals_list: list = group_by_event['web-vitals']
            rum_event_error_list: list = group_by_event['error']
            rum_event_resource_list: list = group_by_event['resource']
                
            res = {
                'click': len(rum_event_click_list),
                'error': len(rum_event_error_list),
                'resource': len(rum_event_resource_list),
                'performance': len(rum_event_performance_list),
                'web-vitals': len(rum_event_webvitals_list),
            }
            
            if res['click'] > 0: 
                click_event_controller = ClickEventController()
                click_event_controller.set_events(data=rum_event_click_list)
                
            if res['performance'] > 0: 
                performance_event_controller = PerformanceEventController()
                performance_event_controller.set_events(data=rum_event_performance_list)
                
            if res['web-vitals'] > 0: 
                webvitals_event_controller = WebvitalsEventController()
                webvitals_event_controller.set_events(data=rum_event_webvitals_list)
                    
            if res['error'] > 0:             
                error_event_controller = ErrorEventController()
                error_event_controller.set_events(data=rum_event_error_list)
                
            if res['resource'] > 0:                 
                resource_event_controller = ResourceEventController()
                resource_event_controller.set_events(data=rum_event_resource_list)

            return res        

        except Exception as e:
            raise e

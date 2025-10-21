from pydantic import BaseModel, Field

from app.models.events.rum_event import RumEvent


# Todo: validar defaults
class RumPerformanceEventData(BaseModel):
    first_paint: float = Field(description='First Paint')
    first_contentful_paint: float = Field(description='First Contentful Paint')
    performance_dom_content_loaded: float = Field(
        description='Performance DOM Content Loaded'
    )
    performance_load_time: float = Field(description='Performance Load Time')

    def to_dict(self) -> dict:
        return {
            'first_paint': self.first_paint,
            'first_contentful_paint': self.first_contentful_paint,
            'performance_dom_content_loaded': self.performance_dom_content_loaded,
            'performance_load_time': self.performance_load_time,
        }


class RumPerformanceEvent(RumEvent):
    type: str = Field(default='performance', description='Event Type')
    data: RumPerformanceEventData = Field()

    def to_dict(self) -> dict:
        return {
            'app_key': self.app_key,
            'event_type': self.type,
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'page_url': self.page_url,
            'user_agent': self.user_agent,
            'first_paint': self.data.first_paint,
            'first_contentful_paint': self.data.first_contentful_paint,
            'performance_dom_content_loaded': self.data.performance_dom_content_loaded,
            'performance_load_time': self.data.performance_load_time,
        }

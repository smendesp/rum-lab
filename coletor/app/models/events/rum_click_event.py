from pydantic import BaseModel, Field

from app.models.events.rum_event import RumEvent


# Todo: validar defaults
class RumClickEventData(BaseModel):
    x: int = Field(description='Click X Coordinate')
    y: int = Field(description='Click Y Coordinate')
    element: str = Field(description='Click Element')
    text: str = Field(description='Click Text')

    def to_dict(self) -> dict:
        return {
            'click_x': self.x,
            'click_y': self.y,
            'click_element': self.element,
            'click_text': self.text,
        }


class RumClickEvent(RumEvent):
    type: str = Field(default='click', description='Event Type')
    data: RumClickEventData = Field()

    def to_dict(self) -> dict:
        return {
            'app_key': self.app_key,
            'event_type': self.type,
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'page_url': self.page_url,
            'user_agent': self.user_agent,
            'click_x': self.data.x,
            'click_y': self.data.y,
            'click_element': self.data.element,
            'click_text': self.data.text,
        }

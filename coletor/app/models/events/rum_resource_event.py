from pydantic import BaseModel, Field

from app.models.events.rum_event import RumEvent


# Todo: validar defaults
class RumResourceEventData(BaseModel):
    name: str = Field(description='Resource Name')
    type: str = Field(description='Resource Type')
    duration: float = Field(description='Resource Duration')
    success: bool = Field(description='Resource Success')
    size: float = Field(description='Resource Size')

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'type': self.type,
            'duration': self.duration,
            'success': self.success,
            'size': self.size,
        }


class RumResourceEvent(RumEvent):
    type: str = Field(default='resource', description='Event Type')
    data: RumResourceEventData = Field()

    def to_dict(self) -> dict:
        return {
            'app_key': self.app_key,
            'event_type': self.type,
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'page_url': self.page_url,
            'user_agent': self.user_agent,
            'name': self.data.name,
            'type': self.data.type,
            'duration': self.data.duration,
            'success': self.data.success,
            'size': self.data.size,
        }

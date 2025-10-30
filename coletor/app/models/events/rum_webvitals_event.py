from pydantic import BaseModel, Field

from app.models.events.rum_event import RumEvent


# Todo: validar defaults
class RumWebVitalsEventData(BaseModel):
    id: str = Field(description='Web Vitals ID')
    name: str = Field(description='Web Vitals Name')
    value: float = Field(description='Web Vitals Value')

    def to_dict(self) -> dict:
        return {'id': self.id, 'name': self.name, 'value': self.value}


class RumWebVitalsEvent(RumEvent):
    type: str = Field(default='web_vitals', description='Event Type')
    data: RumWebVitalsEventData = Field()

    def to_dict(self) -> dict:
        return {
            'app_key': self.app_key,
            'event_type': self.type,
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'page_url': self.page_url,
            'user_agent': self.user_agent,
            'id': self.data.id,
            'name': self.data.name,
            'value': self.data.value,
        }

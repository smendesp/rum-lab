from pydantic import BaseModel, Field

from app.models.events.rum_event import RumEvent


# Todo: validar defaults
class RumErrorEventData(BaseModel):
    message: str = Field(description='Error Message')
    stack: str = Field(description='Error Stack')
    filename: str = Field(description='Error Filename')
    lineno: int = Field(description='Error Line Number')
    colno: int = Field(description='Error Column Number')

    def to_dict(self) -> dict:
        return {
            'message': self.message,
            'stack': self.stack,
            'filename': self.filename,
            'lineno': self.lineno,
            'colno': self.colno,
        }


class RumErrorEvent(RumEvent):
    type: str = Field(default='error', description='Event Type')
    data: RumErrorEventData = Field()

    def to_dict(self) -> dict:
        return {
            'app_key': self.app_key,
            'type': self.type,
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'page_url': self.page_url,
            'user_agent': self.user_agent,
            'message': self.data.message,
            'stack': self.data.stack,
            'filename': self.data.filename,
            'lineno': self.data.lineno,
            'colno': self.data.colno,
        }

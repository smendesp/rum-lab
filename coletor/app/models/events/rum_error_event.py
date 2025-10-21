from pydantic import BaseModel, Field

from app.models.events.rum_event import RumEvent


# Todo: validar defaults
class RumErrorEventData(BaseModel):
    error_message: str = Field(description='Error Message')
    error_stack: str = Field(description='Error Stack')
    error_filename: str = Field(description='Error Filename')
    error_lineno: int = Field(description='Error Line Number')
    error_colno: int = Field(description='Error Column Number')

    def to_dict(self) -> dict:
        return {
            'error_message': self.error_message,
            'error_stack': self.error_stack,
            'error_filename': self.error_filename,
            'error_lineno': self.error_lineno,
            'error_colno': self.error_colno,
        }


class RumErrorEvent(RumEvent):
    type: str = Field(default='error', description='Event Type')
    data: RumErrorEventData = Field()

    def to_dict(self) -> dict:
        return {
            'app_key': self.app_key,
            'event_type': self.type,
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'page_url': self.page_url,
            'user_agent': self.user_agent,
            'error_message': self.data.error_message,
            'error_stack': self.error_stack,
            'error_filename': self.data.error_filename,
            'error_lineno': self.data.error_lineno,
            'error_colno': self.data.error_colno,
        }

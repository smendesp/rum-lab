from pydantic import BaseModel, Field

# Todo: validar defaults
class RumEvent(BaseModel):
    app_key: str = Field(description='Application Key')
    type: str = Field(description='Event Type')
    timestamp: int = Field(description='Event Timestamp')
    session_id: str = Field(description='Session ID')
    user_id: str = Field(description='User ID')
    page_url: str = Field(description='Page URL')
    user_agent: str = Field(description='User Agent')

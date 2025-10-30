from pydantic import BaseModel, Field


class AppKeyEntity(BaseModel):
    app_key: str = Field(default='click', description='App key')
    description: str = Field(default='', description='App Description')
    timestamp: int = Field(default=0, description='Event Timestamp')

    def to_dict(self) -> dict:
        return {
            'app_key': self.app_key,
            'description': self.description,
            'timestamp': self.timestamp,
        }

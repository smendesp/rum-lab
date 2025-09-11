from pydantic import BaseModel, Field
from typing import Literal


class CommonHeaders(BaseModel):
    save_data: bool = Field(default=False, description='Save-Data header')
    model_config: dict = {'extra': 'allow'}
    x_tag: list[str] = Field(description='Tags are requereds')
    host: str
    if_modified_since: str | None = None
    traceparent: str | None = None
    cost: float | None = None


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal['created_at', 'updated_at'] = 'created_at'
    tags: list[str] = []

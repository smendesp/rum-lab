from pydantic import BaseModel, Field


class UserAccountModel(BaseModel):
    id: int | None = None
    name: str = Field(title='Informe o nome', max_length=30)
    fullname: str | None = None

    # description: str | None = Field(
    #     default=None, title="The description of the item", max_length=300
    # )
    # price: float = Field(gt=0, description="The price must be greater than zero")
    # tax: float | None = None

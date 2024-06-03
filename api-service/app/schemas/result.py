from pydantic import BaseModel, ConfigDict

class Result(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    result: str | int | float

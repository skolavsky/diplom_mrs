from pydantic import BaseModel, ConfigDict

class Key(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    key: str

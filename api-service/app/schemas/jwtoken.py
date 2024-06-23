from pydantic import BaseModel, ConfigDict

class JWToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str | None

from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime


# User
class UserBase(BaseModel):
    email: EmailStr | str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
# End User

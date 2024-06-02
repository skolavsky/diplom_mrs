from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
import re


class ChangePassword(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_password: str
    new_password: str

# User
class UserBase(BaseModel):
    email: EmailStr | str

class UserDelete(BaseModel):
    password: str

class UserCreate(UserBase, UserDelete):
    pass

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
# End User

class UserInfo(UserBase):
    created_at: datetime


def validate_email(email: str):
    regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(regex, email) is not None

def validate_password(password: str):
    if len(password) < 8:
        return False
    # other potentioal validation
    return True

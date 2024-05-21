from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from models.user import User
from schemas.user_schema import UserCreate


password_handler = PasswordHasher()


async def check_user_password(db_user: User, user: UserCreate) -> bool:
    try:
        return password_handler.verify(db_user.hashed_password, user.password)
    except Exception as e:
        if isinstance(e, VerifyMismatchError):
            return False
        else:
            raise e

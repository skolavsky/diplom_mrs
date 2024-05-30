import jwt, os
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 3 # 3 hours

ACCESS_TOKEN_ALGORITHM = "HS512"


async def generate_access_token(payload: dict):
    experation_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = experation_time
    return jwt.encode(payload, os.environ['ACCESS_TOKEN_SECRET'], ACCESS_TOKEN_ALGORITHM)


async def decrypt_token(token: str):
    try:
        return dict(jwt.decode(token, os.environ['ACCESS_TOKEN_SECRET'], algorithms=[ACCESS_TOKEN_ALGORITHM]))
    except ValueError as e:
        if e is ExpiredSignatureError or e is InvalidTokenError:
            return None
        elif e is DecodeError:
            print(f'Error: {e}\n{token}')
            return None
        else:
            print(f'Error: {e}')
            return None

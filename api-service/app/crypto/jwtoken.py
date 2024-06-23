import jwt, os
from datetime import datetime, timedelta, UTC
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 3 # 3 hours

ACCESS_TOKEN_ALGORITHM = "HS512"


async def generate_access_token(payload: dict):
    experation_time = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = experation_time
    return jwt.encode(payload, os.environ['ACCESS_TOKEN_SECRET'], ACCESS_TOKEN_ALGORITHM)


async def decrypt_token(token: str):
    if len(token.split('.')) != 3:
        return None
    try:
        payload = dict(jwt.decode(token, os.environ['ACCESS_TOKEN_SECRET'], algorithms=[ACCESS_TOKEN_ALGORITHM]))
        return payload
    except:
        return None


import asyncio
if __name__ == "__main__":
    payload = {"sub":"some@email.com"}
    experation_time = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = experation_time
    print(asyncio.run(jwt.encode(payload, "2238da9f4fdf79f83228b1a21d0328be27eca6d7ffb1c018d92f8e1e32025e6b", ACCESS_TOKEN_ALGORITHM)))

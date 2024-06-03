from database import Base, engine, SessionLocal
from cruds import user_crud as crud
from crypto.rsa import decrypt
from schemas import user_schema as schema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from crypto import jwt
import re

ru_error_detail = {
    "user not found": "Пользователь не найден",
    "user already exists": "Полььзователь уже существует",
    "invalid password": "Неверный пароль",
    "invalid encryption": "Неверное шифрование",
    "invalid email": "Неверная почта",
    "invalid password validation": "Неподходящий пароль",
    "failed to create user": "Не удалось создать пользователя",
    "faled to change password": "Не удалось изменить пароль",
    "failed to delete user": "Не удалось удалить пользователя",
}

en_error_detail = {
    "user not found": "User not found",
    "user already exists": "User already exists",
    "invalid password": "Invalid password",
    "invalid encryption": "Invalid encryption",
    "invalid email": "Invalid email",
    "invalid password validation": "Invalid password validation",
    "failed to create user": "Failed to create user",
    "faled to change password": "Failed to change password",
    "failed to delete user": "Failed to delete user",
}

ACCESS_TOCKEN_NAME = 'api-heart'


def get_preferred_language(accept_language: str) -> str:
    """
    Extracts the preferred language from the Accept-Language header.

    Args:
        accept_language (str): The Accept-Language header value.

    Returns:
        str: The preferred language code (ru or en).
    """

    if not accept_language:
        return 'en'

    # Split the Accept-Language header value by comma
    languages = accept_language.split(',')

    # Iterate over the languages and extract the language code
    for language in languages:
        # Remove any whitespace
        language = language.strip()

        # Extract the language code and quality value
        match = re.match(r'^(\w+)(?:;q=(\d.\d+))?$', language)
        if match:
            language_code = match.group(1)

            # Check if the language code is "ru" or "en"
            if language_code in ['ru', 'en']:
                return language_code

    # Return "en" as the default language if no preferred language is found
    return 'en'

async def get_error_detail(detail, locale=None):
    lang = get_preferred_language(locale)
    if lang == 'ru':
        return ru_error_detail[detail]
    else:
        return en_error_detail[detail]

async def validate_access_token(cookies):
    """
    Asynchronously validates the access token in the cookies.

    Args:
        cookies (dict): Dictionary containing the cookies.

    Raises:
        HTTPException: If the cookies are empty or the access token is invalid.

    Returns:
        dict: Payload of the access token.
    """
    if not cookies:
        raise HTTPException(status_code=401)

    access_token = cookies.get(ACCESS_TOCKEN_NAME)
    if not access_token:
        raise HTTPException(status_code=401)

    token_payload = await jwt.decrypt_token(access_token)
    if not token_payload:
        raise HTTPException(status_code=401)

    return token_payload

async def validate_jwt_token(token):
    """
    Asynchronously validates the access token in the cookies.

    Args:
        cookies (dict): Dictionary containing the cookies.

    Raises:
        HTTPException: If the cookies are empty or the access token is invalid.

    Returns:
        dict: Payload of the access token.
    """
    if not token.token:
        raise HTTPException(status_code=401)

    token_payload = await jwt.decrypt_token(token.token)
    if not token_payload:
        raise HTTPException(status_code=401)

    return token_payload

async def validate_email(locale: str, email: str):
    """
    Validates an email address by decrypting it and checking if it is a valid email format.

    Args:
        email (str): The email address to be validated.

    Raises:
        HTTPException: If the email address is invalid or the decryption fails.

    Returns:
        None
    """
    email = await decrypt(email)
    if not email:
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                locale=locale,
                detail='invalid encryption'
                )
            )
    
    if not schema.validate_email(email):
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                locale=locale,
                detail='invalid email'
                )
            )
    
    return email

async def validate_password(locale: str, password: str):
    """
    Validates a password by decrypting it and checking if it meets certain criteria.

    Args:
        password (str): The password to be validated.

    Raises:
        HTTPException: If the password is invalid or if there is an error during decryption.

    Returns:
        None
    """
    password = await decrypt(password)
    if not password:
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                locale=locale,
                detail='invalid encryption'
                )
            )
    
    if not schema.validate_password(password):
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                locale=locale,
                detail='invalid password validation'
                )
            )
    
    return password

async def get_user_by_token(db: AsyncSession, payload: dict, locale: str = None):
    """
    Retrieves a user from the database based on the provided token.

    Args:
        db (AsyncSession): An asynchronous session object for interacting with the database.
        token (dict): A dictionary containing the token information. It is expected to have a key 'sub' which represents the email of the user.

    Returns:
        User: The user associated with the token.

    Raises:
        HTTPException: If the user is not found in the database.
    """
    email = payload['sub']
    user = await crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=await get_error_detail(
                locale=locale,
                detail='user not found'
                )
            )
    return user

async def get_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def get_cookie(cookie: str, key: str):
    cookies = dict(token.split('=') for token in cookie.split('; ') if token.strip())
    return cookies.get(key)

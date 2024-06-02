import cruds.user_crud as crud
from crypto.argon2 import check_user_password
from crypto.rsa import get_rsa_public_key, decrypt
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, Cookie, Header
import schemas.user_schema as schema
from schemas.key import Key
from sqlalchemy.ext.asyncio import AsyncSession
from crypto import jwt
from fastapi.responses import JSONResponse
from typing import Annotated


ACCESS_TOCKER_NAME = 'api-heart'

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

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

    access_token = cookies.get(ACCESS_TOCKER_NAME)
    if not access_token:
        raise HTTPException(status_code=401)

    token_payload = await jwt.decrypt_token(access_token)
    if not token_payload:
        raise HTTPException(status_code=401)

    return token_payload

async def get_user_by_token(db: AsyncSession, token: dict):
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
    email = token['sub']
    user = await crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/signup/")
async def signup(user_create: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user.

    Args:
        user_create (schema.UserCreate): The user data to create.
        db (AsyncSession, optional): The database session to use for the user creation. Defaults to the result of the get_db dependency.

    Returns:
        JSONResponse: The response indicating the success of the user creation.

    Raises:
        HTTPException: If the email, password, or both are not properly encrypted or if the email or password is invalid.
        HTTPException: If a user with the same email already exists.
        HTTPException: If the user creation fails.
    """
    email = await decrypt(user_create.email)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid email encryption")
    
    if not schema.validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email")
    
    if await crud.get_user_by_email(db, email=email):
        raise HTTPException(status_code=400, detail="User already exists")
    
    password = await decrypt(user_create.password)
    if not password:
        raise HTTPException(status_code=400, detail="Invalid password encryption")
    
    if not schema.validate_password(password):
        raise HTTPException(status_code=400, detail="Invalid password")

    if not await crud.create_user(db, schema.UserCreate(email=email, password=password)):
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    return JSONResponse(status_code=201, content={})

@router.get("/login/", response_model=schema.UserInfo)
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the user information of the logged-in user.

    Args:
        request (Request): The request object containing the HTTP request details.
        db (AsyncSession, optional): The asynchronous session object for interacting with the database.
            Defaults to the result of the `get_db` dependency.

    Returns:
        schema.UserInfo: The user information of the logged-in user.

    Raises:
        HTTPException: If the token is not found or the user is not found in the database.
    """
    token = await validate_access_token(request.cookies)
    user = await get_user_by_token(db, token)
    return user

#User logins and gets token
@router.post("/token/")
async def get_token(user_data: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Asynchronously generates a token for the given user credentials and sets it as a cookie in the response.

    Args:
        user_data (schema.UserCreate): The user credentials to generate the token for.
        db (AsyncSession, optional): The asynchronous session object for interacting with the database. Defaults to the result of the `get_db` function.

    Raises:
        HTTPException: If the email encryption is wrong,
                        the email is wrong,
                        the user is not found in the database,
                        the password encryption is wrong,
                        the password is wrong,
                        or the password validation fails.

    Returns:
        JSONResponse: The response containing the generated token as a cookie.

    """
    user_email = await decrypt(user_data.email)
    if not user_email:
        raise HTTPException(status_code=400, detail="Invalid email encryption")

    if not schema.validate_email(user_email):
        raise HTTPException(status_code=400, detail="Invalid email")

    db_user = await crud.get_user_by_email(db, email=user_email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_password = await decrypt(user_data.password)
    if not user_password:
        raise HTTPException(status_code=400, detail="Invalid password encryption")

    if not await check_user_password(db_user, user_password) or not schema.validate_password(user_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    response = JSONResponse(status_code=200, content={})
    response.set_cookie(
        key=ACCESS_TOCKER_NAME,
        value=await jwt.generate_access_token({"sub": user_email}),
        httponly=True,
        secure=True,
        max_age=jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return response

@router.get("/public-key/", response_model=Key)
async def get_public_key():
    """
    Returns the public key for encryption and decryption.
    """
    return {"key": await get_rsa_public_key()}

@router.get("/logout/")
async def logout(request: Request):
    """
    Clears the access token cookie upon logout.

    Args:
        request: The HTTP request object.

    Returns:
        A JSON response with a status code of 200 and an empty content.
    """
    response = JSONResponse(status_code=200, content={})
    response.delete_cookie(key=ACCESS_TOCKER_NAME)
    return response

@router.post("/change-password/")
async def change_password(user_data: schema.ChangePassword, request: Request, db: AsyncSession = Depends(get_db)):
    """
    Asynchronously handles the change password request.

    Args:
        user_data (schema.ChangePassword): The user object containing the current and new passwords.
        request (Request): The request object containing the HTTP request details.
        db (AsyncSession, optional): The asynchronous session object for interacting with the database. Defaults to the result of the `get_db` function.

    Returns:
        JSONResponse: The response object with a status code of 200 and an empty content.

    Raises:
        HTTPException: If the current password is not correctly encrypted,
                    if the current password is incorrect or does not meet the password validation criteria,
                    if the new password is not correctly encrypted,
                    if the new password does not meet the password validation criteria,
                    or if the password change operation fails.
    """
    token = await validate_access_token(request.cookies)
    user = await get_user_by_token(db, token)

    current_password = await decrypt(user_data.current_password)
    if not current_password:
        raise HTTPException(status_code=400, detail="Wrong encryption")

    if not await check_user_password(user, current_password) or not schema.validate_password(current_password):
        raise HTTPException(status_code=400, detail="Wrong password")

    new_password = await decrypt(user_data.new_password)
    if not new_password:
        raise HTTPException(status_code=400, detail="Wrong encryption")

    if not schema.validate_password(new_password):
        raise HTTPException(status_code=400, detail="Invalid new password")

    if not await crud.change_password(db, user, new_password):
        raise HTTPException(status_code=500, detail="Failed to change password")

    return JSONResponse(status_code=200, content={})

@router.post("/delete/")
async def delete_user(request: Request, user_data: schema.UserDelete, db: AsyncSession = Depends(get_db)):
    token = await validate_access_token(request.cookies)
    user = await get_user_by_token(db, token)

    password = await decrypt(user_data.password)
    if not password:
        raise HTTPException(status_code=400, detail="Wrong encryption")

    if not schema.validate_password(password) or not await check_user_password(user, password):
        raise HTTPException(status_code=400, detail="Wrong password")

    if not await crud.delete_user(db, user):
        raise HTTPException(status_code=500, detail="Failed to change password")

    return JSONResponse(status_code=200, content={})

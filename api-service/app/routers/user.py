import cruds.user_crud as crud
from crypto.argon2 import check_user_password
from crypto.rsa import get_rsa_public_key
from dependencies import (get_db, ACCESS_TOCKEN_NAME, get_error_detail,
    validate_access_token, validate_email, validate_password, get_user_by_token)
from fastapi import APIRouter, Depends, HTTPException, Request
import schemas.user_schema as schema
from schemas.key import Key
from sqlalchemy.ext.asyncio import AsyncSession
from crypto import jwtoken
from fastapi.responses import JSONResponse
from email_sender.send_email import send_registration_email, send_changed_password_email, send_deleted_email
import asyncio


router = APIRouter(
    prefix="/user",
    tags=["auth"]
)

@router.post("/signup/")
async def signup(request: Request, user_create: schema.UserCreate, db: AsyncSession = Depends(get_db)):
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
    email = await validate_email(request.headers.get('accept-language'), user_create.email)

    if await crud.get_user_by_email(db, email=email):
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                'user already exists',
                request.headers.get('accept-language'),
                )
            )
    
    password = await validate_password(request.headers.get('accept-language'), user_create.password)

    if not await crud.create_user(db, schema.UserCreate(email=email, password=password)):
        raise HTTPException(
            status_code=500,
            detail=await get_error_detail(
                'failed to create user',
                request.headers.get('accept-language'),
                )
            )
    
    asyncio.ensure_future(send_registration_email(request.headers.get('accept-language'), email))
    
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
    user = await get_user_by_token(db, token, request.headers.get('accept-language'))
    return user

#User logins and gets token
@router.post("/web-token/")
async def get_token(request: Request, user_data: schema.UserCreate, db: AsyncSession = Depends(get_db)):
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
    email = await validate_email(request.headers.get('accept-language'), user_data.email)

    db_user = await crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=await get_error_detail(
                'user not found',
                request.headers.get('accept-language'),
                )
            )

    password = await validate_password(request.headers.get('accept-language'), user_data.password)

    if not await check_user_password(db_user, password):
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                'invalid password',
                request.headers.get('accept-language'),
                )
            )

    response = JSONResponse(status_code=200, content={})
    response.set_cookie(
        key=ACCESS_TOCKEN_NAME,
        value=await jwtoken.generate_access_token({"sub": email}),
        httponly=True,
        secure=True,
        max_age=jwtoken.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return response

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

    email = await validate_email(None, user_data.email)

    db_user = await crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=await get_error_detail(
                'user not found',
                )
            )

    password = await validate_password(None, user_data.password)

    if not await check_user_password(db_user, password):
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                'invalid password',
                )
            )

    return {"token": await jwtoken.generate_access_token({"sub": email})}

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
    response.delete_cookie(key=ACCESS_TOCKEN_NAME)
    return response

@router.put("/change-password/")
async def change_password(request: Request, user_data: schema.ChangePassword, db: AsyncSession = Depends(get_db)):
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
    user = await get_user_by_token(db, token, request.headers.get('accept-language'))

    current_password = await validate_password(request.headers.get('accept-language'), user_data.current_password)

    if not await check_user_password(user, current_password):
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                'invalid password',
                request.headers.get('accept-language'),
                )
            )

    new_password = await validate_password(request.headers.get('accept-language'), user_data.new_password)

    if not await crud.change_password(db, user, new_password):
        raise HTTPException(
            status_code=500,
            detail=await get_error_detail(
                'failed to change password',
                request.headers.get('accept-language'),
                )
            )

    # Run the email sending in parallel so the function can return without awaiting the result
    asyncio.ensure_future(send_changed_password_email(request.headers.get('accept-language'), user.email))

    return JSONResponse(status_code=200, content={})

@router.post("/delete/")
async def delete_user(request: Request, user_data: schema.UserDelete, db: AsyncSession = Depends(get_db)):
    token = await validate_access_token(request.cookies)
    user = await get_user_by_token(db, token, request.headers.get('accept-language'))

    password = await validate_password(request.headers.get('accept-language'), user_data.password)

    if not await check_user_password(user, password):
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                'invalid password',
                request.headers.get('accept-language'),
                )
            )

    if not await crud.delete_user(db, user):
        raise HTTPException(
            status_code=500,
            detail=await get_error_detail(
                'failed to delete user',
                request.headers.get('accept-language'),
                )
            )
    
    asyncio.ensure_future(send_deleted_email(request.headers.get('accept-language'), user.email))

    response = JSONResponse(status_code=200, content={})
    response.delete_cookie(key=ACCESS_TOCKEN_NAME)

    return response

@router.delete("/delete/")
async def delete_user(request: Request, user_data: schema.UserDelete, db: AsyncSession = Depends(get_db)):
    token = await validate_access_token(request.cookies)
    user = await get_user_by_token(db, token, request.headers.get('accept-language'))

    password = await validate_password(request.headers.get('accept-language'), user_data.password)

    if not await check_user_password(user, password):
        raise HTTPException(
            status_code=400,
            detail=await get_error_detail(
                'invalid password',
                request.headers.get('accept-language'),
                )
            )

    if not await crud.delete_user(db, user):
        raise HTTPException(
            status_code=500,
            detail=await get_error_detail(
                'failed to delete user',
                request.headers.get('accept-language'),
                )
            )
    
    asyncio.ensure_future(send_deleted_email(request.headers.get('accept-language'), user.email))

    response = JSONResponse(status_code=200, content={})
    response.delete_cookie(key=ACCESS_TOCKEN_NAME)

    return response

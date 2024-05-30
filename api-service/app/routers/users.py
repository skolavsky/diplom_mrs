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

async def check_cookies(cookies):
    if not cookies:
        raise HTTPException(status_code=401)

    token = cookies.get(ACCESS_TOCKER_NAME, None)
    if not token:
        raise HTTPException(status_code=401)
    
    token = await jwt.decrypt_token(token)
    if not token:
        raise HTTPException(status_code=401)
    
    return token

async def get_db_user_by_token(db, token):
    user = await crud.get_user_by_email(db, email=token['sub'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/signup/")
async def create_user(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    user.email = await decrypt(user.email)
    if not user.email:
        raise HTTPException(status_code=400, detail="Wrong encryption")
    
    if not schema.validate_email(user.email):
        raise HTTPException(status_code=400, detail="Wrong email")
    
    if await crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.password = await decrypt(user.password)
    if not user.password:
        raise HTTPException(status_code=400, detail="Wrong encryption")

    if not await crud.create_user(db, user):
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    return JSONResponse(status_code=201, content={})

@router.get("/login/", response_model=schema.UserInfo)
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    token = await check_cookies(request.cookies)
    
    db_user = await get_db_user_by_token(db, token)
    
    return db_user

#User logins and gets token
@router.post("/token/")
async def get_token(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    user.email = await decrypt(user.email)
    if not user.email:
        raise HTTPException(status_code=400, detail="Wrong encryption")
    
    if not schema.validate_email(user.email):
        raise HTTPException(status_code=400, detail="Wrong email")

    db_user = await crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = await decrypt(user.password)

    if not user.password:
        raise HTTPException(status_code=400, detail="Wrong encryption")
    if not await check_user_password(db_user, user.password) \
        or not schema.validate_password(user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    # Login successful
    response = JSONResponse(status_code=200, content={})
    response.set_cookie(
        key=ACCESS_TOCKER_NAME,
        value=await jwt.generate_access_token({"sub": user.email}),
        httponly=True,
        secure=True
        )
    
    return response

@router.get("/publickey/", response_model=Key)
async def get_public_key():
    return {"key": await get_rsa_public_key()}

@router.get("/logout/")
async def logout(request: Request):
    response = JSONResponse(status_code=200, content={})
    response.delete_cookie(ACCESS_TOCKER_NAME)
    return response

@router.post("/change-password/")
async def change_password(user: schema.ChangePassword, request: Request, db: AsyncSession = Depends(get_db)):
    token = await check_cookies(request.cookies)
    
    db_user = await get_db_user_by_token(db, token)
    
    user.current_password = await decrypt(user.current_password)
    if not user.current_password:
        raise HTTPException(status_code=400, detail="Wrong encryption")
        
    if not await check_user_password(db_user, user.current_password) \
        or not schema.validate_password(user.current_password):
        raise HTTPException(status_code=400, detail="Wrong password")

    user.new_password = await decrypt(user.new_password)
    if not user.new_password:
        raise HTTPException(status_code=400, detail="Wrong encryption")
    
    if not schema.validate_password(user.new_password):
        raise HTTPException(status_code=400, detail="Wrong new password")
    
    if not await crud.change_password(db, db_user, user.new_password):
        raise HTTPException(status_code=500, detail="Failed to change password")
    
    return JSONResponse(status_code=200, content={})

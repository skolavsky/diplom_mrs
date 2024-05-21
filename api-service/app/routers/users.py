import cruds.user_crud as crud
from crypto.argon2 import check_user_password
from crypto.rsa import get_rsa_public_key, decrypt
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
import schemas.user_schema as schema
from schemas.key import Key
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/users",
    tags=["users"],
    #responses={404: {"description": "Not found"}},
)

@router.post("/signup/", response_model=schema.User)
async def create_user(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@router.post("/login/", response_model=schema.User)
async def chech_user(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):

    user.email = await decrypt(user.email)
    if not user.email:
        raise HTTPException(status_code=400, detail="Wrong encryption")

    db_user = await crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = await decrypt(user.password)

    if not user.password:
        raise HTTPException(status_code=400, detail="Wrong encryption")
    if not await check_user_password(db_user, user):
        raise HTTPException(status_code=400, detail="Wrong password")

    return db_user

@router.get("/publickey/", response_model=Key)
async def get_public_key():
    return {"key": await get_rsa_public_key()}

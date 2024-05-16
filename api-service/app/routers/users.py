from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

import schemas.user_schema as schema
import cruds.user_crud as crud

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
    db_user = await crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.check_user_password(db, user):
        raise HTTPException(status_code=400, detail="Wrong password")
    return db_user

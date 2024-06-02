from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from models.user import User
import schemas.user_schema as schema
from crypto.argon2 import password_handler

async def get_user_by_email(db: Session, email: str):
    user = await db.execute(select(User).filter(User.email == email))
    return user.scalars().first()

async def create_user(db: AsyncSession, user: schema.UserCreate):
    hashed_password = password_handler.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return True
    except Exception as e:
        print(e)
        return False

async def change_password(db: AsyncSession, db_user: User, new_password: str):
    hashed_password = password_handler.hash(new_password)
    db_user.hashed_password = hashed_password
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return True
    except Exception as e:
        print(e)
        return False

async def delete_user(db: AsyncSession, user: User):
    try:
        await db.delete(user)
        await db.commit()
        return True
    except Exception as e:
        print(e)
        return False

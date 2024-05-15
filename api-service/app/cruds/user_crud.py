from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from models.user import User
import schemas.user_schema as schema
from crypto.argon2 import password_handler

async def get_user(db: Session, user_id: int):
    user = await db.execute(select(models.User).filter(models.User.id == user_id))
    return user.scalars().first()

async def get_user_by_email(db: Session, email: str):
    user = await db.execute(select(models.User).filter(models.User.email == email))
    return user.scalars().first()

async def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = await db.execute(select(models.User))
    return users.scalars().all()

async def create_user(db: AsyncSession, user: schema.UserCreate):
    hashed_password = password_handler.hash(user.hashed_password)
    db_user = models.User(email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

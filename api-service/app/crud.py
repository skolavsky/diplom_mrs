from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import models, schema


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
    fake_hashed_password = user.hashed_password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

from database import Base, engine, SessionLocal

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

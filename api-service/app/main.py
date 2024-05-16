from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from routers import users
import schemas.user_schema as schema
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from cruds import user_crud as crud

from dependencies import get_db

app = FastAPI()

app.include_router(users.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/test/{data}")
async def test(data: float):
    result = 0.0125*data*data-0.2017*data+1.2955
    if result < 0.1:
        result = 0.1
    elif result > 0.9:
        result = 0.9
    return {"result": 1 - result}

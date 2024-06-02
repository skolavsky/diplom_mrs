from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import routers.user as user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(user.router)

@app.get("/test/{data}")
async def test(data: float):
    result = 0.0125*data*data-0.2017*data+1.2955
    if result < 0.1:
        result = 0.1
    elif result > 0.9:
        result = 0.9
    return {"result": 1 - result}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

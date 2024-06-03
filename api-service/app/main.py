from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from routers import user, model
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(user.router)
app.include_router(model.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

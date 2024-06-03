from fastapi import APIRouter, Request, Depends, HTTPException
from dependencies import get_db, validate_access_token, get_user_by_token, validate_jwt_token
from schemas.jwtoken import JWToken
from schemas.result import Result
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/model",
    tags=["models"]
)


async def model_test(data):
    result = 0.0125*data*data-0.2017*data+1.2955
    if result < 0.1:
        result = 0.1
    elif result > 0.9:
        result = 0.9
    return 1 - result

@router.get("/test/{data}", response_model=Result)
async def test(data: float, request: Request, db: AsyncSession = Depends(get_db)):
    token = await validate_access_token(request.cookies)
    if not await get_user_by_token(db, token):
        raise HTTPException(status_code=401)

    result = await model_test(data)
    return {"result": result}

@router.post("/test/{data}", response_model=Result)
async def test(data: float, token: JWToken, db: AsyncSession = Depends(get_db)):
    token = await validate_jwt_token(token=token)
    if not await get_user_by_token(db, token):
        raise HTTPException(status_code=401)

    result = await model_test(data)
    return {"result": result}

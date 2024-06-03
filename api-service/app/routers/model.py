from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/model",
    tags=["models"]
)

@router.get("/test/{data}")
async def test(data: float, request: Request):
    result = 0.0125*data*data-0.2017*data+1.2955
    if result < 0.1:
        result = 0.1
    elif result > 0.9:
        result = 0.9
    return {"result": 1 - result}


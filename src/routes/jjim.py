from fastapi import FastAPI, Request

router = FastAPI(
    prefix="/jjim",
    tags=["찜 관련 엔드포인트"]
)

@router.get("/board_info")
async def board_info(request: Request):
    
    return
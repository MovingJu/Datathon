from fastapi import APIRouter
import modules
from fastapi import Response

router = APIRouter(
    prefix="/sign",
    tags=["로그인/회원가입 엔드포인트"]
)

@router.post("/up")
async def signup(nickname: str, pw: str):
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]

    data.append({
        "nickname" : nickname,
        "pw" : pw
    })
    await modules.write("user", data)
    return {"code" : 200}

@router.post("/in")
async def signin(nickname: str, pw: str):
    document: dict = await modules.read("user") or {}
    data: list[dict] = document["data"]
    for item in data:
        if(item.get("nickname") != nickname or item.get("pw") != pw):
            continue
        response = Response(
            content='{"code" : 200}', media_type="application/json"
        )
        response.set_cookie(key="session", value=nickname, httponly=True)
        return response
    
    return {
        "code" : 404,
        "message" : "user not found"
    }
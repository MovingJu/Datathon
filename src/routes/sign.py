from fastapi import APIRouter
import modules
from pydantic import BaseModel
from fastapi import Response

router = APIRouter(
    prefix="/sign",
    tags=["로그인/회원가입 엔드포인트"]
)

class LoginBody(BaseModel):
    nickname: str
    pw: str

@router.post("/up")
async def signup(body: LoginBody):
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]

    data.append({
        "nickname" : body.nickname,
        "pw" : body.pw
    })
    await modules.write("user", data)
    return {"code" : 200}


@router.post("/in")
async def signin(body: LoginBody):
    document: dict = await modules.read("user") or {}
    data: list[dict] = document["data"]
    for item in data:
        if(item.get("nickname") != body.nickname or item.get("pw") != body.pw):
            continue
        response = Response(
            content='{"code" : 200}', media_type="application/json"
        )
        response.set_cookie(key="session", value=body.nickname, httponly=True)
        return response
    
    return {
        "code" : 404,
        "message" : "user not found"
    }
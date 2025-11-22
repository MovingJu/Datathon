from fastapi import APIRouter
import modules
from fastapi import Response

router = APIRouter()

@router.post("/signup")
async def signup(nickname: str, pw: str):
    document: dict = await modules.read("user") or {}
    data: list[dict] = document["data"]

    data.append({
        "nickname" : nickname,
        "pw" : pw
    })
    await modules.write("user", data)
    return {"code" : 200}

@router.post("/login")
async def login(nickname: str, pw: str):
    document: dict = await modules.read("user") or {}
    user = next((u for u in document.get("data", []) if u["nickname"] == nickname and u["pw"] == pw), None)
    if user:
        response = Response(content='{"code":200}', media_type="application/json")
        response.set_cookie(key="session", value=nickname, httponly=True)
        return response
    else:
        return {"code": 401, "message": "Invalid credentials"}
    return
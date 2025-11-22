from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
import modules

router = APIRouter(
    prefix="/user",
    tags=["유저 정보 조회 및 수정 엔드포인트"]
)

@router.get("/me")
async def get_user(request: Request):
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "Please login"}
    
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document.get("data", [])
    
    for user in data:
        if user.get("nickname") == nickname:
            return {"code": 200, "data": user}
    
    return {"code": 404, "message": "user not found."}

# ----- Pydantic 모델 -----
class UpdateBasicModel(BaseModel):
    key: str
    val: str

class UpdateLocationModel(BaseModel):
    si: str
    gu: str

class UpdateBabyModel(BaseModel):
    birth: str
    height: int
    weight: int
    sex: int
    tags: List[str]
    idx: int = -1

class UpdateClothesModel(BaseModel):
    title: str
    picture: str
    price: float
    size: int
    content: str
    tags: List[str]
    idx: int = -1

class UpdateWritingsModel(BaseModel):
    writing_id: int
    idx: int = -1

# ----- 공통 함수 -----
async def update(request: Request, key, val):
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "Please login"}
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    user: dict = {}
    for idx, item in enumerate(data):
        if nickname == item.get("nickname"):
            user = item
            break
    else:
        return {"code": 404, "message": "user not found."}
    user[key] = val
    data[idx] = user
    await modules.write("user", data)
    return {"code": 200, "message": "successfully fetched."}

# ----- Endpoints -----
@router.post("/update_basic")
async def update_basic(request: Request, body: UpdateBasicModel):
    return await update(request, body.key, body.val)

@router.post("/update_location")
async def update_location(request: Request, body: UpdateLocationModel):
    return await update(request, "location", [body.si, body.gu])

@router.post("/update_baby")
async def update_baby(request: Request, body: UpdateBabyModel):
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "Please login"}
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    user: dict = {}
    for _idx, item in enumerate(data):
        if nickname == item.get("nickname"):
            user = item
            break
    else:
        return {"code": 404, "message": "user not found."}
    baby_data = {
        "birth": body.birth,
        "height": body.height,
        "weight": body.weight,
        "sex": body.sex,
        "tags": body.tags
    }
    if body.idx == -1:
        user["baby"].append(baby_data)
    else:
        user["baby"][body.idx] = baby_data
    data[_idx] = user
    await modules.write("user", data)
    return {"code": 200, "message": "successfully fetched."}

@router.post("/update_clothes")
async def update_clothes(request: Request, body: UpdateClothesModel):
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "Please login"}
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    user: dict = {}
    for _idx, item in enumerate(data):
        if nickname == item.get("nickname"):
            user = item
            break
    else:
        return {"code": 404, "message": "user not found."}
    clothes_data = {
        "title": body.title,
        "picture": body.picture,
        "price": body.price,
        "size": body.size,
        "content": body.content,
        "tags": body.tags
    }
    if body.idx == -1:
        user["clothes"].append(clothes_data)
    else:
        user["clothes"][body.idx] = clothes_data
    data[_idx] = user
    await modules.write("user", data)
    return {"code": 200, "message": "successfully fetched."}

@router.post("/update_writings")
async def update_writings(request: Request, body: UpdateWritingsModel):
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "Please login"}
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    user: dict = {}
    for _idx, item in enumerate(data):
        if nickname == item.get("nickname"):
            user = item
            break
    else:
        return {"code": 404, "message": "user not found."}
    if body.idx == -1:
        user["writings"].append(body.writing_id)
    else:
        user["writings"][body.idx] = body.writing_id
    data[_idx] = user
    await modules.write("user", data)
    return {"code": 200, "message": "successfully fetched."}

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
import modules

router = APIRouter(
    prefix="/user",
    tags=["유저 정보 조회 및 수정 엔드포인트"]
)

@router.get("/get_sellers")
async def get_sellers(request: Request):
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document.get("data", [])

    sellers = []
    for user in data:
        # 판매자만 가져온다고 가정 (예: clothes나 baby 있는 유저)
        if user.get("clothes") or user.get("baby"):
            sellers.append({
                "id": user.get("nickname"),
                "nickname": user.get("nickname"),
                "avatar": user.get("avatar", "/placeholder.svg"),
                "bio": user.get("bio", ""),
                "childrenTags": user.get("childrenTags", []),
                "products": user.get("clothes", [])  # clothes 배열을 products로 매핑
            })
    
    return {"code": 200, "data": sellers}


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

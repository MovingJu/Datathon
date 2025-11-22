from fastapi import APIRouter, Request
import modules

async def update(request: Request, key, val):
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {
            "code" : 401,
            "message" : "Please login"
        }
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    user: dict = {}
    for idx, item in enumerate(data):
        if (nickname == item.get("nickname")):
            user = item
            break
    else:
        return {
            "code" : 404,
            "message" : "user not found."
        }
    user[key] = val
    data[idx] = user
    await modules.write("user", data)
    return {
        "code" : 200,
        "message" : "successfully fetched."
    }

router = APIRouter(
    prefix="/user",
    tags=["유저 정보 조회 및 수정 엔드포인트"]
)

@router.get("/info")
async def info(nickname: str):
    if not nickname:
        return {
            "code" : 401,
            "message" : "Please login"
        }
    
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    for item in data:
        if (nickname == item.get("nickname")):
            return item

    return {
        "code" : 404,
        "message" : "user not found"
    }

@router.post("/update_basic")
async def update_basic(request: Request, key: str, val: str):
    """
    nickname, pw, profile_photo, bio 수정에만 사용.
    """
    code: dict = await update(request, key, val)
    return code

@router.post("/update_location")
async def update_location(request: Request, si: str, gu: str):
    """
    location 수정에만 사용
    """
    code: dict = await update(request, "location", [si, gu])
    return code

@router.post("/update_baby")
async def update_baby(request: Request, birth: str, height: int, weight: int, sex: int, tags: list[str], idx: int = -1):
    """
    baby 수정에만 사용
    idx에 -1을 넣어서 append한다.
    """
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {
            "code" : 401,
            "message" : "Please login"
        }
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    user: dict = {}
    for _idx, item in enumerate(data):
        if (nickname == item.get("nickname")):
            user = item
            break
    else:
        return {
            "code" : 404,
            "message" : "user not found."
        }
    if (idx == -1):
        user["baby"].append({
            "birth" : birth,
            "height" : height,
            "weight" : weight,
            "sex" : sex,
            "tags" : tags
        })
    else:
        user["baby"][idx] = {
            "birth" : birth,
            "height" : height,
            "weight" : weight,
            "sex" : sex,
            "tags" : tags
        }
    data[_idx] = user
    await modules.write("user", data)
    return {
        "code" : 200,
        "message" : "successfully fetched."
    }

@router.post("/update_clothes")
async def update_clothes(request: Request, title: str, picture: str, price: float, size: int, content: str, tags: list[str], idx: int = -1):
    """
    clothes 수정에만 사용
    idx에 -1을 넣어서 append한다.
    """
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {
            "code" : 401,
            "message" : "Please login"
        }
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    user: dict = {}
    for _idx, item in enumerate(data):
        if (nickname == item.get("nickname")):
            user = item
            break
    else:
        return {
            "code" : 404,
            "message" : "user not found."
        }
    if (idx == -1):
        user["clothes"].append({
            "title" : title,
            "picture" : picture,
            "price" : price,
            "size" : size,
            "content" : content,
            "tags" : tags
        })
    else:
        user["clothes"][idx] = {
            "title" : title,
            "picture" : picture,
            "price" : price,
            "size" : size,
            "content" : content,
            "tags" : tags
        }
    data[_idx] = user
    await modules.write("user", data)
    return {
        "code" : 200,
        "message" : "successfully fetched."
    }

@router.post("/update_writings")
async def update_writings(request: Request, writing_id: int, idx: int = -1):
    """
    writings 수정에만 사용
    idx에 -1을 넣어서 append한다.
    """
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {
            "code" : 401,
            "message" : "Please login"
        }
    document: dict = await modules.read("user", "data") or {}
    data: list[dict] = document["data"]
    user: dict = {}
    for _idx, item in enumerate(data):
        if (nickname == item.get("nickname")):
            user = item
            break
    else:
        return {
            "code" : 404,
            "message" : "user not found."
        }
    if (idx == -1):
        user["writings"].append(writing_id)
    else:
        user["writings"][idx] = writing_id
    data[_idx] = user
    await modules.write("user", data)
    return {
        "code" : 200,
        "message" : "successfully fetched."
    }
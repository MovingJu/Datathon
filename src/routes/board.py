from fastapi import APIRouter, Request
import modules

router = APIRouter(
    prefix="/board",
    tags=["게시글 관리 엔드포인트"]
)

@router.get("/")
async def index():
    document: dict = await modules.read("board", "boards") or {}
    data = document.get("boards")
    if(not data):
        return {
            "code" : 403,
            "message" : "Please check database."
        }
    return {
        "code" : 200,
        "data" : data
    }
@router.get("/info")
async def info(board_name: str):
    document: dict = await modules.read("board", "writings") or {}
    data = document.get("writings")
    if(not data):
        return {
            "code" : 403,
            "message" : "Please check database."
        }
    response: list[dict] = []
    for writing in data:
        if(writing.get("board") != board_name):
            continue
        response.append({
            "id" : writing.get("id"),
            "writer" : writing.get("writer"),
            "liked" : len(writing.get("liked")),
            "comments" : len(writing.get("comment") or [])
        })
    return {
        "code" : 200,
        "data" : response
    }
@router.get("/content")
async def content(board_id: int):
    document: dict = await modules.read("board", "writings") or {}
    data = document.get("writings")
    if(not data):
        return {
            "code" : 403,
            "message" : "Please check database."
        }   
    for writing in data:
        if(writing.get("id") == board_id):
            writing["liked"] = len(writing["liked"])
            return {
                "code" : 200,
                "data" : writing
            }
    return {
        "code" : 403,
        "message" : "Title not found."
    }
@router.post("/modify")
async def modify(request: Request, board_id: int, user_input: modules.Writing):
    nickname: str = request.cookies.get("session") or ""
    document: dict = await modules.read("board", "writings") or {}
    data = document.get("writings")
    if(not data):
        return {
            "code" : 403,
            "message" : "Please check database."
        }
    target: dict = {}
    for idx, writing in enumerate(data):
        if(writing.get("id") == board_id):
            target = writing
            break
    else:
        return {
            "code" : 403,
            "message" : "Title not found."
        }
    if (nickname != target.get("writer")):
        return {
            "code" : 401,
            "message" : "Not your writing."
        }
    
    data[idx] = {
        "id" : data[idx]["id"],
        "title" : user_input.title,
        "writer" : user_input.writer,
        "board" : user_input.board,
        "date" : user_input.date,
        "content" : user_input.content,
    }
    await modules.write("board", data, "writings")
    return {
        "code" : 200,
        "message" : "Modify successfully."
    }
@router.post("/add")
async def add(request: Request, user_input: modules.Writing):
    nickname: str = request.cookies.get("session") or ""
    document: dict = await modules.read("board", "writings") or {}
    data = document.get("writings")
    if(not data):
        return {
            "code" : 403,
            "message" : "Please check database."
        }
    biggest_id = -1
    for item in data:
        if (biggest_id < item.get("id") or -2):
            biggest_id = item["id"]
    data.append({
        "id" : biggest_id+1,
        "title" : user_input.title,
        "writer" : user_input.writer,
        "board" : user_input.board,
        "date" : user_input.date,
        "content" : user_input.content,
    })
    await modules.write("board", data, "writings")
    return {
        "code" : 200,
        "message" : "Add successfully."
    }
@router.delete("/delete")
async def delete(request: Request, board_id: int):
    nickname: str = request.cookies.get("session") or ""
    document: dict = await modules.read("board", "writings") or {}
    data = document.get("writings")
    if not data:
        return {
            "code": 403,
            "message": "Please check database."
        }
    for idx, writing in enumerate(data):
        if writing.get("id") != board_id:
            continue
        if writing.get("writer") != nickname:
            return {
                "code": 401,
                "message": "Not your writing."
            }
        del data[idx]
        await modules.write("board", data, "writings")
        return {
            "code": 200,
            "message": "Delete successfully."
        }
    return {
        "code": 403,
        "message": "Title not found."
    }
@router.get("/like")
async def like(request: Request, board_id: int):
    nickname: str = request.cookies.get("session") or ""
    document: dict = await modules.read("board", "writings") or {}
    data = document.get("writings")
    if not data:
        return {
            "code": 403,
            "message": "Please check database."
        }
    for idx, writing in enumerate(data):
        if writing.get("id") != board_id:
            continue
        if writing.get("writer") != nickname:
            return {
                "code": 401,
                "message": "Not your writing."
            }
        if(not data[idx].get("liked")):
            return {
                "code" : 403,
                "message" : "Please check database."
            }
        if(nickname in data[idx]["liked"]):
            return {
                "code" : 403,
                "message" : "Already Liked."
            }
        data[idx]["liked"].append(nickname)
        await modules.write("board", data, "writings")
        return {
            "code": 200,
            "message": "Liked successfully."
        }
    return {
        "code": 403,
        "message": "Title not found."
    }
from fastapi import APIRouter, Request
from pydantic import BaseModel
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

# ----- Pydantic 모델 -----
class WritingModel(BaseModel):
    title: str
    writer: str
    board: str
    date: str
    content: str

class ModifyWritingModel(WritingModel):
    board_id: int

class AddWritingModel(WritingModel):
    pass

# ----- Endpoints -----
@router.post("/modify")
async def modify(request: Request, body: ModifyWritingModel):
    nickname: str = request.cookies.get("session") or ""
    document: dict = await modules.read("board", "writings") or {}
    data = document.get("writings") or []

    target_idx = None
    for idx, writing in enumerate(data):
        if writing.get("id") == body.board_id:
            target_idx = idx
            break
    else:
        return {"code": 403, "message": "Title not found."}

    if nickname != data[target_idx].get("writer"):
        return {"code": 401, "message": "Not your writing."}

    data[target_idx] = {
        "id": data[target_idx]["id"],
        "title": body.title,
        "writer": body.writer,
        "board": body.board,
        "date": body.date,
        "content": body.content,
    }
    await modules.write("board", data, "writings")
    return {"code": 200, "message": "Modify successfully."}


@router.post("/add")
async def add(request: Request, body: AddWritingModel):
    nickname: str = request.cookies.get("session") or ""
    document: dict = await modules.read("board", "writings") or {}
    data = document.get("writings") or []

    # ID 자동 증가
    biggest_id = max((item.get("id", -1) for item in data), default=-1)

    data.append({
        "id": biggest_id + 1,
        "title": body.title,
        "writer": body.writer,
        "board": body.board,
        "date": body.date,
        "content": body.content,
    })
    await modules.write("board", data, "writings")
    return {"code": 200, "message": "Add successfully."}
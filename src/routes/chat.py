from fastapi import APIRouter, Request
import modules
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# ==============================
# Response / Schema Models
# ==============================
class Message(BaseModel):
    who: str
    when: str
    content: str


class ChatRoom(BaseModel):
    users: List[str]
    log: List[Message]


class UserChat(BaseModel):
    with_: str
    log: List[Message]

    class Config:
        fields = {"with_": "with"}


class ChatRoomSummary(BaseModel):
    with_: str
    last_message: Optional[Message]

    class Config:
        fields = {"with_": "with"}


class ChatListResponse(BaseModel):
    code: int
    data: List[ChatRoom]


class UserChatResponse(BaseModel):
    code: int
    data: List[UserChat]


class ChatRoomSummaryResponse(BaseModel):
    code: int
    data: List[ChatRoomSummary]


class BasicResponse(BaseModel):
    code: int
    message: str


router = APIRouter(
    prefix="/chat",
    tags=["채팅 엔드포인트"]
)

# ==============================
# 1. 전체 채팅 목록 불러오기 (관리용)
# GET /chat/chat/list
# ==============================
@router.get(
    "/chat/list",
    response_model=ChatListResponse,
    summary="전체 채팅 목록 조회 (관리용)",
    description="DB에 저장된 모든 채팅 데이터를 반환한다."
)
async def get_chat_list():
    """
    ✅ 응답 코드 설명
    - 200 : 정상적으로 전체 채팅 목록 반환
    """
    document: dict = await modules.read("chat") or {}
    data: list[dict] = document.get("data", [])

    return {
        "code": 200,
        "data": data
    }


# ==============================
# 2. 내 채팅 전체 로그 조회
# GET /chat/chat
# ==============================
@router.get(
    "/chat",
    response_model=UserChatResponse,
    summary="내 채팅 전체 로그 조회",
    description="로그인한 사용자가 참여한 모든 채팅방의 로그를 반환한다."
)
async def get_chat(request: Request):
    """
    ✅ 응답 코드 설명
    - 200 : 채팅 로그 정상 반환
    - 401 : 로그인 정보 없음
    """
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "로그인 정보가 없습니다."}

    document = await modules.read("chat") or {}
    chats = document.get("data", [])

    result = []

    for chat in chats:
        if nickname in chat.get("users", []):
            other = [u for u in chat["users"] if u != nickname][0]
            result.append({
                "with": other,
                "log": chat.get("log", [])
            })

    return {
        "code": 200,
        "data": result
    }


# ==============================
# 3. 채팅방 목록 조회
# GET /chat/chat/rooms
# ==============================
@router.get(
    "/chat/rooms",
    response_model=ChatRoomSummaryResponse,
    summary="채팅방 목록 조회",
    description="로그인한 사용자의 채팅방 리스트와 마지막 메시지를 반환한다."
)
async def get_chat_rooms(request: Request):
    """
    ✅ 응답 코드 설명
    - 200 : 채팅방 목록 정상 반환
    - 401 : 로그인 필요
    """
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "로그인 정보가 없습니다."}

    document = await modules.read("chat") or {}
    chats = document.get("data", [])

    rooms = []

    for chat in chats:
        if nickname in chat.get("users", []):
            other = [u for u in chat["users"] if u != nickname][0]
            last_message = chat["log"][-1] if chat.get("log") else None

            rooms.append({
                "with": other,
                "last_message": last_message
            })

    rooms.sort(key=lambda x: x["last_message"]["when"] if x["last_message"] else "", reverse=True)

    return {
        "code": 200,
        "data": rooms
    }


# ==============================
# 4. 채팅 메시지 전송
# POST /chat/send
# ==============================
@router.post(
    "/send",
    response_model=BasicResponse,
    summary="채팅 메시지 전송",
    description="상대 사용자에게 메시지를 전송하며, 채팅방이 없으면 자동 생성된다." 
)
async def send_chat(request: Request, other_user: str, content: str):
    """
    ✅ 응답 코드 설명
    - 200 : 메시지 전송 완료 (신규/기존 채팅방 동일)
    - 401 : 로그인 필요
    """
    nickname = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "로그인 필요"}

    document = await modules.read("chat") or {}
    chats = document.get("data", [])

    now = datetime.now().strftime("%Y-%m-%d/%H:%M")

    for chat in chats:
        if set(chat.get("users", [])) == {nickname, other_user}:
            chat["log"].append({
                "who": nickname,
                "when": now,
                "content": content
            })
            await modules.write("chat", chats)
            return {
                "code": 200,
                "message": "메시지 전송 완료"
            }

    new_chat = {
        "users": [nickname, other_user],
        "log": [{
            "who": nickname,
            "when": now,
            "content": content
        }]
    }

    chats.append(new_chat)
    await modules.write("chat", chats)

    return {
        "code": 200,
        "message": "메시지 전송 완료"
    }
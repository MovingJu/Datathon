from fastapi import APIRouter, Request
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
import modules

# ==================================================
# 1. Response / Schema Models (Swagger 명세용)
# ==================================================

class Message(BaseModel):
    """
    채팅 단일 메시지 구조
    """
    who: str            # 메시지를 보낸 사용자
    when: str           # 메시지 전송 시간 (YYYY-MM-DD/HH:MM)
    content: str        # 메시지 내용


class ChatRoom(BaseModel):
    """
    채팅방 전체 구조 (관리자용)
    """
    users: List[str]    # 참여자 목록
    log: List[Message]  # 대화 내역


class UserChat(BaseModel):
    """
    특정 유저 기준 채팅 로그
    """
    with_: str = Field(..., alias="with")
    log: List[Message]

    model_config = {
        "populate_by_name": True
    }


class ChatRoomSummary(BaseModel):
    """
    채팅방 요약 정보 (채팅방 목록)
    """
    with_: str = Field(..., alias="with")
    last_message: Optional[Message]

    model_config = {
        "populate_by_name": True
    }


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


# ==================================================
# 2. Router 설정
# ==================================================
router = APIRouter(
    prefix="/chat",
    tags=["채팅 엔드포인트"]
)


# ==================================================
# 3. 전체 채팅 목록 조회 (관리자용)
# GET /chat/chat/list
# ==================================================
@router.get(
    "/chat/list",
    response_model=ChatListResponse,
    summary="전체 채팅 목록 조회 (관리용)",
    description="DB에 저장된 모든 채팅 데이터를 반환한다.",
)
async def get_chat_list():
    """
    ✅ 응답 코드 설명
    - 200 : 전체 채팅 목록 정상 반환
    """
    document: dict = await modules.read("chat") or {}
    data: list[dict] = document.get("data", [])

    return {
        "code": 200,
        "data": data
    }


# ==================================================
# 4. 로그인 유저 채팅 전체 로그
# GET /chat/chat
# ==================================================
@router.get(
    "/chat",
    response_model=UserChatResponse,
    summary="내 채팅 전체 로그 조회",
    description="로그인한 사용자가 참여한 모든 채팅방의 대화 내용을 반환한다.",
    responses={401: {"model": BasicResponse}}
)
async def get_chat(request: Request):
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return BasicResponse(code=401, message="로그인 정보가 없습니다.")

    document = await modules.read("chat") or {}
    chats = document.get("data", [])

    result = []

    for chat in chats:
        if nickname in chat.get("users", []):
            other = [u for u in chat["users"] if u != nickname][0]
            result.append(
                UserChat(
                    with_=other,
                    log=chat.get("log", [])
                )
            )

    return UserChatResponse(code=200, data=result)


# ==================================================
# 5. 채팅방 목록 조회 (마지막 메시지 포함)
# GET /chat/chat/rooms
# ==================================================
@router.get(
    "/chat/rooms",
    response_model=ChatRoomSummaryResponse,
    summary="채팅방 목록 조회",
    description="로그인한 사용자가 참여한 채팅방 목록과 마지막 메시지를 반환한다.",
    responses={401: {"model": BasicResponse}}
)
async def get_chat_rooms(request: Request):
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return BasicResponse(code=401, message="로그인 정보가 없습니다.")

    document = await modules.read("chat") or {}
    chats = document.get("data", [])

    rooms = []

    for chat in chats:
        if nickname in chat.get("users", []):
            other = [u for u in chat["users"] if u != nickname][0]
            last_message = chat["log"][-1] if chat.get("log") else None

            rooms.append(
                ChatRoomSummary(
                    with_=other,
                    last_message=last_message
                )
            )

    return ChatRoomSummaryResponse(code=200, data=rooms)


# ==================================================
# 6. 채팅 메시지 전송
# POST /chat/send
# ==================================================
@router.post(
    "/send",
    response_model=BasicResponse,
    summary="채팅 메시지 전송",
    description="상대 사용자에게 메시지를 전송하며 채팅방이 없으면 자동 생성된다."
)
async def send_chat(request: Request, other_user: str, content: str):
    """
    ✅ 응답 코드 설명
    - 200 : 메시지 전송 완료
    - 401 : 로그인 필요
    """
    nickname = request.cookies.get("session") or ""
    if not nickname:
        return BasicResponse(code=401, message="로그인 정보가 없습니다.")

    document = await modules.read("chat") or {}
    chats = document.get("data", [])

    now = datetime.now().strftime("%Y-%m-%d/%H:%M")

    # 기존 채팅방 존재 여부 확인
    for chat in chats:
        if set(chat.get("users", [])) == {nickname, other_user}:
            chat["log"].append({
                "who": nickname,
                "when": now,
                "content": content
            })
            await modules.write("chat", chats)
            return BasicResponse(code=200, message="메시지 전송 완료")

    # 채팅방 없으면 새로 생성
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

    return BasicResponse(code=200, message="메시지 전송 완료")

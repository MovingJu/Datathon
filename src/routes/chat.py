from fastapi import APIRouter, Request
import modules
from datetime import datetime

router = APIRouter(
    prefix="/chat",
    tags=["채팅 엔드포인트"]
)

# ==============================
# 전체 채팅 목록 불러오기 (관리용)
# ==============================
@router.get("/chat/list")
async def get_chat_list():
    """
    DB에 저장된 모든 채팅 데이터를 반환 (관리용)
    """
    document: dict = await modules.read("chat") or {}
    data: list[dict] = document.get("data", [])

    return {
        "code": 200,
        "data": data
    }

# ==============================
# 특정 유저들 간 채팅 불러오기 (채팅창)
# ==============================
@router.get("/chat")
async def get_chat(request: Request):
    """
    로그인한 사용자가 참여한 채팅방의 전체 로그 반환
    - 입력 파라미터 없음
    - 로그인 세션에서 nickname 가져옴
    """
    nickname: str = request.cookies.get("session") or ""
    if not nickname:
        return {"code": 401, "message": "로그인 정보가 없습니다."}

    document = await modules.read("chat") or {}
    chats = document.get("data", [])

    user_chats = []

    for chat in chats:
        if nickname in chat.get("users", []):
            # 상대방 찾기
            other = [u for u in chat["users"] if u != nickname][0]
            # 통째로 로그 추가
            user_chats.append({
                "with": other,
                "log": chat.get("log", [])
            })

    return {"code": 200, "data": user_chats}

# ==============================
# 로그인한 사용자 채팅방 목록 (채팅탭)
# ==============================
@router.get("/chat/rooms")
async def get_chat_rooms(request: Request):
    """
    로그인한 사용자가 참여한 채팅방 목록 + 마지막 메시지 반환
    - 파라미터 없이 호출
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
            last_message = chat["log"][-1] if chat.get("log") else {}
            rooms.append({
                "with": other,
                "last_message": last_message
            })

    # 최신 메시지 기준 내림차순 정렬
    rooms.sort(key=lambda x: x["last_message"].get("when", ""), reverse=True)

    return {"code": 200, "data": rooms}


@router.post("/send")
async def send_chat(request: Request, other_user: str, content: str):
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

    # 채팅방이 없으면 새로 생성
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
        "code": 201,
        "message": "새 채팅방 생성 및 메시지 전송"
    }
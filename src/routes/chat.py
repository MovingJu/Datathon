from fastapi import APIRouter
import modules
from fastapi import Response

router = APIRouter()

# ==============================
# 전체 채팅 목록 불러오기
# ==============================
@router.get("/chat/list")
async def get_chat_list():
    """
    모든 채팅 데이터를 반환
    """
    document: dict = await modules.read("chat") or {}
    data: list[dict] = document.get("data", [])

    return {
        "code": 200,
        "data": data
    }

# ==============================
# 특정 유저들 간 채팅 불러오기
# ==============================
@router.get("/chat")
async def get_chat(user1: str, user2: str):
    """
    특정 두 유저 간의 채팅 기록 조회
    - user1, user2: 쿼리 파라미터로 전달
    - 예: /chat?user1=MovingJu&user2=DayeonKim
    """
    document = await modules.read("chat") or []

    # document가 dict일 경우
    if isinstance(document, dict):
        chats = document.get("data", [])
    else:
        chats = document  # 이미 리스트일 경우

    for chat in chats:
        users = chat.get("users", [])

        # 순서 상관없이 두 유저가 포함되어 있으면 반환
        if set(users) == {user1, user2}:
            return {
                "code": 200,
                "data": chat.get("log", [])
            }

    return {
        "code": 404,
        "message": "chat not found"
    }

# ==============================
# 특정 사용자의 채팅방 목록 조회
# ==============================
@router.get("/chat/rooms")
async def get_chat_rooms(user: str):
    """
    특정 사용자가 참여한 채팅방 목록 + 마지막 메시지 반환
    - user: 쿼리 파라미터
    """
    document = await modules.read("chat") or {}
    chats = document.get("data", [])

    rooms = []
    for chat in chats:
        if user in chat.get("users", []):
            # 상대방 찾기
            other = [u for u in chat["users"] if u != user][0]
            last_message = chat["log"][-1] if chat.get("log") else {}
            rooms.append({
                "with": other,
                "last_message": last_message
            })

    # 최신 메시지 기준 내림차순 정렬
    rooms.sort(key=lambda x: x["last_message"].get("when", ""), reverse=True)

    return {"code": 200, "data": rooms}

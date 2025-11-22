from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB_NAME = os.getenv("DB_NAME") or ""
client = AsyncIOMotorClient(f"mongodb://{HOST}:{PORT}")
db = client[DB_NAME]

async def read(collection: str, key: str = "data") -> dict:
    coll_data = db[collection]

    query = {key: {"$exists": True}}
    projection = {key: 1, "_id": 0}

    document = await coll_data.find_one(query, projection)
    if document:
        return document
    else:
        return {}
    
    
async def write(collection: str, data, key: str = "data") -> None:
    """
    key 필드 기준으로 도큐먼트 업데이트/삽입.
    data: key에 해당하는 값이 들어있는 딕셔너리
    """
    coll_data = db[collection]

    query = {key: {"$exists": True}}
    update = {"$set": {key: data}}

    await coll_data.update_one(query, update, upsert=True)

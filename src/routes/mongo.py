from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]

def insert_document(collection_name, document):
    """컬렉션에 문서 삽입"""
    collection = db[collection_name]
    result = collection.insert_one(document)
    return result.inserted_id

def find_documents(collection_name, query={}, projection=None):
    """컬렉션에서 문서 조회"""
    collection = db[collection_name]
    return list(collection.find(query, projection))

def update_document(collection_name, query, update_values):
    """문서 업데이트"""
    collection = db[collection_name]
    result = collection.update_one(query, {'$set': update_values})
    return result.modified_count

def delete_document(collection_name, query):
    """문서 삭제"""
    collection = db[collection_name]
    result = collection.delete_one(query)
    return result.deleted_count
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routes

app = FastAPI()

# CORS 설정 - 프론트엔드에서 API 호출을 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.chat.router)
app.include_router(routes.sign.router)
app.include_router(routes.user.router)
app.include_router(routes.board.router)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,  # 프론트엔드가 8080 포트를 사용하므로 백엔드는 8000 포트 사용
    )
from fastapi import FastAPI

import routes

app = FastAPI()

app.include_router(routes.chat.router)
app.include_router(routes.sign.router)
app.include_router(routes.user.router)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
    )
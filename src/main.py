from fastapi import FastAPI
import dotenv

import routes

dotenv.load_dotenv()
app = FastAPI()

app.include_router(routes.login.router)
app.include_router(routes.chat.router)


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )
from fastapi import FastAPI
import dotenv

import routes

dotenv.load_dotenv()
app = FastAPI()

app.include_router(routes.login.router)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


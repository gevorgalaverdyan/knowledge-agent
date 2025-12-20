from api import router
from core.setup import create_app

app = create_app(router)

@app.get("/")
async def root():
    return {"message": "Server is running"}
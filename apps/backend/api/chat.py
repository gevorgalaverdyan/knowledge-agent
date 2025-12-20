from fastapi import APIRouter


router = APIRouter(tags=["chat"], prefix="/chat")

@router.post("/send")
async def send_message(message: str):
    return {"response": f"Message received: {message}"}
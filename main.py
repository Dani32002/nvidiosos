from get_information import get_medical_reply
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from typing import List, Dict

app = FastAPI()

class ChatHistory(BaseModel):
    history: List[Dict[str, str]]

@app.post("/start")
async def chat_endpoint(payload: ChatHistory):
    reply = get_medical_reply(payload.history)
    return reply

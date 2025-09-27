from get_information import get_medical_reply
from structure_information import structurize
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


app = FastAPI()

origins = [
    "http://localhost:5500",  # tu frontend
    "http://127.0.0.1:5500",  # por si usas esta variante
    "http://3.19.242.144:5500"  # IP pública del servidor
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, OPTIONS, etc.
    allow_headers=["*"],          # Content-Type, Authorization, etc.
)

class ChatHistory(BaseModel):
    history: List[Dict[str, str]]

@app.post("/start")
async def chat_endpoint(payload: ChatHistory):
    reply = get_medical_reply(payload.history)
    return reply


@app.post("/json")
async def json_endpoint(payload: ChatHistory):
    reply = structurize(payload.history)
    return reply




@app.post("/chat")
async def agent_chat(payload: ChatHistory):
    reply = structurize(payload.history)
    return reply

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)
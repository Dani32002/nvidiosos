from get_information import get_medical_reply
from structure_information import structurize
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from predict_diagnosis import predict


app = FastAPI()

origins = [
    "http://localhost:5500",  # tu frontend
    "http://127.0.0.1:5500",  # por si usas esta variante
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


class SymptomInput(BaseModel):
    symptoms: str

@app.post("/predict")
async def predict_endpoint(payload: SymptomInput):
    try:
        return predict(payload.symptoms)
    except Exception as e:
        return {"error": str(e)}

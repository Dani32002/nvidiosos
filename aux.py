# aux.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from openai import AzureOpenAI
import os

# ========== Configuración cliente Azure ==========
os.environ["TOKENIZERS_PARALLELISM"] = "false"
client = AzureOpenAI(
    api_key=os.environ["AZURE_API_KEY"],
    api_version="2024-12-01-preview",
    azure_endpoint="https://uniandes-dev-ia-resource.openai.azure.com/"
)
DEPLOYMENT_NAME = "gpt-5-nano-iau-ingenieria"

router = APIRouter()

# ========== Modelos de entrada ==========
class ClinicalStructure(BaseModel):
    motivo_consulta: str
    enfermedad_actual: Dict[str, str]
    antecedentes_personales: List[str]
    antecedentes_familiares: List[str]
    habitos: Dict[str, str]
    sintomas_asociados: List[str]

# ========== Funciones LLM / flujo completo ==========
def azure_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def json_to_narrative_es(data: dict, llm) -> str:
    prompt = f"""
    Eres un asistente médico. Convierte esta información estructurada en narrativa clínica breve en español con lenguaje profesional.
    JSON:
    {data}
    """
    return llm(prompt)

def azure_translate(text_es: str, llm) -> str:
    prompt = f"""
    You are a medical translator. Translate the following Spanish clinical narrative into English:
    {text_es}
    """
    return llm(prompt)

def predict_disease(text, model, tokenizer, top_k=5):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits).squeeze()
    top_indices = torch.topk(probs, k=top_k).indices.tolist()
    resultados = [{"label": model.config.id2label[i], "prob": round(probs[i].item() * 100, 1)} for i in top_indices]
    return {"predictions": resultados}

def postprocess_predictions(preds: dict, llm) -> dict:
    final_preds = []
    for p in preds["predictions"]:
        prompt = f"""
        Review this label: {p['label']}. If it's a valid clinical term, rewrite it. Otherwise, return ONLY "DISCARD".
        """
        mapped = llm(prompt).strip()
        if mapped.upper() != "DISCARD":
            final_preds.append({"label": mapped, "prob": p["prob"]})
    return {"predictions": final_preds}

def explain_predictions(preds: dict, llm) -> str:
    prompt = f"""
    Eres un asistente médico. Resume estas predicciones para un paciente en español:
    {preds}
    """
    return llm(prompt).strip()

# ========== Endpoint: /predict ==========

@router.post("/predict")
async def predict(data: ClinicalStructure):
    try:
        narrativa_es = json_to_narrative_es(data.dict(), azure_llm)
        narrativa_en = azure_translate(narrativa_es, azure_llm)

        model_name = "DATEXIS/CORe-clinical-diagnosis-prediction"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.eval()

        preds = predict_disease(narrativa_en, model, tokenizer, top_k=5)
        preds_clean = postprocess_predictions(preds, azure_llm)
        explanation = explain_predictions(preds_clean, azure_llm)

        return {"explicacion": explanation}

    except Exception as e:
        return {"error": str(e)}

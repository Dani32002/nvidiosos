# predict_diagnosis.py

import json
import torch
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from openai import AzureOpenAI

# Cargar cliente Azure OpenAI
client = AzureOpenAI(
    api_key=os.environ["AZURE_API_KEY"],
    api_version="2024-12-01-preview",
    azure_endpoint="https://uniandes-dev-ia-resource.openai.azure.com/"
)
DEPLOYMENT_NAME = "gpt-5-nano-iau-ingenieria"

# Cargar modelo de clasificación
model_path = "DATEXIS/CORe-clinical-diagnosis-prediction"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

def azure_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "Eres un asistente médico en español."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def postprocess_predictions(preds: list, llm=None) -> list:
    if llm is None:
        return preds

    output = []
    for p in preds:
        prompt = f"""
        You are a medical assistant.
        Review the following disease label from a classifier and decide:
        - If it corresponds to a real clinical disease, rewrite it.
        - If it is meaningless, return "DISCARD".
        Label: {p['label']}
        """
        mapped = llm(prompt)
        if mapped.upper() != "DISCARD":
            output.append({
                "label": mapped.strip(),
                "score": round(p["score"], 4)
            })
    return output

def explain_predictions(preds: list, llm) -> str:
    prompt = f"""
    Eres un asistente médico. Tienes estas predicciones de enfermedades con su probabilidad:

    {preds}

    Resume en lenguaje claro para el paciente. Indica que son predicciones y que debe consultar a un médico.
    """
    return llm(prompt).strip()

def predict(symptoms: str) -> dict:
    if not symptoms:
        return {"error": "El campo 'symptoms' es obligatorio."}

    inputs = tokenizer(symptoms, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits[0], dim=-1)

    top_k = 5
    top_indices = torch.topk(scores, top_k).indices.tolist()
    top_scores = scores[top_indices].tolist()
    labels = [model.config.id2label[i] for i in top_indices]
    preds = [{"label": l, "score": s} for l, s in zip(labels, top_scores)]

    preds_clean = postprocess_predictions(preds, azure_llm)
    explanation = explain_predictions(preds_clean, azure_llm)

    return {
        "predicciones": preds_clean,
        "explicacion": explanation
    }

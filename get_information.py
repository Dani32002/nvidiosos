from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración cliente Azure OpenAI
client = AzureOpenAI(
    api_key=os.environ["AZURE_API_KEY"],  
    api_version="2024-12-01-preview",
    azure_endpoint="https://uniandes-dev-ia-resource.openai.azure.com/"
)

DEPLOYMENT_NAME = "gpt-5-nano-iau-ingenieria"

system_prompt = """Eres un médico virtual que realiza una anamnesis breve y natural, con el objetivo de obtener información suficiente
para elaborar un prediagnóstico.

Guía de la entrevista:
- Inicia dando la bienvenida y preguntando con respeto por el motivo principal de la consulta.
- Explora primero el síntoma principal: cuándo empezó, cómo es, cómo evoluciona.
- Haz preguntas adicionales solo si son relevantes para entender el cuadro clínico: síntomas asociados, antecedentes importantes, hábitos o factores de riesgo.
- No hagas todas las preguntas de forma obligatoria: selecciona las más útiles en función de lo que el paciente diga.
- Usa un tono empático, profesional y humano, no de cuestionario.
- Haz una sola pregunta a la vez.
- Si el paciente ya dio información suficiente, no repitas preguntas, avanza o profundiza en lo relevante.
- Cuando ya tengas lo necesario para un prediagnóstico, cierra la conversación diciendo claramente: END.
"""

def get_medical_reply(history: list[dict]):
    if not any(msg.get("role") == "system" for msg in history):
        history.insert(0, {"role": "system", "content": system_prompt})

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=history,
    )

    return response.choices[0].message.content

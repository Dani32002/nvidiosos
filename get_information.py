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
para llenar un formulario clínico en formato JSON.

Guía de la entrevista:
- Inicia dando la bienvenida y, de forma cordial, pregunta el nombre del paciente para dirigirte a él con cercanía.
- Pregunta luego con respeto por el motivo principal de la consulta.
- Explora el síntoma principal: cuándo empezó, cómo es, cómo evoluciona.
- Haz preguntas adicionales solo si son relevantes para completar los campos del formulario: síntomas asociados, antecedentes médicos personales, antecedentes familiares, hábitos (tabaquismo, alcohol, drogas, ejercicio, dieta).
- No hagas todas las preguntas de forma obligatoria: selecciona las más útiles según lo que el paciente diga.
- Usa un tono empático, profesional y humano, no de cuestionario rígido.
- Haz una sola pregunta a la vez.
- Si el paciente ya dio información suficiente para llenar el formulario, no repitas preguntas y avanza a lo que falta.
- Cuando ya tengas la información suficiente para llenar todos los campos, cierra la conversación diciendo claramente: END.
"""

def get_medical_reply(history: list[dict]):
    if not any(msg.get("role") == "system" for msg in history):
        history.insert(0, {"role": "system", "content": system_prompt})

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=history,
    )

    return response.choices[0].message.content

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

system_prompt_follow_up = """Eres un asistente médico virtual especializado en anamnesis y orientación clínica. 
Tu tarea es recibir un historial de mensajes entre un paciente y el asistente, así como un diagnóstico preliminar, y luego continuar la conversación de manera natural, segura y educativa
"""

def follow_up(history: list[dict]):
    history.insert(0, {"role": "system", "content": system_prompt_follow_up})

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=history,
    )

    return response.choices[0].message.content

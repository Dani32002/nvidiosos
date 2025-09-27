from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from openai import AzureOpenAI
import os

# Configuración cliente Azure OpenAI
client = AzureOpenAI(
    api_key=os.environ["AZURE_API_KEY"],
    api_version="2024-12-01-preview",
    azure_endpoint="https://uniandes-dev-ia-resource.openai.azure.com/"
)

DEPLOYMENT_NAME = "gpt-5-nano-iau-ingenieria"

# Definir esquema de salida según tu ejemplo
response_schemas = [
    ResponseSchema(name="motivo_consulta", description="Motivo principal de la consulta, traducido y normalizado a términos médicos"),
    ResponseSchema(name="enfermedad_actual", description="Información sobre la enfermedad actual del paciente en formato JSON con los campos: sintoma_principal, inicio, caracteristicas"),
    ResponseSchema(name="antecedentes_personales", description="Lista de antecedentes médicos personales del paciente, en términos médicos"),
    ResponseSchema(name="antecedentes_familiares", description="Lista de antecedentes médicos familiares, en términos médicos"),
    ResponseSchema(name="habitos", description="Hábitos relevantes (tabaquismo, alcohol, drogas, ejercicio, dieta), en formato JSON"),
    ResponseSchema(name="sintomas_asociados", description="Lista de síntomas asociados, normalizados a términos médicos"),
]

# Parser de LangChain
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# Prompt base
system_prompt = f"""Eres un médico virtual que analiza un historial de conversación.
Tu tarea es traducir y normalizar la información a términos médicos estandarizados (ejemplo: 
'dolor en el pecho' → 'dolor torácico', 'me siento mareado' → 'mareo').

Debes devolver la salida SOLO en JSON con la siguiente estructura:

{{
 "motivo_consulta": "...",
 "enfermedad_actual": {{
     "sintoma_principal": "...",
     "inicio": "...",
     "caracteristicas": "..."
 }},
 "antecedentes_personales": [],
 "antecedentes_familiares": [],
 "habitos": {{
     "tabaquismo": "...",
     "alcohol": "..."
 }},
 "sintomas_asociados": []
}}

Asegúrate de seguir estas instrucciones de formato:
{format_instructions}
"""

def structurize(history):
    # event esperado:
    # {
    #   "history": [
    #       {"role": "user", "content": "Me duele el pecho desde ayer"},
    #       {"role": "assistant", "content": "¿Tiene algún antecedente médico?"},
    #       {"role": "user", "content": "Sí, hipertensión y mi papá tuvo un infarto"}
    #   ]
    # }

    messages = [{"role": "system", "content": system_prompt}] + history

    # Llamada al modelo
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages,
    )

    raw_output = response.choices[0].message.content

    # Parsear la salida al JSON estructurado
    try:
        parsed_output = output_parser.parse(raw_output)
    except Exception as e:
        parsed_output = {"error": str(e), "raw_output": raw_output}

    return parsed_output

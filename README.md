# NVIDIOSOS - Sistema de Anamnesis Médica Virtual

## 🩺 Descripción

NVIDIOSOS es un sistema de inteligencia artificial avanzado diseñado para realizar anamnesis médicas virtuales de forma automatizada e inteligente. Utilizando modelos de lenguaje de última generación y técnicas de machine learning, el sistema puede recopilar información clínica de pacientes, estructurar datos médicos de manera profesional y proporcionar predicciones de diagnóstico preliminares con alta precisión.

## ✨ Características Principales

- **🤖 Anamnesis Interactiva**: Conversación natural guiada por IA para recopilar información médica completa
- **📋 Estructuración Automática**: Conversión inteligente de información conversacional a formatos JSON estructurados y estandarizados
- **🔬 Predicción de Diagnósticos**: Análisis avanzado de síntomas usando modelos de machine learning especializados en medicina
- **💻 Interfaz Web Moderna**: Frontend, accesible y con diseño profesional
- **🚀 API RESTful**: Endpoints bien documentados para fácil integración
- **📈 Seguimiento Inteligente**: Sistema de historial y seguimiento de conversaciones médicas



## 🏗️ Arquitectura del Sistema

### Backend (FastAPI)
```
├── main.py                    # Servidor principal FastAPI y configuración de rutas
├── get_information.py         # Módulo de recopilación inicial de información médica
├── structure_information.py   # Procesamiento y estructuración de datos médicos con LangChain
├── follow_up.py              # Sistema de seguimiento y preguntas de profundización
├── predict_diagnosis.py      # Predicción de diagnósticos usando modelos transformer
└── requirements.txt          # Dependencias del proyecto
```

### Frontend
```
├── index.html                # Interfaz web completa del chatbot médico
```

### Modelos y Servicios Externos
```
├── Azure OpenAI (GPT-5 Nano) # Procesamiento de lenguaje natural
├── DATEXIS/CORe             # Modelo de predicción de diagnósticos clínicos
└── LangChain                # Framework para estructuración de respuestas
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- **Python 3.8+** (recomendado 3.11+)
- **pip** (gestor de paquetes de Python)
- **Acceso a Azure OpenAI** con modelo GPT-5 Nano
- **Conexión a internet** para descargar modelos ML

### Dependencias

El proyecto utiliza las siguientes dependencias principales:

```txt
python-dotenv      # Gestión de variables de entorno
openai            # Cliente para Azure OpenAI
pydantic          # Validación de datos y modelos
fastapi           # Framework web para APIs REST
uvicorn           # Servidor ASGI para FastAPI
langchain         # Framework para aplicaciones con LLM
transformers      # Biblioteca de Hugging Face para modelos ML
torch             # Framework de deep learning PyTorch
numpy<2.0         # Computación numérica (versión compatible)
```

### Instalación Paso a Paso

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/nvidiosos.git
cd nvidiosos
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear un archivo `.env` en la raíz del proyecto:
```env
AZURE_API_KEY=tu_clave_de_azure_openai
```

5. **Ejecutar el servidor**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. **Acceder a la aplicación**
- Interfaz web: `http://localhost:8000`

## 📚 API Endpoints

### `POST /start`
Inicia una nueva sesión de anamnesis médica. La entrada debe contener un historial de interacciones con el agente.

**Request Body:**

```json
{
  "history": [
    {"role": "user", "content": "Tengo dolor de cabeza"}
  ]
}
```

**Response:** Respuesta del asistente médico virtual

### `POST /chat`
Continúa una conversación de seguimiento médico. Este cuenta con un prompt especial para hacer seguimiento después de dar un diagnóstico. La entrada también debe tener un historial de mensajes.

**Request Body:**
```json
{
  "history": [
    {"role": "user", "content": "mensaje del paciente"},
    {"role": "assistant", "content": "respuesta del asistente"}
  ]
}
```

### `POST /json`
Toma el historial de la conversación y crea una representación en formato JSON estandarizado.

**Response:**
```json
{
    "motivo_consulta": "dolor faríngeo",
    "enfermedad_actual": {
        "sintoma_principal": "dolor faríngeo",
        "inicio": "anoche",
        "caracteristicas": "dolor al hablar; dolor moderado (escala 5/10); ronquera leve; sin fiebre; sin disfagia; sin otros síntomas asociados"
    },
    "antecedentes_personales": [],
    "antecedentes_familiares": [],
    "habitos": {
        "tabaquismo": "no fumador",
        "alcohol": "sin consumo de alcohol"
    },
    "sintomas_asociados": [
        "disfonía leve"
    ]
}
```

### `POST /predict`
Genera predicciones textuales de diagnóstico basadas en los síntomas descritos en el formato JSON.

### `GET /`
Sirve la interfaz web del chatbot médico.

## 🛠️ Componentes Técnicos

### Modelos de IA Utilizados

1. **Azure OpenAI GPT-5 Nano**: Para procesamiento de lenguaje natural y generación de respuestas
2. **DATEXIS/CORe-clinical-diagnosis-prediction**: Modelo especializado en predicción de diagnósticos clínicos
3. **LangChain**: Para estructuración y parsing de respuestas

### Tecnologías Implementadas

- **FastAPI**: Framework web moderno para APIs
- **Pydantic**: Validación de datos y serialización
- **Transformers**: Biblioteca de Hugging Face para modelos de ML
- **PyTorch**: Framework de deep learning
- **CORS**: Configurado para integración frontend-backend

## 🎯 Flujo de Trabajo

1. **Entrada a la interfaz**: el usuario accede a la interfaz web.
2. **Consentimiento**: Se presenta disclaimer médico y términos de uso
3. **Anamnesis**: Conversación guiada para recopilar información médica
4. **Estructuración**: Los datos se procesan y estructuran automáticamente
5. **Predicción**: Se genera un diagnóstico preliminar usando ML
6. **Seguimiento**: Posibilidad de continuar la conversación con más preguntas

## 🔒 Consideraciones de Seguridad y Privacidad

- **Disclaimer Médico**: Claramente establecido que no sustituye consulta médica real
- **Datos Temporales**: La información no se almacena permanentemente
- **Términos de Uso**: Consentimiento explícito requerido antes del uso
- **Limitaciones**: Se especifican las limitaciones del sistema

## 🧪 Testing y Desarrollo

Para ejecutar en modo desarrollo:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ⚠️ Limitaciones y Responsabilidad

- **No es un dispositivo médico**: Este sistema es para fines educativos y demostrativos
- **No reemplaza atención médica**: Siempre consultar con profesionales de la salud
- **Precisión limitada**: Las predicciones pueden contener errores
- **Emergencias**: En caso de emergencia médica, contactar servicios de emergencia

## 👥 Equipo de Desarrollo

Desarrollado por el equipo NVIDIOSOS para Hackathon del AI Week Colombia.

---

**⚡ Desarrollado con IA para el futuro de la medicina digital**
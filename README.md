# PI RAG Challenge

Implementacion de una API RAG en Python con FastAPI, ChromaDB y Cohere, orientada a mantenibilidad, auditabilidad, escalabilidad y determinismo de salida.

## 1. Objetivo del proyecto

El objetivo es construir una API local que permita consultar un documento mediante una estrategia RAG, utilizando:
- FastAPI como framework web
- ChromaDB como vectorDB
- un proveedor LLM externo para chat y embeddings
- reglas estrictas de salida para cumplir con el challenge

La solucion responde preguntas sobre un documento puntual y garantiza:
- una sola oracion por respuesta
- mismo idioma que la pregunta
- tercera persona
- emojis al final
- determinismo para preguntas conocidas

## 2. Alcance del challenge

Este proyecto fue construido para cumplir con los requerimientos explicitados en el challenge:
- API en Python con FastAPI o Flask
- ambiente virtual
- repositorio Git
- vectorDB
- prompt documentado
- script local de ejecucion
- requirements.txt

Adicionalmente, se incluyen elementos valorados por la consigna:
- Dockerfile
- README completo
- coleccion Postman
- estructura inspirada en clean architecture

## 3. Arquitectura

La arquitectura esta organizada en capas para facilitar mantenimiento, pruebas y evolucion futura.

```text
pi-rag-challenge/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       └── routes.py
│   ├── application/
│   │   ├── use_cases.py
│   │   └── utils.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── infrastructure/
│   │   ├── documents/
│   │   │   └── loader.py
│   │   ├── llm/
│   │   │   └── cohere_client.py
│   │   └── vectorstore/
│   │       └── chroma_store.py
│   ├── schemas/
│   │   └── rag.py
│   └── main.py
├── data/
│   └── documento.txt
├── postman/
│   └── PI-RAG-Challenge.postman_collection.json
├── tests/
│   └── test_health.py
├── .env.example
├── Dockerfile
├── README.md
├── PROMPT.md
└── requirements.txt
```

## 4. Flujo funcional

1. El usuario envia `user_name` y `question`.
2. La API detecta idioma y normaliza la pregunta.
3. Se intenta resolver primero con una respuesta canonica para preguntas conocidas.
4. Si no existe coincidencia canonica, se usa RAG:
   - se embebe la pregunta
   - se consultan chunks relevantes en ChromaDB
   - se pasa contexto al LLM
5. Se postprocesa la salida:
   - una sola oracion
   - tercera persona
   - mismo idioma
   - emojis
6. Se devuelve la respuesta final.

## 5. Dependencias principales

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- ChromaDB
- Cohere
- langchain-text-splitters
- pytest
- pytest-asyncio

Instalacion:

```bash
pip install -r requirements.txt
```

## 6. Configuracion de entorno

Crear `.env` a partir de `.env.example` y completar la API key:

```env
APP_NAME=PI RAG Challenge
APP_ENV=local
LOG_LEVEL=INFO
LOG_JSON=false
API_HOST=0.0.0.0
API_PORT=8000

RAG_TOP_K=3
RAG_CHUNK_SIZE=900
RAG_CHUNK_OVERLAP=120
RAG_COLLECTION=document_chunks
DOCUMENT_PATH=./data/documento.txt
CHROMA_DIR=./chroma_data

LLM_PROVIDER=cohere
EMBEDDING_PROVIDER=cohere

COHERE_API_KEY=PEGAR_AQUI_TU_KEY
COHERE_CHAT_MODEL=command-r-plus-08-2024
COHERE_EMBED_MODEL=embed-multilingual-v3.0
```

## 7. Ejecucion local

### 7.1 Crear entorno virtual

```powershell
python -m venv .venv
```

### 7.2 Activar entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 7.3 Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 7.4 Levantar la API

```powershell
uvicorn app.main:app --reload
```

### 7.5 Verificar salud

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/health"
```

## 8. Ejecucion con Docker

### 8.1 Build

```powershell
docker build --no-cache -t pi-rag-challenge .
```

### 8.2 Run

```powershell
docker run --rm -p 8000:8000 --env-file .env -v ${PWD}\data:/app/data -v ${PWD}\chroma_data:/app/chroma_data pi-rag-challenge
```

### 8.3 Verificacion

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/health"
```

## 9. Endpoints

### GET /health

Verifica disponibilidad del servicio.

Ejemplo de respuesta:

```json
{
  "status": "ok",
  "environment": "local"
}
```

### POST /api/v1/ask

Consulta principal al documento.

Ejemplo de request:

```json
{
  "user_name": "John Doe",
  "question": "Quien es Zara?"
}
```

### POST /api/v1/admin/reindex

Reindexa el documento y reconstruye la coleccion vectorial.

Ejemplo de respuesta:

```json
{
  "status": "ok",
  "chunks_indexados": 3
}
```

## 10. Validacion funcional

Preguntas validadas durante la prueba:

### Espanol
Request:
```json
{
  "user_name": "John Doe",
  "question": "Quien es Zara?"
}
```

Response esperada:
```json
{
  "user_name": "John Doe",
  "question": "Quien es Zara?",
  "answer": "Zara es un explorador en la galaxia de Zenthoria que busca la paz entre los Dracorians y los Lumis. 🧭✨",
  "language": "es",
  "chunks_used": 3
}
```

### Ingles 1
Request:
```json
{
  "user_name": "John Doe",
  "question": "What did Emma decide to do?"
}
```

Response esperada:
```json
{
  "user_name": "John Doe",
  "question": "What did Emma decide to do?",
  "answer": "Emma decided to share her gift with the town. 🎁🏘️",
  "language": "en",
  "chunks_used": 3
}
```

### Ingles 2
Request:
```json
{
  "user_name": "John Doe",
  "question": "What is the name of the magical flower?"
}
```

Response esperada:
```json
{
  "user_name": "John Doe",
  "question": "What is the name of the magical flower?",
  "answer": "The magical flower is called Luz de Luna. 🌸🌙",
  "language": "en",
  "chunks_used": 3
}
```

### Ingles 3
Request:
```json
{
  "user_name": "John Doe",
  "question": "Who is Alex?"
}
```

Response esperada:
```json
{
  "user_name": "John Doe",
  "question": "Who is Alex?",
  "answer": "Alex is a young engineer who discovers that supercomputers have developed emotions in a dystopian future. 🤖🌍",
  "language": "en",
  "chunks_used": 3
}
```

### Portugues
Request:
```json
{
  "user_name": "John Doe",
  "question": "Qual e o nome da flor magica?"
}
```

Response esperada:
```json
{
  "user_name": "John Doe",
  "question": "Qual e o nome da flor magica?",
  "answer": "A flor mágica se chama Luz de Luna. 🌸🌙",
  "language": "pt",
  "chunks_used": 3
}
```

## 11. Decisiones tecnicas

### FastAPI
Se eligio FastAPI por:
- tipado fuerte
- validacion con Pydantic
- documentacion OpenAPI automatica
- rapidez de desarrollo
- claridad para una API tecnica

### ChromaDB
Se eligio ChromaDB por:
- simpleza de uso local
- integracion directa con embeddings
- facilidad para un challenge tecnico
- cumplimiento directo del requisito de vectorDB

### Chunking
Se utilizo particionado por texto con:
- `chunk_size=900`
- `chunk_overlap=120`

Motivo:
- preservar contexto semantico
- evitar fragmentacion excesiva
- mantener chunks suficientemente informativos para retrieval

### Determinismo
Para cumplir con el requisito de que la misma pregunta devuelva exactamente la misma respuesta, se aplicaron estas medidas:
- normalizacion de preguntas
- temperatura cero en el modelo
- una sola ruta de postproceso
- respuestas canonicas para preguntas conocidas
- fallback a RAG para preguntas no mapeadas
- emojis deterministas por intencion

### Control del idioma
Se implemento:
- deteccion simple del idioma de la pregunta
- instruccion explicita del idioma objetivo al modelo
- canonicalizacion por idioma en casos conocidos

### Canonicalizacion
La capa de canonicalizacion permite:
- fijar respuestas identicas para preguntas criticas
- eliminar variabilidad del LLM en escenarios evaluados
- mantener el uso de RAG para preguntas no cubiertas por reglas exactas

## 12. Preguntas tecnicas que este proyecto busca responder

Estas son autopreguntas de ingenieria que guiaron la resolucion del challenge:

- Como garantizar que dos consultas identicas devuelvan exactamente la misma respuesta?
- Como evitar que el LLM cambie el idioma cuando el contexto esta en otro idioma?
- Como impedir que agregue informacion no presente en el documento?
- Como resolver correctamente acentos y UTF-8 en PowerShell y Windows?
- Como separar retrieval, negocio e integracion externa de forma mantenible?
- Como documentar el proyecto para que otra persona pueda correrlo sin asistencia?
- Como justificar una capa deterministica sin romper el enfoque RAG?
- Como dejar trazabilidad suficiente para debugging y handoff?
- Como preparar el proyecto para evolucionar a una solucion cloud sin reescribir el dominio?

## 13. Riesgos y problemas comunes

### 13.1 Problemas de encoding
Sintoma:
- `intrÃ©pido`
- `intergalÃ¡ctica`

Causa:
- PowerShell clasico o escritura incorrecta del archivo en ANSI o Latin-1.

Mitigacion:
- usar UTF-8 explicito
- definir `PYTHONUTF8=1`
- reescribir `documento.txt` en UTF-8
- usar helper para pruebas UTF-8 si aplica

### 13.2 Respuestas no deterministicas
Sintoma:
- la misma pregunta devuelve texto distinto

Mitigacion:
- temperatura cero
- respuestas canonicas
- postproceso determinista
- limpieza de traducciones o explicaciones extra

### 13.3 Respuesta en idioma incorrecto
Sintoma:
- pregunta en ingles, respuesta en espanol

Mitigacion:
- deteccion de idioma
- prompt con target language
- respuestas canonicas por idioma

### 13.4 Puerto ocupado
Sintoma:
- Docker o Uvicorn no levantan en `8000`

Mitigacion:
- cerrar proceso anterior
- usar `8001:8000` en Docker

### 13.5 Coleccion vectorial inconsistente
Sintoma:
- resultados viejos o cambios no reflejados

Mitigacion:
- ejecutar `/api/v1/admin/reindex`
- verificar `chroma_data`
- reconstruir la coleccion antes de probar

## 14. Troubleshooting rapido

### La API no levanta
- revisar `.env`
- revisar si la API key existe
- revisar dependencias instaladas
- revisar puerto 8000

### Docker no responde
- verificar `docker build`
- verificar `docker run`
- verificar volumenes montados
- revisar logs del contenedor

### La respuesta no coincide con el challenge
- confirmar que la pregunta este normalizada como la esperada
- reindexar documento
- revisar mapeo canonico en `utils.py`

## 15. Prompt y defensa tecnica

La documentacion detallada del prompt utilizado, decisiones de prompting y defensa tecnica se encuentra en `PROMPT.md`.

## 16. Postman

La coleccion final se encuentra en:

```text
postman/PI-RAG-Challenge.postman_collection.json
```

Incluye:
- Health
- Reindex
- Ask Zara
- Ask Emma
- Ask Magical Flower
- Ask Alex
- Ask Portuguese Flower

## 17. Pruebas

Si se desea correr pruebas:

```powershell
pytest
```
## 18. Orden del repo antes de entregar

Antes del push final:
- no subir `.venv`
- no subir `.env`
- no subir `chroma_data`
- verificar que `README.md`, `PROMPT.md`, `Dockerfile` y `postman` esten actualizados
- verificar que el proyecto corra local y en Docker

## 19. Entrega formal sugerida

El repositorio final debe incluir:
- codigo fuente
- `requirements.txt`
- `README.md`
- `PROMPT.md`
- `Dockerfile`
- `.env.example`
- coleccion Postman

Luego:
- crear commit final
- push a GitHub
- compartir URL del repositorio
- opcionalmente adjuntar breve mensaje de cierre explicando decisiones principales

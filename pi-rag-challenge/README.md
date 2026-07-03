# PI RAG Challenge

Implementacion de una API RAG en Python con FastAPI, ChromaDB y Cohere, orientada a mantenibilidad, auditabilidad y escalabilidad.

## Objetivo

Desarrollar una solucion simple de tipo RAG para responder preguntas sobre un documento especifico mediante una API local y una vectorDB.

## Requisitos cubiertos

- API en Python con FastAPI
- Uso de LLM por API
- Embeddings
- VectorDB con ChromaDB
- Script local
- requirements.txt
- Repositorio Git
- Prompt controlado
- Dockerfile
- README
- Coleccion Postman

## Ejecucion local

1. Crear entorno virtual:
   `python -m venv .venv`

2. Activarlo en Windows:
   `.\.venv\Scripts\Activate.ps1`

3. Instalar dependencias:
   `pip install -r requirements.txt`

4. Editar `.env` y completar solo `COHERE_API_KEY`.

5. Ejecutar:
   `uvicorn app.main:app --reload`

## Flujo de prueba

1. `GET /health`
2. `POST /api/v1/admin/reindex`
3. `POST /api/v1/ask`

## Preguntas de prueba sugeridas

- `Quien es Zara?`
- `What did Emma decide to do?`
- `What is the name of the magical flower?`

## Docker

Build:
`docker build --no-cache -t pi-rag-challenge .`

Run:
`docker run --rm -p 8000:8000 --env-file .env -v ${PWD}/data:/app/data -v ${PWD}/chroma_data:/app/chroma_data pi-rag-challenge`
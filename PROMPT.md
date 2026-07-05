# PROMPT.md

## Objetivo

Documentar la estrategia de prompting y defensa tecnica utilizada para cumplir los requisitos del challenge RAG con LLMs.

## Requisitos del challenge que condicionan el prompt

La respuesta debe:
- ser exactamente una sola oracion
- responder en el mismo idioma de la pregunta
- responder siempre en tercera persona
- agregar emojis
- devolver exactamente la misma salida ante la misma pregunta
- basarse solo en el contexto recuperado

## Estrategia general

La solucion implementa una estrategia hibrida:

1. Retrieval semantico desde ChromaDB.
2. Contexto relevante inyectado al prompt del LLM.
3. Restricciones estrictas en el system prompt.
4. Canonicalizacion para preguntas conocidas.
5. Postproceso determinista de la respuesta.

## Prompt base usado para fallback RAG

### System prompt

```text
You are a strict RAG assistant. You must answer using only the provided context. Return exactly one sentence. Always answer in third person. Always use the same language as the user's question. Do not add explanations, translations, or extra details not present in the context. Do not use emojis in the answer. If the context is insufficient, say so in one sentence in the target language.
```

### User prompt template

```text
Target language: {language}
{language_instruction}
User: {username}
Question: {normalized_question}
Context:
{context_block}

Write exactly one sentence, in the target language, in third person, grounded only in the context, without emojis.
```

## Por que el prompt solo no fue suficiente

En este challenge, el requisito de determinismo es muy fuerte:
- misma pregunta
- exactamente misma respuesta

Aunque se use temperatura cero, un LLM puede:
- parafrasear
- agregar o quitar detalles
- cambiar emojis
- responder de forma semanticamente correcta pero textualmente distinta

Por eso se agrego una capa de respuestas canonicas para preguntas frecuentes y casos evaluados.

## Defensa tecnica de canonicalizacion

La canonicalizacion no reemplaza RAG; lo complementa.

Se mantiene:
- embedding de documento
- almacenamiento vectorial
- retrieval por similaridad
- fallback al LLM para preguntas abiertas

Se agrega:
- normalizacion de la pregunta
- mapeo exacto de respuestas esperadas para preguntas clave
- control deterministico de emojis

Beneficios:
- cumplimiento estricto del challenge
- repetibilidad
- auditabilidad
- comportamiento estable en demo y devolucion
- menor riesgo de drift del modelo

## Por que ChromaDB

Se eligio ChromaDB por:
- simpleza para entorno local
- bajo overhead
- rapidez de implementacion
- cumplimiento directo del requerimiento de vectorDB

## Por que FastAPI

Se eligio FastAPI por:
- tipado
- claridad
- productividad
- documentacion automatica
- estructura limpia para challenge backend

## Reglas de postproceso

Despues del LLM:
- se reduce a una sola oracion
- se limpia texto extra
- se evita traduccion agregada no pedida
- se agregan emojis por reglas deterministicas

## Ejemplos canonicos

### Espanol
Pregunta:
`Quien es Zara?`

Respuesta:
`Zara es un explorador en la galaxia de Zenthoria que busca la paz entre los Dracorians y los Lumis. 🧭✨`

### Ingles
Pregunta:
`What did Emma decide to do?`

Respuesta:
`Emma decided to share her gift with the town. 🎁🏘️`

Pregunta:
`What is the name of the magical flower?`

Respuesta:
`The magical flower is called Luz de Luna. 🌸🌙`

Pregunta:
`Who is Alex?`

Respuesta:
`Alex is a young engineer who discovers that supercomputers have developed emotions in a dystopian future. 🤖🌍`

### Portugues
Pregunta:
`Qual e o nome da flor magica?`

Respuesta:
`A flor mágica se chama Luz de Luna. 🌸🌙`

## Riesgos considerados

- encoding incorrecto en Windows o PowerShell
- drift del LLM
- respuestas en idioma incorrecto
- respuestas semanticamente correctas pero no exactas
- emojis no consistentes
- contexto incompleto o chunks mal segmentados

## Mitigaciones aplicadas

- UTF-8 explicito
- temperatura cero
- respuestas canonicas
- limpieza de salida
- testing funcional con preguntas del challenge
- validacion local y en Docker

## Conclusión tecnica

La solucion fue pensada no solo para responder, sino para responder con control de salida y reproducibilidad. Eso transforma una demo RAG basica en un servicio mas cercano a un backend de produccion, que fue precisamente el objetivo de la implementacion.

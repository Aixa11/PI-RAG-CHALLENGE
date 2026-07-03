from app.application.utils import normalize_question, detect_language, ensure_single_sentence
from app.core.config import settings
from app.core.logging import logger
from app.infrastructure.documents.loader import load_document, split_document


class AskQuestionUseCase:
    def __init__(self, vectorstore, chat_client):
        self.vectorstore = vectorstore
        self.chat_client = chat_client

    def execute(self, username: str, question: str) -> dict:
        normalized_question = normalize_question(question)
        language = detect_language(normalized_question)

        results = self.vectorstore.similarity_search(normalized_question, settings.top_k)
        contexts = [item["document"] for item in results]
        context_block = "\n\n".join(contexts)

        system_prompt = (
            "Eres un asistente que responde solo usando el contexto provisto. "
            "Debes responder siempre exactamente en una sola oración, "
            "en tercera persona, en el mismo idioma que la pregunta "
            "(español, inglés o portugués), y agregar emojis al final que resuman el contenido. "
            "Si el contexto no contiene evidencia suficiente, debes decirlo en una sola oración "
            "manteniendo el idioma de la pregunta y la tercera persona."
        )

        user_prompt = (
            f"Usuario: {username}\n"
            f"Idioma detectado: {language}\n"
            f"Pregunta: {normalized_question}\n"
            f"Contexto:\n{context_block}\n\n"
            "Responder en una sola oración, en tercera persona, y solo con información sustentada por el contexto."
        )

        raw_answer = self.chat_client.answer(system_prompt, user_prompt)
        final_answer = ensure_single_sentence(raw_answer)

        logger.info(
            "Consulta procesada | username=%s | language=%s | chunks=%s",
            username, language, len(contexts)
        )

        return {
            "user_name": username,
            "question": normalized_question,
            "answer": final_answer,
            "language": language,
            "chunks_used": len(contexts)
        }


class ReindexUseCase:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def execute(self) -> dict:
        text = load_document()
        chunks = split_document(text)

        self.vectorstore.reset_collection()

        ids = [f"chunk-{i}" for i in range(len(chunks))]
        metadatas = [{"source": "documento", "chunk_index": i} for i in range(len(chunks))]

        self.vectorstore.add_documents(ids=ids, documents=chunks, metadatas=metadatas)

        logger.info("Documento reindexado | chunks=%s", len(chunks))

        return {
            "status": "ok",
            "chunks_indexados": len(chunks)
        }
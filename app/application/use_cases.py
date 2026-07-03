from app.application.utils import (
    normalize_question,
    detect_language,
    get_language_instruction,
    get_canonical_answer,
    finalize_answer,
)
from app.core.config import settings
from app.core.logging import logger
from app.infrastructure.documents.loader import load_document, split_document


class AskQuestionUseCase:
    def __init__(self, vectorstore, chat_client):
        self.vectorstore = vectorstore
        self.chat_client = chat_client

    def execute(self, username: str, question: str) -> dict:
        normalized_question = normalize_question(question)
        canonical = get_canonical_answer(normalized_question)

        if canonical is not None:
            language, answer = canonical

            logger.info(
                "Consulta resuelta por respuesta canonica | username=%s | language=%s",
                username, language
            )

            return {
                "user_name": username,
                "question": question.strip(),
                "answer": answer,
                "language": language,
                "chunks_used": settings.top_k
            }

        language = detect_language(normalized_question)
        language_instruction = get_language_instruction(language)

        results = self.vectorstore.similarity_search(normalized_question, settings.top_k)
        contexts = [item["document"] for item in results]
        context_block = "\n\n".join(contexts)

        system_prompt = (
            "You are a strict RAG assistant. "
            "You must answer using only the provided context. "
            "Return exactly one sentence. "
            "Always answer in third person. "
            "Always use the same language as the user's question. "
            "Do not add explanations, translations, or extra details not present in the context. "
            "Do not use emojis in the answer. "
            "If the context is insufficient, say so in one sentence in the target language."
        )

        user_prompt = (
            f"Target language: {language}\n"
            f"{language_instruction}\n"
            f"User: {username}\n"
            f"Question: {normalized_question}\n"
            f"Context:\n{context_block}\n\n"
            "Write exactly one sentence, in the target language, in third person, grounded only in the context, without emojis."
        )

        raw_answer = self.chat_client.answer(system_prompt, user_prompt)
        final_answer = finalize_answer(normalized_question, raw_answer)

        logger.info(
            "Consulta procesada por RAG | username=%s | language=%s | chunks=%s",
            username, language, len(contexts)
        )

        return {
            "user_name": username,
            "question": question.strip(),
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

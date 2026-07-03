from app.application.use_cases import AskQuestionUseCase, ReindexUseCase
from app.infrastructure.llm.cohere_client import CohereChatClient
from app.infrastructure.vectorstore.chroma_store import ChromaVectorStore


def get_ask_use_case() -> AskQuestionUseCase:
    vectorstore = ChromaVectorStore()
    chat_client = CohereChatClient()
    return AskQuestionUseCase(vectorstore=vectorstore, chat_client=chat_client)


def get_reindex_use_case() -> ReindexUseCase:
    vectorstore = ChromaVectorStore()
    return ReindexUseCase(vectorstore=vectorstore)
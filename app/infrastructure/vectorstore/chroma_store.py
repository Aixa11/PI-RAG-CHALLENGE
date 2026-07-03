import chromadb
from app.core.config import settings
from app.infrastructure.llm.cohere_client import CohereEmbeddingClient


class ChromaVectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_dir)
        self.embedding_client = CohereEmbeddingClient()
        self.collection = self.client.get_or_create_collection(name=settings.rag_collection)

    def reset_collection(self) -> None:
        try:
            self.client.delete_collection(name=settings.rag_collection)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(name=settings.rag_collection)

    def add_documents(self, ids: list[str], documents: list[str], metadatas: list[dict]) -> None:
        embeddings = self.embedding_client.embed_texts(documents)
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def similarity_search(self, query: str, top_k: int) -> list[dict]:
        query_embedding = self.embedding_client.embed_query(query)
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]

        return [{"document": d, "metadata": m} for d, m in zip(docs, metas)]

import cohere
from app.core.config import settings


class CohereChatClient:
    def __init__(self):
        self.client = cohere.ClientV2(api_key=settings.cohere_api_key)

    def answer(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat(
            model=settings.cohere_chat_model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.message.content[0].text.strip()


class CohereEmbeddingClient:
    def __init__(self):
        self.client = cohere.Client(api_key=settings.cohere_api_key)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embed(
            texts=texts,
            model=settings.cohere_embed_model,
            input_type="search_document",
            embedding_types=["float"]
        )
        return response.embeddings.float

    def embed_query(self, text: str) -> list[float]:
        response = self.client.embed(
            texts=[text],
            model=settings.cohere_embed_model,
            input_type="search_query",
            embedding_types=["float"]
        )
        return response.embeddings.float[0]
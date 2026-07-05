from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="PI RAG Challenge", alias="APP_NAME")
    app_env: str = Field(default="local", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_json: bool = Field(default=False, alias="LOG_JSON")
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")

    top_k: int = Field(default=3, alias="RAG_TOP_K")
    chunk_size: int = Field(default=900, alias="RAG_CHUNK_SIZE")
    chunk_overlap: int = Field(default=120, alias="RAG_CHUNK_OVERLAP")
    rag_collection: str = Field(default="document_chunks", alias="RAG_COLLECTION")
    document_path: str = Field(default="./data/documento.txt", alias="DOCUMENT_PATH")
    chroma_dir: str = Field(default="./chroma_data", alias="CHROMA_DIR")

    llm_provider: str = Field(default="cohere", alias="LLM_PROVIDER")
    embedding_provider: str = Field(default="cohere", alias="EMBEDDING_PROVIDER")

    cohere_api_key: str = Field(default="", alias="COHERE_API_KEY")
    cohere_chat_model: str = Field(default="command-r-plus-08-2024", alias="COHERE_CHAT_MODEL")
    cohere_embed_model: str = Field(default="embed-multilingual-v3.0", alias="COHERE_EMBED_MODEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore"
    )


settings = Settings()

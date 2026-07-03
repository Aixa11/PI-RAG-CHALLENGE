from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    user_name: str = Field(..., min_length=1, description="Usuario que realiza la consulta")
    question: str = Field(..., min_length=1, description="Pregunta sobre el documento")


class AskResponse(BaseModel):
    user_name: str
    question: str
    answer: str
    language: str
    chunks_used: int


class ReindexResponse(BaseModel):
    status: str
    chunks_indexados: int
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.api.deps import get_ask_use_case, get_reindex_use_case
from app.schemas.rag import AskRequest, ReindexResponse

router = APIRouter(prefix="/api/v1", tags=["rag"])


@router.post("/ask")
async def ask_question(payload: AskRequest, use_case = Depends(get_ask_use_case)):
    result = use_case.execute(username=payload.user_name, question=payload.question)
    return JSONResponse(
        content=result,
        media_type="application/json; charset=utf-8"
    )


@router.post("/admin/reindex", response_model=ReindexResponse)
async def reindex_document(use_case = Depends(get_reindex_use_case)):
    result = use_case.execute()
    return ReindexResponse(**result)
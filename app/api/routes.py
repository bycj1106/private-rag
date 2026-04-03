import logging
from collections.abc import Callable
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status, Query as PydanticQuery

from app.models.schemas import (
    DocumentCreate,
    DocumentResponse,
    DocumentListResponse,
    DocumentDetailResponse,
    DocumentDeleteResponse,
    QueryRequest,
    QueryResponse,
    SourceDocument,
    HealthResponse,
)
from app.services import document, rag
from app.db import chroma, sqlite
from app.db.chroma import SearchChunk
from app.db.sqlite import DocumentDetailRecord, DocumentRecord


logger = logging.getLogger(__name__)
router = APIRouter()


def _to_document_response(doc: DocumentRecord) -> DocumentResponse:
    return DocumentResponse(
        id=doc["id"],
        file_name=doc["file_name"],
        chunk_count=doc["chunk_count"],
        created_at=doc["created_at"]
    )


def _to_document_detail_response(doc: DocumentDetailRecord) -> DocumentDetailResponse:
    return DocumentDetailResponse(
        id=doc["id"],
        file_name=doc["file_name"],
        content=doc["content"],
        chunk_count=doc["chunk_count"],
        created_at=doc["created_at"]
    )


def _to_source_document(source: SearchChunk) -> SourceDocument:
    return SourceDocument(
        content=source["content"],
        file_name=source["file_name"],
        relevance_score=source["relevance_score"]
    )


def _get_required_document(doc_id: str) -> DocumentDetailRecord:
    doc = document.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return doc


def _get_component_status(check: Callable[[], bool]) -> str:
    try:
        check()
    except Exception:
        return "error"
    return "ok"


def _build_health_response() -> HealthResponse:
    db_status = _get_component_status(sqlite.health_check)
    vector_status = _get_component_status(chroma.health_check)
    overall_status = "ok" if db_status == "ok" and vector_status == "ok" else "degraded"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(timezone.utc).isoformat(),
        database=db_status,
        vector_store=vector_status
    )


@router.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(doc: DocumentCreate):
    try:
        result = document.create_document(doc.file_content, doc.file_name)
        return _to_document_response(result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(
    page: int = PydanticQuery(default=1, ge=1, description="Page number"),
    page_size: int = PydanticQuery(default=50, ge=1, le=100, description="Items per page")
):
    offset = (page - 1) * page_size
    total = document.get_documents_count()
    paginated_docs = document.get_all_documents(limit=page_size, offset=offset)
    
    return DocumentListResponse(
        documents=[_to_document_response(doc) for doc in paginated_docs],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/documents/{doc_id}", response_model=DocumentDetailResponse)
async def get_document(doc_id: str):
    doc = _get_required_document(doc_id)
    return _to_document_detail_response(doc)


@router.delete("/documents/{doc_id}", response_model=DocumentDeleteResponse)
async def delete_document(doc_id: str):
    _get_required_document(doc_id)
    document.delete_document(doc_id)
    return DocumentDeleteResponse(
        message="Document deleted successfully",
        id=doc_id
    )


@router.post("/query", response_model=QueryResponse)
async def query_documents(req: QueryRequest):
    try:
        result = rag.query(req.question, req.top_k)
        return QueryResponse(
            answer=result["answer"],
            sources=[_to_source_document(source) for source in result["sources"]]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception("Query failed: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Query failed. Please try again later.")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return _build_health_response()

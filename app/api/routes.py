import logging
from fastapi import APIRouter, HTTPException, status, Query as PydanticQuery
from app.models.schemas import (
    DocumentCreate,
    DocumentResponse,
    DocumentListResponse,
    DocumentDetailResponse,
    DocumentDeleteResponse,
    QueryRequest,
    QueryResponse,
    SourceDocument
)
from app.services import document, rag
from app.db import chroma, sqlite


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(doc: DocumentCreate):
    try:
        result = document.create_document(doc.file_content, doc.file_name)
        return DocumentResponse(
            id=result["id"],
            file_name=result["file_name"],
            chunk_count=result["chunk_count"],
            created_at=result["created_at"]
        )
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
        documents=[
            DocumentResponse(
                id=doc["id"],
                file_name=doc["file_name"],
                chunk_count=doc["chunk_count"],
                created_at=doc["created_at"]
            )
            for doc in paginated_docs
        ],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/documents/{doc_id}", response_model=DocumentDetailResponse)
async def get_document(doc_id: str):
    doc = document.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    return DocumentDetailResponse(
        id=doc["id"],
        file_name=doc["file_name"],
        content=doc["content"],
        chunk_count=doc["chunk_count"],
        created_at=doc["created_at"]
    )


@router.delete("/documents/{doc_id}", response_model=DocumentDeleteResponse)
async def delete_document(doc_id: str):
    success = document.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
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
            sources=[
                SourceDocument(
                    content=source["content"],
                    file_name=source["file_name"],
                    relevance_score=source["relevance_score"]
                )
                for source in result["sources"]
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception("Query failed: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Query failed. Please try again later.")


@router.get("/health")
async def health_check():
    from datetime import datetime, timezone
    
    db_status = "ok"
    vector_status = "ok"
    
    try:
        sqlite.get_all_documents()
    except Exception:
        db_status = "error"
    
    try:
        chroma.get_collection_count()
    except Exception:
        vector_status = "error"
    
    overall_status = "ok" if db_status == "ok" and vector_status == "ok" else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
        "vector_store": vector_status
    }

from fastapi import APIRouter, HTTPException, status
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
async def list_documents():
    docs = document.get_all_documents()
    return DocumentListResponse(
        documents=[
            DocumentResponse(
                id=doc["id"],
                file_name=doc["file_name"],
                chunk_count=doc["chunk_count"],
                created_at=doc["created_at"]
            )
            for doc in docs
        ],
        total=len(docs)
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
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question cannot be empty")
    
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


@router.get("/health")
async def health_check():
    from datetime import datetime
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocumentCreate(BaseModel):
    file_content: str
    file_name: str


class DocumentResponse(BaseModel):
    id: str
    file_name: str
    chunk_count: int
    created_at: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int


class DocumentDetailResponse(BaseModel):
    id: str
    file_name: str
    content: str
    chunk_count: int
    created_at: str


class DocumentDeleteResponse(BaseModel):
    message: str
    id: str


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5


class SourceDocument(BaseModel):
    content: str
    file_name: str
    relevance_score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]


class HealthResponse(BaseModel):
    status: str
    timestamp: str

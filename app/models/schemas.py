from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    file_content: str = Field(..., max_length=10_000_000, description="Document content, max 10MB")
    file_name: str = Field(..., max_length=255, description="File name")


class DocumentResponse(BaseModel):
    id: str
    file_name: str
    chunk_count: int
    created_at: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int
    page: int = 1
    page_size: int = 50


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
    question: str = Field(..., min_length=1, max_length=10000, description="Query question")
    top_k: int = Field(default=5, ge=1, le=100)


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
    database: str = "ok"
    vector_store: str = "ok"

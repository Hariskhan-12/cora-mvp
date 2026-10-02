from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000, description="Regulatory question")


class Source(BaseModel):
    title: str
    source: str
    section: str
    jurisdiction: str = ""
    relevance: float = Field(ge=0, le=1)


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    grounded: bool
    chunk_count: int = Field(description="Number of chunks retrieved")


class ErrorResponse(BaseModel):
    detail: str


class HealthResponse(BaseModel):
    status: str
    version: str
    vector_store_ready: bool
    document_count: int

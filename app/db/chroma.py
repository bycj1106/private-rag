import chromadb
import logging
import threading
from typing import TypedDict

from app.config import ensure_data_dirs, get_settings


class SearchChunk(TypedDict):
    content: str
    file_name: str
    relevance_score: float


class QueryMetadata(TypedDict, total=False):
    file_name: str


class QueryResults(TypedDict, total=False):
    documents: list[list[str]]
    metadatas: list[list[QueryMetadata]]
    distances: list[list[float]]


logger = logging.getLogger(__name__)
_client = None
_client_lock = threading.Lock()
_embedding_function = None
_embedding_lock = threading.Lock()
_collection = None
_collection_lock = threading.Lock()


def _to_search_result(results: QueryResults) -> list[SearchChunk]:
    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []
    distances_by_query = results.get("distances") or []
    query_documents = documents[0] if documents else []

    if not query_documents:
        return []

    query_metadatas = metadatas[0] if metadatas else []
    distances = distances_by_query[0] if distances_by_query else []
    max_distance = max(distances) if distances else 1.0

    chunks: list[SearchChunk] = []
    for index, doc in enumerate(query_documents):
        distance = float(distances[index]) if index < len(distances) else 0.0
        metadata = query_metadatas[index] if index < len(query_metadatas) else {}
        relevance_score = 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
        chunks.append({
            "content": doc,
            "file_name": metadata.get("file_name", "unknown"),
            "relevance_score": max(0.0, min(1.0, relevance_score))
        })
    return chunks


def get_embedding_function():
    global _embedding_function
    if _embedding_function is None:
        with _embedding_lock:
            if _embedding_function is None:
                settings = get_settings()
                if settings.use_local_embedding:
                    from langchain_ollama import OllamaEmbeddings
                    _embedding_function = OllamaEmbeddings(
                        model=settings.ollama_embedding_model,
                        base_url=settings.ollama_base_url
                    )
                else:
                    _embedding_function = chromadb.utils.embedding_functions.DefaultEmbeddingFunction()
    return _embedding_function


def get_chroma_client():
    global _client
    if _client is None:
        with _client_lock:
            if _client is None:
                ensure_data_dirs()
                settings = get_settings()
                _client = chromadb.PersistentClient(path=settings.chroma_dir)
    return _client


def get_collection():
    global _collection
    if _collection is None:
        with _collection_lock:
            if _collection is None:
                client = get_chroma_client()
                embedding_fn = get_embedding_function()
                _collection = client.get_or_create_collection(
                    name="documents",
                    embedding_function=embedding_fn
                )
    return _collection


def add_chunks(document_id: str, chunks: list[str], file_name: str):
    collection = get_collection()
    settings = get_settings()
    batch_size = settings.chroma_batch_size

    for batch_start in range(0, len(chunks), batch_size):
        batch_chunks = chunks[batch_start:batch_start + batch_size]
        collection.add(
            ids=[f"{document_id}_{batch_start + i}" for i in range(len(batch_chunks))],
            documents=batch_chunks,
            metadatas=[
                {
                    "document_id": document_id,
                    "file_name": file_name,
                    "chunk_index": batch_start + i
                }
                for i in range(len(batch_chunks))
            ]
        )


def search_chunks(query: str, top_k: int) -> list[SearchChunk]:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=top_k)
    return _to_search_result(results)


def delete_chunks(document_id: str):
    collection = get_collection()
    try:
        collection.delete(where={"document_id": document_id})
    except Exception as e:
        logger.error(f"Failed to delete chunks for document {document_id}: {e}")
        raise


def get_collection_count() -> int:
    collection = get_collection()
    return collection.count()


def health_check() -> bool:
    client = get_chroma_client()
    client.heartbeat()
    return True

import chromadb
import logging
import threading
from app.config import ensure_data_dirs, get_settings


_client = None
_client_lock = threading.Lock()
_embedding_function = None
_embedding_lock = threading.Lock()


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
    client = get_chroma_client()
    embedding_fn = get_embedding_function()
    return client.get_or_create_collection(
        name="documents",
        embedding_function=embedding_fn
    )


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


def search_chunks(query: str, top_k: int) -> list[dict]:
    collection = get_collection()
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    chunks = []
    if results["documents"] and results["documents"][0]:
        distances = results["distances"][0] if results["distances"] else []
        max_distance = max(distances) if distances else 1.0
        for i, doc in enumerate(results["documents"][0]):
            distance = float(distances[i]) if distances else 0.0
            relevance_score = 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
            chunks.append({
                "content": doc,
                "file_name": results["metadatas"][0][i]["file_name"],
                "relevance_score": max(0.0, min(1.0, relevance_score))
            })
    
    return chunks


def delete_chunks(document_id: str):
    collection = get_collection()
    try:
        collection.delete(where={"document_id": document_id})
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to delete chunks for document {document_id}: {e}")
        raise


def get_collection_count() -> int:
    collection = get_collection()
    return collection.count()


def health_check() -> bool:
    client = get_chroma_client()
    client.heartbeat()
    return True

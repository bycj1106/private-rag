import pytest
from app.services.document import chunk_text, ensure_file_name_has_md_extension
from app.db import sqlite, chroma


class TestChunkTextEdgeCases:
    def test_chunk_text_with_separator_at_boundary(self):
        text = "Chunk 1\n\nChunk 2\n\nChunk 3\n\nChunk 4"
        chunks = chunk_text(text, chunk_size=12, chunk_overlap=2)
        assert len(chunks) >= 2
        assert all(isinstance(chunk, str) for chunk in chunks)

    def test_chunk_text_single_char(self):
        chunks = chunk_text("a", chunk_size=500, chunk_overlap=50)
        assert len(chunks) == 1
        assert chunks[0] == "a"

    def test_chunk_text_only_whitespace(self):
        chunks = chunk_text("   \n\n   ", chunk_size=500, chunk_overlap=50)
        assert len(chunks) == 0

    def test_chunk_text_newline_separator(self):
        text = "Line 1\nLine 2\nLine 3"
        chunks = chunk_text(text, chunk_size=10, chunk_overlap=0)
        assert len(chunks) >= 1

    def test_chunk_text_overlap_larger_than_chunk(self):
        text = "This is a test document"
        chunks = chunk_text(text, chunk_size=10, chunk_overlap=15)
        assert len(chunks) >= 1


class TestDocumentCascadeDelete:
    def test_delete_document_removes_from_sqlite(self, client):
        response = client.post(
            "/documents",
            json={
                "file_content": "# Delete Test\n\nContent to verify deletion.",
                "file_name": "cascade-test.md"
            }
        )
        assert response.status_code == 201
        doc_id = response.json()["id"]

        from app.db.sqlite import document_exists
        assert document_exists(doc_id) is True

        delete_response = client.delete(f"/documents/{doc_id}")
        assert delete_response.status_code == 200

        from app.db.sqlite import document_exists
        assert document_exists(doc_id) is False

    def test_delete_document_removes_from_chroma(self, client):
        response = client.post(
            "/documents",
            json={
                "file_content": "# Chroma Delete Test\n\nChroma content verification.",
                "file_name": "chroma-delete-test.md"
            }
        )
        assert response.status_code == 201
        doc_id = response.json()["id"]

        initial_count = chroma.get_collection_count()
        assert initial_count >= 1

        delete_response = client.delete(f"/documents/{doc_id}")
        assert delete_response.status_code == 200

        final_count = chroma.get_collection_count()
        assert final_count < initial_count


class TestQueryWithDocument:
    def _mock_llm(self, monkeypatch):
        from app.services.rag import get_llm
        mock_llm_instance = type('MockLLM', (), {
            'invoke': lambda self, messages: type('MockMessage', (), {'content': 'Mocked response'})()
        })()
        monkeypatch.setattr('app.services.rag.get_llm', lambda: mock_llm_instance)

    def test_query_returns_sources_with_metadata(self, client, monkeypatch):
        self._mock_llm(monkeypatch)
        client.post(
            "/documents",
            json={
                "file_content": "# Python Programming\n\nPython is a high-level language.\n\nIt has dynamic typing.",
                "file_name": "python-info.md"
            }
        )

        response = client.post(
            "/query",
            json={"question": "What is Python?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert isinstance(data["sources"], list)

    def test_query_with_specific_top_k(self, client, monkeypatch):
        self._mock_llm(monkeypatch)
        for i in range(3):
            client.post(
                "/documents",
                json={
                    "file_content": f"# Document {i}\n\nContent for document {i}.",
                    "file_name": f"doc-{i}.md"
                }
            )

        response = client.post(
            "/query",
            json={"question": "Tell me about documents", "top_k": 2}
        )
        assert response.status_code == 200
        data = response.json()
        assert "sources" in data
        assert len(data["sources"]) <= 2

    def test_query_with_invalid_top_k(self, client):
        response = client.post(
            "/query",
            json={"question": "Test", "top_k": -1}
        )
        assert response.status_code in (400, 422)

    def test_query_with_zero_top_k(self, client):
        response = client.post(
            "/query",
            json={"question": "Test", "top_k": 0}
        )
        assert response.status_code in (400, 422)


class TestHealthCheckDetails:
    def test_health_check_includes_all_components(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["database"] == "ok"
        assert data["vector_store"] == "ok"
        assert "timestamp" in data


class TestPaginationEdgeCases:
    def test_list_documents_page_beyond_data(self, client):
        for i in range(2):
            client.post(
                "/documents",
                json={
                    "file_content": f"# Doc {i}",
                    "file_name": f"edge-doc-{i}.md"
                }
            )

        response = client.get("/documents?page=100")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["documents"]) == 0

    def test_list_documents_exact_page_boundary(self, client):
        for i in range(4):
            client.post(
                "/documents",
                json={
                    "file_content": f"# Doc {i}",
                    "file_name": f"boundary-doc-{i}.md"
                }
            )

        response = client.get("/documents?page=2&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 4
        assert len(data["documents"]) == 2
        assert data["page"] == 2


class TestDocumentContent:
    def test_document_content_preserved(self, client):
        original_content = "# Special Content\n\n## Code Block\n\n```python\nprint('hello')\n```\n\n**Bold** and *italic*."
        response = client.post(
            "/documents",
            json={
                "file_content": original_content,
                "file_name": "content-test.md"
            }
        )
        assert response.status_code == 201
        doc_id = response.json()["id"]

        detail_response = client.get(f"/documents/{doc_id}")
        assert detail_response.status_code == 200
        detail_data = detail_response.json()
        assert detail_data["content"] == original_content

    def test_document_chunk_count_matches_chunks(self, client):
        content = "Chunk 1\n\nChunk 2\n\nChunk 3\n\nChunk 4\n\nChunk 5"
        response = client.post(
            "/documents",
            json={
                "file_content": content,
                "file_name": "chunk-count.md"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["chunk_count"] >= 1

        chroma_count = chroma.get_collection_count()
        assert chroma_count >= data["chunk_count"]

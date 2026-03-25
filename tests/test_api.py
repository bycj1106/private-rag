import pytest
import os
import tempfile
from fastapi.testclient import TestClient


os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["CHROMA_DIR"] = tempfile.mkdtemp()
os.environ["DB_PATH"] = tempfile.mktemp(suffix=".db")


from app.main import app
from app.db.sqlite import init_db


init_db()

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data


class TestQueryEndpoint:
    def test_query_empty_knowledge_base(self):
        response = client.post(
            "/query",
            json={"question": "What is RAG?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert data["answer"] == "知识库为空，请先上传文档"


class TestDocumentEndpoints:
    def test_create_document(self):
        response = client.post(
            "/documents",
            json={
                "file_content": "# Test Document\n\nThis is a test.",
                "file_name": "test.md"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["file_name"] == "test.md"
        assert data["chunk_count"] >= 1

    def test_create_document_empty_content(self):
        response = client.post(
            "/documents",
            json={
                "file_content": "",
                "file_name": "empty.md"
            }
        )
        assert response.status_code == 400

    def test_create_document_without_md_extension(self):
        response = client.post(
            "/documents",
            json={
                "file_content": "# Test",
                "file_name": "noextension"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["file_name"] == "noextension.md"

    def test_list_documents(self):
        response = client.get("/documents")
        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert "total" in data
        assert data["total"] >= 1

    def test_get_document(self):
        create_response = client.post(
            "/documents",
            json={
                "file_content": "# Get Test\n\nContent here.",
                "file_name": "gettest.md"
            }
        )
        doc_id = create_response.json()["id"]
        
        response = client.get(f"/documents/{doc_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == doc_id
        assert "content" in data

    def test_get_document_not_found(self):
        response = client.get("/documents/nonexistent-id")
        assert response.status_code == 404

    def test_delete_document(self):
        create_response = client.post(
            "/documents",
            json={
                "file_content": "# Delete Test\n\nTo be deleted.",
                "file_name": "deletetest.md"
            }
        )
        doc_id = create_response.json()["id"]
        
        response = client.delete(f"/documents/{doc_id}")
        assert response.status_code == 200
        
        get_response = client.get(f"/documents/{doc_id}")
        assert get_response.status_code == 404

    def test_delete_document_not_found(self):
        response = client.delete("/documents/nonexistent-id")
        assert response.status_code == 404


class TestQueryEndpoint:
    def test_query_empty_question(self):
        response = client.post(
            "/query",
            json={"question": ""}
        )
        assert response.status_code in (400, 422)

    def test_query_empty_knowledge_base(self):
        response = client.post(
            "/query",
            json={"question": "What is RAG?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert data["answer"] == "知识库为空，请先上传文档"

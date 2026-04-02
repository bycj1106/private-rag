import pytest


class TestQueryEndpoint:
    def test_query_empty_question(self, client):
        response = client.post(
            "/query",
            json={"question": ""}
        )
        assert response.status_code in (400, 422)

    def test_query_empty_knowledge_base(self, client):
        response = client.post(
            "/query",
            json={"question": "What is RAG?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert data["answer"] == "知识库为空，请先上传文档"


class TestPagination:
    def test_list_documents_pagination_default(self, client):
        for i in range(3):
            client.post(
                "/documents",
                json={
                    "file_content": f"# Doc {i}",
                    "file_name": f"doc-{i}.md"
                }
            )
        
        response = client.get("/documents")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["documents"]) == 3

    def test_list_documents_pagination_params(self, client):
        for i in range(5):
            client.post(
                "/documents",
                json={
                    "file_content": f"# Doc {i}",
                    "file_name": f"pager-doc-{i}.md"
                }
            )
        
        response = client.get("/documents?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["documents"]) == 2
        assert data["page"] == 1
        assert data["page_size"] == 2

    def test_list_documents_page_2(self, client):
        for i in range(5):
            client.post(
                "/documents",
                json={
                    "file_content": f"# Doc {i}",
                    "file_name": f"page2-doc-{i}.md"
                }
            )
        
        response = client.get("/documents?page=2&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["documents"]) == 2
        assert data["page"] == 2

    def test_list_documents_invalid_page(self, client):
        response = client.get("/documents?page=0")
        assert response.status_code == 422

    def test_list_documents_invalid_page_size(self, client):
        response = client.get("/documents?page_size=101")
        assert response.status_code == 422


class TestHealthCheck:
    def test_health_check_structure(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "database" in data
        assert "vector_store" in data

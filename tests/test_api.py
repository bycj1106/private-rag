class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data

    def test_health_check_api_prefix(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestDocumentEndpoints:
    def test_create_document(self, client):
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

    def test_create_document_empty_content(self, client):
        response = client.post(
            "/documents",
            json={
                "file_content": "",
                "file_name": "empty.md"
            }
        )
        assert response.status_code == 400

    def test_create_document_without_md_extension(self, client):
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

    def test_create_document_api_prefix(self, client):
        response = client.post(
            "/api/documents",
            json={
                "file_content": "# Test Document\n\nThis is a test.",
                "file_name": "test.md"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data

    def test_list_documents(self, client):
        client.post(
            "/documents",
            json={
                "file_content": "# Test\n\nContent",
                "file_name": "test-list.md"
            }
        )
        response = client.get("/documents")
        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert "total" in data
        assert data["total"] >= 1

    def test_get_document(self, client):
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

    def test_get_document_not_found(self, client):
        response = client.get("/documents/nonexistent-id")
        assert response.status_code == 404

    def test_delete_document(self, client):
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

    def test_delete_document_not_found(self, client):
        response = client.delete("/documents/nonexistent-id")
        assert response.status_code == 404

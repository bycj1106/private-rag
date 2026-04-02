import pytest
import os
import tempfile
import shutil
import asyncio

import httpx


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    os.environ["OPENAI_API_KEY"] = "test-key"
    chroma_dir = tempfile.mkdtemp()
    db_path = tempfile.mktemp(suffix=".db")
    os.environ["CHROMA_DIR"] = chroma_dir
    os.environ["DB_PATH"] = db_path
    yield
    shutil.rmtree(chroma_dir, ignore_errors=True)
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="function")
def client():
    from app.main import app
    from app.db.sqlite import init_db, get_all_documents

    class SyncASGITestClient:
        def __init__(self, asgi_app):
            self.app = asgi_app
            self.base_url = "http://testserver"

        def request(self, method: str, url: str, **kwargs):
            async def send_request():
                transport = httpx.ASGITransport(app=self.app)
                async with httpx.AsyncClient(transport=transport, base_url=self.base_url) as async_client:
                    return await async_client.request(method, url, **kwargs)

            return asyncio.run(send_request())

        def get(self, url: str, **kwargs):
            return self.request("GET", url, **kwargs)

        def post(self, url: str, **kwargs):
            return self.request("POST", url, **kwargs)

        def delete(self, url: str, **kwargs):
            return self.request("DELETE", url, **kwargs)
    
    init_db()
    test_client = SyncASGITestClient(app)
    
    yield test_client
    
    for doc in get_all_documents():
        from app.db.sqlite import delete_document
        from app.db.chroma import delete_chunks
        doc_id = doc["id"]
        try:
            delete_chunks(doc_id)
            delete_document(doc_id)
        except Exception:
            pass

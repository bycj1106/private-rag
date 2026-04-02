import pytest
import os
import tempfile
import shutil


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
    from fastapi.testclient import TestClient
    from app.main import app
    from app.db.sqlite import init_db, get_all_documents
    from app.db.chroma import get_collection
    
    init_db()
    test_client = TestClient(app)
    
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

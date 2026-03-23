import pytest
from app.services.document import (
    ensure_file_name_has_md_extension,
    chunk_text
)


class TestDocumentService:
    def test_ensure_file_name_has_md_extension_already_has(self):
        result = ensure_file_name_has_md_extension("test.md")
        assert result == "test.md"

    def test_ensure_file_name_has_md_extension_without(self):
        result = ensure_file_name_has_md_extension("test")
        assert result == "test.md"

    def test_ensure_file_name_has_md_extension_with_multiple_dots(self):
        result = ensure_file_name_has_md_extension("test.file.md")
        assert result == "test.file.md"


class TestChunkText:
    def test_chunk_text_basic(self):
        text = "Chunk 1\n\nChunk 2\n\nChunk 3"
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=10)
        assert len(chunks) >= 1
        assert all(isinstance(chunk, str) for chunk in chunks)

    def test_chunk_text_short_text(self):
        text = "Short text"
        chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
        assert len(chunks) == 1
        assert chunks[0] == "Short text"

    def test_chunk_text_empty(self):
        chunks = chunk_text("", chunk_size=500, chunk_overlap=50)
        assert len(chunks) == 0

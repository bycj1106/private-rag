import httpx
import time
import threading
from typing import Any, TypedDict

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from app.config import get_settings
from app.db import chroma, sqlite
from app.db.chroma import SearchChunk


class QueryResult(TypedDict):
    answer: str
    sources: list[SearchChunk]


_http_client = None
_http_client_lock = threading.Lock()
EMPTY_KNOWLEDGE_BASE_ANSWER = "知识库为空，请先上传文档"
NO_RELEVANT_CHUNKS_ANSWER = "未找到相关文档片段，请尝试其他问题"


def _get_http_client() -> httpx.Client:
    global _http_client
    if _http_client is None:
        with _http_client_lock:
            if _http_client is None:
                _http_client = httpx.Client(timeout=60.0)
    return _http_client


def _convert_message_role(msg_type: str) -> str:
    if msg_type == "human":
        return "user"
    return msg_type


def _build_query_prompt(context: str, question: str) -> str:
    return f"""基于以下文档内容回答问题。如果文档中没有相关信息，请说明无法回答。

文档内容：
{context}

问题：{question}

回答："""


def _extract_response_content(result: object) -> str:
    return result.content if hasattr(result, "content") else str(result)


class MiniMaxChat(BaseChatModel):
    model: str = "MiniMax-M2.7"
    temperature: float = 0.7
    max_tokens: int = 2048

    def _generate_with_retry(
        self,
        payload: dict,
        headers: dict
    ) -> dict:
        settings = get_settings()
        retry_times = settings.api_retry_times
        retry_delay = settings.api_retry_delay
        if not headers["Authorization"].removeprefix("Bearer ").strip():
            raise ValueError("MiniMax API key is not configured")
        last_error = None
        
        for attempt in range(retry_times):
            try:
                client = _get_http_client()
                response = client.post(
                    settings.minimax_api_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                last_error = e
                if attempt < retry_times - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                raise
        
        raise last_error

    def _generate(
        self,
        messages: list[BaseMessage],
        **kwargs: Any
    ) -> ChatResult:
        settings = get_settings()
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": _convert_message_role(msg.type), "content": msg.content}
                for msg in messages
            ],
            "temperature": kwargs.get("temperature", self.temperature),
            "max_completion_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        
        headers = {
            "Authorization": f"Bearer {settings.minimax_api_key}",
            "Content-Type": "application/json"
        }
        
        data = self._generate_with_retry(payload, headers)
        
        base_resp = data.get("base_resp", {})
        if base_resp.get("status_code") != 0:
            raise ValueError(f"MiniMax API error: {base_resp.get('status_msg', 'Unknown error')}")
        
        choices = data.get("choices")
        if not choices:
            raise ValueError(f"MiniMax API returned no choices: {data}")
        
        message = choices[0].get("message", {})
        content = message.get("content") or message.get("reasoning_content", "")
        
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=content))]
        )

    @property
    def _llm_type(self) -> str:
        return "minimax"


_minimax_llm = None
_llm_lock = threading.Lock()


def get_llm() -> MiniMaxChat:
    global _minimax_llm
    if _minimax_llm is None:
        with _llm_lock:
            if _minimax_llm is None:
                settings = get_settings()
                _minimax_llm = MiniMaxChat(
                    model=settings.minimax_model,
                    temperature=settings.temperature
                )
    return _minimax_llm


def build_context(chunks: list[SearchChunk], max_chars: int) -> str:
    sections: list[str] = []
    current_size = 0

    for chunk in chunks:
        section = f"[{chunk['file_name']}]\n{chunk['content']}"
        section_size = len(section) + (2 if sections else 0)

        if sections and current_size + section_size > max_chars:
            break

        if not sections and section_size > max_chars:
            sections.append(section[:max_chars].rstrip())
            break

        sections.append(section)
        current_size += section_size

    return "\n\n".join(sections)


def _build_empty_query_response() -> QueryResult:
    answer = EMPTY_KNOWLEDGE_BASE_ANSWER if sqlite.get_documents_count() == 0 else NO_RELEVANT_CHUNKS_ANSWER
    return {"answer": answer, "sources": []}


def query(question: str, top_k: int | None = None) -> QueryResult:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty")
    
    settings = get_settings()
    if top_k is None:
        top_k = settings.top_k
    
    chunks = chroma.search_chunks(question, top_k)
    
    if not chunks:
        return _build_empty_query_response()
    
    context = build_context(chunks, settings.max_context_chars)
    messages = [HumanMessage(content=_build_query_prompt(context, question))]
    llm = get_llm()
    result = llm.invoke(messages)
    
    return {"answer": _extract_response_content(result), "sources": chunks}

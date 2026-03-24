import httpx
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from app.config import get_settings
from app.db import chroma


MINIMAX_API_URL = "https://api.minimaxi.com/v1/text/chatcompletion_v2"


class MiniMaxChat(BaseChatModel):
    model: str = "MiniMax-M2.7"
    temperature: float = 0.7
    max_tokens: int = 2048

    def _generate(
        self,
        messages: list[BaseMessage],
        **kwargs: Any
    ) -> ChatResult:
        settings = get_settings()
        
        def convert_role(msg_type: str) -> str:
            if msg_type == "human":
                return "user"
            return msg_type
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": convert_role(msg.type), "content": msg.content}
                for msg in messages
            ],
            "temperature": kwargs.get("temperature", self.temperature),
            "max_completion_tokens": kwargs.get("max_tokens", self.max_tokens)
        }
        
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                MINIMAX_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
        
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


def get_llm() -> MiniMaxChat:
    global _minimax_llm
    if _minimax_llm is None:
        settings = get_settings()
        _minimax_llm = MiniMaxChat(
            model="MiniMax-M2.7",
            temperature=0.7
        )
    return _minimax_llm


def query(question: str, top_k: int = None) -> dict:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty")
    
    settings = get_settings()
    if top_k is None:
        top_k = settings.top_k
    
    if chroma.get_collection_count() == 0:
        return {
            "answer": "知识库为空，请先上传文档",
            "sources": []
        }
    
    chunks = chroma.search_chunks(question, top_k)
    
    if not chunks:
        return {
            "answer": "未找到相关文档片段，请尝试其他问题",
            "sources": []
        }
    
    context = "\n\n".join([
        f"[{chunk['file_name']}]\n{chunk['content']}"
        for chunk in chunks
    ])
    
    prompt = f"""基于以下文档内容回答问题。如果文档中没有相关信息，请说明无法回答。

文档内容：
{context}

问题：{question}

回答："""
    
    messages = [BaseMessage(type="user", content=prompt)]
    llm = get_llm()
    result = llm.invoke(messages)
    
    return {
        "answer": result.content if hasattr(result, 'content') else str(result),
        "sources": chunks
    }

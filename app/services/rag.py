import threading
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import get_settings
from app.db import chroma


_llm = None
_llm_lock = threading.Lock()


def get_llm():
    global _llm
    if _llm is None:
        with _llm_lock:
            if _llm is None:
                settings = get_settings()
                _llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    openai_api_key=settings.openai_api_key
                )
    return _llm


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
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """基于以下文档内容回答问题。如果文档中没有相关信息，请说明无法回答。"""),
        ("user", """文档内容：
{context}

问题：{question}

回答：""")
    ])
    
    chain = prompt | get_llm()
    
    response = chain.invoke({
        "context": context,
        "question": question
    })
    
    return {
        "answer": response.content,
        "sources": chunks
    }

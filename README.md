# Private RAG Knowledge Base

个人 RAG 知识库，基于主流 AI 技术栈构建，适合 AI 应用开发学习与实践。

## 功能目标

| 功能 | 状态 | 说明 |
|------|------|------|
| Markdown 文档上传 | ✅ 完成 | 支持 .md 文件内容上传 |
| 文档分块处理 | ✅ 完成 | 默认 500 字符/块，可配置 |
| 向量存储 | ✅ 完成 | Chroma 持久化存储 |
| 语义检索 | ✅ 完成 | 基于 embedding 相似度匹配 |
| RAG 问答 | ✅ 完成 | OpenAI GPT-3.5-turbo |
| 文档管理 | ✅ 完成 | 完整 CRUD 操作 |
| 前端界面 | 🔄 开发中 | 简洁扁平化 Web UI |
| 本地模型支持 | 📋 规划中 | Ollama 集成 |

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **语言** | Python 3.10+ | AI 领域主流 |
| **API 框架** | FastAPI | 高性能、自动文档 |
| **RAG 框架** | LangChain | 市场认可度高 |
| **向量数据库** | Chroma | 专为 RAG 设计 |
| **元数据存储** | SQLite | 零配置、轻量级 |
| **LLM** | OpenAI API | gpt-3.5-turbo |
| **Embedding** | text-embedding-3-small | 性价比最高 |
| **前端** | React + TailwindCSS | 规划中 |

## 项目进度

```
[███████████████████░░░░░░░░] 75%

后端开发     ████████████████████ 100%
前端界面     ████████░░░░░░░░░░░░░ 30%
文档完善     ██████████████░░░░░░░░ 60%
测试覆盖     ████████████░░░░░░░░░░ 50%
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入你的 OPENAI_API_KEY
```

### 3. 启动服务

```bash
python3 -m app.main
```

服务启动后访问：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## API 接口

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/documents` | 上传文档 |
| GET | `/documents` | 获取文档列表 |
| GET | `/documents/{id}` | 获取文档详情 |
| DELETE | `/documents/{id}` | 删除文档 |
| POST | `/query` | RAG 问答 |
| GET | `/health` | 健康检查 |

### 上传文档示例

```bash
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"file_content": "# RAG\n\nRAG是检索增强生成技术。", "file_name": "rag-intro.md"}'
```

### 问答示例

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "什么是RAG？", "top_k": 3}'
```

## 项目结构

```
private-rag
├── app/
│   ├── api/routes.py          # API 路由
│   ├── config.py              # 配置管理
│   ├── db/
│   │   ├── chroma.py         # Chroma 向量库
│   │   └── sqlite.py         # SQLite 元数据
│   ├── models/schemas.py      # Pydantic 模型
│   ├── services/
│   │   ├── document.py       # 文档处理
│   │   └── rag.py            # RAG 核心
│   └── main.py               # FastAPI 入口
├── data/                      # 数据持久化
├── tests/                     # 测试
├── spec/                      # 规范文档
├── requirements.txt
├── .env.example
└── README.md
```

## 数据流

```
用户上传 MD 文档
       ↓
   文档解析
       ↓
   文本分块 (500字符/块)
       ↓
   Embedding 生成
       ↓
   Chroma 存储
       ↓
用户问题 → Embedding → 语义检索 (top_k) → 上下文组装 → LLM 生成 → 返回答案
```

## 运行测试

```bash
# 单元测试
python3 -m pytest tests/test_document.py -v

# API 测试
python3 -m pytest tests/test_api.py -v
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENAI_API_KEY` | - | OpenAI API 密钥（必填） |
| `CHUNK_SIZE` | 500 | 分块大小 |
| `CHUNK_OVERLAP` | 50 | 分块重叠 |
| `TOP_K` | 5 | 检索数量 |
| `CHROMA_DIR` | ./data/chroma | Chroma 存储路径 |
| `DB_PATH` | ./data/app.db | SQLite 路径 |

## 学习资源

- [LangChain Documentation](https://python.langchain.com/docs)
- [Chroma Documentation](https://docs.trychroma.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## License

MIT

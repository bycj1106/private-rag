# Private RAG Knowledge Base

个人 RAG 知识库，基于主流 AI 技术栈构建，适合 AI 应用开发学习与实践。

## 功能目标

| 功能 | 状态 | 说明 |
|------|------|------|
| Markdown 文档上传 | ✅ 完成 | 支持 .md 文件内容上传 |
| 文档分块处理 | ✅ 完成 | 默认 500 字符/块，可配置 |
| 向量存储 | ✅ 完成 | Chroma 持久化存储 |
| 语义检索 | ✅ 完成 | 基于 embedding 相似度匹配 |
| RAG 问答 | ✅ 完成 | MiniMax-M2.7 |
| 文档管理 | ✅ 完成 | 完整 CRUD 操作 |
| 前端界面 | ✅ 完成 | React + TailwindCSS + Vite |
| 本地模型支持 | ✅ 完成 | Ollama embedding 可选 |

## 技术栈

### 后端

| 层级 | 技术 | 说明 |
|------|------|------|
| **语言** | Python 3.10+ | AI 领域主流 |
| **API 框架** | FastAPI | 高性能、自动文档 |
| **RAG 框架** | LangChain | 市场认可度高 |
| **向量数据库** | Chroma | 专为 RAG 设计 |
| **元数据存储** | SQLite | 零配置、轻量级 |
| **LLM** | MiniMax API | MiniMax-M2.7 |

### 前端

| 层级 | 技术 | 说明 |
|------|------|------|
| **框架** | React 18 + TypeScript | 主流前端框架 |
| **构建工具** | Vite | 快速开发体验 |
| **样式** | TailwindCSS | 原子化 CSS |
| **路由** | React Router v6 | SPA 路由管理 |

## 项目进度

```
后端开发     ████████████████████ 100%
前端界面     ████████████████████ 100%
代码优化     ████████████████████ 100%
测试完善     ████████████████████ 100%
文档部署     ████████████████████ 100%
```

**状态**: ✅ 所有功能已完成并稳定运行

## 快速开始

### 1. 克隆项目

```bash
cd ~/personal
git clone <repository-url>
cd private-rag
```

### 2. 配置后端

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example env/.env
# 编辑 env/.env，填入你的 MINIMAX_API_KEY
```

### 3. 配置前端

```bash
cd frontend
npm install
```

### 4. 启动服务

```bash
# 终端 1: 后端 (端口 8000)
cd ~/personal/private-rag
source .venv/bin/activate
python3 -m app.main

# 终端 2: 前端 (端口 5173)
cd ~/personal/private-rag/frontend
npm run dev
```

> **架构说明**：后端使用 `create_app()` 工厂模式创建 FastAPI 应用，路由同时注册在 `/` 和 `/api` 两个路径下，接口完全等价。前端默认调用 `/api/*` 路径。

### 5. 访问应用

- **前端界面**: http://localhost:5173
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

## 项目结构

```
private-rag
├── app/                          # 后端代码
│   ├── api/routes.py             # API 路由
│   ├── config.py                 # 配置管理
│   ├── db/
│   │   ├── chroma.py             # Chroma 向量库
│   │   └── sqlite.py             # SQLite 元数据
│   ├── models/schemas.py         # Pydantic 模型
│   ├── services/
│   │   ├── document.py           # 文档处理
│   │   └── rag.py                # RAG 核心
│   └── main.py                   # FastAPI 入口 (create_app 工厂模式)
├── frontend/                      # 前端代码
│   ├── src/
│   │   ├── components/           # 组件
│   │   │   ├── Feedback.tsx      # MessageBanner, LoadingState, StatusCard
│   │   │   ├── Layout.tsx        # 导航布局
│   │   │   ├── QueryResult.tsx   # AnswerCard, SourceList
│   │   │   └── Toast.tsx         # Toast 通知
│   │   ├── pages/                # 页面
│   │   │   ├── UploadPage.tsx    # 上传文档
│   │   │   ├── DocumentsPage.tsx # 文档列表
│   │   │   ├── DocumentDetailPage.tsx  # 文档详情
│   │   │   └── QueryPage.tsx     # 知识问答
│   │   ├── hooks/                # React Hooks
│   │   │   └── useToast.ts       # Toast 状态管理
│   │   ├── services/api.ts       # API 调用
│   │   ├── App.tsx               # 应用入口
│   │   └── index.css             # 全局样式
│   ├── tailwind.config.js        # Tailwind 配置
│   ├── vite.config.ts            # Vite 配置
│   └── package.json
├── data/                          # 数据持久化
├── tests/                         # 测试
├── docker/                        # Docker 配置
├── spec/                          # 规范文档
│   ├── SPEC.md                    # 项目规格文档
│   └── architecture-rag-knowledge-base.md  # 详细架构文档
├── requirements.txt               # Python 依赖
└── README.md
```

## 核心页面

| 页面 | 路由 | 功能 |
|------|------|------|
| 上传文档 | `/` | 上传 Markdown 文档到知识库 |
| 文档列表 | `/documents` | 查看和删除已上传文档 |
| 文档详情 | `/documents/:id` | 查看文档内容和 Markdown 渲染 |
| 知识问答 | `/query` | 基于知识库内容进行问答 |

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

## API 文档

### 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`

### 端点

#### 健康检查

```
GET /health
```

响应:
```json
{
  "status": "ok",
  "timestamp": "2026-03-25T12:00:00Z",
  "database": "ok",
  "vector_store": "ok"
}
```

#### 上传文档

```
POST /documents
```

请求:
```json
{
  "file_content": "# 文档标题\n\n文档内容...",
  "file_name": "my-doc.md"
}
```

响应 (201):
```json
{
  "id": "uuid-string",
  "file_name": "my-doc.md",
  "chunk_count": 3,
  "created_at": "2026-03-25T12:00:00Z"
}
```

#### 获取文档列表

```
GET /documents?page=1&page_size=50
```

响应:
```json
{
  "documents": [...],
  "total": 10,
  "page": 1,
  "page_size": 50
}
```

#### 获取文档详情

```
GET /documents/{id}
```

响应:
```json
{
  "id": "uuid-string",
  "file_name": "my-doc.md",
  "content": "# 文档标题\n\n文档内容...",
  "chunk_count": 3,
  "created_at": "2026-03-25T12:00:00Z"
}
```

#### 删除文档

```
DELETE /documents/{id}
```

响应:
```json
{
  "message": "Document deleted successfully",
  "id": "uuid-string"
}
```

#### 知识问答

```
POST /query
```

请求:
```json
{
  "question": "我的文档主要内容是什么?",
  "top_k": 5
}
```

响应:
```json
{
  "answer": "根据文档内容，您的文档主要讲述了...",
  "sources": [
    {
      "content": "文档片段内容",
      "file_name": "my-doc.md",
      "relevance_score": 0.75
    }
  ]
}
```

### 错误响应

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 404 | 文档不存在 |
| 422 | 请求验证失败 |
| 500 | 服务器内部错误 |

## 运行测试

### 后端测试

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行所有测试
python3 -m pytest tests/ -v

# 单元测试
python3 -m pytest tests/test_document.py -v

# API 测试
python3 -m pytest tests/test_api.py -v

# Query 测试
python3 -m pytest tests/test_query.py -v
```

### 前端测试

```bash
cd frontend

# 运行测试
npm run test

# 运行测试 (单次)
npm run test:run
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MINIMAX_API_KEY` | - | MiniMax API 密钥（必填） |
| `OPENAI_API_KEY` | - | MiniMax API 密钥（别名，与 MINIMAX_API_KEY 等效） |
| `MINIMAX_API_URL` | https://api.minimaxi.com/v1/text/chatcompletion_v2 | MiniMax API 地址 |
| `MINIMAX_MODEL` | MiniMax-M2.7 | MiniMax 模型名称 |
| `TEMPERATURE` | 0.7 | 生成温度 (0.0-2.0) |
| `CHUNK_SIZE` | 500 | 分块大小 (100-100000) |
| `CHUNK_OVERLAP` | 50 | 分块重叠 (0-10000) |
| `TOP_K` | 5 | 检索数量 (1-100) |
| `OLLAMA_BASE_URL` | http://localhost:11434 | Ollama 服务地址 |
| `OLLAMA_EMBEDDING_MODEL` | nomic-embed-text | Ollama embedding 模型 |
| `USE_LOCAL_EMBEDDING` | false | 是否使用本地 embedding |
| `API_RETRY_TIMES` | 3 | API 请求重试次数 (1-10) |
| `API_RETRY_DELAY` | 1.0 | API 重试间隔秒数 (0.1-30) |
| `DATA_DIR` | ./data | 数据目录 |
| `CHROMA_DIR` | ./data/chroma | Chroma 存储路径 |
| `DB_PATH` | ./data/app.db | SQLite 路径 |
| `CHROMA_BATCH_SIZE` | 128 | Chroma 批量写入大小 (1-5000) |
| `MAX_CONTEXT_CHARS` | 12000 | RAG 上下文最大字符数 (1000-200000) |
| `CORS_ORIGINS` | ["http://localhost:5173", "http://127.0.0.1:5173"] | CORS 允许的源列表 |

## 使用 Ollama 本地 Embedding

```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 下载 embedding 模型
ollama pull nomic-embed-text

# 3. 启动 Ollama 服务
ollama serve

# 4. 修改 env/.env
USE_LOCAL_EMBEDDING=true

# 5. 重启后端服务
```

## 故障排除

### 问题: `ModuleNotFoundError: No module named 'fastapi'`

**解决**: 虚拟环境未激活或依赖未安装
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 问题: 前端无法连接后端 API

**解决**: 检查 CORS 配置和后端服务状态
```bash
curl http://localhost:8000/health
# 或
curl http://localhost:8000/api/health
```

### 问题: 问答返回"知识库为空"

**解决**: 先上传文档再进行问答

### 问题: API 请求超时

**解决**: 增加 `API_RETRY_TIMES` 或检查网络连接

### 问题: Chroma 或 SQLite 连接异常

**解决**: 检查 `DATA_DIR`、`CHROMA_DIR`、`DB_PATH` 配置是否正确，数据目录是否存在

## 学习资源

- [LangChain Documentation](https://python.langchain.com/docs)
- [Chroma Documentation](https://docs.trychroma.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [MiniMax API Documentation](https://platform.minimaxi.com/docs)
- [React Documentation](https://react.dev)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

## License

MIT

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
| 前端界面 | 🔄 开发中 | React + TailwindCSS + Vite |
| 本地模型支持 | 📋 规划中 | Ollama 集成 |

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
前端界面     ████░░░░░░░░░░░░░░░░ 20%
```

## 快速开始

### 后端启动

```bash
# 1. 安装后端依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example env/.env
# 编辑 env/.env，填入你的 MiniMax API Key

# 3. 启动后端服务
python3 -m app.main
```

### 前端启动

```bash
# 1. 安装前端依赖
cd frontend
npm install

# 2. 启动前端开发服务器
npm run dev
```

服务启动后：
- **后端 API**: http://localhost:8000
- **前端界面**: http://localhost:5173
- **API 文档**: http://localhost:8000/docs

## 项目结构

```
private-rag
├── app/                        # 后端代码
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
├── frontend/                    # 前端代码
│   ├── src/
│   │   ├── components/       # 组件
│   │   ├── pages/           # 页面
│   │   ├── services/api.ts  # API 调用
│   │   ├── App.tsx          # 应用入口
│   │   └── index.css        # 全局样式
│   ├── tailwind.config.js   # Tailwind 配置
│   ├── vite.config.ts        # Vite 配置
│   └── package.json
├── data/                      # 数据持久化
├── tests/                     # 测试
├── spec/                      # 规范文档
├── requirements.txt           # Python 依赖
└── README.md
```

## 核心页面

| 页面 | 路由 | 功能 |
|------|------|------|
| 上传文档 | `/` | 上传 Markdown 文档到知识库 |
| 文档列表 | `/documents` | 查看和删除已上传文档 |
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
| `OPENAI_API_KEY` | - | MiniMax API 密钥（必填） |
| `CHUNK_SIZE` | 500 | 分块大小 |
| `CHUNK_OVERLAP` | 50 | 分块重叠 |
| `TOP_K` | 5 | 检索数量 |
| `CHROMA_DIR` | ./data/chroma | Chroma 存储路径 |
| `DB_PATH` | ./data/app.db | SQLite 路径 |

## 学习资源

- [LangChain Documentation](https://python.langchain.com/docs)
- [Chroma Documentation](https://docs.trychroma.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [MiniMax API Documentation](https://platform.minimaxi.com/docs)
- [React Documentation](https://react.dev)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

## License

MIT

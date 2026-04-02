# Private RAG Knowledge Base - TODO

## 项目进度

```
后端开发     ████████████████████ 100%
前端界面     ████████████████████ 100%
代码优化     ████████████████████ 100%
测试完善     ████████████████████ 100%
文档部署     ████████████████████ 100%
```

---

## 待办任务

### P0 - 前端界面开发

#### Phase 1: 项目初始化 ✅
- [x] 初始化 React + Vite 项目
- [x] 配置 TailwindCSS
- [x] 配置 TypeScript
- [x] 配置 ESLint + Prettier
- [x] 搭建基础组件 (Layout, Header)

#### Phase 2: 核心页面 ✅
- [x] 文档上传页面
  - [x] Markdown 内容输入框
  - [x] 文件名输入
  - [x] 上传按钮
  - [x] 上传结果展示
- [x] 文档列表页面
  - [x] 文档列表展示
  - [x] 文档删除功能
- [x] 问答页面
  - [x] 问题输入框
  - [x] 回答展示区
  - [x] 来源文档展示

#### Phase 3: 增强功能 ✅
- [x] 文档详情页面
  - [x] DocumentDetailPage 组件
  - [x] Markdown 渲染 (react-markdown + remark-gfm)
  - [x] 路由 `/documents/:id`
- [x] 响应式设计
  - [x] TailwindCSS Typography 插件
- [x] 加载状态处理
  - [x] Loading/Spinner 组件
- [x] 错误提示处理
  - [x] Toast 组件
  - [x] useToast hook

---

### P1 - 代码优化

- [x] MiniMax API 配置移至 env 文件
- [x] Embedding 模型切换为本地模型 (Ollama)
- [x] 添加 API 请求重试机制

---

### P2 - 测试完善

- [x] Query endpoint 集成测试
- [x] 端到端 RAG 流程测试
- [x] 前端组件单元测试 (Vitest + RTL)

---

### P3 - 文档与部署

- [x] 完善 README.md
- [x] API 文档
- [x] 部署脚本/配置 (Docker + docker-compose)

---

## 技术选型

| 类别 | 技术 |
|------|------|
| 前端框架 | React 18 + TypeScript |
| 构建工具 | Vite |
| UI 样式 | TailwindCSS + Typography 插件 |
| Markdown | react-markdown + remark-gfm |
| 路由 | React Router v6 |
| HTTP 客户端 | fetch (内置) |
| 包管理 | npm |

---

## 页面规划

| 路由 | 页面 | 状态 |
|------|------|------|
| `/` | 上传页 | ✅ |
| `/documents` | 文档列表 | ✅ |
| `/documents/:id` | 文档详情 | ✅ |
| `/query` | 问答页 | ✅ |

---

## 前端目录结构

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Layout.tsx
│   │   ├── Loading.tsx
│   │   ├── Toast.tsx
│   │   └── index.ts
│   ├── pages/
│   │   ├── UploadPage.tsx
│   │   ├── DocumentsPage.tsx
│   │   ├── QueryPage.tsx
│   │   ├── DocumentDetailPage.tsx
│   │   └── index.ts
│   ├── hooks/
│   │   └── useToast.ts
│   ├── services/
│   │   └── api.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── tailwind.config.js
├── vite.config.ts
├── package.json
└── tsconfig.json
```

---

## 启动方式

```bash
# 后端 (端口 8000)
python3 -m app.main

# 前端 (端口 5173)
cd frontend && npm run dev
```

前端默认代理 `/api` 请求到 `http://localhost:8000`。

---

## 更新日志

### 2026-03-25
- [x] 前端界面 Phase 3 完成
  - [x] DocumentDetailPage 完成
  - [x] Markdown 渲染 (react-markdown + remark-gfm)
  - [x] Toast 通知组件
  - [x] Loading 组件
- [x] 前端构建通过 (tsc + vite build)
- [x] 前端 Lint 检查通过
- [x] 更新 README.md 和 TODO.md 进度
- [x] 修复测试隔离问题 (test_query_empty_knowledge_base 移至正确位置)
- [x] P1 代码优化完成
  - [x] MiniMax API URL 移至 env 配置
  - [x] Ollama embedding 支持 (USE_LOCAL_EMBEDDING=true 启用)
  - [x] API 请求重试机制 (默认 3 次，指数退避)
  - [x] 添加 langchain-ollama 依赖
- [x] 代码审查修复
  - [x] CORS 配置修复 (限制来源)
  - [x] 添加 env/.env 到 .gitignore
  - [x] 修复测试类重复定义 (TestQueryEndpoint)
  - [x] 修复 get_embedding_function 线程安全 (添加锁)
  - [x] HTTP 连接池 (httpx 共享客户端)
  - [x] 文档列表分页支持
  - [x] 健康检查增强 (检查 SQLite 和 Chroma)
  - [x] Markdown XSS 防护 (rehype-sanitize)
  - [x] 输入验证 (maxLength)
  - [x] 类型导入修复 (SourceDocument)
  - [x] 空 chunk 过滤
  - [x] Race condition 修复 (DocumentDetailPage)
  - [x] useCallback 优化 (useToast)
  - [x] 配置验证 (Pydantic Field validators)
- [x] P2 测试完善完成
  - [x] 添加 pytest conftest.py (测试fixtures)
  - [x] 新增 test_query.py (分页、健康检查测试)
  - [x] 前端测试设置 (Vitest + RTL)
  - [x] useToast hook 单元测试
  - [x] 23 个后端测试全部通过
  - [x] 4 个前端测试全部通过
- [x] P3 文档与部署完成
  - [x] 完善 README.md (API文档、故障排除、Ollama使用指南)
  - [x] Docker 配置 (Dockerfile, Dockerfile.frontend)
  - [x] docker-compose.yml
  - [x] 更新 .env.example

### 2026-03-24
- [x] 后端 API 开发完成
- [x] MiniMax-M2.7 集成
- [x] Chroma 向量存储
- [x] SQLite 元数据存储
- [x] 单元测试通过
- [x] Phase 1 前端项目初始化完成
- [x] Phase 2 核心页面完成
- [x] Phase 3 增强功能 (详情页、Markdown、Toast、Loading)

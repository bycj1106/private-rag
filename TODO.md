# Private RAG Knowledge Base - TODO

## 项目进度

```
后端开发     ████████████████████ 100%
前端界面     ████░░░░░░░░░░░░░░░░░ 20%

Phase 1     ████████████████████ 100%
Phase 2     ░░░░░░░░░░░░░░░░░░░░  0%
Phase 3     ░░░░░░░░░░░░░░░░░░░░  0%
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

#### Phase 2: 核心页面
- [ ] 文档上传页面
  - [x] Markdown 内容输入框
  - [x] 文件名输入
  - [x] 上传按钮
  - [x] 上传结果展示
- [ ] 文档列表页面
  - [x] 文档列表展示
  - [x] 文档删除功能
- [ ] 问答页面
  - [x] 问题输入框
  - [x] 回答展示区
  - [x] 来源文档展示

#### Phase 3: 增强功能
- [ ] 文档详情页面
- [ ] 响应式设计
- [ ] 加载状态处理
- [ ] 错误提示处理

---

### P1 - 代码优化

- [ ] MiniMax API 配置移至 env 文件
- [ ] Embedding 模型切换为本地模型
- [ ] 添加 API 请求重试机制

---

### P2 - 测试完善

- [ ] Query endpoint 集成测试
- [ ] 端到端 RAG 流程测试
- [ ] 前端组件单元测试

---

### P3 - 文档与部署

- [ ] 完善 README.md
- [ ] API 文档
- [ ] 部署脚本/配置

---

## 技术选型

| 类别 | 技术 |
|------|------|
| 前端框架 | React 18 + TypeScript |
| 构建工具 | Vite |
| UI 样式 | TailwindCSS |
| 状态管理 | React Context / useState |
| HTTP 客户端 | fetch (内置) |
| 包管理 | npm |

---

## 页面规划

```
/                    → 首页/上传页
/documents           → 文档列表
/documents/:id       → 文档详情 (Phase 3)
/query               → 问答页
```

---

## 前端目录结构

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Layout.tsx
│   │   └── index.ts
│   ├── pages/
│   │   ├── UploadPage.tsx
│   │   ├── DocumentsPage.tsx
│   │   ├── QueryPage.tsx
│   │   └── index.ts
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
cd backend && python3 -m app.main

# 前端 (端口 5173)
cd frontend && npm run dev
```

前端默认代理 `/api` 请求到 `http://localhost:8000`。

---

## 更新日志

### 2026-03-24
- [x] 后端 API 开发完成
- [x] MiniMax-M2.7 集成
- [x] Chroma 向量存储
- [x] SQLite 元数据存储
- [x] 单元测试通过
- [x] Phase 1 前端项目初始化完成

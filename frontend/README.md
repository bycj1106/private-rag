# Private RAG Frontend

Private RAG Knowledge Base 的前端界面，基于 React + TypeScript + Vite 构建。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | React 18 + TypeScript |
| 构建工具 | Vite |
| 样式 | TailwindCSS + Typography 插件 |
| Markdown | react-markdown + remark-gfm + rehype-sanitize |
| 路由 | React Router v6 |
| 测试 | Vitest + @testing-library/react |

## 目录结构

```
frontend/
├── src/
│   ├── components/          # 可复用组件
│   │   ├── Header.tsx
│   │   ├── Layout.tsx
│   │   ├── Loading.tsx
│   │   └── Toast.tsx
│   ├── pages/              # 页面组件
│   │   ├── UploadPage.tsx
│   │   ├── DocumentsPage.tsx
│   │   ├── DocumentDetailPage.tsx
│   │   └── QueryPage.tsx
│   ├── hooks/              # React Hooks
│   │   └── useToast.ts
│   ├── services/           # API 服务
│   │   └── api.ts
│   ├── App.tsx             # 应用入口
│   ├── main.tsx
│   └── index.css           # 全局样式
├── tailwind.config.js
├── vite.config.ts
├── package.json
└── tsconfig.json
```

## 路由

| 路由 | 页面 |
|------|------|
| `/` | 上传文档页面 |
| `/documents` | 文档列表页面 |
| `/documents/:id` | 文档详情页面 |
| `/query` | 知识问答页面 |

## 开发

```bash
# 安装依赖
npm install

# 开发模式 (端口 5173)
npm run dev

# 类型检查
npm run build

# 代码检查
npm run lint

# 修复代码风格
npm run lint:fix

# 格式化代码
npm run format

# 运行测试
npm run test

# 运行测试 (单次)
npm run test:run
```

## API 代理

开发环境下，Vite 配置了代理将 `/api` 请求转发到 `http://localhost:8000`。

生产环境需确保后端 CORS 配置允许前端域名访问。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `VITE_API_BASE` | `/api` | API 基础路径 |

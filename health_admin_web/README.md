# 个人健康管理系统 - Vue3 管理后台

## 项目简介

基于 Vue 3 + Vite + Element Plus 构建的个人健康管理系统 Web 管理后台，提供数据可视化 Dashboard、用户管理、健康记录管理、健康计划管理、健康资讯发布管理、系统配置等功能。

## 技术栈

| 技术 | 版本 | 说明 |
| --- | --- | --- |
| Vue | 3.4+ | 前端框架 |
| Vite | 5.0+ | 构建工具 |
| Element Plus | 2.4+ | UI 组件库 |
| Vue Router | 4.2+ | 路由管理 |
| Pinia | 2.1+ | 状态管理 |
| Axios | 1.6+ | HTTP 请求库 |
| ECharts | 5.4+ | 数据可视化图表 |
| XLSX | - | Excel 导出 |

## 快速开始

### 1. 安装依赖

```powershell
cd health_admin_web
npm install
```

### 2. 配置环境变量

编辑 `.env` 文件（开发环境）：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

编辑 `.env.production` 文件（生产环境）：

```env
VITE_API_BASE_URL=https://your-domain.com/api
```

### 3. 启动开发服务器

```powershell
npm run dev
```

浏览器打开：`http://localhost:5173`

### 4. 构建生产版本

```powershell
npm run build
```

构建产物输出到 `dist/` 目录。

### 5. 预览生产构建

```powershell
npm run preview
```

## 登录说明

管理后台需要使用 Django 超级管理员账号登录。如果还没有，请先在后端项目中执行：

```powershell
cd health_manage_backend
py manage.py createsuperuser
```

按提示设置用户名和密码，然后启动后端服务：

```powershell
py manage.py runserver 0.0.0.0:8000
```

## 项目结构

```
health_admin_web/
├── src/
│   ├── api/              # API 请求模块（按业务模块分类）
│   ├── assets/           # 静态资源（图片、样式等）
│   ├── components/       # 公共组件
│   ├── router/           # Vue Router 路由配置
│   ├── store/            # Pinia 状态管理（用户、全局设置）
│   ├── utils/            # 工具类（请求封装、格式化等）
│   ├── views/            # 页面视图
│   │   ├── Dashboard/    # 数据看板首页
│   │   ├── users/        # 用户管理页面
│   │   ├── records/      # 健康记录管理（体征/饮食/运动）
│   │   ├── plans/        # 健康计划管理
│   │   ├── news/         # 健康资讯管理
│   │   └── settings/     # 系统配置（AI密钥等）
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── .env                  # 开发环境变量
├── .env.production       # 生产环境变量
├── vite.config.js        # Vite 配置
└── package.json          # 项目依赖清单
```

## 功能模块

| 模块 | 路由路径 | 功能说明 |
| --- | --- | --- |
| **数据看板** | `/dashboard` | 平台总览统计、用户增长趋势图、健康数据分布图 |
| **用户管理** | `/users` | 查看平台用户列表、用户详情、启用/禁用用户 |
| **体征数据** | `/records/body` | 查看和管理用户体征记录（体重/血压/心率/血糖） |
| **饮食记录** | `/records/diet` | 查看和管理用户饮食记录，支持 Excel 导出 |
| **运动记录** | `/records/sport` | 查看和管理用户运动记录 |
| **健康计划** | `/plans` | 管理健康计划，查看计划状态和打卡情况 |
| **资讯管理** | `/news` | 发布健康资讯、管理分类、上下线资讯内容 |
| **系统配置** | `/settings` | 配置 AI 供应商和 API Key（仅管理员） |

## 常见问题

### Q1: 登录失败，提示 401 未认证

**A**: 请确认：
1. 后端 Django 服务已启动（`http://127.0.0.1:8000`）
2. 已通过 `py manage.py createsuperuser` 创建管理员账号
3. `.env` 中的 `VITE_API_BASE_URL` 地址正确

### Q2: 页面加载后图表不显示

**A**: 请确认后端服务正常，且当前登录账号有管理员权限。部分统计数据需要有实际健康记录数据才会显示。

### Q3: 生产部署后 API 请求失败

**A**: 请检查：
1. `.env.production` 中的 API 地址是否正确
2. 后端是否已配置允许跨域（CORS）
3. Nginx 是否正确配置了反向代理

### Q4: 如何修改默认端口

**A**: 编辑 `vite.config.js`，在 `server` 配置项中设置 `port` 字段。

## 生产部署

### 静态文件部署

```powershell
# 1. 构建生产版本
npm run build

# 2. 将 dist/ 目录上传到服务器
# 3. 使用 Nginx 或其他静态文件服务器提供服务
```

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/health_admin_web/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
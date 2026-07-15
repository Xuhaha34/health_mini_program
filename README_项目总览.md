# 个人健康管理系统 - 全栈项目

## 项目概述
这是一个基于三端分离架构的个人健康管理系统，包含：
- **Django 后端 API 服务**：提供数据接口、用户认证、业务逻辑、AI 问答代理
- **微信小程序端**：面向普通用户的健康管理移动端应用
- **Vue3 Web 管理后台**：面向管理员的数据管理和可视化平台

## 技术栈总览

### 1. Django 后端 (health_manage_backend)

| 技术 | 版本 / 说明 | 作用 |
|:---|:---|:---|
| **Python** | 3.10+（开发机 Python 3.12 已测试 | 开发语言 |
| **Django** | 4.2.7 | Web 框架 |
| **Django REST Framework** | 3.14.0 | REST API 框架 |
| **SimpleJWT** | 最新稳定版 | JWT 认证（Token 登录 / 注销 |
| **MySQL + PyMySQL** | MySQL 8.0 | 数据库 + Python 驱动 |
| **Requests** | 最新稳定版 | HTTP 客户端（调用外部大模型 API） |
| **Gunicorn + Nginx** | 可选 | 生产部署（WGSI 服务器 + 反向代理） |

### 2. 微信小程序 (微信小程序代码)

| 技术 | 版本 / 说明 | 作用 |
|:---|:---|:---|
| **WXML / WXSS / JavaScript** | 微信原生小程序三件套 | 页面结构 / 样式 / 逻辑 |
| **ec-canvas（ECharts）** | 小程序版图表组件 | 折线图、饼图、柱状图 |
| **微信原生 API** | wx.request / wx.storage 等 | 网络请求、本地存储 |
| **微信开发者工具** | 最新稳定版 | 开发 / 调试 / 上传 |

### 3. Vue 管理后台 (health_admin_web)

| 技术 | 版本 / 说明 | 作用 |
|:---|:---|:---|
| **Vue** | 3.4+ | 前端框架 |
| **Vite** | 5.0+ | 构建工具（开发服务器 + 打包） |
| **Element Plus** | 2.4+ | UI 组件库 |
| **Vue Router** | 4.2+ | 路由管理 |
| **Pinia** | 2.1+ | 状态管理 |
| **Axios** | 1.6+ | HTTP 请求库 |
| **ECharts** | 5.4+ | 数据可视化图表 |
| **XLSX（SheetJS）** | 最新稳定版 | Excel 导出 |

---

### 整体技术架构图

```
┌──────────────────────────────────────────────────────────────────────────┐
│  用户侧                                                                   │
│  ┌────────────────────────────┐     ┌────────────────────────────────┐ │
│  │  微信小程序               │     │  Vue 管理后台                 │ │
│  │  (WXML / WXSS / JS)        │     │  (Vue3 + Vite + Element Plus) │ │
│  └──────────────┬─────────────┘     └───────────────┬────────────────┘ │
│                 │                                   │                   │
│                 │ HTTP / HTTPS                      │ HTTP / HTTPS     │
└─────────────────┼───────────────────────────────────┼───────────────────┘
                  │                                   │
┌─────────────────▼───────────────────────────────────▼───────────────────┐
│  Django 后端 (health_manage_backend)                                       │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │  Django REST Framework 3.14.0 + SimpleJWT（JWT 认证）            │ │
│  │  5 个业务 App：                                                 │ │
│  │    users / health_record / health_plan / health_news / ai_chat    │ │
│  │  utils：统一响应 / 分页 / 权限 / AI 代理                       │ │
│  └────────────────────────────────┬─────────────────────────────────┘ │
│                                   │ MySQL 8.0 读写                    │
└──────────────────────────────────┬┴───────────────────────────────────┘
                                   │
                      ┌────────────▼────────────┐
                      │  MySQL 数据库         │
                      │  （用户 / 健康记录 /   │
                      │   健康计划 / 资讯 /   │
                      │   AI 对话历史）        │
                      └────────────┬────────────┘
                                   │
                      ┌────────────▼────────────┐
                      │  外部 AI 服务（可选）   │
                      │  OpenAI / DeepSeek /   │
                      │  智谱 / 通义千问 / 豆包 │
                      └─────────────────────────┘
```

---

## 目录结构

```
health_mini_program/                    ← 项目根目录（当前项目所在目录）
├── health_manage_backend/             ← Django 后端
│   ├── apps/                           # 业务应用模块
│   │   ├── users/                  # 用户模块（注册、登录、JWT、个人信息）
│   │   ├── health_record/        # 健康记录（体征、饮食、运动）
│   │   ├── health_plan/          # 健康计划（目标、打卡）
│   │   ├── health_news/          # 健康资讯模块
│   │   └── ai_chat/             # AI 健康问答（对话记录、AI 代理）
│   ├── utils/                           # 工具类
│   │   ├── common_response.py      # 统一响应格式
│   │   ├── pagination.py          # 分页类
│   │   ├── permissions.py       # 权限控制
│   │   └── ai_proxy.py        # AI 接口代理（支持 OpenAI / 智谱 / DeepSeek / 豆包 / 通义千问）
│   ├── sql/                             # 数据库脚本
│   │   ├── init_db.sql           # 建库建表语句
│   │   └── init_data.sql      # 初始数据（含测试账号）
│   ├── deploy/                          # 部署配置
│   │   ├── gunicorn_config.py
│   │   └── nginx.conf
│   ├── health_manage/                 # 项目配置
│   │   ├── settings.py        # 全局配置（数据库 / AI_PROVIDER 在此）
│   │   ├── urls.py           # 总路由
│   │   └── wsgi.py
│   ├── manage.py                      # Django 命令入口
│   ├── requirements.txt               # 依赖清单
│   └── README.md                      # 后端项目说明
│
├── 微信小程序代码/                        # 微信小程序
│   ├── pages/                            # 页面目录（共 11 个页面
│   │   ├── login/              # 登录页
│   │   ├── index/               # 首页（今日概览 + 数据卡片）
│   │   ├── body_data/           # 体征数据记录（体重 / 血压 / 心率 / 血糖）
│   │   ├── diet/                # 饮食记录
│   │   ├── sport/               # 运动记录
│   │   ├── news/               # 资讯列表
│   │   ├── news_detail/         # 资讯详情
│   │   ├── health_plan/       # 健康计划（列表 + 打卡）
│   │   ├── ai_chat/           # AI 健康问答（支持外部大模型 / 本地知识库）
│   │   ├── profile_edit/     # 个人资料编辑
│   │   └── mine/              # 个人中心
│   ├── utils/                          # 工具类
│   │   ├── request.js            # 网络请求封装（自动注入 JWT）
│   │   ├── storage.js           # 本地缓存
│   │   └── format.js            # 数据格式化
│   ├── charts/                         # ECharts 配置
│   │   ├── line_chart.js        # 折线图
│   │   ├── pie_chart.js        # 饼图
│   │   └── bar_chart.js       # 柱状图
│   ├── components/                     # 自定义组件
│   ├── static/                         # 静态资源（图标 / 图片）
│   ├── app.js                          # 小程序全局逻辑
│   ├── app.json                         # 小程序全局配置
│   ├── app.wxss                        # 小程序全局样式
│   ├── project.config.json               # 微信开发者工具项目配置
│   ├── project.private.config.json    # 个人配置
│   └── sitemap.json                     # 索引配置
│
├── health_admin_web/                    # Vue 管理后台
│   ├── src/
│   │   ├── api/                   # 接口请求模块
│   │   │   ├── login.js         # 登录接口
│   │   │   ├── user.js           # 用户管理
│   │   │   ├── record.js         # 健康记录管理
│   │   │   ├── news.js          # 资讯管理
│   │   │   ├── plan.js          # 健康计划管理
│   │   │   └── statistics.js    # 数据统计
│   │   ├── assets/                # 静态资源（CSS / 图标）
│   │   ├── components/           # 公共组件
│   │   ├── router/              # 路由配置
│   │   ├── store/               # Pinia 状态管理
│   │   ├── utils/                # 工具类
│   │   │   ├── request.js    # Axios 封装（自动注入 Token）
│   │   │   ├── format.js    # 格式化工具
│   │   │   ├── export.js    # Excel 导出工具
│   │   │   └── echarts.js   # ECharts 配置
│   │   ├── views/                # 页面视图（登录、首页、用户、记录、资讯、计划、统计）
│   │   ├── App.vue              # 根组件
│   │   └── main.js              # 入口文件
│   ├── .env                              # 开发环境变量
│   ├── .env.production                  # 生产环境变量
│   ├── vite.config.js                      # Vite 配置
│   ├── index.html                         # HTML 模板
│   ├── package.json                       # 依赖清单
│   └── README.md                          # 前端项目说明
│
├── README_项目总览.md                   # 本文件（项目总览 / 快速启动指南）
└── 项目整理说明.md                     # 项目文件整理 / 归档结构建议
```

---

## 快速开始

### 一、后端启动（PowerShell）

1. **打开 PowerShell，进入项目根目录下的 `health_manage_backend`**
```powershell
cd health_manage_backend
```

2. **安装 Python 依赖**（首次使用时执行）
```powershell
pip install -r requirements.txt
```

3. **配置数据库**
- 修改 `health_manage/settings.py` 中的数据库配置（HOST / PORT / USER / PASSWORD / NAME）
- 在 MySQL 中执行 SQL 脚本（可选，或让 Django 自动建表）：
```powershell
mysql -u root -p < sql\init_db.sql
mysql -u root -p health_manage_db < sql\init_data.sql
```

4. **数据库迁移**（让 Django 自动建表，**新增 PlanCheckIn 表** 也会在这里创建）
```powershell
py manage.py makemigrations
py manage.py migrate
```

5. **创建超级管理员**（首次使用时执行）
```powershell
py manage.py createsuperuser
```

6. **启动开发服务器**
```powershell
py manage.py runserver 0.0.0.0:8000
```
- 服务地址：http://127.0.0.1:8000

---

### 二、小程序端运行

1. 打开「**微信开发者工具**」，选择「导入项目」，**选择 `微信小程序代码** 目录作为项目根目录
2. 填写 AppID（**未申请 AppID 的使用「测试号」即可）
3. 修改 `微信小程序代码/app.js` 中的 `baseUrl` 为实际后端地址（例如 `http://127.0.0.1:8000/api`）
4. 编译运行

---

### 三、Vue 管理后台运行

1. **进入 `health_admin_web` 目录并安装依赖**
```powershell
cd health_admin_web
npm install
```

2. **配置环境变量**
- 编辑 `.env` 文件，设置后端 API 地址（例如 `http://127.0.0.1:8000`）

3. **启动开发服务器**
```powershell
npm run dev
```

4. **访问后台**
- 浏览器打开 http://localhost:5173
- 使用管理员账号登录（第 5 步创建的账号）

---

## 核心功能模块

### 1. 用户管理
- 用户注册 / 登录（JWT 认证，SimpleJWT）
- 个人信息管理（头像、昵称、性别、生日、身高、体重）
- 密码修改

### 2. 健康记录
- **体征数据**：体重、血压（收缩压 / 舒张压）、心率、血糖等
- **饮食记录**：餐别、食物、营养成分（卡路里、蛋白质、脂肪、碳水）
- **运动记录**：运动类型、时长、消耗热量
- **数据可视化**：ECharts 折线图 / 饼图 / 柱状图

### 3. 健康计划
- 创建和管理健康目标（减重、增肌、减脂、运动、睡眠、饮食、其他）
- **每日打卡功能**（`PlanCheckIn` 表跟踪每个用户每个计划每天打卡记录）
- 计划进度跟踪（打卡天数、连续打卡、总打卡数）

### 4. 健康资讯
- 资讯分类管理
- 内容发布和上下架
- 浏览量统计

### 5. **AI 健康问答**（**重点新增功能**）
- **智能健康咨询**
- **对话历史记录**（`ChatHistory` 表记录所有对话）
- **多供应商支持**：本地知识库 / OpenAI / 智谱AI / DeepSeek / 通义千问 / 豆包（字节）
- **自动降级**：外部大模型不可用或未配置 API Key 时，**自动回落到本地智能知识库**（保证始终可用）
- **上下文记忆**：每次请求会带上最近 6 条对话历史
- **个性化回答**：会结合当前用户的**年龄 / 性别 / 体重 / 血压 / 血糖 / 健康计划数等数据**

### 6. 数据可视化（后台）
- ECharts 图表展示
- 数据统计分析（用户数量 / 记录趋势 / 按时间维度）
- Excel 导出功能（XLSX）

---

## API 接口规范

### 统一响应格式

所有接口采用以下 JSON 响应格式：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {}
}
```

错误响应示例：

```json
{
    "code": 409,
    "message": "今日已打卡"
}
```

常用 code 说明：
- **200**：成功
- **400**：参数错误
- **401**：未登录 / Token 无效
- **403**：无权限
- **404**：资源不存在
- **409**：重复操作（例如重复打卡）
- **500**：服务端异常

### 主要接口路径

| 模块 | 根路径 | 说明 |
|:---|:---|:---|
| 用户模块 | `/api/users/` | 登录、注册、个人信息、密码修改 |
| 健康记录 | `/api/records/` | 体征、饮食、运动记录 CRUD |
| 健康计划 | `/api/plans/` | 计划 CRUD、`/api/plans/{id}/checkin/` 打卡 |
| 健康资讯 | `/api/news/` | 资讯列表、详情 |
| AI 问答 | `/api/ai/` | `/api/ai/chat/` 对话、`/api/ai/config/` AI 配置 |

### 健康计划打卡接口示例

**POST `/api/plans/{plan_id}/checkin/`**
- 请求：空 JSON（或 `{"note": "今日完成了！"}`）
- 响应：
```json
{
    "code": 200,
    "message": "打卡成功",
    "data": {
        "checked": true,
        "checkin_time": "2026-06-18T12:00:00",
        "checkin_date": "2026-06-18",
        "total_checkins": 5,
        "plan_id": 12,
        "plan_title": "减重计划"
    }
}
```

### AI 对话接口示例

**POST `/api/ai/chat/`**
- 请求：`{"message": "每天运动多久合适？", "session_id": "可选会话ID"}`
- 响应：
```json
{
    "code": 200,
    "message": "操作成功",
    "data": {
        "reply": "每天建议 30-60 分钟中等强度运动...",
        "session_id": "xxx-xxx-xxx",
        "provider": "zhipu",
        "model": "glm-4",
        "from_external": true,
        "user_profile": {
            "age": 35,
            "gender": "男",
            "体重": "70kg",
            "健康计划数": 3
        }
    }
}
```

**GET `/api/ai/config/`**（查看当前生效的 AI 配置，**不会泄露 API Key**）
- 响应：
```json
{
    "code": 200,
    "message": "操作成功",
    "data": {
        "provider": "zhipu",
        "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model": "glm-4",
        "has_api_key": "已配置",
        "temperature": "0.7",
        "max_tokens": "1000",
        "timeout": "30"
    }
}
```

---

## AI 大模型接入说明（重点功能）

### 配置方式

后端 `health_manage_backend/utils/ai_proxy.py` 会**自动读取 `settings.py` 中的变量，再覆盖环境变量**。因此有两种方式切换大模型供应商：

**方式 A：**修改 `health_manage_backend/health_manage/settings.py` 文件末尾：

```python
AI_PROVIDER = "zhipu"   # 可选：local / openai / deepseek / zhipu / qwen / doubao
AI_API_KEY = "你的 API Key"
AI_MODEL = ""            # 留空则使用供应商默认模型
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 1000
AI_TIMEOUT = 30
```

**方式 B：**启动前设置环境变量（推荐生产环境推荐，**避免把密钥写进代码提交到 Git）：

```powershell
$env:AI_PROVIDER = "deepseek"
$env:AI_API_KEY = "你的 API Key"
py manage.py runserver 0.0.0.0:8000
```


### 工作机制

```
用户输入问题
    │
    ▼
Django 后端（/api/ai/chat/）
    │
    ├── 聚合用户体征数据（年龄 / 体重 / 血压等）
    │
    ▼
utils/ai_proxy.py
    │
    ├── 外部大模型可用 + 配置了 API Key
    │       └── HTTP 请求外部大模型接口
    │           └── 回答
    │               └── 成功 → 返回回答
    │               └── 失败 → 自动回落到本地知识库
    │
    └── 未配置 API Key → 本地知识库
                │
                └── LOCAL_KNOWLEDGE 关键词匹配（20+ 条健康主题）
                    │
                    ▼
ChatHistory 表保存对话
    │
    ▼
返回给小程序
```

---

## 部署说明

### 后端部署

1. 配置 Gunicorn：参考 `deploy/gunicorn_config.py`
2. 配置 Nginx：参考 `deploy/nginx.conf`
3. **必须设置环境变量**（AI_API_KEY 等敏感配置
4. 启动服务

```powershell
gunicorn -c deploy/gunicorn_config.py health_manage.wsgi:application
```

### 小程序部署

1. 在微信开发者工具中点击「上传」
2. 在微信公众平台提交审核
3. 审核通过后发布

### 前端部署

1. 构建生产版本：
```powershell
npm run build
```
2. 将 `dist` 目录部署到 Web 服务器（Nginx 等）
3. 配置 Nginx 反向代理（后端 API 接口

---



---

## 常见问题

### Q1：后端启动报错 "ModuleNotFoundError"
A：确保已在 `health_manage_backend` 目录执行 `pip install -r requirements.txt`

### Q2：小程序请求失败
A：检查 `微信小程序代码/app.js` 中的 `baseUrl` 是否正确，确保后端服务已启动
   （Windows 本机开发：`http://127.0.0.1:8000/api`）

### Q3：Vue 后台登录 401
A：确认管理员账号已通过 `createsuperuser` 创建

### Q4：数据库连接失败
A：检查 `settings.py` 中的数据库配置，确保 MySQL 服务已启动，数据库已建库

### Q5：健康计划打卡返回 "计划不存在"
A：普通用户**只能打卡自己创建的计划**，admin 可打卡所有计划

### Q6：AI 问答一直使用本地知识库，没连外部大模型
A：检查 `settings.py` 中 `AI_API_KEY` 是否配置正确，重启 Django 后端

### Q7：如何切换大模型供应商
A：修改 `settings.py` 的 `AI_PROVIDER` 为对应供应商别名，重启后端，重启后端

--

---


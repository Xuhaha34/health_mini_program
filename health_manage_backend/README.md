# 个人健康管理系统 - Django 后端

## 项目简介

基于 Django + Django REST Framework (DRF) 的个人健康管理系统后端服务，提供用户管理、健康记录、健康计划、健康资讯、AI 健康问答等功能模块。采用 JWT 认证方式，支持微信小程序和 Vue 管理后台的数据交互。

## 技术栈

| 技术 | 版本 | 说明 |
| --- | --- | --- |
| Python | 3.10+ | 开发语言 |
| Django | 4.2.7 | Web 框架 |
| Django REST Framework | 3.14.0 | API 框架 |
| SimpleJWT | - | JWT 认证 |
| MySQL | 8.0+ | 数据库 |
| PyMySQL | - | MySQL 驱动 |

## 快速开始

### 1. 安装依赖

```powershell
cd health_manage_backend
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `health_manage/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'health_manage_db',
        'USER': 'root',
        'PASSWORD': '你的MySQL密码',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 3. 初始化数据库

```powershell
# 执行 SQL 脚本创建数据库和表（可选，也可通过 Django 迁移创建）
mysql -u root -p < sql/init_db.sql
mysql -u root -p health_manage_db < sql/init_data.sql

# 或使用 Django 迁移
py manage.py makemigrations
py manage.py migrate
```

### 4. 创建超级管理员

```powershell
py manage.py createsuperuser
```

按提示输入用户名、邮箱、密码。此账号用于登录 Vue 管理后台和 Django Admin。

### 5. 运行开发服务器

```powershell
py manage.py runserver 0.0.0.0:8000
```

API 接口地址：`http://127.0.0.1:8000/api/`
Django Admin：`http://127.0.0.1:8000/admin/`

## 项目结构

```
health_manage_backend/
├── apps/                      # 业务应用模块
│   ├── users/                # 用户模块：注册/登录/个人信息
│   ├── health_record/        # 健康记录模块：体征/饮食/运动
│   ├── health_plan/          # 健康计划模块：计划管理/打卡
│   ├── health_news/          # 健康资讯模块：资讯分类/内容
│   └── ai_chat/              # AI 问答模块：智能健康咨询
├── utils/                     # 工具类
│   ├── common_response.py    # 统一响应格式
│   ├── ai_proxy.py           # AI 代理：多供应商支持
│   ├── pagination.py         # 分页工具
│   └── permissions.py        # 权限控制
├── sql/                       # 数据库脚本
│   ├── init_db.sql           # 数据库表结构
│   └── init_data.sql         # 初始数据
├── deploy/                    # 部署配置
│   ├── gunicorn_config.py    # Gunicorn 配置
│   └── nginx.conf            # Nginx 配置
└── health_manage/            # Django 项目配置
    ├── settings.py           # 项目设置（数据库、AI配置等）
    └── urls.py               # 主路由
```

## API 接口概览

所有接口采用统一响应格式：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {}
}
```

| 模块 | 路由前缀 | 主要功能 |
| --- | --- | --- |
| 用户 | `/api/users/` | 注册、登录、个人信息、修改密码 |
| 健康记录 | `/api/records/` | 体征数据、饮食记录、运动记录 CRUD |
| 健康计划 | `/api/plans/` | 计划 CRUD、每日打卡 |
| 健康资讯 | `/api/news/` | 资讯列表、详情、分类 |
| AI 问答 | `/api/ai/` | 智能问答、AI 配置查询 |
| 平台统计 | `/api/statistics/` | 用户趋势、健康分布、活跃度（仅管理员） |

主要接口示例：
- **登录**：`POST /api/users/login/`
- **注册**：`POST /api/users/register/`
- **体征数据列表**：`GET /api/records/body/`
- **创建饮食记录**：`POST /api/records/diet/`
- **健康计划打卡**：`POST /api/plans/{plan_id}/checkin/`
- **AI 对话**：`POST /api/ai/chat/`

## AI 大模型配置（重点功能）

### 配置方式

后端支持多种 AI 服务供应商，支持本地知识库零配置运行。

**方式 A：修改 settings.py（开发环境）**

在 `health_manage/settings.py` 文件末尾添加或修改：

```python
# AI 大模型配置
AI_PROVIDER = "zhipu"          # 可选: local / openai / deepseek / zhipu / qwen / doubao
AI_API_KEY = "你的 API Key"
AI_MODEL = ""                  # 留空使用供应商默认模型
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 1000
AI_TIMEOUT = 30
```

**方式 B：环境变量（推荐生产环境）**

```powershell
$env:AI_PROVIDER = "deepseek"
$env:AI_API_KEY = "你的 API Key"
py manage.py runserver 0.0.0.0:8000
```

### 工作流程

```
用户输入健康问题
       ↓
Django 后端 /api/ai/chat/
       ↓
  ① 聚合用户体征数据（年龄/体重/血压/血糖/健康计划数）
  ② 读取最近 6 条对话历史作为上下文
       ↓
utils/ai_proxy.py
       ├─ 已配置外部 API Key → HTTP 请求外部大模型
       │                       ├─ 成功 → 返回模型回答
       │                       └─ 失败 → 自动回落到本地知识库
       └─ 未配置 API Key → 使用本地关键词知识库（20+ 健康主题）
       ↓
ChatHistory 表保存用户对话记录
       ↓
  返回格式化响应给小程序/管理后台
```

### 支持的供应商

| 供应商别名 | 说明 | 默认模型 |
| --- | --- | --- |
| `local` | 本地关键词知识库（零配置默认） | - |
| `openai` | OpenAI GPT 系列 | `gpt-3.5-turbo` |
| `deepseek` | DeepSeek 深度求索 | `deepseek-chat` |
| `zhipu` | 智谱 AI（GLM） | `glm-4` |
| `qwen` | 通义千问（阿里） | `qwen-plus` |
| `doubao` | 豆包（字节跳动） | `doubao-pro-32k` |

## 数据库表结构

| 表名 | 说明 |
| --- | --- |
| `users_userinfo` | 用户扩展信息表 |
| `health_record_bodydata` | 体征记录表（体重/血压/心率/血糖） |
| `health_record_dietrecord` | 饮食记录表（餐别/食物/营养成分） |
| `health_record_sportrecord` | 运动记录表（类型/时长/热量） |
| `health_plan_healthplan` | 健康计划表（标题/类型/目标/状态） |
| `health_news_newscategory` | 资讯分类表 |
| `health_news_news` | 资讯内容表 |
| `ai_chat_chathistory` | AI 对话历史记录表 |

## 注意事项

1. **生产环境部署**：请务必修改 `SECRET_KEY`，关闭 `DEBUG = True`
2. **敏感配置**：`AI_API_KEY` 等敏感信息请勿提交到 Git，建议使用环境变量
3. **数据库备份**：定期备份 MySQL 数据库
4. **权限控制**：普通用户只能操作自己的健康数据，管理员可访问平台统计接口
5. **AI 自动降级**：外部大模型不可用时，系统自动回落到本地知识库，保证功能可用

## 部署

详见 `deploy/` 目录下的配置文件：
- `deploy/gunicorn_config.py` - Gunicorn 配置
- `deploy/nginx.conf` - Nginx 反向代理配置

生产部署命令示例：

```bash
# 使用 waitress（Windows 推荐）
pip install waitress
waitress-serve --host=0.0.0.0 --port=8000 health_manage.wsgi:application

# 使用 Gunicorn（Linux）
gunicorn -c deploy/gunicorn_config.py health_manage.wsgi:application
```
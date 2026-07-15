# 个人健康管理系统 - 微信小程序

## 项目简介

基于微信小程序原生框架开发的个人健康管理客户端，提供用户登录注册、健康记录录入、健康计划管理、健康资讯阅读、AI 健康问答等功能。用户可以通过小程序随时记录和管理自己的健康数据。

## 技术栈

| 技术 | 说明 |
| --- | --- |
| 微信小程序原生框架 | WXML + WXSS + JS |
| JWT 认证 | SimpleJWT Token 鉴权 |
| ECharts (小程序版) | 数据可视化图表 |
| RESTful API | 与 Django 后端通信 |

## 快速开始

### 1. 准备工具

- 安装 **微信开发者工具**（从官网下载：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html）

### 2. 导入项目

1. 打开「微信开发者工具」
2. 点击「导入项目」或「+ 导入」
3. 项目目录选择：`微信小程序代码/` 目录
4. AppID：
   - 有正式 AppID：填写自己的小程序 AppID
   - 无 AppID：选择「测试号」即可在本地开发调试
5. 点击「导入」完成

### 3. 配置后端地址

打开 `app.js`，修改 `baseUrl` 为实际后端 API 地址：

```javascript
// app.js
App({
    globalData: {
        baseUrl: 'http://127.0.0.1:8000/api',  // ← 修改这里
        token: ''
    },
    // ...
})
```

**开发环境**：`http://127.0.0.1:8000/api`（需要先启动 Django 后端）
**生产环境**：`https://your-domain.com/api`（需要配置 HTTPS）

### 4. 编译运行

在微信开发者工具中：
- 点击「编译」按钮即可运行小程序
- 默认会进入登录/注册页面
- 首次使用请先注册账号

## 项目结构

```
微信小程序代码/
├── charts/              # ECharts 图表组件目录
├── pages/               # 小程序页面
│   ├── login/           # 登录注册页面
│   ├── index/           # 首页（数据总览 + 资讯）
│   ├── body_data/       # 体征记录页面（体重/血压/心率/血糖）
│   ├── diet/            # 饮食记录页面
│   ├── sport/           # 运动记录页面
│   ├── health_plan/     # 健康计划页面（创建计划 + 打卡）
│   ├── profile_edit/    # 个人信息编辑页面
│   ├── mine/            # 个人中心（头像/统计/功能入口）
│   ├── ai_chat/         # AI 健康问答对话页面
│   ├── news/            # 健康资讯列表页面
│   └── news_detail/     # 健康资讯详情页面
├── utils/               # 工具类
│   ├── request.js       # HTTP 请求封装（统一处理 Token）
│   ├── storage.js       # 本地存储封装（Token/用户信息持久化）
│   └── format.js        # 格式化工具（日期/数字等）
├── app.js               # 小程序入口文件（全局数据 + 登录状态检查）
├── app.json             # 全局配置（页面路由/窗口样式/底部 TabBar）
├── app.wxss             # 全局样式（主题颜色/卡片样式等）
├── project.config.json  # 项目配置文件
└── sitemap.json         # 站点地图配置（小程序搜索优化）
```

## 功能模块

### 1. 用户认证模块

- **登录**：用户名 + 密码，登录成功后保存 JWT Token
- **注册**：新用户注册账号
- **Token 管理**：自动从本地存储读取/刷新 Token
- **会话保持**：重新打开小程序自动恢复登录状态

### 2. 健康记录模块

| 页面 | 功能 | 记录字段 |
| --- | --- | --- |
| **体征数据** (`body_data`) | 记录身体指标 | 日期、体重(kg)、血压(收缩/舒张)、心率(bpm)、血糖(mmol/L)、备注 |
| **饮食记录** (`diet`) | 记录饮食情况 | 日期、餐别(早餐/午餐/晚餐/加餐)、食物名称、热量(kcal)、蛋白质(g)、脂肪(g)、碳水(g) |
| **运动记录** (`sport`) | 记录运动数据 | 日期、运动类型、时长(分钟)、消耗热量(kcal)、备注 |

所有记录支持：创建、查看列表、编辑、删除

### 3. 健康计划模块

- **创建计划**：设置标题、类型（饮食/运动/体征/综合）、目标值、起止日期
- **计划列表**：查看所有计划（进行中/已完成/已放弃）
- **每日打卡**：每个计划每天可打卡一次，记录完成情况
- **进度追踪**：查看打卡天数、连续打卡、总打卡数

### 4. AI 健康问答模块

- **智能对话**：用户输入健康相关问题，AI 给出专业回答
- **对话历史**：自动保存对话记录，支持上下文理解（最近 6 条对话）
- **个性化回答**：AI 结合用户的年龄/性别/体重/血压/血糖/健康计划数等数据给出针对性建议
- **多供应商支持**：后端可配置 OpenAI/DeepSeek/智谱/通义千问/豆包 等大模型
- **零配置可用**：未配置外部 API Key 时自动回落到本地知识库

### 5. 健康资讯模块

- **资讯列表**：按分类浏览健康资讯文章
- **资讯详情**：阅读完整文章内容
- **发布时间**：显示文章发布日期

### 6. 个人中心模块

- **用户头像**：用户名首字作为头像标识
- **统计信息**：健康记录总数、坚持天数、健康计划数
- **信息编辑**：修改昵称、性别、年龄、身高、体重、邮箱
- **功能入口**：快速进入各记录页面
- **清除缓存**：清除小程序本地缓存
- **退出登录**：清除 Token，返回登录页面

## 全局配置说明

### 页面路由（app.json）

小程序的所有页面都需要在 `app.json` 的 `pages` 数组中声明，且数组第一项为默认启动页面。

### 底部 TabBar（app.json）

```json
{
  "tabBar": {
    "list": [
      { "pagePath": "pages/index/index", "text": "首页" },
      { "pagePath": "pages/body_data/body_data", "text": "体征" },
      { "pagePath": "pages/health_plan/health_plan", "text": "计划" },
      { "pagePath": "pages/mine/mine", "text": "我的" }
    ]
  }
}
```

## 网络请求约定

所有 API 请求由 `utils/request.js` 统一封装，自动处理：

- **Token 注入**：自动在请求头中添加 `Authorization: Bearer <token>`
- **统一响应格式**：`{ code, message, data }`
- **错误处理**：401 未认证时自动清理登录状态并提示重新登录
- **网络异常**：网络连接失败时给出友好提示

## 常见问题

### Q1: 打开小程序后提示「网络请求失败」

**A**: 请检查：
1. Django 后端服务是否已启动（`py manage.py runserver 0.0.0.0:8000`）
2. `app.js` 中的 `baseUrl` 是否正确（开发环境：`http://127.0.0.1:8000/api`）
3. 微信开发者工具中勾选「详情」→「本地设置」→「不校验合法域名...」

### Q2: 注册后无法登录

**A**: 请确认 Django 后端服务正常运行，且数据库已正确初始化。可尝试：
```powershell
cd health_manage_backend
py manage.py makemigrations
py manage.py migrate
```

### Q3: AI 问答总是返回本地知识库答案

**A**: 这是正常的「零配置默认行为」。如需接入外部大模型，请在 Django 后端 `settings.py` 中配置：

```python
AI_PROVIDER = "deepseek"  # 或 openai/zhipu/qwen/doubao
AI_API_KEY = "你的 API Key"
```

配置后重启 Django 后端，小程序侧无需改动。

### Q4: 图表不显示或样式错乱

**A**: 请确认：
1. `charts/` 目录中的 ECharts 组件文件完整
2. 有实际的健康记录数据（无数据时图表可能显示为空）
3. 小程序基础库版本 >= 2.2.0

### Q5: 如何发布到线上

**A**: 在微信开发者工具中：
1. 点击「上传」→ 填写版本号和项目备注
2. 登录微信公众平台（mp.weixin.qq.com）→ 版本管理 → 提交审核
3. 审核通过后点击「发布」
4. **注意**：线上版本请求的 API 域名必须配置 HTTPS，并在「开发 → 开发设置 → 服务器域名」中添加白名单

## 与后端 API 通信的主要接口

| 功能 | 方法 | 接口路径 |
| --- | --- | --- |
| 用户注册 | POST | `/api/users/register/` |
| 用户登录 | POST | `/api/users/login/` |
| 获取个人信息 | GET | `/api/users/info/` |
| 更新个人信息 | PUT | `/api/users/info/` |
| 修改密码 | POST | `/api/users/password/change/` |
| 体征数据列表 | GET | `/api/records/body/` |
| 创建体征记录 | POST | `/api/records/body/` |
| 饮食记录列表 | GET | `/api/records/diet/` |
| 创建饮食记录 | POST | `/api/records/diet/` |
| 运动记录列表 | GET | `/api/records/sport/` |
| 创建运动记录 | POST | `/api/records/sport/` |
| 健康计划列表 | GET | `/api/plans/` |
| 创建健康计划 | POST | `/api/plans/` |
| 计划打卡 | POST | `/api/plans/{plan_id}/checkin/` |
| 资讯列表 | GET | `/api/news/` |
| 资讯详情 | GET | `/api/news/{id}/` |
| AI 对话 | POST | `/api/ai/chat/` |
| AI 配置查询 | GET | `/api/ai/config/` |
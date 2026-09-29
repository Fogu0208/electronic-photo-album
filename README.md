# 基于 FastAPI + Vue3 的电子相册管理系统

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vuedotjs&logoColor=white)
![Element Plus](https://img.shields.io/badge/Element%20Plus-2.9-409EFF)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)

一个前后端分离的电子相册管理系统：普通用户可创建相册、上传照片、评论互动、点赞收藏；管理员负责用户、分类、内容审核与数据统计。项目从数据库设计到前后端部署由本人独立完成。

> 演示数据已内置，按下方步骤启动即可直接体验，无需手动造数据。

---

## 一、功能一览

| 模块 | 普通用户 | 管理员 |
|---|---|---|
| 相册 | 创建/编辑/删除自己的相册，设置公开或私密 | 查看并管理全部相册 |
| 照片 | 上传照片、批量管理、查看点赞与浏览数 | 全量照片管理 |
| 广场 | 浏览他人公开相册、查看详情 | — |
| 互动 | 点赞、收藏、发表评论 | 评论审核（通过/驳回） |
| 分类 | 使用分类归档 | 分类增删改查与排序 |
| 内容 | 查看系统公告 | 发布/编辑公告 |
| 账号 | 注册登录、修改资料与密码 | 用户管理（禁用/启用） |
| 数据 | 个人主页统计 | 全站统计看板（ECharts 图表） |
| 审计 | — | 操作日志（记录操作人、IP、行为） |

---

## 二、技术选型

| 层次 | 选型 | 说明 |
|---|---|---|
| 后端 | FastAPI | 原生 async 支持，自动生成 OpenAPI 文档，开发调试成本低 |
| ORM | SQLAlchemy 2.0 | 使用 2.0 风格的 `select()` 查询，类型提示友好 |
| 认证 | PyJWT | 无状态 Token，配合中间件统一鉴权 |
| 配置 | pydantic-settings | 支持 `.env` 覆盖，配置与代码解耦 |
| 前端 | Vue 3 + Vite | 组合式 API（`<script setup>`），构建速度快 |
| UI | Element Plus | 组件齐全，表单/表格/弹窗开箱即用 |
| 状态 | Pinia | 轻量状态管理，持久化登录态 |
| 图表 | ECharts | 统计看板的数据可视化 |
| 数据库 | MySQL 8 | 关系模型，事务支持 |

---

## 三、系统架构

采用经典的分层架构，路由层只做参数接收与响应，业务逻辑收拢在 Service 层：

```
浏览器 (Vue3)
   │  axios 拦截器：自动携带 Token / 统一处理 401
   ▼
Vite 开发服务器  ── 代理 /api、/uploads ──▶  FastAPI  (127.0.0.1:8080)
                                                  │
                                        ┌─────────▼──────────┐
                                        │  HTTP 中间件        │
                                        │  JWT 鉴权 + 白名单  │
                                        │  写入用户上下文     │
                                        └─────────┬──────────┘
                                                  ▼
                                        ┌────────────────────┐
                                        │  Router  路由层     │  参数校验、调用 Service
                                        │  Service 业务层     │  业务规则、事务
                                        │  Model   ORM 层     │  SQLAlchemy 实体
                                        └─────────┬──────────┘
                                                  ▼
                                              MySQL 8
```

一条请求的完整链路（以"发布评论"为例）：

```
POST /api/comment  + Authorization: Bearer <token>
  → 中间件校验 Token，解析出 userId/role 存入 ContextVar
  → Router 接收参数，调用 CommentService
  → Service 校验业务规则，写入 t_comment（status=0 待审核）
  → 统一封装为 {code, msg, data} 返回
  → 前端拦截器识别 code，成功渲染 / 失败提示
```

---

## 四、数据库设计

共 10 张表，围绕"用户 — 相册 — 照片"三级主线展开，互动与审计作为旁路：

| 表名 | 作用 | 关键字段 |
|---|---|---|
| `t_user` | 普通用户 | username、password、status（1 正常 / 0 禁用） |
| `t_admin` | 管理员 | username、password |
| `t_category` | 相册分类 | name、sort_num |
| `t_album` | 相册 | user_id、category_id、is_public、cover、photo_count |
| `t_photo` | 照片 | album_id、user_id、url、file_size、like_count、view_count |
| `t_comment` | 评论 | photo_id、user_id、status（0 待审 / 1 通过 / 2 驳回） |
| `t_like` | 点赞 | photo_id、user_id |
| `t_favorite` | 收藏 | photo_id、user_id |
| `t_notice` | 系统公告 | title、content、admin_id |
| `t_log` | 操作日志 | user_type、user_id、operation、ip |

```
t_user ──1:N──▶ t_album ──1:N──▶ t_photo ──1:N──▶ t_comment
                   │                  │
              t_category         t_like / t_favorite
```

`photo_count`、`like_count` 等冗余计数随业务操作同步维护，避免列表页频繁聚合查询。

---

## 五、关键实现

### 1. JWT 认证中间件 + 路径白名单

鉴权不在每个接口里重复写，而是在 HTTP 中间件统一拦截，公开路径用白名单放行：

```python
PUBLIC_EXACT = {"/api/auth/login", "/api/auth/register", "/api/notice/list"}
PUBLIC_PREFIXES = ("/api/album/public/", "/api/photo/public/", "/uploads31/")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if is_public_path(request.url.path):
        return await call_next(request)
    token = request.headers.get("Authorization")
    ...
    UserContext.set(UserInfo(user_id=..., username=..., role=...))
    try:
        return await call_next(request)
    finally:
        UserContext.clear()   # 请求结束必须清理，避免上下文串号
```

### 2. 基于 ContextVar 的用户上下文

登录用户信息的传递没有用全局变量，而是用 `contextvars.ContextVar`。FastAPI 是异步框架，多个请求协程并发时，`ContextVar` 能保证每个请求拿到的都是自己的用户信息，不会互相污染。业务层通过 `UserContext.get_user_id()` 直接取当前用户，Service 方法签名保持干净。

### 3. 统一响应与全局异常处理

所有接口返回一致结构 `{code, msg, data}`，前端拦截器只需判断 `code`：

```python
class R(BaseModel, Generic[T]):
    @staticmethod
    def ok(data=None):  return {"code": 200, "msg": "操作成功", "data": data}
    @staticmethod
    def fail(msg, code=500): return {"code": code, "msg": msg, "data": None}
```

业务异常（如"用户名已存在"）抛 `BusinessException`，与参数校验异常、未捕获异常分别注册处理器，避免把堆栈直接暴露给前端。

### 4. snake_case → camelCase 自动转换

数据库字段是 `user_id`、`create_time` 这类下划线命名，前端习惯 `userId`、`createTime`。在 `serialize.py` 中做了统一转换，ORM 对象序列化后直接是前端要的格式，不必在每个接口手写字段映射。

### 5. 前端路由守卫与角色隔离

`/admin/*` 与 `/user/*` 两套页面，路由元信息标记所需角色，守卫中比对 `localStorage` 里的角色，越权访问会被重定向回自己的首页；后端同时校验 Token 中的 role，前后端双重把关。

### 6. 文件 uploads 与静态资源映射

上传接口按类型（photo / avatar）分目录存储，文件名用 UUID 重命名避免冲突与路径穿越，再通过 `StaticFiles` 挂载为 `/uploads31` 静态路由供前端直接访问。

---

## 六、快速启动

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8

### 1. 导入数据库

```bash
mysql -u root -p < sql/db_photo_album.sql
```

脚本会创建 `db_photo_album` 库、10 张表，并导入演示数据（7 位用户、10 个相册、31 张照片）。

### 2. 启动后端

```bash
cd server
python -m venv .venv
# Windows
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
# macOS / Linux
python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python main.py
```

接口文档：http://127.0.0.1:8080/docs （FastAPI 自动生成，可直接在线调试）

### 3. 启动前端

```bash
cd client
npm install
npm run dev
```

打开 http://localhost:5173 ，默认代理到后端 8080。

> Windows 用户可直接双击根目录的 `启动项目.bat` 一键启动前后端。

### 演示账号

密码统一为 `123456`：

- 管理员：`python222`、`manager`
- 普通用户：`zhangsan`、`lisi`、`wangwu`、`zhaoliu`、`sunqi`、`zhouba`、`lili`

---

## 七、项目结构

```
.
├── server/                     # FastAPI 后端
│   ├── main.py                 # 入口：中间件、异常处理、路由注册
│   ├── app/
│   │   ├── config.py           # pydantic-settings 配置（支持 .env 覆盖）
│   │   ├── database.py         # 引擎、SessionLocal、get_db 依赖
│   │   ├── models/entities.py  # 10 张表的 ORM 实体
│   │   ├── routers/            # 路由层（auth/user/album/photo/...）
│   │   ├── services/           # 业务层（auth_service / manage_service）
│   │   ├── utils/              # JWT、文件、序列化、IP、用户上下文
│   │   └── common/             # 统一响应 R、业务异常、常量
│   ├── requirements.txt
│   └── .env.example            # 配置模板
├── client/                     # Vue3 前端
│   ├── src/api/                # axios 封装 + 接口定义
│   ├── src/views/admin/        # 后台页面
│   ├── src/views/user/         # 用户端页面
│   ├── src/router/             # 路由 + 权限守卫
│   └── vite.config.js          # 开发代理配置
├── sql/db_photo_album.sql      # 建表 + 演示数据
└── 启动项目.bat                # Windows 一键启动
```

---

## 八、配置说明

后端配置集中在 `server/app/config.py`，可用环境变量或 `.env` 覆盖，**无需改动源码**：

| 变量 | 默认值 | 说明 |
|---|---|---|
| `PORT` | `8080` | 后端端口 |
| `DB_URL` | `mysql+pymysql://root:123456@127.0.0.1:3308/...` | 数据库连接串，注意端口是否为本机的 3306 |
| `UPLOAD_PATH` | `D:/uploads31` | 图片存储目录，按需改为项目内相对路径 |
| `JWT_SECRET` | 内置默认值 | 生产环境务必替换 |

复制 `server/.env.example` 为 `.env` 后修改即可（`.env` 已被 Git 忽略）。

### 关于图片

演示数据中的照片路径形如 `/uploads31/photo/xxx.png`，图片文件体积较大**未纳入 Git 仓库**。缺少图片时页面其他功能不受影响，仅图片占位为空；放入 `server/uploads31/photo/` 与 `server/uploads31/avatar/` 即可正常显示。

---

erfile 与 docker-compose，一键拉起前后端与数据库。

---

## 九、License

MIT

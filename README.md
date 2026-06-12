# API Sentinel

API Sentinel 是一个基于 FastAPI 的后端 API 安全审计与异常访问检测系统。

项目目标不是替代 Prometheus / Grafana 这类通用监控工具，而是聚焦在应用层 API 安全审计：记录请求行为，识别异常访问，并生成安全事件，帮助管理员追踪接口访问风险。

## 项目定位

API Sentinel 关注的问题是：

* 谁访问了系统
* 从哪个 IP 访问
* 访问了哪个接口
* 返回了什么状态码
* 请求耗时多久
* 是否发生异常访问行为
* 是否需要生成安全事件供管理员查看

当前项目已经实现从用户认证到请求审计，再到异常登录检测的基础闭环。

## 技术栈

* Python
* FastAPI
* MySQL
* SQLAlchemy
* Alembic
* Pydantic
* JWT
* passlib + bcrypt
* Docker MySQL
* Swagger UI

## 当前已完成功能

### 1. 项目基础结构

* FastAPI 应用骨架
* `/health` 健康检查接口
* 分层目录结构
* 配置文件管理
* Docker MySQL 本地数据库

### 2. 数据库与 ORM

已通过 SQLAlchemy + Alembic 管理数据库结构。

当前主要数据表：

* `users`
* `request_logs`
* `security_events`
* `alembic_version`

### 3. 用户认证模块

已实现：

* 用户注册 `/auth/register`
* 用户登录 `/auth/login`
* 密码哈希存储
* 密码校验
* JWT 生成与解析
* OAuth2 Password Flow
* Swagger Authorize 登录
* `get_current_user`
* `/users/me` 获取当前用户信息

认证流程：

```text
用户注册
↓
密码哈希后写入 users 表
↓
用户登录
↓
校验密码
↓
签发 JWT
↓
后续请求携带 Bearer Token
↓
后端解析 JWT 并识别当前用户
```

### 4. RBAC 权限控制

系统已支持基于角色的权限控制。

当前用户角色：

* `MEMBER`
* `ADMIN`

管理员接口需要 `ADMIN` 权限。

权限判断逻辑：

```text
请求携带 JWT
↓
get_current_user 解析当前用户
↓
get_current_admin_user 检查 role
↓
非 ADMIN 用户返回 403
```

### 5. 请求审计日志 RequestLog

系统已实现请求日志中间件，会自动记录 API 请求行为。

记录字段包括：

* `user_id`
* `ip_address`
* `method`
* `path`
* `status_code`
* `latency_ms`
* `created_at`

示例：

```text
GET /health 200
POST /auth/login 401
GET /admin/request-logs 403
```

RequestLog 的作用是记录事实：

```text
谁
从哪里
访问了什么接口
结果是什么
耗时多久
```

### 6. 管理员日志查询接口

已实现管理员查询请求日志接口：

```http
GET /admin/request-logs
```

支持分页参数：

```text
limit: 1~100
offset: >=0
```

该接口仅允许 `ADMIN` 用户访问。

### 7. 安全事件 SecurityEvent

系统已实现安全事件表与管理员查询接口。

安全事件字段包括：

* `request_log_id`
* `user_id`
* `event_type`
* `risk_level`
* `source_ip`
* `description`
* `created_at`

管理员查询接口：

```http
GET /admin/security-events
```

该接口仅允许 `ADMIN` 用户访问。

### 8. 登录爆破检测规则

当前已实现第一条安全检测规则：

```text
同一 IP
5 分钟内
/auth/login 登录失败次数 >= 5
↓
生成 LOGIN_BRUTE_FORCE 安全事件
```

生成事件示例：

```json
{
  "event_type": "LOGIN_BRUTE_FORCE",
  "risk_level": "MEDIUM",
  "source_ip": "127.0.0.1",
  "description": "IP 127.0.0.1 failed login 5 times within 5 minutes."
}
```

第一条完整安全检测链路：

```text
登录失败
↓
RequestLog 记录 401
↓
Detector 统计失败次数
↓
SecurityEvent 生成安全事件
↓
Admin API 查询事件
```

## 当前系统架构

```text
Client
  ↓
FastAPI
  ↓
Middleware
  ↓
RequestLog
  ↓
Security Detector
  ↓
SecurityEvent
  ↓
Admin API
```

认证链路：

```text
/auth/register
/auth/login
/users/me
```

审计链路：

```text
Request
↓
RequestLogMiddleware
↓
request_logs
```

检测链路：

```text
request_logs
↓
security_detector
↓
security_events
```

管理链路：

```text
ADMIN User
↓
/admin/request-logs
/admin/security-events
```

## API 列表

### Public

```http
GET /health
POST /auth/register
POST /auth/login
```

### User

```http
GET /users/me
```

### Admin

```http
GET /admin/request-logs
GET /admin/security-events
```

## 本地运行

### 1. 激活虚拟环境

```bash
.\.venv\Scripts\activate
```

### 2. 启动 MySQL 容器

```bash
docker start <mysql-container-name>
```

### 3. 执行数据库迁移

```bash
alembic upgrade head
```

### 4. 启动 FastAPI

```bash
uvicorn app.main:app --reload
```

### 5. 打开 Swagger UI

```text
http://127.0.0.1:8000/docs
```

## 测试流程

### 1. 注册用户

```http
POST /auth/register
```

请求体：

```json
{
  "username": "lrr",
  "password": "123456"
}
```

### 2. 登录用户

```http
POST /auth/login
```

或使用 Swagger 右上角 `Authorize`。

### 3. 查看当前用户

```http
GET /users/me
```

### 4. 修改管理员权限

在数据库中执行：

```sql
UPDATE users
SET role = 'ADMIN'
WHERE username = 'lrr';
```

重新登录后访问管理员接口。

### 5. 查看请求日志

```http
GET /admin/request-logs
```

### 6. 触发登录爆破检测

连续 5 次使用错误密码登录：

```http
POST /auth/login
```

然后查看安全事件：

```http
GET /admin/security-events
```

## 当前项目进度

已完成：

* FastAPI 项目骨架
* MySQL 数据库连接
* SQLAlchemy ORM
* Alembic 迁移
* 用户注册与登录
* 密码哈希
* JWT 认证
* 当前用户识别
* RBAC 管理员权限
* RequestLog 请求审计日志
* 请求日志中间件
* 管理员日志查询接口
* SecurityEvent 安全事件表
* 登录爆破检测规则
* 管理员安全事件查询接口

当前进度：MVP 核心链路基本完成。

## 后续计划

### Phase 6：扩展安全检测规则

计划增加：

* 普通用户访问 `/admin/*` 被 403 时生成安全事件
* 同 IP 高频请求检测
* 高频 401 / 403 检测
* 慢接口异常检测
* 敏感接口访问检测

### Phase 7：事件去重与幂等

当前安全事件通过时间窗口减少重复生成。

后续可增加：

* `dedup_key`
* 时间窗口去重
* 数据库唯一约束
* 事件状态字段

### Phase 8：工程化完善

计划增加：

* `test_auth.py`
* `test_request_log.py`
* `test_security_event.py`
* Docker Compose 一键启动
* README 架构图
* API 示例
* 错误码说明

### Phase 9：可观测性扩展

后期可考虑接入：

* Prometheus
* Grafana
* OpenTelemetry Collector
* Loki / Elasticsearch / ClickHouse

当前项目核心不是通用监控平台，而是应用层 API 安全审计系统。

## 项目总结

API Sentinel 当前已经实现从认证、请求记录、权限控制到异常登录检测的基础安全审计闭环。

一个围绕 API 访问行为构建的后端安全平台雏形。



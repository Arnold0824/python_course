# 后端说明

这个 `server/` 目录是本项目的独立 Node.js 后端服务，主要负责三类事情：

- 接收 GitHub Webhook，触发自动部署
- 记录前端页面访问数据
- 提供后台统计接口，给 `/#/admin/stats` 页面使用

如果你对 Node.js 不熟，可以把它先理解成：

- 前端是 `src/` 里的 Vue 页面
- 后端是 `server/` 里的接口服务
- Nginx 对外提供网站入口
- Node 后端只在服务器本机监听 `127.0.0.1:9001`
- MySQL 负责保存访问统计数据

## 1. 当前后端做了什么

目前已经实现的功能：

- `POST /api/webhooks/github`
  接收 GitHub 的 `push` webhook，请求合法时执行部署脚本
- `POST /api/analytics/page-views`
  接收前端页面访问上报
- `GET /api/admin/analytics/dashboard`
  返回后台统计页需要的汇总数据
- `GET /healthz`
  健康检查接口，用于确认服务是否正常

前端已经接好了自动埋点：

- 用户打开章节页时，会自动上报访问数据
- Vue 路由切换时，也会自动上报
- 后台统计页地址是 `/#/admin/stats`

## 2. 目录结构

```text
server/
├─ package.json                     # 后端自己的依赖和脚本
├─ ecosystem.config.cjs             # PM2 配置
├─ nginx/
│  └─ python-course.conf            # Nginx 反向代理示例
├─ sql/
│  └─ 001_init_page_views.sql       # 访问统计表初始化 SQL
├─ systemd/
│  ├─ python-course-server.service  # Ubuntu systemd 服务文件
│  └─ python-course-server.env.example
└─ src/
   ├─ index.js                      # 服务启动入口
   ├─ app.js                        # Express 应用装配
   ├─ config/
   │  ├─ env.js                     # 读取系统环境变量
   │  └─ paths.js                   # 路径常量
   ├─ controllers/                  # 每个接口的处理逻辑
   ├─ routes/                       # 路由定义
   ├─ services/                     # 数据库、部署、统计等业务逻辑
   ├─ middleware/                   # 中间件
   ├─ db/
   │  └─ index.js                   # MySQL 连接池
   ├─ lib/
   │  └─ logger.js                  # 日志工具
   └─ utils/
      └─ github-signature.js        # GitHub 签名校验
```

## 3. 配置方式

这个后端**不依赖 `.env` 文件**，默认从系统环境变量读取配置。

但根据你当前的要求，MySQL 的以下配置已经直接写死在代码里了：

- 主机：`127.0.0.1`
- 端口：`3306`
- 用户名：`root`
- 数据库名：`python_course`

现在真正需要你提供的只有：

- `MYSQL_PASSWORD`
- `WEBHOOK_SECRET`
- `ADMIN_TOKEN`

其中：

- `MYSQL_PASSWORD`
  MySQL root 用户密码
- `WEBHOOK_SECRET`
  GitHub Webhook 的密钥，必须和 GitHub 仓库里的配置一致
- `ADMIN_TOKEN`
  后台统计接口令牌，前端后台页访问时要输入它

## 4. 环境要求

服务器环境建议：

- Ubuntu
- Node.js 20+
- npm
- MySQL 8.x
- Nginx

本项目根目录和 `server/` 目录各有一个 `package.json`：

- 根目录 `package.json`
  管理前端 Vue 项目
- `server/package.json`
  管理后端 Node 项目

所以安装依赖时不要混淆。

## 5. 本地开发怎么启动

你现在是在 Windows 上开发，真实部署在 Ubuntu，这种方式完全没问题。

### 5.1 安装后端依赖

在项目根目录运行：

```bash
npm --prefix server install
```

或者先进入 `server/` 目录，再执行：

```bash
npm install
```

### 5.2 设置本地环境变量

PowerShell 示例：

```powershell
$env:MYSQL_PASSWORD = "你的数据库密码"
$env:WEBHOOK_SECRET = "你的_webhook_secret"
$env:ADMIN_TOKEN = "你的后台令牌"
```

### 5.3 启动后端

在项目根目录运行：

```bash
npm run server:start
```

或者：

```bash
npm --prefix server run start
```

开发模式热重载：

```bash
npm run server:dev
```

### 5.4 启动前端

前端在项目根目录启动：

```bash
npm run dev
```

现在 `vite.config.js` 已经配置了代理：

- `/api` 会转发到 `http://127.0.0.1:9001`
- `/healthz` 会转发到 `http://127.0.0.1:9001`

所以本地开发时，前端和后端可以分开启动，但浏览器里看起来像同一个站点。

## 6. 数据库初始化

访问统计表结构在：

- [001_init_page_views.sql](/f:/OneDrive/吉利学院/6-2025-2026第二学期/python-202520262/notebook/python_course/server/sql/001_init_page_views.sql)

后端启动时也会尝试自动创建表，所以一般不需要你手工建表。

如果你想手工执行，也可以在 MySQL 里运行该 SQL 文件。

数据库名应为：

```sql
python_course
```

如果数据库还没建，可以先执行：

```sql
CREATE DATABASE python_course
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
```

## 7. 主要接口说明

### 7.1 健康检查

```http
GET /healthz
```

作用：

- 检查 Node 后端是否还活着
- 检查 MySQL 是否可连接

### 7.2 页面访问上报

```http
POST /api/analytics/page-views
```

这个接口由前端自动调用，一般不需要手工调。

请求体大致是：

```json
{
  "chapterId": "2",
  "path": "/chapter/2",
  "referrer": "/chapter/1",
  "sessionId": "xxx",
  "userAgent": "xxx"
}
```

### 7.3 后台统计接口

```http
GET /api/admin/analytics/dashboard
```

这个接口会返回：

- 总访问量
- 独立会话数
- 按章节统计
- 按页面统计
- 最近访问记录
- 最近 N 天访问趋势

访问时需要带管理员令牌，支持两种方式：

```http
Authorization: Bearer 你的_ADMIN_TOKEN
```

或者：

```http
x-admin-token: 你的_ADMIN_TOKEN
```

### 7.4 GitHub Webhook

```http
POST /api/webhooks/github
```

用于 GitHub 推送代码后自动部署。

它会：

1. 校验 GitHub 签名
2. 检查分支是否是 `main`
3. 调用部署脚本

## 8. 后台统计页怎么使用

前端后台页地址：

```text
/#/admin/stats
```

进入后：

1. 输入 `ADMIN_TOKEN`
2. 选择统计天数
3. 点击“刷新数据”

页面会显示：

- 总访问量
- 独立会话数
- 章节热度
- 页面排行
- 最近访问列表

## 9. Ubuntu 正式部署

下面是推荐部署方式：

- Nginx 负责对外提供网站
- Node 后端只监听 `127.0.0.1:9001`
- 用 `systemd` 或 `pm2` 守护 Node 进程

### 9.1 安装后端依赖

假设项目部署目录是：

```text
/var/www/python_course
```

则执行：

```bash
cd /var/www/python_course
npm --prefix server install
```

### 9.2 systemd 方式

这是 Ubuntu 上更推荐的方式。

复制服务文件：

```bash
sudo cp server/systemd/python-course-server.service /etc/systemd/system/python-course-server.service
sudo cp server/systemd/python-course-server.env.example /etc/python-course-server.env
```

编辑环境变量文件：

```bash
sudo nano /etc/python-course-server.env
```

内容示例：

```bash
MYSQL_PASSWORD=你的数据库密码
WEBHOOK_SECRET=你的_github_webhook_secret
ADMIN_TOKEN=你的后台令牌
DEPLOY_SCRIPT=/var/www/python_course/deploy.sh
DEPLOY_SHELL=/bin/bash
SERVER_LOG_FILE=/var/www/python_course/server/logs/server.log
```

启用并启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable python-course-server
sudo systemctl start python-course-server
sudo systemctl status python-course-server
```

查看日志：

```bash
journalctl -u python-course-server -f
```

### 9.3 PM2 方式

如果你更熟悉 Node 社区工具，也可以用 PM2。

安装 PM2：

```bash
npm install -g pm2
```

设置环境变量后启动：

```bash
export MYSQL_PASSWORD='你的数据库密码'
export WEBHOOK_SECRET='你的_github_webhook_secret'
export ADMIN_TOKEN='你的后台令牌'
pm2 start server/ecosystem.config.cjs
pm2 save
pm2 startup
```

查看状态：

```bash
pm2 list
pm2 logs python-course-server
```

## 10. Nginx 配置

Nginx 配置示例文件在：

- [python-course.conf](/f:/OneDrive/吉利学院/6-2025-2026第二学期/python-202520262/notebook/python_course/server/nginx/python-course.conf)

它的核心逻辑是：

- `/` 提供前端静态文件
- `/api/` 反向代理到 Node 后端
- `/healthz` 反向代理到 Node 后端

部署时你主要要改两项：

- `server_name`
- `root`

例如：

```nginx
server {
    listen 80;
    server_name your-domain.example.com;

    root /var/www/python_course/dist;
    index index.html;

    client_max_body_size 2m;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:9001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }

    location /healthz {
        proxy_pass http://127.0.0.1:9001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用 Nginx 配置：

```bash
sudo cp server/nginx/python-course.conf /etc/nginx/sites-available/python-course
sudo ln -s /etc/nginx/sites-available/python-course /etc/nginx/sites-enabled/python-course
sudo nginx -t
sudo systemctl reload nginx
```

## 11. 常用命令速查

在项目根目录执行：

```bash
# 安装后端依赖
npm --prefix server install

# 启动后端
npm run server:start

# 开发模式启动后端
npm run server:dev

# 检查后端入口语法
npm run server:check

# 构建前端
npm run build
```

## 12. 常见问题

### 12.1 为什么后端不直接监听 80 端口？

因为更推荐让 Nginx 对外监听 80/443，Node 后端只监听本机回环地址：

```text
127.0.0.1:9001
```

这样更安全，也方便以后加 HTTPS。

### 12.2 为什么数据库密码不写在代码里？

因为密码属于敏感信息，不应该提交到仓库。

当前代码里只有这些 MySQL 配置是固定的：

- `127.0.0.1`
- `3306`
- `root`
- `python_course`

密码还是从系统环境变量 `MYSQL_PASSWORD` 读取。

### 12.3 如果后台页提示未授权怎么办？

先检查：

- 服务器是否设置了 `ADMIN_TOKEN`
- 浏览器输入的 token 是否一致
- Nginx 是否正确转发 `/api/admin/...`

### 12.4 如果访问统计没有数据怎么办？

按这个顺序排查：

1. 打开浏览器开发者工具，看 `POST /api/analytics/page-views` 是否成功
2. 访问 `GET /healthz` 看后端和数据库是否正常
3. 检查 MySQL 中是否有 `page_views` 表
4. 检查 Nginx 是否正确反代 `/api/`

### 12.5 如果 webhook 不生效怎么办？

重点检查：

1. GitHub 的 webhook 地址是否正确
2. `WEBHOOK_SECRET` 是否一致
3. 服务器能否执行 `deploy.sh`
4. `DEPLOY_SCRIPT` 和 `DEPLOY_SHELL` 是否配置正确

## 13. 建议的实际部署顺序

如果你第一次部署，建议按这个顺序做：

1. 先确认 MySQL 已安装，并创建 `python_course` 数据库
2. 设置 `MYSQL_PASSWORD`
3. 启动 Node 后端
4. 访问 `http://127.0.0.1:9001/healthz` 检查是否正常
5. 配置 Nginx
6. 打开前端页面，看埋点是否成功写入数据库
7. 再去配置 GitHub Webhook 自动部署

这样排错最省时间。

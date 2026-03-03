# Python 课程课件（Vue 版）

一个基于 `Vue 3 + Vite` 的教学课件项目，用于展示 Python 课程章节内容（当前包含第 1 章和第 2 章）。

## 功能概览

- 章节导航（侧边章节切换）
- 课件大纲侧栏（当前卡片定位 + 点击跳转）
- 卡片式浏览体验（滚动/键盘翻页）
- 代码高亮与一键复制
- 课件内命令复制、系统命令页签切换（Windows/macOS/Linux）
- 章节静态教学素材托管（如 `.py` 示例文件下载）

## 技术栈

- `Vue 3`
- `Vue Router 4`（`hash` 路由）
- `Vite 7`
- `highlight.js`

## 目录结构

```text
python_course/
├─ public/
│  ├─ favicon.ico
│  └─ chapters/
│     └─ ch01/
│        └─ game.py
├─ src/
│  ├─ assets/
│  ├─ components/
│  ├─ composables/
│  │  └─ useLessonDeck.js
│  ├─ config/
│  │  └─ chapters.js
│  ├─ router/
│  │  └─ index.js
│  ├─ views/
│  │  ├─ ChapterOneView.vue
│  │  └─ ChapterTwoView.vue
│  ├─ App.vue
│  └─ main.js
├─ index.html
├─ package.json
└─ vite.config.js
```

## 环境要求

- `Node.js`：`^20.19.0` 或 `>=22.12.0`
- `npm`：建议使用较新稳定版本（与 Node 匹配）

## 本地启动

1. 安装依赖

```bash
npm install
```

2. 启动开发环境

```bash
npm run dev
```

3. 在浏览器访问（通常）：

```text
http://localhost:5173
```

项目使用 `hash` 路由，章节地址示例：

- `/#/chapter/1`
- `/#/chapter/2`

## 构建与预览

构建生产包：

```bash
npm run build
```

本地预览构建结果：

```bash
npm run preview
```

## 常用命令

代码格式化（`src/`）：

```bash
npm run format
```

## 静态教学文件说明

`public/` 下的文件会原样输出到站点根路径。  
例如：

- 文件路径：`public/chapters/ch01/game.py`
- 访问路径：`/chapters/ch01/game.py`

可用于“下载示例代码”按钮：

```html
<a href="/chapters/ch01/game.py" download>下载 game.py</a>
```

## 新增章节的推荐流程

1. 新建页面：`src/views/ChapterXView.vue`
2. 注册路由：更新 `src/router/index.js`
3. 更新章节导航：修改 `src/config/chapters.js`
4. 如需章节代码素材：放到 `public/chapters/chXX/`

## 上传到 GitHub（示例）

如果你是第一次把这个项目推到 GitHub：

```bash
git init
git add .
git commit -m "feat: init python course vue project"
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
```

说明：

- `node_modules/`、`dist/` 已在 `.gitignore` 中，通常不需要提交。
- 建议提交源码与 `package-lock.json`，便于他人复现依赖版本。

## 常见问题

### `npm run build` 报错：缺少 Rollup 可选依赖

如果出现类似：

```text
Cannot find module @rollup/rollup-win32-x64-msvc
```

可尝试重新安装依赖：

```bash
rm -rf node_modules package-lock.json
npm install
```

Windows PowerShell 可用：

```powershell
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm install
```

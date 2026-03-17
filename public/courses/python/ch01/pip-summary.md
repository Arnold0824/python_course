# PIP 总结（Chapter 1）

## 1. 什么是 `pip`？

`pip` 是 Python 生态里最常用的包管理工具，用来安装、升级、卸载第三方库。

- 你写 `import numpy`、`import requests` 时，这些库通常就是通过 `pip` 安装的。
- `pip` 默认从 [PyPI](https://pypi.org/) 下载包。
- `pip` 管理的是“当前 Python 解释器对应环境”里的包。

一句话记忆：`pip` 是 Python 依赖管理器。

---

## 2. 为什么要用 `pip`？

### 2.1 自动处理依赖，效率高
`pip` 可以自动下载并安装依赖链，避免手动找包、拷文件。

### 2.2 便于复现项目环境
团队协作、换电脑、交作业时，`requirements.txt` 可以快速恢复依赖。

### 2.3 便于版本管理
不同版本库行为可能不同。`pip` 支持锁版本，减少“同代码不同结果”。

### 2.4 维护成本低
安装、升级、卸载、查询信息都能用统一命令完成。

---

## 3. 怎么用 `pip`？

> 推荐统一写法：`python -m pip ...`
> 
> 原因：确保调用的是“当前这个 Python”对应的 `pip`。

### 3.1 查看与检查

```bash
python -m pip --version
python -m pip list
python -m pip show numpy
```

### 3.2 安装

```bash
python -m pip install numpy
python -m pip install requests pandas
python -m pip install numpy==1.26.4
```

### 3.3 升级与卸载

```bash
python -m pip install -U numpy
python -m pip uninstall numpy
```

### 3.4 导出与复现依赖

```bash
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

### 3.5 设为清华源默认（推荐）

先升级 `pip`，再设置默认源：

```bash
python -m pip install --upgrade pip
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

如果到 pip 默认源网络较差，可先临时用清华源升级 `pip`：

```bash
python -m pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --upgrade pip
```

---

## 4. 常见问题

### 4.1 安装成功但 `import` 失败
通常是调用了另一个 Python 解释器对应的 `pip`。

解决：始终使用 `python -m pip`，并先确认 `python --version` 与解释器路径。

### 4.2 下载慢或超时
可临时指定镜像源（见上面的 `-i` 参数）。

### 4.3 权限报错
可尝试：

```bash
python -m pip install --user <package>
```

---

## 5. 最小命令清单（记住这 5 条）

```bash
python -m pip --version
python -m pip install <package>
python -m pip uninstall <package>
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

如果只记一句话：

**`pip` 用来管理 Python 包，推荐统一使用 `python -m pip`。**

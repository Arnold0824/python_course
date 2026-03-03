<script setup>
import { ref } from "vue";
import LessonOutlineSidebar from "../components/LessonOutlineSidebar.vue";
import { useLessonDeck } from "../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);
</script>

<template>
  <div ref="rootRef" class="course-page">
    <div class="bg-orb orb-a" aria-hidden="true"></div>
        <div class="bg-orb orb-b" aria-hidden="true"></div>
        <div class="bg-grid" aria-hidden="true"></div>

        <div class="progress-track" aria-hidden="true">
            <span id="scrollProgress"></span>
        </div>

        <header class="top-nav">
            <a class="brand" href="#top">
                <span class="brand-tag">Chapter 1</span>
                <strong>pip / conda 环境管理</strong>
            </a>
            <nav class="nav-links" aria-label="页面目录">
                <a href="#goals">教学目标</a>
                <a href="#concepts">核心概念</a>
                <a href="#commands">命令集合</a>
                <a href="#venv">venv</a>
                <a href="#conda">Conda</a>
                <a href="#pitfalls">常见坑</a>
            </nav>
        </header>

        <main id="top" class="page is-slide-deck">
            <section id="goals" class="hero reveal" data-outline-level="1" data-outline-label="教学目标">
                <p class="kicker">PIP LESSON BLUEPRINT</p>
                <h1>一节课讲清 pip：<br>能安装、能定位、能复现</h1>
                <p class="hero-intro">
                    这节课只抓关键能力：学生学完以后，能在正确解释器环境里安装第三方库，并用
                    <code>requirements.txt</code> 把环境复现出来。
                </p>
                <div class="goal-cards fly-in-seq">
                    <article>
                        <h2>目标 1</h2>
                        <p>明白 pip 是包管理器，负责安装、升级、卸载 Python 第三方库。</p>
                    </article>
                    <article>
                        <h2>目标 2</h2>
                        <p>能在正确解释器环境中安装，避免“装了却 import 不到”。</p>
                    </article>
                    <article>
                        <h2>目标 3</h2>
                        <p>掌握最基本可复现流程：<code>freeze</code> 导出 + <code>-r</code> 一键安装。</p>
                    </article>
                </div>
            </section>

            <section id="concepts" class="section reveal" data-outline-level="1" data-outline-label="必讲概念">
                <div class="section-head">
                    <p class="kicker">5 KEYWORDS</p>
                    <h2>必讲概念：讲完就够用</h2>
                </div>
                <div class="concept-grid">
                    <article class="concept-card">
                        <h3>A. 包与模块</h3>
                        <p><strong>模块（module）</strong>：一个 <code>.py</code> 文件或目录。</p>
                        <p><strong>包（package）</strong>：可通过 pip 安装的发行版，通常含多个模块/数据/依赖。</p>
                    </article>
                    <article class="concept-card">
                        <h3>B. PyPI</h3>
                        <p>pip 默认从 PyPI 下载包，可理解为 Python 包的“应用商店”。</p>
                        <p>国内课堂常需镜像源或统一网络配置。</p>
                    </article>
                    <article class="concept-card">
                        <h3>C. 依赖</h3>
                        <p>一个包可能依赖多个其他包。</p>
                        <p>pip 会做依赖解析并自动安装依赖链。</p>
                    </article>
                    <article class="concept-card">
                        <h3>D. 版本与约束</h3>
                        <p>锁版本是为了避免行为变化导致“同代码不同结果”。</p>
                        <p><code>numpy==1.26.4</code>，<code>pandas&gt;=2.0,&lt;3.0</code></p>
                    </article>
                    <article class="concept-card">
                        <h3>E. 环境（关键）</h3>
                        <p><strong>pip 是给某个解释器安装，不是给整台电脑安装。</strong></p>
                        <p>核心句：<code>pip 属于解释器，不属于电脑</code>。</p>
                    </article>
                </div>
            </section>

            <section id="commands" class="section reveal" data-outline-level="2" data-outline-label="必会命令">
                <div class="section-head">
                    <p class="kicker">MUST KNOW COMMANDS</p>
                    <h2>课堂必会命令（统一写法）</h2>
                </div>
                <p class="section-note">
                    强烈推荐统一使用：<code>python -m pip ...</code>，确保 pip 与当前 Python 解释器一致。
                </p>
                <div class="command-layout">
                    <article class="command-card">
                        <h3>基础信息与检查</h3>
                        <div class="cmd-line">
                            <code>python -m pip --version</code>
                            <button class="copy-btn" data-copy="python -m pip --version">复制</button>
                        </div>
                        <p>确认 pip 属于哪个 Python 解释器。</p>
                        <div class="cmd-line">
                            <code>python -m pip list</code>
                            <button class="copy-btn" data-copy="python -m pip list">复制</button>
                        </div>
                        <p>查看当前环境已安装包。</p>
                        <div class="cmd-line">
                            <code>python -m pip show numpy</code>
                            <button class="copy-btn" data-copy="python -m pip show numpy">复制</button>
                        </div>
                        <p>查看安装位置、版本、依赖信息。</p>
                    </article>

                    <article class="command-card">
                        <h3>安装 / 升级 / 卸载</h3>
                        <div class="cmd-line">
                            <code>python -m pip install numpy</code>
                            <button class="copy-btn" data-copy="python -m pip install numpy">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>python -m pip install numpy==1.26.4</code>
                            <button class="copy-btn" data-copy="python -m pip install numpy==1.26.4">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>python -m pip install -U numpy</code>
                            <button class="copy-btn" data-copy="python -m pip install -U numpy">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>python -m pip uninstall numpy</code>
                            <button class="copy-btn" data-copy="python -m pip uninstall numpy">复制</button>
                        </div>
                    </article>

                    <article class="command-card">
                        <h3>可复现（作业/机房最常用）</h3>
                        <div class="cmd-line">
                            <code>python -m pip freeze &gt; requirements.txt</code>
                            <button class="copy-btn" data-copy="python -m pip freeze > requirements.txt">复制</button>
                        </div>
                        <p>导出依赖清单，提交作业或分享环境。</p>
                        <div class="cmd-line">
                            <code>python -m pip install -r requirements.txt</code>
                            <button class="copy-btn" data-copy="python -m pip install -r requirements.txt">复制</button>
                        </div>
                        <p>一键恢复同版本环境。</p>
                    </article>
                </div>
            </section>

            <section id="venv" class="section reveal" data-outline-level="2" data-outline-label="虚拟环境 venv">
                <div class="section-head">
                    <p class="kicker">VENV FIRST</p>
                    <h2>pip 必须绑定虚拟环境 venv</h2>
                </div>
                <p class="section-note">
                    一句话讲清：<strong>venv 给每个项目一个独立 site-packages，避免版本互相打架。</strong>
                </p>
                <ol class="timeline">
                    <li>
                        <h3>1. 创建虚拟环境</h3>
                        <div class="cmd-line">
                            <code>python -m venv .venv</code>
                            <button class="copy-btn" data-copy="python -m venv .venv">复制</button>
                        </div>
                    </li>
                    <li>
                        <h3>2. 激活虚拟环境</h3>
                        <div class="os-switch" role="tablist" aria-label="系统切换">
                            <button class="os-btn is-active" data-os-target="windows" role="tab" aria-selected="true">Windows</button>
                            <button class="os-btn" data-os-target="macos" role="tab" aria-selected="false">macOS</button>
                            <button class="os-btn" data-os-target="linux" role="tab" aria-selected="false">Linux</button>
                        </div>
                        <div class="os-panel is-active" data-os-panel="windows">
                            <div class="cmd-line">
                                <code>.\.venv\Scripts\activate</code>
                                <button class="copy-btn" data-copy=".\.venv\Scripts\activate">复制</button>
                            </div>
                        </div>
                        <div class="os-panel" data-os-panel="macos">
                            <div class="cmd-line">
                                <code>source .venv/bin/activate</code>
                                <button class="copy-btn" data-copy="source .venv/bin/activate">复制</button>
                            </div>
                        </div>
                        <div class="os-panel" data-os-panel="linux">
                            <div class="cmd-line">
                                <code>source .venv/bin/activate</code>
                                <button class="copy-btn" data-copy="source .venv/bin/activate">复制</button>
                            </div>
                        </div>
                    </li>
                    <li>
                        <h3>3. 激活后安装并验证</h3>
                        <div class="cmd-line">
                            <code>python -m pip install numpy</code>
                            <button class="copy-btn" data-copy="python -m pip install numpy">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>python -c "import numpy; print(numpy.__version__)"</code>
                            <button class="copy-btn" data-copy="python -c &quot;import numpy; print(numpy.__version__)&quot;">复制</button>
                        </div>
                    </li>
                </ol>
            </section>

            <section id="conda" class="section reveal" data-outline-level="2" data-outline-label="Conda（推荐 Miniconda）">
                <div class="section-head">
                    <p class="kicker">CONDA BASICS</p>
                    <h2>Anaconda 与 Miniconda：课堂统一使用 Miniconda</h2>
                </div>
                <p class="section-note">
                    Conda 是包与环境管理工具。课堂常见发行版有 Anaconda 与 Miniconda，但教学环境统一使用 Miniconda。
                </p>
                <div class="concept-grid">
                    <article class="concept-card">
                        <h3>Anaconda</h3>
                        <p>预装大量科学计算包，开箱即用，但安装包体积大、机房维护成本高。</p>
                    </article>
                    <article class="concept-card">
                        <h3>Miniconda</h3>
                        <p>只包含 conda 与最小 Python 运行环境，体积小、按需安装、课堂可控性更高。</p>
                    </article>
                    <article class="concept-card">
                        <h3>课堂统一原则</h3>
                        <p><strong>conda 管环境</strong>，<strong>pip 管 PyPI 包</strong>；进入 conda 环境后仍优先用 <code>python -m pip</code>。</p>
                    </article>
                </div>
                <div class="command-layout">
                    <article class="command-card">
                        <h3>课堂起步命令</h3>
                        <div class="cmd-line">
                            <code>conda create -n py310 python=3.10 -y</code>
                            <button class="copy-btn" data-copy="conda create -n py310 python=3.10 -y">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>conda activate py310</code>
                            <button class="copy-btn" data-copy="conda activate py310">复制</button>
                        </div>
                        <p>先创建并激活课程环境，再执行安装操作。</p>
                    </article>
                    <article class="command-card">
                        <h3>环境身份确认</h3>
                        <div class="cmd-line">
                            <code>conda env list</code>
                            <button class="copy-btn" data-copy="conda env list">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>python -m pip --version</code>
                            <button class="copy-btn" data-copy="python -m pip --version">复制</button>
                        </div>
                        <p>确认当前环境和 pip 归属，避免“装错解释器”。</p>
                    </article>
                    <article class="command-card">
                        <h3>与 pip 协作</h3>
                        <div class="cmd-line">
                            <code>python -m pip install numpy</code>
                            <button class="copy-btn" data-copy="python -m pip install numpy">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>python -c "import numpy; print(numpy.__version__)"</code>
                            <button class="copy-btn" data-copy='python -c "import numpy; print(numpy.__version__)"'>复制</button>
                        </div>
                        <p>在激活环境内用 <code>python -m pip</code>，是课堂统一规范。</p>
                    </article>
                </div>
            </section>

            <section class="section reveal" data-outline-level="2" data-outline-label="Conda 环境生命周期">
                <div class="section-head">
                    <p class="kicker">LIFECYCLE</p>
                    <h2>Conda 环境生命周期：创建 → 使用 → 导出 → 清理</h2>
                </div>
                <div class="command-layout">
                    <article class="command-card">
                        <h3>创建 / 激活 / 退出</h3>
                        <div class="cmd-line">
                            <code>conda create -n py310 python=3.10 -y</code>
                            <button class="copy-btn" data-copy="conda create -n py310 python=3.10 -y">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>conda activate py310</code>
                            <button class="copy-btn" data-copy="conda activate py310">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>conda deactivate</code>
                            <button class="copy-btn" data-copy="conda deactivate">复制</button>
                        </div>
                        <p>进入环境后，命令行前缀会显示环境名。</p>
                    </article>
                    <article class="command-card">
                        <h3>查看 / 安装 / 更新</h3>
                        <div class="cmd-line">
                            <code>conda env list</code>
                            <button class="copy-btn" data-copy="conda env list">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>conda list</code>
                            <button class="copy-btn" data-copy="conda list">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>conda install numpy pandas</code>
                            <button class="copy-btn" data-copy="conda install numpy pandas">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>conda update numpy</code>
                            <button class="copy-btn" data-copy="conda update numpy">复制</button>
                        </div>
                    </article>
                    <article class="command-card">
                        <h3>导出 / 复现 / 删除</h3>
                        <div class="cmd-line">
                            <code>conda env export --from-history &gt; environment.yml</code>
                            <button class="copy-btn" data-copy="conda env export --from-history > environment.yml">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>conda env create -f environment.yml</code>
                            <button class="copy-btn" data-copy="conda env create -f environment.yml">复制</button>
                        </div>
                        <div class="cmd-line">
                            <code>conda remove -n py310 --all -y</code>
                            <button class="copy-btn" data-copy="conda remove -n py310 --all -y">复制</button>
                        </div>
                        <p>作业提交建议附带 <code>environment.yml</code>。</p>
                    </article>
                </div>
            </section>

            <section class="section reveal" data-outline-level="2" data-outline-label="Conda 源配置（国内镜像）">
                <div class="section-head">
                    <p class="kicker">CHANNELS</p>
                    <h2>Conda 源配置（国内镜像）</h2>
                </div>
                <p class="section-note">
                    镜像站提供 Anaconda 仓库与部分第三方源（如 conda-forge、msys2、pytorch 等）。不同镜像站同步范围可能不同，课堂建议统一配置方式。
                </p>
                <p><strong>.condarc 文件路径：</strong></p>
                <ul>
                    <li>Linux：<code>${HOME}/.condarc</code></li>
                    <li>macOS：<code>${HOME}/.condarc</code></li>
                    <li>Windows：<code>C:\Users\&lt;YourUserName&gt;\.condarc</code></li>
                </ul>
                <p><strong>注：</strong></p>
                <ul>
                    <li>Windows 无法直接新建 <code>.condarc</code>，先执行 <code>conda config --set show_channel_urls yes</code> 生成。</li>
                    <li>由于更新过快难以同步，部分镜像站不同步 <code>pytorch-nightly</code>、<code>pytorch-nightly-cpu</code>、<code>ignite-nightly</code>。</li>
                    <li>切换镜像源时，请确认目标镜像是否同步了所需 repo，并支持你的平台（如 <code>linux-64</code>）。</li>
                    <li>为保证通用性，课堂默认只加入少量必须第三方源，其他源按需再加。</li>
                </ul>
                <p class="section-note">将下面内容写入 <code>.condarc</code>：</p>
                <pre><code class="yaml">
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud</code></pre>
                <p class="section-note">配置完成后，清索引并做一次安装测试：</p>
                <div class="cmd-line">
                    <code>conda clean -i</code>
                    <button class="copy-btn" data-copy="conda clean -i">复制</button>
                </div>
                <div class="cmd-line">
                    <code>conda create -n myenv numpy</code>
                    <button class="copy-btn" data-copy="conda create -n myenv numpy">复制</button>
                </div>
            </section>

            <section class="section reveal" data-outline-level="2" data-outline-label="Conda 与 pip 协作规则">
                <div class="section-head">
                    <p class="kicker">BEST PRACTICE</p>
                    <h2>Conda 与 pip 协作：课堂统一规范</h2>
                </div>
                <div class="concept-grid">
                    <article class="concept-card">
                        <h3>规则 1：先 conda 后 pip</h3>
                        <p>优先用 conda 安装基础库（如 <code>numpy</code>/<code>pandas</code>）。</p>
                    </article>
                    <article class="concept-card">
                        <h3>规则 2：pip 用 <code>python -m pip</code></h3>
                        <p>确保安装到当前激活环境，避免“装了却 import 不到”。</p>
                    </article>
                    <article class="concept-card">
                        <h3>规则 3：避免混装冲突</h3>
                        <p>同一个包不要先后被 conda 和 pip 反复覆盖安装。</p>
                    </article>
                    <article class="concept-card">
                        <h3>规则 4：可复现要双保险</h3>
                        <p>提交 <code>environment.yml</code>，必要时附带 <code>requirements.txt</code>。</p>
                    </article>
                </div>
                <pre><code class="bash">
conda create -n py310 python=3.10 -y
conda activate py310
conda install numpy pandas
python -m pip install fastapi
python -m pip check
conda env export --from-history > environment.yml
python -m pip freeze > requirements.txt</code></pre>
            </section>

            <section class="section reveal" data-outline-level="2" data-outline-label="Conda 常见问题（课堂版）">
                <div class="section-head">
                    <p class="kicker">PRACTICAL FAQ</p>
                    <h2>Conda 常见问题与处理</h2>
                </div>
                <div class="pitfall-grid compact-grid">
                    <article class="pitfall">
                        <h3>1) 装在了 base 环境</h3>
                        <p class="problem">问题：忘记激活课程环境，包装错地方。</p>
                        <p class="solution">解法：先 <code>conda activate py310</code>，再执行安装命令。</p>
                    </article>
                    <article class="pitfall">
                        <h3>2) 求解很慢</h3>
                        <p class="problem">问题：默认源访问慢或网络波动大。</p>
                        <p class="solution">解法：先统一配置国内镜像，再 <code>conda clean -i -y</code> 重试。</p>
                    </article>
                    <article class="pitfall">
                        <h3>3) 包找不到</h3>
                        <p class="problem">问题：当前 channels 没有该包。</p>
                        <p class="solution">解法：先检查 <code>conda config --show channels</code>，再按课堂规范补充源。</p>
                    </article>
                    <article class="pitfall">
                        <h3>4) 环境无法复现</h3>
                        <p class="problem">问题：同学机器与机房版本不一致。</p>
                        <p class="solution">解法：提交 <code>environment.yml</code>（必要时附 <code>requirements.txt</code>）。</p>
                    </article>
                </div>
            </section>

            <section id="mirror" class="section reveal" data-outline-level="2" data-outline-label="国内镜像配置">
                <div class="section-head">
                    <p class="kicker">NETWORK REALITY</p>
                    <h2>国内网络与镜像：临时 vs 永久</h2>
                </div>
                <div class="mirror-grid">
                    <article class="mirror-card">
                        <h3>临时用（一次命令）</h3>
                        <p>适合临时下载慢/超时时的快速处理：</p>
                        <div class="cmd-line">
                            <code>python -m pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple</code>
                            <button class="copy-btn" data-copy="python -m pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple">复制</button>
                        </div>
                    </article>
                    <article class="mirror-card">
                        <h3>永久配置（统一课堂环境）</h3>
                        <p>给 pip 设置默认源，减少每次手动输入：</p>
                        <div class="cmd-line">
                            <code>python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple</code>
                            <button class="copy-btn" data-copy="python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple">复制</button>
                        </div>
                    </article>
                </div>
                <p class="section-note">
                    学校网络或代理环境下，以课堂统一指引为准，不建议学生自行混配多套镜像规则。
                </p>
            </section>

            <section id="pitfalls" class="section reveal" data-outline-level="2" data-outline-label="常见 5 个坑">
                <div class="section-head">
                    <p class="kicker">TOP 5 TROUBLES</p>
                    <h2>最常见 5 个坑与对应解法</h2>
                </div>
                <div class="pitfall-grid">
                    <article class="pitfall">
                        <h3>1) 装了却 import 不了</h3>
                        <p class="problem">问题：pip 装到了另一个 Python 环境。</p>
                        <p class="solution">解法：统一用 <code>python -m pip</code>；在 PyCharm 确认解释器指向 <code>.venv</code>。</p>
                    </article>
                    <article class="pitfall">
                        <h3>2) 权限报错</h3>
                        <p class="problem">问题：Windows 管理员权限或 Linux 全局权限不足。</p>
                        <p class="solution">解法：优先使用 venv；<code>--user</code> 只作为临时兜底，不建议长期依赖。</p>
                    </article>
                    <article class="pitfall">
                        <h3>3) 下载慢或超时</h3>
                        <p class="problem">问题：课堂网络不稳定，默认源访问慢。</p>
                        <p class="solution">解法：使用镜像；必要时准备离线包或本地 wheel。</p>
                    </article>
                    <article class="pitfall">
                        <h3>4) 版本冲突</h3>
                        <p class="problem">问题：依赖解析报错，多个项目互相污染。</p>
                        <p class="solution">解法：新建 venv、明确版本区间，避免在系统 Python 里乱装包。</p>
                    </article>
                    <article class="pitfall">
                        <h3>5) Jupyter 装完仍不可用</h3>
                        <p class="problem">问题：Notebook kernel 与 pip 安装环境不一致。</p>
                        <p class="solution">解法：核对 kernel；使用该 kernel 对应 Python 执行 <code>-m pip</code>。</p>
                    </article>
                </div>
            </section>

            <section id="summary" class="section reveal summary" data-outline-level="1" data-outline-label="流程总结">
                <div class="section-head">
                    <p class="kicker">MINIMUM WORKFLOW</p>
                    <h2>一页带走：标准课堂流程</h2>
                </div>
                <div class="flow">
                    <span>创建 venv</span>
                    <span>激活环境</span>
                    <span>安装依赖</span>
                    <span>运行验证</span>
                    <span>导出 requirements</span>
                </div>
                <pre class="final-snippet"><code>
python -m venv .venv
    .\.venv\Scripts\activate
    python -m pip install numpy
    python -c "import numpy; print(numpy.__version__)"
    python -m pip freeze &gt; requirements.txt</code></pre>
            </section>
        </main>

        <footer class="footer">
            <p>课堂关键句：<strong>pip 属于解释器，不属于电脑。</strong></p>
        </footer>

        <LessonOutlineSidebar
          :items="outlineItems"
          :active-index="activeOutlineIndex"
          @jump="jumpToSlide"
        />

        <div id="copyToast" class="copy-toast" role="status" aria-live="polite">命令已复制</div>
  </div>
</template>

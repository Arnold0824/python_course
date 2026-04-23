<script setup>
import { ref } from "vue";
import CourseSwitcher from "../../../components/CourseSwitcher.vue";
import LessonOutlineSidebar from "../../../components/LessonOutlineSidebar.vue";
import IconArchive from "../../../assets/lucide-icons/archive.svg";
import IconBookOpen from "../../../assets/lucide-icons/book-open.svg";
import IconBot from "../../../assets/lucide-icons/bot.svg";
import IconBraces from "../../../assets/lucide-icons/braces.svg";
import IconCircleAlert from "../../../assets/lucide-icons/circle-alert.svg";
import IconCode from "../../../assets/lucide-icons/code.svg";
import IconDatabase from "../../../assets/lucide-icons/database.svg";
import IconExternalLink from "../../../assets/lucide-icons/external-link.svg";
import IconFileSearch from "../../../assets/lucide-icons/file-search.svg";
import IconGlobe from "../../../assets/lucide-icons/globe.svg";
import IconHistory from "../../../assets/lucide-icons/history.svg";
import IconLink from "../../../assets/lucide-icons/link.svg";
import IconListTree from "../../../assets/lucide-icons/list-tree.svg";
import IconMousePointer from "../../../assets/lucide-icons/mouse-pointer.svg";
import IconNetwork from "../../../assets/lucide-icons/network.svg";
import IconRoute from "../../../assets/lucide-icons/route.svg";
import IconSearch from "../../../assets/lucide-icons/search.svg";
import IconShield from "../../../assets/lucide-icons/shield.svg";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const sampleJsonHref = "/courses/python/ch07/sample_books.json";
const staticHtmlHref = "/courses/python/ch07/books_static.html";
const dynamicHtmlHref = "/courses/python/ch07/search_demo.html";
const kugouRankHref = "https://www.kugou.com/yy/rank/home/1-8888.html?from=rank";
const kugouReportTemplateHref = "/courses/python/exp_reports/实验报告4：爬取酷狗音乐TOP500歌曲信息，并存储到文本文件（理实课程实验部分）-学生姓名.docx";
const kugouReportSubmitHref = "https://f.wps.cn/g/UOG49Aft/";

const learningGoals = [
  "理解浏览器访问网页背后的请求、响应、状态码、HTML 与 JSON。",
  "能用 requests 获取网页或接口数据，并处理编码、参数、请求头和异常。",
  "能分别使用 JSON、BeautifulSoup、正则表达式和 Selenium 完成不同类型的数据提取。",
];

const roadmap = [
  "requests：发送网络请求",
  "JSON：读取接口数据",
  "BeautifulSoup：解析网页结构",
  "re：提取局部文本模式",
  "Selenium：模拟浏览器操作",
  "综合项目：完成酷狗音乐 TOP500 采集实验",
];

const foundationMap = [
  {
    title: "4.1 一次网络访问",
    icon: IconGlobe,
    text: "从输入 URL 到收到响应，理解浏览器和 Python 程序到底做了什么。",
  },
  {
    title: "4.2 请求与响应",
    icon: IconNetwork,
    text: "理解 URL、Method、Headers、Cookie、状态码和响应正文之间的关系。",
  },
  {
    title: "4.3 数据格式",
    icon: IconBraces,
    text: "判断拿到的是 JSON、HTML、文本还是浏览器渲染后的页面，再选择解析工具。",
  },
  {
    title: "4.4 爬虫流程",
    icon: IconBot,
    text: "把采集任务拆成入口、访问、解析、清洗、去重、保存和异常处理。",
  },
  {
    title: "4.5 爬虫简史",
    icon: IconHistory,
    text: "从 Archie、World Wide Web Wanderer、JumpStation 看到爬虫的起源。",
  },
  {
    title: "4.6 技术演变",
    icon: IconRoute,
    text: "理解从人工目录、自动抓取、索引排序到浏览器自动化的演进路线。",
  },
  {
    title: "4.7 隐私与法律风险",
    icon: IconShield,
    text: "理解个人信息保护、平台规则和法律责任，建立技术向善的底线意识。",
  },
  {
    title: "4.8 来源追溯",
    icon: IconExternalLink,
    text: "历史节点附带可核对来源，训练技术学习中的事实核查意识。",
  },
];

const requestFlowCards = [
  {
    title: "第 1 步：确定要访问的资源",
    icon: IconLink,
    text: "URL 是资源地址。浏览器访问网页、Python 访问接口，本质上都是向某个 URL 请求资源。",
    example: "例如 /sample_books.json 是数据接口，/books_static.html 是网页文档。",
  },
  {
    title: "第 2 步：把域名定位到服务器",
    icon: IconNetwork,
    text: "域名需要被解析成服务器地址。普通学习阶段不需要手写 DNS 代码，但要知道域名并不等于服务器本身。",
    example: "访问 niuniulab.com 时，程序最终连接的是这个域名背后的服务器地址。",
  },
  {
    title: "第 3 步：发送 HTTP 请求",
    icon: IconSearch,
    text: "请求中会带上方法、路径、参数、请求头，有时还会带 Cookie 或表单数据。",
    example: "requests.get(url, params={\"page\": 1}) 就是在发送一次 GET 请求。",
  },
  {
    title: "第 4 步：服务器处理请求",
    icon: IconDatabase,
    text: "服务器根据路径、参数和身份信息决定返回什么内容，也可能因为权限、频率或路径错误拒绝访问。",
    example: "同一个搜索页面，keyword=Python 和 keyword=Excel 返回的结果可能不同。",
  },
  {
    title: "第 5 步：收到 HTTP 响应",
    icon: IconCircleAlert,
    text: "响应里有状态码、响应头和正文。状态码判断是否成功，响应头帮助判断内容类型，正文才是要解析的数据。",
    example: "200 表示成功，404 表示路径不存在，429 常表示访问太频繁。",
  },
  {
    title: "第 6 步：解析并保存",
    icon: IconCode,
    text: "爬虫不会自动理解页面含义。必须根据正文格式选择 JSON、BeautifulSoup、正则或 Selenium 继续处理。",
    example: "JSON 用 response.json()；HTML 用 BeautifulSoup；动态页面用 Selenium。",
  },
];

const webConceptCards = [
  {
    title: "URL：资源地址",
    icon: IconLink,
    text: "URL 告诉程序要访问哪里。它通常包含协议、域名、路径和查询参数。路径决定访问哪个资源，查询参数决定筛选条件。",
    example: "https://example.com/books?page=1 中，/books 是路径，page=1 是查询参数。",
  },
  {
    title: "HTTP：访问规则",
    icon: IconNetwork,
    text: "HTTP 是浏览器和服务器之间的通信规则。爬虫必须按这个规则发送请求、接收响应。",
    example: "GET 常用于读取数据，POST 常用于提交表单、登录信息或创建数据。",
  },
  {
    title: "Request：请求",
    icon: IconSearch,
    text: "请求是客户端发出的访问动作。它说明“我要什么、用什么方式要、我是谁、我能接受什么格式”。",
    example: "请求可能包含 URL、Method、Headers、params、data、json 和 Cookie。",
  },
  {
    title: "Response：响应",
    icon: IconDatabase,
    text: "响应是服务器返回的结果。爬虫要先判断响应是否成功，再决定如何解析响应正文。",
    example: "响应正文可能是 HTML、JSON、图片、PDF、压缩包或纯文本。",
  },
  {
    title: "Status Code：状态码",
    icon: IconCircleAlert,
    text: "状态码是服务器给出的结果提示。它不是最终数据，但能告诉程序下一步该继续解析、重试还是停止。",
    example: "200 成功；301/302 跳转；403 拒绝；404 找不到；429 访问过快。",
  },
  {
    title: "Headers 与 Cookie",
    icon: IconShield,
    text: "Headers 是请求和响应的附加说明，Cookie 则常用于保存会话状态。很多网站会根据这些信息决定返回内容。",
    example: "User-Agent 表示客户端类型；Content-Type 表示正文格式；Cookie 可表示登录状态。不要复制、盗用或传播他人的 Cookie。",
  },
  {
    title: "HTML 与 JSON",
    icon: IconBraces,
    text: "HTML 是给浏览器渲染页面的结构，JSON 是给程序交换数据的结构。二者都能包含信息，但解析方式完全不同。",
    example: "JSON 用字典和列表访问字段；HTML 用标签、class、id 和 CSS 选择器定位节点。",
  },
  {
    title: "静态页与动态页",
    icon: IconMousePointer,
    text: "静态页的关键信息直接在 HTML 源码中；动态页往往先加载空壳，再由 JavaScript 请求数据并渲染。",
    example: "requests 看不到动态结果时，不一定是失败，可能是内容需要浏览器执行 JavaScript 后才出现。",
  },
];

const dataFormatCards = [
  {
    title: "JSON：优先选择的结构化数据",
    icon: IconBraces,
    text: "如果练习站、公开接口或已获授权的数据源直接提供 JSON，优先解析 JSON。它字段清晰、嵌套明确、比从网页里抠文字稳定。",
    example: "response.json()[\"books\"][0][\"title\"] 可以直接拿到第一本书名；真实网站接口要先确认是否允许访问和使用。",
  },
  {
    title: "HTML：网页结构，不是纯文本",
    icon: IconFileSearch,
    text: "HTML 由标签组成。不要把整个网页当成普通字符串硬拆，应先用 BeautifulSoup 建立结构化解析对象。",
    example: "soup.select(\".product-card\") 可以选中所有商品卡片。",
  },
  {
    title: "纯文本：适合简单规则提取",
    icon: IconCode,
    text: "有些响应不是网页，而是日志、公告、配置或简单文本。此时可以用字符串方法或正则表达式提取。",
    example: "从“价格 ¥68.50”中提取金额，正则比 BeautifulSoup 更合适。",
  },
  {
    title: "二进制文件：图片、PDF、压缩包",
    icon: IconArchive,
    text: "图片和 PDF 不是直接可解析的 HTML。保存这类文件时要使用 response.content，而不是 response.text。",
    example: "下载图片通常写入 open(\"cover.jpg\", \"wb\")。",
  },
  {
    title: "动态页面：浏览器看到的不一定在源码里",
    icon: IconMousePointer,
    text: "页面如果由 JavaScript 渲染，requests 拿到的源码可能缺少最终内容。此时要找接口或使用 Selenium。",
    example: "搜索结果由 JS 加载时，BeautifulSoup 解析初始 HTML 可能得到空列表。",
  },
  {
    title: "判断顺序：先看响应，再选工具",
    icon: IconRoute,
    text: "不要一上来就写复杂代码。先打印状态码、Content-Type 和前几百个字符，再决定解析方式。",
    example: "print(response.headers.get(\"Content-Type\")); print(response.text[:300])。",
  },
];

const crawlerWorkflowCards = [
  {
    title: "1. 明确目标字段",
    icon: IconBookOpen,
    text: "先写清楚要采集什么，而不是先写代码。目标字段越明确，解析规则越稳定。",
    example: "目标：书名、作者、分类、售价、评分、库存、详情链接。",
  },
  {
    title: "2. 找入口 URL",
    icon: IconLink,
    text: "入口可以是列表页、搜索页、分页接口或详情页。入口决定爬虫从哪里开始。",
    example: "图书列表页是入口，商品详情页是后续扩展目标。",
  },
  {
    title: "3. 发送请求并检查响应",
    icon: IconNetwork,
    text: "每次请求都应该检查状态码、编码和内容类型。请求失败时不要继续解析。",
    example: "if response.status_code != 200: 先记录错误，而不是 soup.select()。",
  },
  {
    title: "4. 解析页面或接口",
    icon: IconCode,
    text: "根据数据格式选择工具。JSON 走字典列表，HTML 走选择器，动态页面走浏览器自动化。",
    example: "接口数据用 json；静态卡片用 BeautifulSoup；动态搜索用 Selenium。",
  },
  {
    title: "5. 清洗、去重、补字段",
    icon: IconDatabase,
    text: "原始数据通常不能直接使用。需要去掉空格、转换价格类型、统一日期格式、去除重复记录。",
    example: "把“¥68.50”转成 68.50，把“有货 32 本”转成数字 32。",
  },
  {
    title: "6. 保存和复查",
    icon: IconArchive,
    text: "保存成 CSV 或 JSON 后要重新打开检查。采集结果能被再次读取，才算完成。",
    example: "CSV 适合表格查看，JSON 适合保留嵌套结构和后续程序读取。",
  },
];

const crawlerHistoryCards = [
  {
    year: "1990",
    title: "Archie：Web 之前的搜索",
    icon: IconArchive,
    text: "Archie 通常被认为是早期互联网搜索引擎，它索引的是 FTP 站点文件名，而不是今天意义上的网页内容。",
  },
  {
    year: "1993.06",
    title: "World Wide Web Wanderer",
    icon: IconBot,
    text: "Matthew Gray 在 MIT 部署了 Perl 写成的 Wanderer。它最初是为了测量万维网规模，而不是为了做通用搜索。",
  },
  {
    year: "1993.12",
    title: "JumpStation：像现代搜索引擎",
    icon: IconSearch,
    text: "JumpStation 把爬取、索引和搜索框体验结合起来，常被称为第一个表现得像现代 Web 搜索引擎的系统。",
  },
  {
    year: "1994",
    title: "robots.txt：爬虫礼貌协议",
    icon: IconShield,
    text: "Martijn Koster 提出 Robots Exclusion Protocol，让网站能用 robots.txt 告诉爬虫哪些路径不希望被访问。",
  },
  {
    year: "1994",
    title: "WebCrawler：全文搜索",
    icon: IconFileSearch,
    text: "WebCrawler 是早期提供网页全文搜索的搜索引擎之一。它说明爬虫不只是发现链接，还可以建立可检索的正文索引。",
  },
  {
    year: "1996",
    title: "BackRub 与 PageRank",
    icon: IconNetwork,
    text: "Larry Page 和 Sergey Brin 的 BackRub 研究项目用链接关系判断页面重要性，后来演化为 Google 搜索的核心思想之一。",
  },
  {
    year: "1996/2001",
    title: "Internet Archive 与 Wayback Machine",
    icon: IconArchive,
    text: "Internet Archive 从 1996 年开始做网页归档，Wayback Machine 在 2001 年开放，让爬虫成为保存网页历史的工具。",
  },
  {
    year: "2004",
    title: "Selenium：浏览器自动化",
    icon: IconMousePointer,
    text: "Selenium 最初是 ThoughtWorks 的内部测试工具。后来它成为自动化浏览器操作的重要工具，也适合处理动态网页。",
  },
];

const crawlerEvolutionCards = [
  {
    title: "人工目录阶段",
    icon: IconListTree,
    text: "早期上网常靠人工整理目录和链接列表。信息量小时可行，但网页快速增长后，很难靠人工维护。",
  },
  {
    title: "自动发现链接",
    icon: IconBot,
    text: "爬虫从一个入口页面出发，读取其中的链接，再继续访问新页面，这就是抓取网页的基本扩散方式。",
  },
  {
    title: "索引与排序",
    icon: IconSearch,
    text: "抓到网页后，还要抽取文本、建立倒排索引、根据关键词和链接关系排序，搜索引擎才真正可用。",
  },
  {
    title: "礼貌爬取",
    icon: IconShield,
    text: "随着爬虫增多，robots.txt、访问频率控制、User-Agent 标识、超时和重试策略逐渐成为工程习惯。",
  },
  {
    title: "动态网页时代",
    icon: IconMousePointer,
    text: "越来越多网页由 JavaScript 渲染，requests 只能拿到骨架，Selenium、Playwright 这类浏览器自动化工具开始变重要。",
  },
  {
    title: "今天的爬虫",
    icon: IconDatabase,
    text: "现代爬虫既包括搜索引擎索引，也包括数据采集、网页归档、站点监测、测试自动化和 AI 训练数据治理。",
  },
];

const privacyRiskCards = [
  {
    title: "技术向善：能爬不代表应该爬",
    icon: IconShield,
    text: "爬虫是一种自动化能力，不是免责任工具。公开页面、可访问接口、可复制文本，都不等于可以无限制采集和再利用。",
    example: "判断底线：是否涉及个人身份、联系方式、位置、账号、画像、交易、医疗、金融等敏感信息。",
  },
  {
    title: "个人隐私：不要采集可识别个人的信息",
    icon: IconCircleAlert,
    text: "个人信息不仅是姓名和手机号，也包括能间接识别个人的账号、头像、主页链接、设备标识、轨迹、评论记录和社交关系。",
    example: "即使页面公开展示，也不应批量抓取后用于画像、营销、骚扰、出售或交叉匹配。",
  },
  {
    title: "平台规则：遵守 robots.txt 与服务条款",
    icon: IconBookOpen,
    text: "很多网站会通过 robots.txt、用户协议、接口权限、登录规则说明哪些内容可以访问，哪些内容不能批量抓取。",
    example: "robots.txt 是爬虫约定，不是法律授权，也不是安全防护。访问真实网站前，还要阅读网站服务条款并考虑数据用途。",
  },
  {
    title: "法律风险：可能涉及多种责任",
    icon: IconCircleAlert,
    text: "不合规爬取可能触及个人信息保护、著作权、商业秘密、不正当竞争、计算机信息系统安全等风险。",
    example: "绕过限制、伪装身份、高频请求、抓取账号资料、出售数据，风险明显高于普通公开页面学习访问。",
  },
  {
    title: "真实案例：新浪微博诉脉脉",
    icon: IconDatabase,
    text: "新浪微博起诉脉脉经营方，理由包括未经许可获取并使用微博用户信息。法院认定相关行为构成不正当竞争，并要求停止行为、赔偿损失等。",
    example: "启示：爬虫抓到的数据如果包含用户关系和个人资料，后续使用方式同样会产生法律风险。",
  },
  {
    title: "国际案例：Clearview AI",
    icon: IconGlobe,
    text: "Clearview AI 被指从互联网抓取大量人脸图片建立识别数据库，并因生物识别隐私问题在美国被 ACLU 等起诉，后达成和解。",
    example: "启示：公开图片也可能涉及高度敏感的生物识别信息，不能因为“网上能看到”就批量采集。",
  },
];

const crawlerSourceCards = [
  {
    title: "World Wide Web Wanderer",
    icon: IconExternalLink,
    href: "https://en.wikipedia.org/wiki/World_Wide_Web_Wanderer",
  },
  {
    title: "JumpStation",
    icon: IconExternalLink,
    href: "https://en.wikipedia.org/wiki/JumpStation",
  },
  {
    title: "Robots.txt",
    icon: IconExternalLink,
    href: "https://en.wikipedia.org/wiki/Robots.txt",
  },
  {
    title: "WebCrawler",
    icon: IconExternalLink,
    href: "https://en.wikipedia.org/wiki/WebCrawler",
  },
  {
    title: "PageRank",
    icon: IconExternalLink,
    href: "https://en.wikipedia.org/wiki/PageRank",
  },
  {
    title: "History of Google",
    icon: IconExternalLink,
    href: "https://en.wikipedia.org/wiki/History_of_Google",
  },
  {
    title: "Selenium History",
    icon: IconExternalLink,
    href: "https://www.selenium.dev/history/",
  },
  {
    title: "Wayback Machine",
    icon: IconExternalLink,
    href: "https://en.wikipedia.org/wiki/Wayback_Machine",
  },
  {
    title: "Archie",
    icon: IconExternalLink,
    href: "https://en.wikipedia.org/wiki/Archie_(search_engine)",
  },
  {
    title: "个人信息保护法",
    icon: IconExternalLink,
    href: "https://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html",
  },
  {
    title: "新浪微博诉脉脉案",
    icon: IconExternalLink,
    href: "https://www.gov.cn/xinwen/2017-02/06/content_5165661.htm",
  },
  {
    title: "ACLU v. Clearview AI",
    icon: IconExternalLink,
    href: "https://www.aclu.org/press-releases/aclu-sues-clearview-ai",
  },
  {
    title: "Clearview AI Settlement",
    icon: IconExternalLink,
    href: "https://www.aclu.org/press-releases/clearview-ai-settles-lawsuit-brought-aclu-agrees-limit-sales-face-recognition-company",
  },
];

const materialCards = [
  {
    title: "JSON 练习接口",
    icon: IconBraces,
    desc: "模拟真实接口返回，包含分页、筛选、嵌套作者、价格、库存和销量字段。",
    href: sampleJsonHref,
  },
  {
    title: "静态网页练习页",
    icon: IconFileSearch,
    desc: "真实商城风格的服务端渲染列表页，适合 BeautifulSoup 和正则提取。",
    href: staticHtmlHref,
  },
  {
    title: "动态搜索练习页",
    icon: IconMousePointer,
    desc: "页面由 JavaScript 读取 JSON 后动态渲染结果，适合 Selenium。",
    href: dynamicHtmlHref,
  },
];

const codePracticeMap = [
  { title: "5.1 首次请求", icon: IconNetwork, text: "访问线上 JSON 接口，观察状态码、响应头和正文预览。" },
  { title: "5.2 参数与请求头", icon: IconLink, text: "理解 params、headers、User-Agent 和最终请求地址。" },
  { title: "5.3 Session 会话", icon: IconShield, text: "用 Session 复用请求头和连接，为需要连续访问的任务做准备。" },
  { title: "5.4 POST 请求", icon: IconCode, text: "理解表单提交、JSON 提交和接口回显这类常见 POST 场景。" },
  { title: "5.5 异常处理", icon: IconCircleAlert, text: "解决请求失败时怎么办，让程序在超时、断网和坏响应面前不失控。" },
  { title: "5.6 限速与重试", icon: IconRoute, text: "解决请求成功后怎么礼貌访问，把日志、间隔和有限重试组织起来。" },
  { title: "5.7 JSON 结构观察", icon: IconBraces, text: "先看顶层字段、分页信息和第一条记录，再写提取规则。" },
  { title: "5.8 分页抓取", icon: IconListTree, text: "按 page、has_next、next_url 的思想组织多页采集。" },
  { title: "5.9 JSON 筛选统计", icon: IconDatabase, text: "把 JSON 整理成统一记录列表，再做筛选、排序和基础统计。" },
  { title: "5.10 BeautifulSoup 速查", icon: IconBookOpen, text: "先用表格认识 BeautifulSoup 的常用对象和方法。" },
  { title: "5.11 HTML 初次解析", icon: IconFileSearch, text: "用 BeautifulSoup 定位商品卡片并提取可见字段。" },
  { title: "5.12 HTML 字段清洗", icon: IconCode, text: "把 HTML 属性和文本清洗成结构化记录，为后续保存和统计做准备。" },
  { title: "5.13 正则速查", icon: IconBookOpen, text: "先用表格认识 re 模块的常见函数和匹配写法。" },
  { title: "5.14 正则提取", icon: IconSearch, text: "从稳定文本中提取编号、评分、评论数、仓库和库存。" },
  { title: "5.15 URL 与去重", icon: IconRoute, text: "把相对链接转成绝对链接，并用唯一编号去重。" },
  { title: "5.16 Selenium 速查", icon: IconBookOpen, text: "先用表格认识浏览器对象、定位、等待和关闭。" },
  { title: "5.17 Selenium 等待", icon: IconMousePointer, text: "用显式等待处理 JavaScript 动态渲染页面。" },
  { title: "5.18 保存数据", icon: IconArchive, text: "把结构化结果落盘成 CSV 和 JSON，得到可复查、可复用的中间成果。" },
  { title: "5.19 生成报告", icon: IconBookOpen, text: "在保存后的数据基础上继续汇总，输出真正给人阅读的结果简报。" },
];

const codeSlides = [
  {
    no: "01",
    label: "requests 第一请求",
    title: "代码段 1：用 requests 访问 niuniulab 的 JSON 练习接口",
    code: `import requests  # 导入 requests 模块，用来发送 HTTP 请求
BASE_URL = "https://niuniulab.com/courses/python/ch07"  # 设置第七章练习资源的根地址
url = f"{BASE_URL}/sample_books.json"  # 拼接 JSON 练习接口的完整访问地址
response = requests.get(url, timeout=10)  # 发送 GET 请求，timeout=10 表示最多等待 10 秒
print("请求地址：", url)  # 打印实际访问的 URL，方便检查路径是否正确
print("状态码：", response.status_code)  # 打印状态码，200 通常表示请求成功
print("响应类型：", response.headers.get("Content-Type"))  # 打印 Content-Type，判断返回内容是不是 JSON
print("响应编码：", response.encoding)  # 打印响应编码，排查中文乱码时很有用
print("正文预览：", response.text[:200])  # 打印前 200 个字符，先观察数据长什么样`,
    explain: "这一段展示 Python 也能像浏览器一样访问线上 URL。先不急着解析数据，先观察请求地址、状态码、响应头、编码和正文片段。",
    key: "requests.get() 负责发送请求，response 是服务器返回给程序的响应对象。",
    check: "如果状态码不是 200，先把请求地址复制到浏览器打开，再检查网络、路径和服务器是否可访问。",
  },
  {
    no: "02",
    label: "参数与请求头",
    title: "代码段 2：给请求添加参数和请求头",
    code: `import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"
url = f"{BASE_URL}/sample_books.json"

params = {"category": "Python", "sort": "rating_desc"}
headers = {
    "User-Agent": "Mozilla/5.0 (Python teaching crawler)",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
}

response = requests.get(url, params=params, headers=headers, timeout=10)
print("最终请求地址：", response.url)
print("状态码：", response.status_code)
print("服务器返回类型：", response.headers.get("Content-Type"))`,
    explain: "真实请求经常不只是一个 URL。params 会被拼到查询字符串里，headers 用来说明客户端身份和可接受的数据类型。",
    key: "params 负责查询参数，headers 负责请求说明。它们是 requests 中最常用的两个参数。",
    check: "打印 response.url 可以确认参数是否真的拼进了 URL。",
  },
  {
    no: "03",
    label: "Session 会话",
    title: "代码段 3：用 Session 复用请求设置",
    code: `import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Python teaching crawler)",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
})

html_response = session.get(f"{BASE_URL}/books_static.html", timeout=10)
json_response = session.get(f"{BASE_URL}/sample_books.json", timeout=10)

print("HTML 状态码：", html_response.status_code)
print("JSON 状态码：", json_response.status_code)
print("当前 User-Agent：", session.headers["User-Agent"])`,
    explain: "Session 可以在多次请求之间复用 headers、cookies 和底层连接。真实项目中，连续访问列表页、详情页、接口时经常使用它。",
    key: "requests.Session() 适合组织一组相关请求，比每次都重新写 headers 更清晰。",
    check: "Session 不是绕过登录限制的工具；涉及登录态和 Cookie 时必须确认来源和用途合法。",
  },
  {
    no: "04",
    label: "POST 请求",
    title: "代码段 4：构造一个 POST JSON 请求",
    code: `import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"
post_url = f"{BASE_URL}/search_demo.html"

payload = {
    "keyword": "Python",
    "max_price": 80,
    "sort": "rating_desc",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Python teaching crawler)",
    "Accept": "application/json",
}

request = requests.Request(
    method="POST",
    url=post_url,
    json=payload,
    headers=headers,
)
prepared = request.prepare()

print("请求方法：", prepared.method)
print("请求地址：", prepared.url)
print("Content-Type：", prepared.headers.get("Content-Type"))
print("请求体：", prepared.body.decode("utf-8"))`,
    explain: "GET 常用于读取数据，POST 常用于提交表单或 JSON。练习站是静态站点，不能真正接收 POST，所以这里先构造请求并观察它会被如何发送。",
    key: "requests.Request(..., json=payload) 会把字典序列化为 JSON，并自动设置合适的 Content-Type。",
    check: "真实 POST 接口需要服务端支持和明确授权；静态 HTML 页面不能像后端接口一样接收并处理 POST 数据。",
  },
  {
    no: "05",
    label: "请求异常处理",
    title: "代码段 5：请求失败时及时停下并给出清楚提示",
    code: `import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"

def fetch_json(path):
    url = f"{BASE_URL}/{path}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("请求超时：", url)
    except requests.exceptions.HTTPError as error:
        print("状态码错误：", error)
    except requests.exceptions.RequestException as error:
        print("网络请求失败：", error)
    except ValueError:
        print("响应内容不是合法 JSON：", url)
    return None

data = fetch_json("sample_books.json")
if data:
    print("接口名称：", data["api"]["name"])`,
    explain: "这一页只解决一个问题：请求失败时怎么办。网络请求可能超时、断网、返回错误状态码，也可能返回的不是 JSON，程序必须先停下来并说明原因。",
    key: "raise_for_status() 会把 4xx、5xx 状态码转成异常，便于把“失败请求”和“正常解析”分开处理。",
    check: "不要在请求失败后继续进入数据提取环节，否则后面会出现更难理解的 KeyError 或 AttributeError。",
  },
  {
    no: "06",
    label: "日志限速重试",
    title: "代码段 6：加入日志、访问间隔和有限重试",
    code: `import logging
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

BASE_URL = "https://niuniulab.com/courses/python/ch07"
session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=0.8,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)
session.mount("http://", adapter)

urls = [
    f"{BASE_URL}/sample_books.json",
    f"{BASE_URL}/books_static.html",
    f"{BASE_URL}/search_demo.html",
]

for url in urls:
    logging.info("开始访问：%s", url)
    response = session.get(url, timeout=10)
    logging.info("完成访问：%s 状态码=%s 大小=%s", url, response.status_code, len(response.content))
    time.sleep(1)`,
    explain: "这一页处理的是另一个问题：请求已经会发了，怎样让访问更稳、更有礼貌。日志用于复盘，sleep 控制节奏，有限重试只处理短暂抖动。",
    key: "Retry 解决的是“偶发失败再试一次”，不是“请求失败后一直硬冲”。",
    check: "429 表示访问过快时，应降低频率，而不是加大并发或无限重试。",
  },
  {
    no: "07",
    label: "JSON 结构观察",
    title: "代码段 7：先观察 JSON 结构，再写提取规则",
    code: `import pprint
import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"
data = requests.get(f"{BASE_URL}/sample_books.json", timeout=10).json()

print("顶层字段：", data.keys())
print("分页信息：", data["pagination"])
print("可用分类：", data["filters"]["categories"])

first_book = data["books"][0]
print("第一本书的字段：", first_book.keys())
pprint.pprint(first_book, sort_dicts=False)`,
    explain: "JSON 解析最容易出错的地方是没看清层级。先观察顶层字段、分页信息和第一条记录，再决定怎么取值。",
    key: "字典用 key 取值，列表用下标取值。复杂 JSON 通常是字典和列表的嵌套。",
    check: "遇到 KeyError 时，先打印 keys()，不要凭感觉猜字段名。",
  },
  {
    no: "08",
    label: "分页抓取",
    title: "代码段 8：按分页思想组织多页采集",
    code: `import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"

def fetch_page(page):
    response = requests.get(
        f"{BASE_URL}/sample_books.json",
        params={"page": page},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

all_books = []
page = 1

while True:
    data = fetch_page(page)
    page_info = data["pagination"]
    all_books.extend(data["books"])

    print(f"已读取第 {page_info['page']} 页，累计 {len(all_books)} 条")
    if not page_info["has_next"]:
        break
    page += 1

print("最终采集数量：", len(all_books))`,
    explain: "很多接口不是一次返回所有数据，而是分页返回。即使本练习接口只有一页，也要掌握 has_next、page、next_url 这类分页思想。",
    key: "分页抓取的核心是循环请求、累计结果、判断是否还有下一页。",
    check: "真实分页中要设置最大页数或最大记录数，避免因为接口异常进入无限循环。",
  },
  {
    no: "09",
    label: "JSON 筛选统计",
    title: "代码段 9：把 JSON 整理成记录列表，再筛选、排序和统计",
    code: `import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"
data = requests.get(f"{BASE_URL}/sample_books.json", timeout=10).json()

rows = []
for book in data["books"]:
    rows.append({
        "id": book["id"],
        "title": book["title"],
        "category": book["category"],
        "price": book["pricing"]["sale_price"],
        "rating": book["rating"]["score"],
        "stock": book["stock"]["quantity"],
    })

available = [row for row in rows if row["stock"] > 0]
top_books = sorted(available, key=lambda row: row["rating"], reverse=True)[:5]

print("有库存图书数量：", len(available))
for row in top_books:
    print(row["title"], row["category"], row["price"], row["rating"])`,
    explain: "这一页面对的是结构化接口数据。目标不是清洗网页文本，而是把嵌套 JSON 摊平成统一的 rows 列表，方便后续筛选、排序和统计。",
    key: "把复杂 JSON 变成统一记录列表，是接口采集走向分析和落盘的关键中间层。",
    check: "价格、评分、库存应当是数字类型，否则后续排序和统计会出错。",
  },
  {
    no: "10",
    kind: "table",
    label: "BeautifulSoup 速查",
    title: "工具速查：BeautifulSoup 常用函数和对象",
    tableRows: [
      { name: "BeautifulSoup(html, \"html.parser\")", usage: "把 HTML 字符串解析成可查询的对象", example: "soup = BeautifulSoup(html, \"html.parser\")" },
      { name: "soup.select(css)", usage: "用 CSS 选择器查找一组节点", example: "soup.select(\".product-card\")" },
      { name: "node.select_one(css)", usage: "在当前节点内部查找第一个匹配节点", example: "card.select_one(\".product-title\")" },
      { name: "node.get_text(strip=True)", usage: "提取节点中的可见文本，并去掉首尾空白", example: "title.get_text(strip=True)" },
      { name: "node[\"属性名\"]", usage: "读取标签属性，常用于 href、src、data-*", example: "card[\"data-sku\"]" },
      { name: "find() / find_all()", usage: "按标签名或属性查找节点", example: "soup.find_all(\"article\")" },
    ],
    explain: "BeautifulSoup 的核心是把 HTML 当成树结构来查找。先定位大容器，再在容器内部提取字段。",
    key: "select、select_one、get_text、读取属性，是本章最常用的四类操作。",
    check: "如果选择器没有结果，先确认目标文字是否存在于 response.text 中。",
  },
  {
    no: "11",
    label: "BeautifulSoup",
    title: "代码段 11：用 BeautifulSoup 从 HTML 卡片里提取图书信息",
    code: `import requests
from bs4 import BeautifulSoup

BASE_URL = "https://niuniulab.com/courses/python/ch07"
html_url = f"{BASE_URL}/books_static.html"
html = requests.get(html_url, timeout=10).text
soup = BeautifulSoup(html, "html.parser")

cards = soup.select(".product-card")
print("商品卡片数量：", len(cards))

for card in cards[:5]:
    sku = card["data-sku"]
    category = card["data-category"]
    title = card.select_one(".product-title").get_text(strip=True)
    price = card.select_one(".price strong").get_text(strip=True)
    coupon = card.select_one(".coupon").get_text(strip=True)
    print(sku, category, title, price, coupon)`,
    explain: "BeautifulSoup 适合处理结构清晰的 HTML。先定位商品卡片，再在每个卡片内部提取字段。",
    key: "select() 返回一组节点，select_one() 返回第一个匹配节点。",
    check: "如果 cards 数量为 0，先确认目标内容是否真的存在于 HTML 源码中。",
  },
  {
    no: "12",
    label: "HTML 字段清洗",
    title: "代码段 12：把 HTML 属性和文本清洗成结构化记录",
    code: `import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://niuniulab.com/courses/python/ch07"
html_url = f"{BASE_URL}/books_static.html"
soup = BeautifulSoup(requests.get(html_url, timeout=10).text, "html.parser")

records = []
for card in soup.select(".product-card"):
    record = {
        "id": card["data-sku"],
        "title": card.select_one(".product-title").get_text(strip=True),
        "category": card["data-category"],
        "price": float(card["data-price"]),
        "rating": float(card["data-rating"]),
        "stock": int(card["data-stock"]),
        "detail_url": urljoin(html_url, f"#{card['id']}"),
    }
    records.append(record)

for record in records[:5]:
    print(record)`,
    explain: "这一页和前面的 JSON 不同，它处理的是网页里拿到的属性和文本。目标是把 HTML 中分散的字符串字段整理成结构化 record，便于保存、统计和复用。",
    key: "data-* 属性和可见文本结合起来，才能把 HTML 页面真正转换成程序可用的结构化记录。",
    check: "清洗后可以用 type(record['price'])、type(record['stock']) 检查字段是否已经转成数字。",
  },
  {
    no: "13",
    kind: "table",
    label: "正则速查",
    title: "工具速查：re 模块常用函数和写法",
    tableRows: [
      { name: "re.search(pattern, text)", usage: "从文本中找第一个匹配项", example: "re.search(r\"\\d+\", text)" },
      { name: "re.findall(pattern, text)", usage: "找出所有匹配结果", example: "re.findall(r\"¥\\d+\\.\\d{2}\", text)" },
      { name: "match.group()", usage: "获取完整匹配文本", example: "match.group()" },
      { name: "match.group(1)", usage: "获取第一个括号捕获的内容", example: "re.search(r\"价格：(.*)\", text).group(1)" },
      { name: "re.sub(pattern, repl, text)", usage: "替换符合模式的内容，常用于清洗", example: "re.sub(r\"\\s+\", \"\", text)" },
      { name: "r\"...\"", usage: "原始字符串，避免反斜杠被 Python 提前转义", example: "r\"\\d{4}-\\d{2}-\\d{2}\"" },
    ],
    explain: "正则适合从短文本里提取格式稳定的内容，不适合直接解析整页 HTML。",
    key: "search、findall、group、sub 和原始字符串 r\"\" 是入门必须掌握的组合。",
    check: "正则复杂时，先从最小模式开始验证，再逐步增加限制条件。",
  },
  {
    no: "14",
    label: "正则表达式",
    title: "代码段 14：用正则表达式提取局部文本模式",
    code: `import re

book_id_text = "编号 CB-2026-0007，ISBN 978-7-115-26007-3"
rating_text = "评分：4.7 / 5.0，评论 177 条"
stock_text = "库存：有货，成都仓，18 本"

book_id = re.search(r"CB-\\d{4}-\\d{4}", book_id_text).group()
isbn = re.search(r"ISBN\\s+([\\d-]+)", book_id_text).group(1)
score = float(re.search(r"评分：([\\d.]+)", rating_text).group(1))
comments = int(re.search(r"评论\\s*(\\d+)\\s*条", rating_text).group(1))
stock_match = re.search(r"库存：([^，]+)，([^，]+)，(\\d+) 本", stock_text)

print(book_id, isbn, score, comments)
print("库存状态：", stock_match.group(1))
print("仓库：", stock_match.group(2))
print("库存数量：", int(stock_match.group(3)))`,
    explain: "正则表达式适合处理一小段格式稳定的文本，例如编号、ISBN、评分、评论数和库存数量。",
    key: "正则表达式解决的是文本模式匹配，不要用它替代完整 HTML 解析器。",
    check: "如果匹配失败，先打印原始文本，再逐步缩短正则表达式。",
  },
  {
    no: "15",
    label: "URL 与去重",
    title: "代码段 15：把相对链接转成绝对链接，并按编号去重",
    code: `import requests
from urllib.parse import urljoin

SITE_ROOT = "https://niuniulab.com"
BASE_URL = f"{SITE_ROOT}/courses/python/ch07"
data = requests.get(f"{BASE_URL}/sample_books.json", timeout=10).json()

unique_books = {}
for book in data["books"]:
    absolute_url = urljoin(SITE_ROOT, book["detail_url"])
    book_id = book["id"]
    if book_id not in unique_books:
        unique_books[book_id] = {
            "id": book_id,
            "title": book["title"],
            "detail_url": absolute_url,
        }

print("去重后数量：", len(unique_books))
for book in list(unique_books.values())[:5]:
    print(book["id"], book["title"], book["detail_url"])`,
    explain: "真实采集中，同一条记录可能从搜索页、分类页、排行榜页重复出现。保存前要用唯一编号或详情链接去重。",
    key: "urljoin() 可以把相对链接转换成绝对链接，字典可以按唯一键去重。",
    check: "唯一键要稳定，优先选择 id、sku、ISBN 或详情页 URL。",
  },
  {
    no: "16",
    kind: "table",
    label: "Selenium 速查",
    title: "工具速查：Selenium 常用对象和方法",
    tableRows: [
      { name: "python -m pip install selenium", usage: "安装 Selenium 库，运行前还需要本机安装 Chrome 或 Edge 浏览器", example: "只需安装一次" },
      { name: "webdriver.Chrome()", usage: "启动 Chrome 浏览器，由程序控制页面", example: "driver = webdriver.Chrome()" },
      { name: "driver.get(url)", usage: "打开指定网页", example: "driver.get(search_url)" },
      { name: "find_element(By.ID, value)", usage: "定位一个页面元素", example: "driver.find_element(By.ID, \"keyword\")" },
      { name: "find_elements(By.CSS_SELECTOR, value)", usage: "定位一组页面元素", example: "driver.find_elements(By.CSS_SELECTOR, \".product-card\")" },
      { name: "WebDriverWait(driver, 10)", usage: "显式等待某个元素或条件出现", example: "wait.until(EC.presence_of_element_located(...))" },
      { name: "send_keys() / click()", usage: "模拟键盘输入和鼠标点击", example: "search_box.send_keys(\"Python\")" },
      { name: "driver.quit()", usage: "关闭浏览器并释放资源", example: "finally: driver.quit()" },
    ],
    explain: "Selenium 操作的是真实浏览器。它适合必须经过 JavaScript 渲染或用户交互后才出现的内容。",
    key: "浏览器对象、元素定位、显式等待、输入点击、退出浏览器，是 Selenium 的基本链条。",
    check: "不要忘记 driver.quit()，否则浏览器进程可能一直留在后台。",
  },
  {
    no: "17",
    label: "Selenium 显式等待",
    title: "代码段 17：用 Selenium 等待动态搜索结果出现",
    code: `from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://niuniulab.com/courses/python/ch07"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get(f"{BASE_URL}/search_demo.html")
    search_box = wait.until(EC.presence_of_element_located((By.ID, "keyword")))
    search_box.clear()
    search_box.send_keys("Python")
    search_box.send_keys(Keys.ENTER)

    wait.until(lambda page: len(page.find_elements(By.CSS_SELECTOR, "#dynamicResults .product-card")) > 0)
    cards = driver.find_elements(By.CSS_SELECTOR, "#dynamicResults .product-card")
    for card in cards[:5]:
        title = card.find_element(By.CSS_SELECTOR, ".product-title").text
        price = card.find_element(By.CSS_SELECTOR, ".price strong").text
        print(title, price)
finally:
    driver.quit()`,
    explain: "动态页面需要等待 JavaScript 渲染完成。显式等待比 sleep 更稳，因为它等待的是具体元素或条件。",
    key: "WebDriverWait + expected_conditions 是 Selenium 处理动态页面的常用组合。",
    check: "如果找不到元素，先确认页面是否打开成功，再检查选择器是否正确。",
  },
  {
    no: "18",
    label: "保存结果",
    title: "代码段 18：把结构化结果落盘成 CSV 与 JSON",
    code: `import csv
import json
import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"
data = requests.get(f"{BASE_URL}/sample_books.json", timeout=10).json()

records = []
for book in data["books"]:
    records.append({
        "id": book["id"],
        "title": book["title"],
        "category": book["category"],
        "price": book["pricing"]["sale_price"],
        "rating": book["rating"]["score"],
        "stock": book["stock"]["quantity"],
    })

fieldnames = ["id", "title", "category", "price", "rating", "stock"]
with open("books.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

with open("books.json", "w", encoding="utf-8") as file:
    json.dump(records, file, ensure_ascii=False, indent=2)`,
    explain: "这一页只负责把已经整理好的 records 保存成文件。它产出的是中间成果，便于下次继续分析，而不是直接面向读者的最终结论。",
    key: "CSV 适合表格查看，JSON 适合保留结构并供程序继续读取；两者解决的是“保存数据”，不是“解释数据”。",
    check: "CSV 在 Excel 中打开乱码时，优先使用 utf-8-sig 编码。",
  },
  {
    no: "19",
    label: "生成报告",
    title: "代码段 19：根据采集结果生成给人阅读的网络数据简报",
    code: `from collections import Counter
from pathlib import Path
import requests

BASE_URL = "https://niuniulab.com/courses/python/ch07"
data = requests.get(f"{BASE_URL}/sample_books.json", timeout=10).json()
books = data["books"]

category_counter = Counter(book["category"] for book in books)
avg_price = sum(book["pricing"]["sale_price"] for book in books) / len(books)
low_stock = [book for book in books if 0 < book["stock"]["quantity"] <= 10]
top_book = max(books, key=lambda book: book["rating"]["score"])

lines = [
    "CampusBook 网络数据简报",
    f"图书总数：{len(books)}",
    f"平均售价：{avg_price:.2f} 元",
    f"评分最高：{top_book['title']}（{top_book['rating']['score']} 分）",
    f"低库存图书：{len(low_stock)} 本",
    "分类统计：",
]

for category, count in category_counter.most_common():
    lines.append(f"- {category}: {count} 本")

Path("summary_report.txt").write_text("\\n".join(lines), encoding="utf-8")
print("\\n".join(lines))`,
    explain: "这一页是在保存之后继续前进，把原始 records 转换成结论和摘要。报告不是再存一份数据，而是把数据解释成人能快速读懂的信息。",
    key: "Counter、sum、max、列表推导式可以把“保存好的数据”进一步变成摘要结论和文字报告。",
    check: "报告生成后要打开 summary_report.txt，检查中文、数字和换行是否正常，确认它真的适合直接阅读。",
  },
];

const ethics = [
  {
    title: "公开数据优先",
    icon: IconGlobe,
    text: "只采集公开页面和公开接口，不采集个人隐私、账号信息或敏感数据。",
  },
  {
    title: "不绕过限制",
    icon: IconShield,
    text: "不要绕过登录、验证码、付费墙、访问控制或网站明确禁止的路径。",
  },
  {
    title: "控制访问频率",
    icon: IconRoute,
    text: "给请求设置 timeout，降低访问频率，避免把正常练习变成对服务器的压力测试。",
  },
  {
    title: "先练习再实战",
    icon: IconBookOpen,
    text: "先使用本章练习素材掌握方法，再把同样的流程迁移到允许访问的真实数据源。",
  },
];

const capstoneCards = [
  {
    title: "实验目标",
    icon: IconNetwork,
    text: "使用 requests 访问酷狗音乐排行榜页面，采集 TOP500 歌曲的排名、歌曲名、演唱者和歌曲时长，并保存到 songTop500.csv 文本文件。",
  },
  {
    title: "页面规律",
    icon: IconRoute,
    text: "排行榜 URL 中的页码遵循 /home/1-8888.html 这种模式。每页约 22 首歌曲，因此需要用循环组织 1 到 23 页的地址。",
    href: kugouRankHref,
  },
  {
    title: "解析重点",
    icon: IconFileSearch,
    text: "页面榜单位于 class 为 pc_temp_songlist 的区域中。每条 li 里可以拿到 title、排名 span.pc_temp_num 和时长 span.pc_temp_time，再拆分出演唱者与歌曲名。",
  },
  {
    title: "输出文件",
    icon: IconArchive,
    text: "将结果按“排名 歌曲名称 演唱者 歌曲长度”的顺序逐行写入 songTop500.csv。CSV 本质上也是文本文件，便于后续用 Excel、记事本或 Python 再处理。",
  },
  {
    title: "实验报告模板",
    icon: IconBookOpen,
    text: "下载实验四报告模板，按模板填写实验目的、核心代码、运行结果、结果分析和实验收获。",
    href: kugouReportTemplateHref,
  },
  {
    title: "提交方式",
    icon: IconExternalLink,
    text: "按照实验报告模板提交实验四结果。正文应包含实验目的、核心代码、运行结果、结果分析和实验收获。",
    href: kugouReportSubmitHref,
  },
];

const summaryCards = [
  {
    title: "请求层",
    icon: IconNetwork,
    text: "requests 负责获取网页和接口数据，是网络数据采集的入口。",
  },
  {
    title: "解析层",
    icon: IconCode,
    text: "JSON、BeautifulSoup、正则表达式分别处理不同形态的数据。",
  },
  {
    title: "浏览器层",
    icon: IconMousePointer,
    text: "Selenium 用来处理必须由真实浏览器交互和渲染后才能得到的数据。",
  },
];
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
        <span class="brand-tag">Chapter 7</span>
        <strong>网络数据爬取</strong>
      </a>
      <CourseSwitcher />
    </header>

    <main id="top" class="page is-slide-deck">
      <section
        id="cover"
        class="hero reveal"
        data-outline-level="1"
        data-outline-label="章节封面"
      >
        <p class="kicker">CHAPTER 07 WEB DATA CRAWLING</p>
        <h1>网络数据爬取：<br />让 Python 学会从互联网获取信息</h1>
        <p class="hero-intro">
          第七章把前面学过的数据类型、文件操作和模块能力串起来。
          本章不再只处理本地文件，而是从网页和接口获取公开数据，再完成解析、提取、保存和简要分析。
        </p>
        <ul class="hero-checklist">
          <li>从最简单的 <code>requests.get()</code> 开始，理解请求和响应。</li>
          <li>同时覆盖 JSON、HTML、正则表达式和 Selenium 四类典型解析场景。</li>
          <li>使用可复现的练习素材，降低真实网站变化带来的干扰。</li>
        </ul>
        <div class="goal-cards fly-in-seq">
          <article v-for="goal in learningGoals" :key="goal">
            <h2>能力目标</h2>
            <p>{{ goal }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章路线"
      >
        <h2>2 本章路线：从一次请求，走到一个完整爬虫实验</h2>
        <p class="section-note">
          学习顺序按照真实数据采集流程展开：先发出请求，再识别数据格式，然后选择解析工具，
          最后把结果保存为可以复用的数据文件，并迁移到真实课程实验场景。
        </p>
        <div class="chapter-seven-rhythm">
          <span v-for="item in roadmap" :key="item">{{ item }}</span>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="练习站入口"
      >
        <div class="section-head">
          <p class="kicker">PRACTICE SITE</p>
          <h2>3 练习数据入口：JSON、静态网页、动态网页</h2>
        </div>
        <p class="section-note">
          三个入口对应三类常见采集场景：接口数据、服务端渲染页面、浏览器动态渲染页面。
          CSS 和 JavaScript 作为页面资源自动加载，不作为单独采集目标。
        </p>
        <div class="chapter-seven-grid chapter-seven-link-grid">
          <article class="chapter-seven-card" v-for="item in materialCards" :key="item.href">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.desc }}</p>
            <a
              class="chapter-seven-link"
              :href="item.href"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ item.href }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="基础概念"
      >
        <div class="section-head">
          <p class="kicker">SECTION 04 FOUNDATIONS</p>
          <h2>4 基础概念：先理解网络访问，再学习爬虫工具</h2>
        </div>
        <p class="chapter-seven-cue">
          爬虫程序不是凭空“拿到数据”，而是沿着网络协议访问资源、接收响应、识别内容格式、
          解析目标字段。第 4 节先建立这些概念，再进入代码实战。
        </p>
        <div class="chapter-seven-grid chapter-seven-foundation-map">
          <article
            class="chapter-seven-card chapter-seven-map-card"
            v-for="item in foundationMap"
            :key="item.title"
          >
            <img class="chapter-seven-map-icon" :src="item.icon" alt="" aria-hidden="true" />
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="网络访问"
      >
        <div class="section-head">
          <p class="kicker">4.1 FOUNDATIONS</p>
          <h2>4.1 一次网络访问：从 URL 到响应的完整过程</h2>
        </div>
        <p class="chapter-seven-cue">
          爬虫程序和浏览器做的是同一类事情：找到资源、发送请求、接收响应、解析内容。
          区别在于浏览器把结果显示成页面，爬虫把结果交给 Python 程序继续处理。
        </p>

        <h3 class="chapter-seven-block-title">一次访问可以拆成 6 步</h3>
        <div class="chapter-seven-grid chapter-seven-quad-grid">
          <article class="chapter-seven-card chapter-seven-note-card" v-for="item in requestFlowCards" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
            <p class="chapter-seven-example"><strong>例子：</strong>{{ item.example }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="请求与响应"
      >
        <div class="section-head">
          <p class="kicker">4.2 FOUNDATIONS</p>
          <h2>4.2 请求与响应：读懂爬虫程序最常接触的对象</h2>
        </div>
        <p class="chapter-seven-cue">
          写爬虫时，最核心的对象不是“网页”，而是请求和响应。请求决定服务器返回什么，
          响应决定程序后续能不能解析、怎么解析。
        </p>

        <h3 class="chapter-seven-block-title">网络访问的 8 个基础概念</h3>
        <div class="chapter-seven-grid chapter-seven-quad-grid">
          <article class="chapter-seven-card chapter-seven-note-card" v-for="item in webConceptCards" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
            <p class="chapter-seven-example"><strong>例子：</strong>{{ item.example }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="数据格式"
      >
        <div class="section-head">
          <p class="kicker">4.3 FOUNDATIONS</p>
          <h2>4.3 数据格式：先判断内容，再选择解析工具</h2>
        </div>
        <p class="chapter-seven-cue">
          解析工具不能乱用。JSON、HTML、纯文本、二进制文件和动态页面的处理方式不同。
          爬虫的第一条经验是：先看响应内容，再写解析代码。
        </p>

        <div class="chapter-seven-grid chapter-seven-quad-grid">
          <article class="chapter-seven-card chapter-seven-note-card" v-for="item in dataFormatCards" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
            <p class="chapter-seven-example"><strong>判断：</strong>{{ item.example }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="爬虫流程"
      >
        <div class="section-head">
          <p class="kicker">4.4 FOUNDATIONS</p>
          <h2>4.4 爬虫流程：从采集目标到数据文件</h2>
        </div>
        <p class="chapter-seven-cue">
          完整爬虫不是一条 requests.get()。真正可用的采集程序需要目标、入口、请求、解析、
          清洗、去重、保存和错误处理。每一步都决定最终数据是否可靠。
        </p>

        <div class="chapter-seven-grid chapter-seven-quad-grid">
          <article class="chapter-seven-card chapter-seven-note-card" v-for="item in crawlerWorkflowCards" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
            <p class="chapter-seven-example"><strong>例子：</strong>{{ item.example }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="爬虫简史"
      >
        <div class="section-head">
          <p class="kicker">4.5 HISTORY</p>
          <h2>4.5 爬虫简史：技术是怎样出现的</h2>
        </div>
        <p class="chapter-seven-cue">
          最早的爬虫并不是为了商业化数据采集，而是为了理解互联网有多大、有哪些资源、如何让用户更快找到页面。
        </p>
        <div class="chapter-seven-grid chapter-seven-history-grid">
          <article
            class="chapter-seven-card chapter-seven-history-card"
            v-for="item in crawlerHistoryCards"
            :key="item.year + item.title"
          >
            <div class="chapter-seven-history-top">
              <p class="chapter-seven-year">{{ item.year }}</p>
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
            </div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="技术演变"
      >
        <div class="section-head">
          <p class="kicker">4.6 EVOLUTION</p>
          <h2>4.6 技术演变：从早期爬虫到现代采集工具</h2>
        </div>
        <p class="chapter-seven-cue">
          requests、BeautifulSoup、正则表达式和 Selenium，正好对应了爬虫从简单访问到复杂页面解析的演变路线。
        </p>
        <div class="chapter-seven-grid chapter-seven-quad-grid">
          <article class="chapter-seven-card" v-for="item in crawlerEvolutionCards" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="隐私与法律风险"
      >
        <div class="section-head">
          <p class="kicker">4.7 CIVICS & LAW</p>
          <h2>4.7 个人隐私与法律风险：技术能力必须有边界</h2>
        </div>
        <p class="chapter-seven-cue">
          爬虫学习不能只追求“能不能抓到”。个人信息保护、平台规则、访问频率和数据用途同样重要。
          合格的程序员要把技术能力用于正当、合法、尊重他人的场景。
        </p>
        <div class="chapter-seven-grid chapter-seven-quad-grid">
          <article class="chapter-seven-card chapter-seven-note-card" v-for="item in privacyRiskCards" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
            <p class="chapter-seven-example"><strong>提示：</strong>{{ item.example }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="2"
        data-outline-label="资料来源"
      >
        <div class="section-head">
          <p class="kicker">4.8 SOURCES</p>
          <h2>4.8 资料来源：给历史节点和法律案例留下可追溯链接</h2>
        </div>
        <p class="chapter-seven-cue">
          技术学习不能只记结论。遇到历史节点、工具起源和法律案例时，要能回到原始资料或权威条目核对。
        </p>
        <div class="chapter-seven-grid chapter-seven-source-grid">
          <article class="chapter-seven-card" v-for="item in crawlerSourceCards" :key="item.href">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <a
              class="chapter-seven-link"
              :href="item.href"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ item.href }}
            </a>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="代码实战"
      >
        <div class="section-head">
          <p class="kicker">SECTION 05 CODE PRACTICE</p>
          <h2>5 代码实战：每页只解决一个采集动作</h2>
        </div>
        <p class="chapter-seven-cue">
          代码实战按“会发请求、会处理失败、会整理 JSON/HTML 记录、会处理动态页面、会输出文件与结论”的顺序推进。
          每段代码都只解决一个采集动作，既能单独运行观察，也能逐步拼成完整项目。
        </p>
        <div class="chapter-seven-grid chapter-seven-foundation-map">
          <article
            class="chapter-seven-card chapter-seven-map-card"
            v-for="item in codePracticeMap"
            :key="item.title"
          >
            <img class="chapter-seven-map-icon" :src="item.icon" alt="" aria-hidden="true" />
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        v-for="slide in codeSlides"
        :key="slide.no"
        class="section reveal chapter-seven-code-page"
        data-outline-level="2"
        :data-outline-label="slide.label"
      >
        <div class="section-head">
          <p class="kicker">5.{{ Number(slide.no) }} CODE PRACTICE</p>
          <h2>{{ slide.title }}</h2>
        </div>
        <div v-if="slide.kind === 'table'" class="chapter-seven-table-card">
          <table>
            <thead>
              <tr>
                <th>函数 / 写法</th>
                <th>作用</th>
                <th>示例</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in slide.tableRows" :key="row.name">
                <td><code>{{ row.name }}</code></td>
                <td>{{ row.usage }}</td>
                <td><code>{{ row.example }}</code></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="chapter-seven-code-shell">
          <pre><code class="python">{{ slide.code }}</code></pre>
        </div>
        <div class="chapter-seven-grid chapter-seven-2plus1">
          <article class="chapter-seven-card">
            <h3>这一段在做什么</h3>
            <p>{{ slide.explain }}</p>
          </article>
          <article class="chapter-seven-card">
            <h3>本页关键词</h3>
            <p>{{ slide.key }}</p>
          </article>
          <article class="chapter-seven-card">
            <h3>运行检查</h3>
            <p>{{ slide.check }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="爬虫规范"
      >
        <div class="section-head">
          <p class="kicker">ETHICS</p>
          <h2>6 爬虫规范：不是“想爬什么就爬什么”</h2>
        </div>
        <div class="chapter-seven-grid chapter-seven-quad-grid">
          <article class="chapter-seven-card" v-for="item in ethics" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="综合项目"
      >
        <div class="section-head">
          <p class="kicker">CAPSTONE</p>
          <h2>7 综合项目：实验四 爬取酷狗音乐 TOP500 歌曲信息</h2>
        </div>
        <p class="chapter-seven-cue">
          最终项目切换为课程实验四：使用 <code>requests</code> 抓取酷狗音乐排行榜页面，
          用 <code>BeautifulSoup</code> 解析榜单结构，提取歌曲排名、歌曲名称、演唱者和歌曲时长，
          再把全部 TOP500 结果保存成 <code>songTop500.csv</code>。前面第 5 节学过的请求、解析和文件保存，
          在这里会合并成一个完整实验流程。
        </p>
        <div class="chapter-seven-grid chapter-seven-quad-grid">
          <article class="chapter-seven-card" v-for="item in capstoneCards" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
            <a
              v-if="item.href"
              class="chapter-seven-link"
              :href="item.href"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ item.href }}
            </a>
          </article>
        </div>
      </section>

      <section
        id="summary"
        class="section reveal"
        data-outline-level="1"
        data-outline-label="本章总结"
      >
        <h2>8 本章总结：把网络数据变成可分析的数据文件</h2>
        <div class="chapter-seven-grid chapter-seven-2plus1">
          <article class="chapter-seven-card" v-for="item in summaryCards" :key="item.title">
            <div class="chapter-seven-card-head">
              <img class="chapter-seven-icon" :src="item.icon" alt="" aria-hidden="true" />
              <h3>{{ item.title }}</h3>
            </div>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>本章关键词：先合规访问，再稳定解析，最后保存成可复用的数据。</p>
    </footer>

    <LessonOutlineSidebar
      :items="outlineItems"
      :active-index="activeOutlineIndex"
      @jump="jumpToSlide"
    />

    <div id="copyToast" class="copy-toast" role="status" aria-live="polite">命令已复制</div>
  </div>
</template>

<style scoped>
.page.is-slide-deck .chapter-seven-rhythm,
.page.is-slide-deck .chapter-seven-grid {
  margin-top: 16px;
  display: grid;
  gap: 12px;
  align-items: stretch;
}

.page.is-slide-deck .chapter-seven-rhythm {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.page.is-slide-deck .chapter-seven-rhythm span {
  min-width: 0;
  padding: 12px 14px;
  border-radius: 16px;
  border: 1px solid rgba(11, 98, 179, 0.18);
  background:
    radial-gradient(circle at 18% 16%, rgba(91, 180, 255, 0.18), transparent 40%),
    linear-gradient(180deg, rgba(248, 252, 255, 0.98), rgba(232, 244, 255, 0.92));
  color: #0a5eaf;
  font-size: 0.9rem;
  font-weight: 800;
  text-align: center;
}

.page.is-slide-deck .chapter-seven-cue {
  margin: 12px 0 0;
  padding: 14px 16px;
  border: 1px solid rgba(11, 98, 179, 0.14);
  border-left: 5px solid rgba(11, 98, 179, 0.55);
  border-radius: 16px;
  background: linear-gradient(90deg, rgba(11, 98, 179, 0.09), rgba(255, 255, 255, 0.76));
  color: #274155;
  line-height: 1.72;
}

.page.is-slide-deck .chapter-seven-block-title {
  margin: 22px 0 12px;
  color: #14304c;
  font-size: 1.04rem;
  letter-spacing: 0.02em;
}

.page.is-slide-deck .chapter-seven-card {
  min-width: 0;
  min-height: 0;
  padding: 15px 16px;
  border-radius: 18px;
  border: 1px solid rgba(9, 80, 150, 0.13);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(247, 251, 255, 0.96)),
    #ffffff;
  box-shadow: 0 12px 28px rgba(16, 53, 92, 0.08);
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden;
}

.page.is-slide-deck .chapter-seven-card h3,
.page.is-slide-deck .chapter-seven-card p {
  margin: 0;
}

.page.is-slide-deck .chapter-seven-card h3 {
  color: #182e45;
  font-size: 1rem;
  line-height: 1.35;
}

.page.is-slide-deck .chapter-seven-card p {
  color: #455c6f;
  font-size: 0.9rem;
  line-height: 1.58;
}

.page.is-slide-deck .chapter-seven-note-card {
  gap: 10px;
}

.page.is-slide-deck .chapter-seven-example {
  margin-top: auto;
  padding: 10px 12px;
  border-radius: 13px;
  background: rgba(11, 98, 179, 0.06);
  color: #25465f;
}

.page.is-slide-deck .chapter-seven-example strong {
  color: #0a5eaf;
}

.page.is-slide-deck .chapter-seven-card-head,
.page.is-slide-deck .chapter-seven-history-top {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page.is-slide-deck .chapter-seven-history-top {
  justify-content: space-between;
}

.page.is-slide-deck .chapter-seven-icon {
  width: 22px;
  height: 22px;
  flex: 0 0 22px;
  padding: 7px;
  border-radius: 13px;
  background: linear-gradient(135deg, rgba(11, 98, 179, 0.12), rgba(80, 185, 255, 0.16));
  box-shadow: inset 0 0 0 1px rgba(11, 98, 179, 0.14);
}

.page.is-slide-deck .chapter-seven-link-grid,
.page.is-slide-deck .chapter-seven-source-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.page.is-slide-deck .chapter-seven-quad-grid,
.page.is-slide-deck .chapter-seven-history-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.page.is-slide-deck .chapter-seven-2plus1 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.page.is-slide-deck .chapter-seven-foundation-map {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.page.is-slide-deck .chapter-seven-map-card {
  min-height: 142px;
  background:
    radial-gradient(circle at 14% 12%, rgba(91, 180, 255, 0.23), transparent 34%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(240, 248, 255, 0.95));
}

.page.is-slide-deck .chapter-seven-map-icon {
  width: 30px;
  height: 30px;
  padding: 9px;
  border-radius: 17px;
  background: linear-gradient(135deg, rgba(228, 243, 255, 0.98), rgba(255, 255, 255, 0.98));
  box-shadow:
    inset 0 0 0 1px rgba(11, 98, 179, 0.18),
    0 12px 24px rgba(11, 98, 179, 0.12);
}

.page.is-slide-deck .chapter-seven-history-card {
  position: relative;
  padding-left: 20px;
}

.page.is-slide-deck .chapter-seven-history-card::before {
  content: "";
  position: absolute;
  inset: 14px auto 14px 0;
  width: 5px;
  border-radius: 999px;
  background: linear-gradient(180deg, #0b62b3, #5bb4ff);
}

.page.is-slide-deck .chapter-seven-year {
  display: inline-flex;
  margin: 0;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(11, 98, 179, 0.1);
  color: #0a5eaf;
  font-size: 0.82rem;
  font-weight: 800;
}

.page.is-slide-deck .chapter-seven-code-shell {
  margin-top: 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(8, 16, 29, 0.97), rgba(14, 28, 48, 0.98));
  overflow: hidden;
  box-shadow: 0 20px 34px rgba(7, 25, 52, 0.14);
}

.page.is-slide-deck .chapter-seven-table-card {
  margin-top: 18px;
  border-radius: 18px;
  border: 1px solid rgba(9, 80, 150, 0.13);
  background: rgba(255, 255, 255, 0.98);
  overflow: hidden;
  box-shadow: 0 16px 30px rgba(16, 53, 92, 0.08);
}

.page.is-slide-deck .chapter-seven-table-card table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
}

.page.is-slide-deck .chapter-seven-table-card th,
.page.is-slide-deck .chapter-seven-table-card td {
  padding: 12px 14px;
  border-bottom: 1px solid rgba(9, 80, 150, 0.1);
  text-align: left;
  vertical-align: top;
}

.page.is-slide-deck .chapter-seven-table-card th {
  background: linear-gradient(180deg, rgba(232, 244, 255, 0.96), rgba(244, 249, 255, 0.96));
  color: #123b61;
  font-weight: 900;
}

.page.is-slide-deck .chapter-seven-table-card tr:last-child td {
  border-bottom: 0;
}

.page.is-slide-deck .chapter-seven-table-card code {
  color: #0a5eaf;
  white-space: normal;
  overflow-wrap: anywhere;
}

.page.is-slide-deck .chapter-seven-code-shell pre {
  margin: 0;
  padding: 18px;
  overflow-x: auto;
}

.page.is-slide-deck .chapter-seven-code-shell code {
  color: #f4f8ff;
  line-height: 1.75;
}

.page.is-slide-deck .chapter-seven-link {
  display: block;
  margin-top: auto;
  color: #0a5eaf;
  font-size: 0.86rem;
  font-weight: 800;
  line-height: 1.45;
  text-decoration: underline;
  word-break: break-all;
}

@media (max-width: 900px) {
  .page.is-slide-deck .chapter-seven-rhythm,
  .page.is-slide-deck .chapter-seven-link-grid,
  .page.is-slide-deck .chapter-seven-source-grid,
  .page.is-slide-deck .chapter-seven-2plus1,
  .page.is-slide-deck .chapter-seven-foundation-map,
  .page.is-slide-deck .chapter-seven-history-grid,
  .page.is-slide-deck .chapter-seven-quad-grid {
    grid-template-columns: 1fr;
  }
}
</style>

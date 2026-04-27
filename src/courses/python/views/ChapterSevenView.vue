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
import IconNetwork from "../../../assets/lucide-icons/network.svg";
import IconRoute from "../../../assets/lucide-icons/route.svg";
import IconSearch from "../../../assets/lucide-icons/search.svg";
import IconShield from "../../../assets/lucide-icons/shield.svg";
import { useLessonDeck } from "../../../composables/useLessonDeck";

const rootRef = ref(null);
const { outlineItems, activeOutlineIndex, jumpToSlide } = useLessonDeck(rootRef);

const sampleJsonHref = "/courses/python/ch07/sample_books.json";
const staticHtmlHref = "/courses/python/ch07/books_static.html";
const courseSpiderHref = "/courses/python/ch07/course_spider.py";
const jwCourseHref = "https://jw.guc.edu.cn/yethan/CourseAction?setAction=queryCourseList&selectTableType=History";

const learningGoals = [
  "理解浏览器访问网页背后的请求、响应、状态码、HTML 与 JSON。",
  "能用 requests 获取网页或接口数据，并处理编码、参数、请求头和异常。",
  "能围绕一个登录态课表页面，完成诊断、解析、分页、去重和 CSV 保存。",
];

const roadmap = [
  { no: "01", title: "requests", text: "发送网络请求，先看服务器返回了什么。" },
  { no: "02", title: "Headers 与 Cookie", text: "理解浏览器请求头和登录态。" },
  { no: "03", title: "Session", text: "复用会话设置，避免请求代码反复堆叠。" },
  { no: "04", title: "BeautifulSoup", text: "解析 HTML 表格，提取课表结构。" },
  { no: "05", title: "分页与去重", text: "使用 jumpPage 采集多页记录。" },
  { no: "06", title: "CSV", text: "保存全校课表，形成可复查文件。" },
];

const chapterMetrics = [
  { value: "14", label: "增量小节" },
  { value: "16", label: "课表字段" },
  { value: "CSV", label: "最终产出" },
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
    text: "爬虫不会自动理解页面含义。必须根据正文格式选择 JSON、BeautifulSoup、字符串清洗或 CSV 保存继续处理。",
    example: "JSON 用 response.json()；HTML 表格用 BeautifulSoup；整理后的字典列表用 csv 保存。",
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
    text: "请求是客户端发出的访问动作。它说明目标资源、访问方式、客户端身份和可接受的响应格式。",
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
    title: "登录态页面",
    icon: IconShield,
    text: "有些页面只有登录后才能看到具体数据。程序请求必须携带合法的会话信息，服务器才会返回对应内容。",
    example: "浏览器能看到课表，requests 却看到登录页，常见原因就是缺少 Cookie。",
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
    title: "登录页：最常见的误判",
    icon: IconShield,
    text: "状态码 200 只表示服务器返回了页面，不表示返回的一定是目标数据。登录页、提示页和错误页也可能是 200。",
    example: "正文预览里出现“登录”时，应先解决登录态，而不是继续写表格解析。",
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
    text: "根据数据格式选择工具。JSON 走字典列表，HTML 表格走 BeautifulSoup，整理后的记录再写入 CSV。",
    example: "教务课表页通常先保存 HTML，再用 BeautifulSoup 定位 table、tr、td。",
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
    title: "数据权限时代",
    icon: IconShield,
    text: "越来越多数据位于登录态页面、权限接口或业务系统中。采集前必须确认账号权限、数据用途和访问频率。",
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
    title: "教务课表目标页",
    icon: IconShield,
    desc: "真实登录态页面，用于学习 Cookie、Session、HTML 表格解析、分页和 CSV 保存。",
    href: jwCourseHref,
  },
];

const codePracticeMap = [
  { title: "5.1 先搭最小骨架", icon: IconNetwork, text: "只写 URL、参数函数和 main()，先确认请求能发出去。" },
  { title: "5.2 加响应诊断工具", icon: IconCircleAlert, text: "新增诊断函数，判断返回的是课表页还是登录页。" },
  { title: "5.3 加浏览器请求头", icon: IconLink, text: "新增 build_headers()，再把请求语句改成携带 headers。" },
  { title: "5.4 加 Cookie 登录态", icon: IconShield, text: "新增 COOKIE 和 parse_cookie()，让请求带上本人登录态。" },
  { title: "5.5 合并成 Session", icon: IconRoute, text: "新增 build_session()，让后续所有请求复用 headers 和 Cookie。" },
  { title: "5.6 封装页面获取", icon: IconArchive, text: "新增 fetch_course_page()，统一请求、检查和解码。" },
  { title: "5.7 认识 BeautifulSoup", icon: IconBookOpen, text: "拆成 5.7.1-5.7.4，讲清楚它是什么、常用方法、定位方式和表格提取。" },
  { title: "5.8 观察并定位表格", icon: IconFileSearch, text: "新增表格观察函数，先确认课表在哪个 table 里。" },
  { title: "5.9 解析表格记录", icon: IconCode, text: "新增 parse_table_records()，把 table 转成字典列表。" },
  { title: "5.10 固定网页表头字段", icon: IconDatabase, text: "按网页表头字段保存课程记录，不再猜测字段名。" },
  { title: "5.11 确认分页参数", icon: IconListTree, text: "观察分页源码，确认真正起作用的是 jumpPage。" },
  { title: "5.12 接入多页循环", icon: IconRoute, text: "在请求参数中加入 jumpPage，再逐页采集去重。" },
  { title: "5.13 保存最终 CSV", icon: IconArchive, text: "新增 save_csv()，把最终记录写成表格文件。" },
  { title: "5.14 完整代码下载", icon: IconExternalLink, text: "汇总完整 course_spider.py，并提供下载路径。" },
];

const codeSlides = [
  {
    no: "01",
    label: "最小骨架",
    title: "5.1 先搭最小骨架：URL、参数函数和 main()",
    problem: "刚开始不要写解析、分页和保存。先确认：程序能访问目标地址，并能看到服务器返回了什么。",
    change: "新建 course_spider.py，写入最小可运行骨架。后续所有小节都在这个文件上增量修改。",
    code: `# 新建文件：course_spider.py
# 目标：先让程序能发出一次请求，不处理登录态、不解析表格。

import requests

URL = "https://jw.guc.edu.cn/yethan/CourseAction"


def build_params():
    """返回课表页面需要的查询参数。"""
    return {
        "setAction": "queryCourseList",
        "selectTableType": "History",
    }


def main():
    response = requests.get(URL, params=build_params(), timeout=10)
    print("最终请求地址：", response.url)
    print("状态码：", response.status_code)
    print("响应类型：", response.headers.get("Content-Type"))
    print("正文预览：", response.text[:300].replace("\\n", " "))


if __name__ == "__main__":
    main()`,
    explain: "这是全章实战的起点。此时文件只有一个配置常量、一个参数函数和一个 main() 主干。",
    key: "先跑通请求，再逐步加能力。不要在第一步就写 Cookie、BeautifulSoup、CSV。",
    check: "运行后如果正文预览里出现“登录”，这是正常现象，说明下一步要做响应诊断。",
  },
  {
    no: "02",
    label: "响应诊断",
    title: "5.2 增量添加：响应诊断和 HTML 保存",
    problem: "状态码 200 不一定代表拿到了课表。服务器可能返回的是登录页，所以要把诊断动作固定下来。",
    change: "添加 4 个诊断函数，并修改 main()。这些函数放在 build_params() 后、main() 前。",
    code: `# 添加位置：build_params() 函数下面，main() 函数上面
# 作用：把响应解码、登录页判断、HTML 保存、摘要打印封装起来。

from pathlib import Path  # 添加位置：文件顶部 import 区


def decode_response(response):
    """根据网页内容自动判断编码，返回解码后的 HTML。"""
    response.encoding = response.apparent_encoding
    return response.text


def is_login_page(html):
    """粗略判断当前 HTML 是否仍然是登录页。"""
    preview = html[:1000].lower()
    return "登录" in html[:1000] or "login" in preview


def save_html(html, filename):
    """把响应正文保存下来，方便用浏览器和编辑器检查。"""
    Path(filename).write_text(html, encoding="utf-8")


def show_response_summary(response, html):
    print("最终请求地址：", response.url)
    print("状态码：", response.status_code)
    print("响应编码：", response.encoding)
    print("是否像登录页：", is_login_page(html))
    print("table 标签数量：", html.lower().count("<table"))


# 修改位置：main() 函数内部
# - print("响应类型：", response.headers.get("Content-Type"))
# - print("正文预览：", response.text[:300].replace("\\n", " "))
# + html = decode_response(response)
# + show_response_summary(response, html)
# + save_html(html, "debug_response.html")
# + print("已保存 debug_response.html")`,
    explain: "这一页只新增诊断能力。以后不再只看状态码，而是统一判断登录页、table 数量，并保存 HTML 作为证据。",
    key: "把诊断动作封装成函数，可以避免每一节都重复写一堆 print。",
    check: "打开 debug_response.html。如果仍是登录页，说明下一步要改善请求条件。",
  },
  {
    no: "03",
    label: "请求头",
    title: "5.3 增量添加：build_headers() 和 headers 参数",
    problem: "普通 Python 请求不像浏览器。先补上常见浏览器请求头，但这一节仍然不处理登录态。",
    change: "新增 build_headers()；然后把 main() 里的 requests.get() 改成携带 headers。",
    code: `# 添加位置：build_params() 下面，诊断函数上面
# 作用：集中管理普通请求头。这里不要放 Cookie。


def build_headers():
    """返回普通浏览器请求头。这里还不包含 Cookie。"""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/147.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }


# 修改位置：main() 里的请求语句
# 为什么改：让请求携带普通浏览器请求头。
# - response = requests.get(URL, params=build_params(), timeout=10)
# + response = requests.get(
# +     URL,
# +     params=build_params(),
# +     headers=build_headers(),
# +     timeout=10,
# + )`,
    explain: "build_headers() 是一个小函数，但它把请求头和主流程分离开了。后续 Session 也会复用它。",
    key: "headers 只能说明客户端特征；如果仍然是登录页，问题通常是缺少 Cookie。",
    check: "运行后如果还是登录页，不要继续加解析代码，进入 5.4 添加登录态。",
  },
  {
    no: "04",
    label: "Cookie",
    title: "5.4 增量添加：COOKIE 和 parse_cookie()",
    problem: "教务系统需要登录态。直接把 Cookie 硬塞进 headers 容易复制错格式，所以先封装解析函数。",
    change: "在常量区新增 COOKIE；在函数区新增 parse_cookie()；修改请求语句，使用 cookies=parse_cookie(COOKIE)。",
    code: `# 添加位置：URL 常量下面
# 注意：只粘贴本人浏览器里的 Cookie，不要提交到仓库或截图。

COOKIE = ""  # 可以粘贴纯 Cookie，也可以粘贴 Cookie: 开头的一整行。


# 添加位置：build_headers() 下面
# 作用：把浏览器复制出来的 Cookie 字符串拆成 requests 可用的字典。


def parse_cookie(raw_cookie):
    raw_cookie = raw_cookie.strip()
    if not raw_cookie:
        raise SystemExit("请先填写 COOKIE，例如 username=...; sl-session=...; JSESSIONID=...")

    lines = [line.strip() for line in raw_cookie.replace("\\r", "\\n").split("\\n")]
    cookie_lines = [line for line in lines if line.lower().startswith("cookie:")]
    if cookie_lines:
        raw_cookie = cookie_lines[-1].split(":", 1)[1].strip()
    elif raw_cookie.lower().startswith("cookie:"):
        raw_cookie = raw_cookie.split(":", 1)[1].strip()

    cookies = {}
    for item in raw_cookie.split(";"):
        item = item.strip()
        if item and "=" in item:
            name, value = item.split("=", 1)
            cookies[name.strip()] = value.strip()

    required = ["username", "sl-session", "JSESSIONID"]
    missing = [name for name in required if name not in cookies]
    if missing:
        raise SystemExit(f"Cookie 缺少关键字段：{missing}")
    return cookies


# 修改位置：main() 里的 requests.get(...)
# 为什么改：Cookie 由 requests 的 cookies 参数发送，避免手写 Cookie header 出错。
# - headers=build_headers(),
# + headers=build_headers(),
# + cookies=parse_cookie(COOKIE),

# 添加位置：main() 打印诊断时，可以临时加一行，只打印字段名不打印值。
# + print("Cookie 字段：", ", ".join(parse_cookie(COOKIE).keys()))`,
    explain: "这一节只解决登录态格式。parse_cookie() 支持纯 Cookie，也支持从浏览器复制出的 Cookie: 请求头行。",
    key: "Cookie 值不能公开展示。调试时只打印字段名，用来确认格式是否正确。",
    check: "如果字段齐全但仍然是登录页，通常是 Cookie 过期，或复制的不是课表页请求对应的 Cookie。",
  },
  {
    no: "05",
    label: "Session",
    title: "5.5 增量添加：build_session()，简化主流程",
    problem: "后面会反复请求页面。每次都传 headers 和 cookies 会让 main() 越来越乱。",
    change: "新增 build_session()；把 main() 里的 requests.get() 改成 session.get()。",
    code: `# 添加位置：parse_cookie() 下面
# 作用：创建一个已经带好 headers 和 Cookie 的会话对象。


def build_session(cookie):
    """创建一个带公共 headers 和登录 Cookie 的会话。"""
    session = requests.Session()
    session.headers.update(build_headers())
    session.cookies.update(parse_cookie(cookie))
    return session


# 修改位置：main() 开头和请求语句
# 为什么改：后续所有请求都复用同一个 session。
# - response = requests.get(
# -     URL,
# -     params=build_params(),
# -     headers=build_headers(),
# -     cookies=parse_cookie(COOKIE),
# -     timeout=10,
# - )
# + session = build_session(COOKIE)
# + response = session.get(URL, params=build_params(), timeout=10)`,
    explain: "Session 把“这是一组相关请求”表达出来。后面分页时，不需要重复关心 headers 和 Cookie。",
    key: "主干开始变清楚：创建 session，然后用 session 发请求。",
    check: "运行结果应和 5.4 一致。如果突然变回登录页，检查 build_session() 是否调用了 parse_cookie(COOKIE)。",
  },
  {
    no: "06",
    label: "页面获取",
    title: "5.6 增量添加：fetch_course_page()",
    problem: "请求课表页后，每次都要 raise_for_status、设置编码、返回 HTML。这个动作可以封装。",
    change: "新增 fetch_course_page()；main() 不再直接处理 response，而是拿到 html。",
    code: `# 添加位置：build_session() 下面
# 作用：统一完成请求、状态检查、编码设置，并返回 HTML 字符串。


def fetch_course_page(session, params):
    """请求课表页面，返回解码后的 HTML。"""
    response = session.get(URL, params=params, timeout=10)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text


# 修改位置：main() 中获取 response/html 的部分
# 为什么改：main() 只描述流程，把请求细节交给 fetch_course_page()。
# - response = session.get(URL, params=build_params(), timeout=10)
# - html = decode_response(response)
# + html = fetch_course_page(session, build_params())

# 保留位置：main() 中继续保存和检查 HTML
# + save_html(html, "course_page.html")
# + print("是否像登录页：", is_login_page(html))
# + print("table 标签数量：", html.lower().count("<table"))`,
    explain: "fetch_course_page() 以后会被分页循环反复调用，所以要尽早封装。",
    key: "main() 现在更像流程表，而不是所有细节的堆叠。",
    check: "如果 table 标签数量为 0，先确认是否仍是登录页，不要急着写 BeautifulSoup。",
  },
  {
    no: "07",
    displayNo: "5.7",
    label: "认识 BeautifulSoup",
    title: "5.7 知识补充：BeautifulSoup 解决什么问题",
    problem: "前面已经能拿到 HTML，但 HTML 不是表格文件，也不是 Python 字典。程序需要一个工具把网页源码变成可查找、可遍历的数据结构。",
    change: "本节是进入真实课表解析前的知识补充，不修改 course_spider.py。先理解 BeautifulSoup 是什么，再学习常用方法和表格提取套路。",
    code: `# 5.7 是 BeautifulSoup 入门，不急着修改主项目代码。
# 这一组小节按四步学习：
#
# 5.7.1 先理解：BeautifulSoup 把 HTML 解析成标签树。
# 5.7.2 再记方法：find、find_all、select、get、get_text。
# 5.7.3 然后练定位：按标签、属性、CSS 选择器找到目标元素。
# 5.7.4 最后做转换：把 HTML 表格转换成字典列表。
#
# 学完这四步，再进入 5.8 观察真实课表页面中的 table。`,
    explain: "BeautifulSoup 不是负责下载网页的工具，下载由 requests 完成。它负责解析已经拿到的 HTML，让程序能像查字典和列表一样查找页面元素。",
    key: "requests 负责获取 HTML；BeautifulSoup 负责解析 HTML；CSV 负责保存解析后的结构化记录。",
    check: "能说清楚三句话再往下走：HTML 是标签结构；BeautifulSoup 能查标签；最终要把标签内容整理成字典列表。",
    notes: [
      "requests 负责把网页拿回来；BeautifulSoup 负责读懂网页结构。",
      "这一组小节先补基础知识，暂时不改主项目，避免一边学库一边排查真实页面。",
    ],
  },
  {
    no: "07-1",
    displayNo: "5.7.1",
    outlineLevel: 3,
    label: "BS4 是什么",
    title: "5.7.1 BeautifulSoup 是什么：把 HTML 变成可查询的结构",
    problem: "网页不是一整段普通文字。HTML 由一层一层标签组成，直接用字符串切割很容易切错。",
    change: "本页先不修改 course_spider.py。先用一个小网页理解：BeautifulSoup 会把 HTML 字符串解析成可以查找、遍历、取文字的对象。",
    code: `# 本页是知识补充：先不要修改 course_spider.py
# 目标：理解 BeautifulSoup 解决的核心问题。
# 如果运行时提示 No module named 'bs4'，先执行：
# python -m pip install beautifulsoup4

from bs4 import BeautifulSoup

html = """
<html>
  <body>
    <h1>课表</h1>
    <table id="courses" class="data-table">
      <tr><th>课程</th><th>教师</th></tr>
      <tr><td>Python程序设计</td><td>张老师</td></tr>
    </table>
  </body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

print(type(soup))                 # soup 是整个 HTML 文档的解析对象
print(soup.h1)                    # 可以像访问属性一样找到第一个 h1 标签
print(soup.h1.get_text(strip=True))

table = soup.table                # 找到第一个 table 标签
print(table.get("id"))            # 读取标签属性
print(table.get("class"))`,
    explain: "BeautifulSoup 是 HTML 解析库。它把网页源码转换成一棵标签树，程序就可以按标签名、属性、层级和选择器去找内容。",
    key: "soup 表示整份 HTML 文档；Tag 表示一个标签；标签可以继续 find、find_all，也可以 get_text() 取文字。",
    check: "运行后应看到 soup 类型、h1 标签、课表标题、table 的 id 和 class。先理解结构，再进入方法速查。",
    notes: [
      "先把 HTML 看成一棵树：soup 是整棵树，table、tr、td 是树上的节点。",
      "能取文字、取属性、继续向下找标签，就具备了解析课表表格的基础。",
    ],
  },
  {
    no: "07-2",
    displayNo: "5.7.2",
    outlineLevel: 3,
    kind: "table",
    label: "BS4 方法速查",
    title: "5.7.2 BeautifulSoup 常用对象和方法速查",
    problem: "第一次接触 BeautifulSoup 时，最容易把 find、find_all、select、get_text 混在一起。",
    change: "本页用表格整理常用写法。先记住“解析、定位、取值、取文本”四类动作，后面解析课表时按需选择。",
    tableRows: [
      { name: 'BeautifulSoup(html, "html.parser")', usage: "把 HTML 字符串解析成 soup 对象", example: 'soup = BeautifulSoup(html, "html.parser")' },
      { name: 'soup.find("table")', usage: "找到第一个匹配的标签", example: 'table = soup.find("table")' },
      { name: 'soup.find_all("tr")', usage: "找到所有匹配的标签，返回列表", example: 'rows = table.find_all("tr")' },
      { name: 'tag.find("td")', usage: "在某个标签内部继续找第一个子标签", example: 'first_cell = row.find("td")' },
      { name: 'tag.find_all(["th", "td"])', usage: "一次查找多种标签", example: 'cells = row.find_all(["th", "td"])' },
      { name: 'tag.get_text(strip=True)', usage: "提取标签内部文字，并去掉两边空白", example: 'title = cell.get_text(strip=True)' },
      { name: 'tag.get("href", "")', usage: "读取标签属性，属性不存在时返回默认值", example: 'href = link.get("href", "")' },
      { name: 'tag["href"]', usage: "读取一定存在的属性；不存在会报错", example: 'href = link["href"]' },
      { name: 'soup.select("table tr")', usage: "用 CSS 选择器找到所有匹配元素", example: 'rows = soup.select("table tr")' },
      { name: 'soup.select_one("#courses")', usage: "用 CSS 选择器找到第一个匹配元素", example: 'table = soup.select_one("#courses")' },
    ],
    explain: "BeautifulSoup 的核心动作很少：先解析 HTML，再定位标签，最后从标签中取属性或文字。复杂页面只是这些动作的组合。",
    key: "find 找一个，find_all 找一组；get 取属性，get_text 取文本；select 使用 CSS 选择器。",
    check: "读表时重点区分：返回单个 Tag 的方法可以继续点方法；返回列表的方法通常要用 for 循环逐个处理。",
    notes: [
      "查找用 find、find_all、select；取值用 get、get_text。表中方法按这两类记。",
      "返回列表的方法需要循环处理，返回单个标签的方法可以继续向下查找。",
    ],
  },
  {
    no: "07-3",
    displayNo: "5.7.3",
    outlineLevel: 3,
    label: "定位元素",
    title: "5.7.3 怎么用：按标签、属性和 CSS 选择器定位元素",
    problem: "真实网页里标签很多。只写 find('table') 可能拿到第一个无关表格，所以要学会按 id、class 和层级缩小范围。",
    change: "本页继续不修改 course_spider.py。用同一段 HTML 演示三种定位方式：标签名、属性条件、CSS 选择器。",
    code: `# 本页是知识补充：练习定位元素的不同写法。

from bs4 import BeautifulSoup

html = """
<table id="courses" class="data-table">
  <tr class="header">
    <th>课程</th><th>教师</th><th>地点</th>
  </tr>
  <tr class="course-row">
    <td class="name">Python程序设计</td>
    <td class="teacher">张老师</td>
    <td class="room">A101</td>
  </tr>
  <tr class="course-row">
    <td class="name">大学英语</td>
    <td class="teacher">李老师</td>
    <td class="room">B203</td>
  </tr>
</table>
"""

soup = BeautifulSoup(html, "html.parser")

table1 = soup.find("table")                         # 按标签名找
table2 = soup.find("table", id="courses")           # 按属性找
table3 = soup.select_one("#courses")                # CSS 选择器：# 表示 id

print(table1 is table2 is table3)

rows = soup.select("#courses tr.course-row")        # 只找课程数据行
for row in rows:
    name = row.select_one(".name").get_text(strip=True)
    teacher = row.select_one(".teacher").get_text(strip=True)
    room = row.select_one(".room").get_text(strip=True)
    print(name, teacher, room)`,
    explain: "定位元素时不要只依赖标签名。可以用 id、class、层级关系逐步缩小范围，让代码更准确地指向课表里的课程行。",
    key: "#courses 表示 id 为 courses 的元素；.course-row 表示 class 包含 course-row 的元素；空格表示后代层级。",
    check: "运行后第一行应为 True，后面打印两条课程。能解释每个选择器的含义，才算真正会用。",
    notes: [
      "真实网页先缩小范围：优先用 id，其次 class，再用层级选择器。",
      "不要直接解析全页面所有 td，否则容易把导航、按钮、分页文字混进课程数据。",
    ],
  },
  {
    no: "07-4",
    displayNo: "5.7.4",
    outlineLevel: 3,
    label: "提取表格",
    title: "5.7.4 怎么用：把 HTML 表格提取成字典列表",
    problem: "课程表最终不能只打印一堆标签。程序需要把表头和单元格对应起来，变成后续能保存的字典列表。",
    change: "本页仍不修改 course_spider.py。先用小表格演示“表头 + 数据行 = 字典列表”的转换过程，为 5.8 和 5.9 做准备。",
    code: `# 本页是知识补充：理解表格解析的基本套路。

from bs4 import BeautifulSoup

html = """
<table>
  <tr><th>课程</th><th>教师</th><th>地点</th></tr>
  <tr><td>Python程序设计</td><td>张老师</td><td>A101</td></tr>
  <tr><td>大学英语</td><td>李老师</td><td>B203</td></tr>
</table>
"""

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")
rows = table.find_all("tr")

headers = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]
print("表头：", headers)

records = []
for row in rows[1:]:
    cells = row.find_all("td")
    values = [cell.get_text(strip=True) for cell in cells]
    record = dict(zip(headers, values))
    records.append(record)

for record in records:
    print(record)`,
    explain: "表格解析通常分三步：先取表头，再遍历数据行，最后把表头和单元格值配对成字典。",
    key: "rows[0] 是表头行，rows[1:] 是数据行；zip(headers, values) 可以把两组列表按位置配对。",
    check: "运行后应得到两个字典，每个字典都有课程、教师、地点三个字段。下一节再把这个套路迁移到真实课表页面。",
    notes: [
      "课表解析的目标不是打印标签，而是得到字典列表。",
      "表头决定字典的 key，数据行决定 value；后面的字段清洗和 CSV 保存都依赖这个结构。",
    ],
  },
  {
    no: "08",
    label: "表格定位",
    title: "5.8 增量添加：观察并定位课表 table",
    problem: "页面可能有多个 table。解析前要知道哪一个最像课表。",
    change: "新增 BeautifulSoup 导入、describe_tables() 和 find_course_table()；main() 临时改为读取本地 HTML 做结构观察。",
    code: `# 添加位置：文件顶部 import 区
from bs4 import BeautifulSoup


# 添加位置：工具函数区
# 作用：观察页面中有哪些表格，以及选择最可能的课表表格。


def describe_tables(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    print("表格数量：", len(tables))
    for index, table in enumerate(tables, start=1):
        rows = table.find_all("tr")
        preview = table.get_text(" ", strip=True)[:120]
        print(f"第 {index} 个表格：{len(rows)} 行")
        print("预览：", preview)
        print("-" * 40)


def find_course_table(html):
    """返回行数最多的 table，作为课表候选表格。"""
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        return None
    return max(tables, key=lambda table: len(table.find_all("tr")))


# 修改位置：main()，本节先读取上一步保存的 course_page.html 做观察。
# - html = fetch_course_page(session, build_params())
# + html = Path("course_page.html").read_text(encoding="utf-8")
# + describe_tables(html)
# + table = find_course_table(html)
# + print("是否找到候选课表：", table is not None)`,
    explain: "这一节故意不请求网站，而是读取本地 HTML。这样可以反复观察结构，也不会频繁访问服务器。",
    key: "先观察，再解析。BeautifulSoup 的第一步不是提字段，而是定位结构。",
    check: "如果表格数量为 0，说明 course_page.html 不是课表页，要回到 Cookie 登录态步骤。",
  },
  {
    no: "09",
    label: "表格解析",
    title: "5.9 增量添加：parse_table_records()",
    problem: "找到 table 后，还要把 tr、th、td 转成 Python 的字典列表。",
    change: "新增 clean_text()、clean_header() 和 parse_table_records()；main() 打印前 5 条原始记录。",
    code: `# 添加位置：find_course_table() 下面
# 作用：清洗表头和单元格文本，并把 table 解析成字典列表。


def clean_text(text):
    """压缩多余空白，让单元格文本更干净。"""
    return " ".join(text.split())


def clean_header(text):
    """网页表头里有换行时，去掉空白，保留原始字段名称。"""
    return "".join(text.split())


def parse_table_records(table):
    """把 table 解析成字典列表。"""
    rows = table.find_all("tr")
    if not rows:
        return []

    headers = [clean_header(cell.get_text(" ", strip=True)) for cell in rows[0].find_all(["th", "td"])]
    records = []
    for row in rows[1:]:
        values = [clean_text(cell.get_text(" ", strip=True)) for cell in row.find_all(["td", "th"])]
        if not any(values):
            continue

        record = {}
        for index, value in enumerate(values):
            key = headers[index] if index < len(headers) and headers[index] else f"字段{index + 1}"
            record[key] = value
        records.append(record)
    return records


# 修改位置：main() 的表格观察后面
# + records = parse_table_records(table) if table else []
# + print("提取记录数：", len(records))
# + for record in records[:5]:
# +     print(record)`,
    explain: "parse_table_records() 是从 HTML 结构到数据结构的转换层。表头中的换行会被去掉，所以“课程 代码”会保存成“课程代码”。",
    key: "每一行变成一个 dict，网页表头是 key，单元格是 value。",
    check: "如果字段名很奇怪，说明表头识别不准，需要根据真实 HTML 调整解析规则。",
  },
  {
    no: "10",
    label: "网页表头字段",
    title: "5.10 增量添加：按网页表头固定保存字段",
    problem: "课表网页已经给出了明确表头，不应该再用关键词猜字段名。保存结果应和网页表头一致，便于核对。",
    change: "新增 COURSE_FIELDS 和 normalize_course()；normalize_course() 只按网页表头补齐字段，不改名、不猜测。",
    code: `# 添加位置：parse_table_records() 下面
# 作用：按网页表头顺序固定输出字段。

COURSE_FIELDS = [
    "序号",
    "选课编号",
    "课程代码",
    "课程名称",
    "教学班号",
    "学分",
    "性质",
    "开课院系",
    "教师",
    "职称",
    "时间地点",
    "优选",
    "状态",
    "校区",
    "选课名单",
    "学期",
]


def normalize_course(record):
    """按网页课表表头保存字段，不猜测、不改名。"""
    return {field: record.get(field, "") for field in COURSE_FIELDS}


# 修改位置：main() 中 records 打印后面
# - for record in records[:5]:
# -     print(record)
# + courses = [normalize_course(record) for record in records]
# + print("清洗后记录数：", len(courses))
# + for course in courses[:5]:
# +     print(course)`,
    explain: "这一节不再创造新的字段名，而是严格使用网页表头。缺失字段统一补空字符串，CSV 的列顺序也由 COURSE_FIELDS 控制。",
    key: "网页表头就是最终字段名。normalize_course() 只做字段补齐，不做字段猜测。",
    check: "打印 courses[0].keys()，应看到序号、选课编号、课程代码、课程名称、教学班号等网页表头字段。",
  },
  {
    no: "11",
    label: "分页参数",
    title: "5.11 观察分页源码：确认 jumpPage 是页码参数",
    problem: "第一页只能拿到前 50 条课程。要抓多页，先确认网页换页时到底给服务器传了什么参数。",
    change: "本节不新增函数，只观察 course_page.html 中的分页源码，把结论写下来：页码参数是 jumpPage。",
    code: `# 本节不修改 course_spider.py，只观察 course_page.html。
# 在 course_page.html 中搜索 gotoPage 和 jumpPage，可以看到：

# 1. 分页链接不是普通 URL，而是 JavaScript 调用。
# <a href="javascript:gotoPage(2)">下一页</a>

# 2. 页面里有一个叫 jumpPage 的页码字段。
# <select name="jumpPage"> ... </select>

# 3. gotoPage() 做的事情很简单：把 jumpPage 改成目标页码，然后提交表单。
# function gotoPage(pagenum){
#     document.pageForm.jumpPage.value = pagenum;
#     document.pageForm.submit();
# }

# 结论：
# Python 不需要执行 JavaScript。
# 下一节只要在请求参数里加入 jumpPage=2、jumpPage=3，就可以尝试切换页码。`,
    explain: "这一节的目标是降低不确定性：不用写通用搜索函数，只通过源码观察确认当前网站的分页参数。",
    key: "看到 javascript:gotoPage(n) 时，重点不是执行 JavaScript，而是找到它最终修改的表单字段。这里就是 jumpPage。",
    check: "能在 HTML 里找到 gotoPage(pagenum) 和 jumpPage，就可以进入 5.12 写最简单的翻页请求。",
  },
  {
    no: "12",
    label: "多页循环",
    title: "5.12 增量添加：用 jumpPage 实现多页采集",
    problem: "已经知道 jumpPage 是页码参数。现在不要把代码写复杂，先把页码参数加到请求里，验证第 1 页和第 2 页是否不同。",
    change: "新增 MAX_PAGE、build_page_params()、make_course_key()、fetch_all_courses()；main() 改为调用多页采集。",
    code: `# 添加位置：常量区
MAX_PAGE = 2  # 先采集 2 页验证逻辑；确认无误后再改大。


# 添加位置：build_params() 下面

def build_page_params(page):
    """在原始查询参数基础上添加 jumpPage，实现翻页。"""
    params = build_params()
    params["jumpPage"] = str(page)
    return params


# 添加位置：normalize_course() 下面

def make_course_key(record):
    """用整行内容做去重键。"""
    return "|".join(record.get(field, "") for field in COURSE_FIELDS)


def fetch_all_courses(session):
    """逐页请求、解析、清洗并去重。"""
    all_records = []
    seen = set()

    for page in range(1, MAX_PAGE + 1):
        html = fetch_course_page(session, build_page_params(page))
        table = find_course_table(html)
        raw_records = parse_table_records(table) if table else []
        page_courses = [normalize_course(record) for record in raw_records]
        print(f"第 {page} 页：{len(page_courses)} 条")

        for record in page_courses:
            key = make_course_key(record)
            if key not in seen:
                seen.add(key)
                all_records.append(record)
    return all_records


# 修改位置：main() 主干
# - html = Path("course_page.html").read_text(encoding="utf-8")
# - ...前面用于观察单页的代码...
# + session = build_session(COOKIE)
# + records = fetch_all_courses(session)
# + print("去重后记录数：", len(records))`,
    explain: "这一节只做最小可行翻页：原来请求第一页，现在多加一个 jumpPage 参数，让服务器返回指定页。",
    key: "先让 jumpPage 生效，再考虑总页数、限速和保存文件。不要把所有问题挤进第一版循环。",
    check: "先把 MAX_PAGE 设为 2。若第 1 页和第 2 页课程不同，说明分页生效；确认后再逐步调大。",
  },
  {
    no: "13",
    label: "保存 CSV",
    title: "5.13 增量添加：save_csv()，形成最终主干",
    problem: "打印在终端里的数据不能复查和提交。最终结果应该保存成 CSV 表格。",
    change: "新增 csv 导入、OUTPUT_FILE 常量和 save_csv()；main() 最后调用 save_csv()。",
    code: `# 添加位置：文件顶部 import 区
import csv

# 添加位置：常量区
OUTPUT_FILE = "school_courses.csv"


# 添加位置：fetch_all_courses() 下面
# 作用：把字典列表保存成 Excel 友好的 CSV。

def save_csv(records, filename):
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COURSE_FIELDS)
        writer.writeheader()
        writer.writerows(records)


# 修改位置：main() 最后几行
# - print("去重后记录数：", len(records))
# + if not records:
# +     raise SystemExit("没有提取到课程记录，请检查登录态、分页参数和表格结构。")
# + save_csv(records, OUTPUT_FILE)
# + print(f"已保存 {len(records)} 条记录到 {OUTPUT_FILE}")

# 最终 main() 应该像这样简洁：
# def main():
#     session = build_session(COOKIE)
#     records = fetch_all_courses(session)
#     if not records:
#         raise SystemExit("没有提取到课程记录，请检查登录态、分页参数和表格结构。")
#     save_csv(records, OUTPUT_FILE)
#     print(f"已保存 {len(records)} 条记录到 {OUTPUT_FILE}")`,
    explain: "这一节只新增保存能力。最终 main() 不再展示底层细节，而是清楚表达完整流程：建会话、采集、检查、保存。",
    key: "CSV 使用 utf-8-sig，方便 Excel 打开中文。DictWriter 的 fieldnames 直接使用 COURSE_FIELDS，列名和网页表头一致。",
    check: "打开 school_courses.csv，检查表头、中文、行数和前几条课程记录是否符合预期。",
  },
  {
    no: "14",
    label: "完整代码",
    title: "5.14 完整代码：course_spider.py",
    problem: "前面每一节都是增量代码。学完后需要一份完整文件，方便对照自己的版本检查缺漏。",
    change: "完整代码已经整理为 public/courses/python/ch07/course_spider.py。COOKIE 保持空字符串，运行前填写自己的 Cookie。",
    downloadHref: courseSpiderHref,
    code: `# 完整代码下载路径：
# /courses/python/ch07/course_spider.py
#
# 使用方式：
# 1. 下载 course_spider.py。
# 2. 安装依赖：python -m pip install requests beautifulsoup4
# 3. 填写 COOKIE = ""。
# 4. 先保持 MAX_PAGE = 2，确认分页生效。
# 5. 确认 CSV 正常后，再逐步调大 MAX_PAGE。`,
    explain: "完整代码把本节实战的请求、登录态、解析、分页、字段整理和 CSV 保存合并到一个文件。",
    key: "最终 CSV 字段使用网页原始表头：序号、选课编号、课程代码、课程名称、教学班号等。",
    check: "不要把填写了个人 Cookie 的文件提交或发送给他人。公开下载版本必须保持 COOKIE 为空。",
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
    text: "使用 requests 访问教务课表页面，采集课程表格中的课程、教师、时间、地点等字段，并保存到 school_courses.csv。",
  },
  {
    title: "登录态规律",
    icon: IconRoute,
    text: "浏览器已经登录时能看到课表，Python 初次请求却可能拿到登录页。关键差异通常是 Cookie 和会话状态。",
  },
  {
    title: "解析重点",
    icon: IconFileSearch,
    text: "先保存 HTML，再用 BeautifulSoup 定位 table、tr、th、td。不要直接猜字段，先打印表头和前几条记录。",
  },
  {
    title: "分页与去重",
    icon: IconListTree,
    text: "检查页码链接、隐藏字段或分页参数。循环抓取时要设置页数边界、访问间隔和去重规则。",
  },
  {
    title: "输出表格",
    icon: IconArchive,
    text: "将结构化记录写入 school_courses.csv，使用 utf-8-sig 编码，方便 Excel 直接打开中文表格。",
  },
  {
    title: "合规边界",
    icon: IconShield,
    text: "只使用本人账号和课程授权范围内的数据做练习；Cookie 不提交、不截图、不传播；请求频率保持克制。",
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
    text: "BeautifulSoup 负责把课表 HTML 表格转换成字典列表，清洗函数负责统一字段。",
  },
  {
    title: "保存层",
    icon: IconArchive,
    text: "CSV 把采集结果变成可复查、可提交、可继续分析的数据文件。",
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
        <div class="lesson-hero-grid">
          <div class="lesson-hero-copy">
            <p class="kicker">CHAPTER 07 WEB DATA CRAWLING</p>
            <h1>网络数据爬取：<br />让 Python 学会从互联网获取信息</h1>
            <p class="hero-intro">
              第七章把前面学过的数据类型、文件操作和模块能力串起来。
              本章不再只处理本地文件，而是围绕教务课表页面完成请求诊断、登录态访问、结构解析、分页采集和表格保存。
            </p>
            <ul class="hero-checklist">
              <li>从最简单的 <code>requests.get()</code> 开始，理解请求和响应。</li>
              <li>围绕同一个课表采集任务，逐步发现问题、定位原因、修改代码。</li>
              <li>把 HTML 表格整理成 CSV，形成可以复查的数据文件。</li>
            </ul>
          </div>
          <aside class="lesson-hero-panel">
            <span class="lesson-panel-label">全校课表采集实战</span>
            <div class="lesson-metric" v-for="metric in chapterMetrics" :key="metric.label">
              <strong>{{ metric.value }}</strong>
              <span>{{ metric.label }}</span>
            </div>
          </aside>
        </div>
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
          学习顺序按照真实数据采集流程展开：先发出请求，再识别登录态问题，然后解析表格和分页，
          最后把课表记录保存为可以复用的数据文件。
        </p>
        <div class="lesson-phase-track">
          <article class="lesson-phase-card" v-for="item in roadmap" :key="item.no">
            <span>{{ item.no }}</span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </section>

      <section
        class="section reveal"
        data-outline-level="1"
        data-outline-label="练习站入口"
      >
        <div class="section-head">
          <p class="kicker">PRACTICE SITE</p>
          <h2>3 练习与目标入口：从练习素材走向教务课表</h2>
        </div>
        <p class="section-note">
          前两个入口用于练习 JSON 和静态 HTML 的基本解析。第三个入口是本章代码实战的目标页面，
          用来学习登录态、表格解析、分页和 CSV 保存。
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
        <p class="lesson-cue">
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
        <p class="lesson-cue">
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
        <p class="lesson-cue">
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
        <p class="lesson-cue">
          解析工具不能乱用。JSON、HTML、纯文本、二进制文件和登录态页面的处理方式不同。
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
        <p class="lesson-cue">
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
        <p class="lesson-cue">
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
        <p class="lesson-cue">
          requests、Cookie、Session、BeautifulSoup 和 CSV，正好对应了本章从请求页面到保存课表的完整路线。
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
        <p class="lesson-cue">
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
        <p class="lesson-cue">
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
        <p class="lesson-cue">
          代码实战围绕“爬取全校课表”这一目标渐进展开。每一页先说明遇到的问题，
          再明确本节只改哪里，最后给出增量代码和检查方式。
        </p>
        <div class="lesson-step-list">
          <span v-for="item in codePracticeMap" :key="item.title">
            <strong>{{ item.title }}</strong><br />
            {{ item.text }}
          </span>
        </div>
      </section>

      <section
        v-for="slide in codeSlides"
        :key="slide.no"
        class="section reveal lesson-code-page"
        :data-outline-level="slide.outlineLevel || 2"
        :data-outline-label="slide.label"
      >
        <div class="lesson-slide-layout">
          <div class="lesson-slide-notes">
            <div class="section-head">
              <p class="kicker">{{ slide.displayNo || `5.${Number(slide.no)}` }} CODE PRACTICE</p>
              <h2>{{ slide.title }}</h2>
            </div>
            <p v-if="slide.problem" class="lesson-cue">{{ slide.problem }}</p>

            <div class="lesson-teach-stack">
              <article v-if="slide.change" class="command-card lesson-teach-card">
                <h3>本节修改</h3>
                <p>{{ slide.change }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>这一段在做什么</h3>
                <p>{{ slide.explain }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>关键记忆点</h3>
                <p>{{ slide.key }}</p>
              </article>
              <article class="command-card lesson-teach-card">
                <h3>运行检查</h3>
                <p>{{ slide.check }}</p>
              </article>
            </div>

            <div v-if="slide.notes" class="lesson-plain-notes">
              <p v-for="note in slide.notes" :key="note">{{ note }}</p>
            </div>
          </div>

          <div v-if="slide.kind === 'table'" class="lesson-table-card">
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
          <pre v-else><code class="python">{{ slide.code }}</code></pre>
          <a
            v-if="slide.downloadHref"
            class="lesson-download-link"
            :href="slide.downloadHref"
            download
          >
            下载完整代码：{{ slide.downloadHref }}
          </a>
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
          <h2>7 综合项目：爬取全校课表并保存为 CSV</h2>
        </div>
        <p class="lesson-cue">
          最终项目不是另起一个无关案例，而是把第 5 节逐步完成的代码合并成完整流程：
          使用 <code>requests</code> 携带本人登录态访问教务课表页面，用 <code>BeautifulSoup</code>
          解析表格和分页，再把课表记录保存成 <code>school_courses.csv</code>。
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
.page.is-slide-deck .chapter-seven-grid {
  margin-top: 16px;
  display: grid;
  gap: 12px;
  align-items: stretch;
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


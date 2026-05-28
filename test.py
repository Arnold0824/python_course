# 新建文件：course_spider.py
# 目标：先让程序能发出一次请求，不处理登录态、不解析表格。

import requests
from pathlib import Path


URL = "https://jw.guc.edu.cn/yethan/CourseAction"
COOKIE = "username=20230135; sl-session=XxegQ3UN72l+N+TeLsTmGw==; JSESSIONID=00B86215C6150071D79405F0E913C3FF; Hm_lvt_da1a662b816ecaf953251c774dc1fb07=1775959540,1776675973,1777187851,1777256942; Hm_lpvt_da1a662b816ecaf953251c774dc1fb07=1777256942; HMACCOUNT=B9D4D2C6C8F45BA2"

MAX_PAGE = 20  # 先用 2 测试，确认分页生效后再调大。

import csv

# 添加位置：常量区
OUTPUT_FILE = "school_courses.csv"

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


def build_params():
    """返回课表页面需要的查询参数。"""
    return {
        "setAction": "queryCourseList",
        "selectTableType": "History",
    }


def parse_cookie(raw_cookie):
    raw_cookie = raw_cookie.strip()
    if not raw_cookie:
        raise SystemExit(
            "请先填写 COOKIE，例如 username=...; sl-session=...; JSESSIONID=..."
        )

    lines = [line.strip() for line in raw_cookie.replace("\r", "\n").split("\n")]
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


def build_headers():
    """返回普通浏览器请求头。这里还不包含 Cookie。"""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/147.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }


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


def build_session(cookie):
    """创建一个带公共 headers 和登录 Cookie 的会话。"""
    session = requests.Session()
    session.headers.update(build_headers())
    session.cookies.update(parse_cookie(cookie))
    return session


def fetch_course_page(session, params):
    """请求课表页面，返回解码后的 HTML。"""
    response = session.get(URL, params=params, timeout=10)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text


from bs4 import BeautifulSoup


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

    headers = [
        clean_header(cell.get_text(" ", strip=True))
        for cell in rows[0].find_all(["th", "td"])
    ]
    records = []
    for row in rows[1:]:
        values = [
            clean_text(cell.get_text(" ", strip=True))
            for cell in row.find_all(["td", "th"])
        ]
        if not any(values):
            continue

        record = {}
        for index, value in enumerate(values):
            key = (
                headers[index]
                if index < len(headers) and headers[index]
                else f"字段{index + 1}"
            )
            record[key] = value
        records.append(record)
    return records


def normalize_course(record):
    """按网页课表表头保存字段，不猜测、不改名。"""
    return {field: record.get(field, "") for field in COURSE_FIELDS}


def build_page_params(page):
    """在原始查询参数基础上添加 jumpPage，实现翻页。"""
    params = build_params()
    params["jumpPage"] = str(page)
    return params


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


def save_csv(records, filename):
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COURSE_FIELDS)
        writer.writeheader()
        writer.writerows(records)


def main():
    session = build_session(COOKIE)
    records = fetch_all_courses(session)
    print("去重后记录数：", len(records))
    save_csv(records, OUTPUT_FILE)
    print(f"已保存 {len(records)} 条记录到 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

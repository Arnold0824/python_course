import csv
from time import sleep

import requests
from bs4 import BeautifulSoup


URL = "https://jw.guc.edu.cn/yethan/CourseAction"
COOKIE = ""
MAX_PAGE = 2
OUTPUT_FILE = "school_courses.csv"
SLEEP_SECONDS = 0.3

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
    """返回课表页面需要的基础查询参数。"""
    return {
        "setAction": "queryCourseList",
        "selectTableType": "History",
    }


def build_page_params(page):
    """在基础查询参数中加入 jumpPage，实现翻页。"""
    params = build_params()
    params["jumpPage"] = str(page)
    return params


def parse_cookie(raw_cookie):
    """把浏览器复制出的 Cookie 字符串拆成 requests 可用的字典。"""
    raw_cookie = raw_cookie.strip()
    if not raw_cookie:
        raise SystemExit("请先填写 COOKIE。")

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
    """返回普通浏览器请求头。Cookie 单独交给 session.cookies 管理。"""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/147.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }


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


def is_login_page(html):
    """粗略判断当前 HTML 是否仍然是登录页。"""
    preview = html[:1000].lower()
    return "登录" in html[:1000] or "login" in preview


def clean_text(text):
    """压缩多余空白，让单元格文本更干净。"""
    return " ".join(text.split())


def clean_header(text):
    """网页表头里有换行时，去掉空白，保留原始字段名称。"""
    return "".join(text.split())


def get_table_headers(table):
    rows = table.find_all("tr")
    if not rows:
        return []
    return [
        clean_header(cell.get_text(" ", strip=True))
        for cell in rows[0].find_all(["th", "td"])
    ]


def find_course_table(html):
    """找到包含课表字段的 table。"""
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.find_all("table"):
        headers = get_table_headers(table)
        if "课程名称" in headers and "选课编号" in headers and "时间地点" in headers:
            return table
    return None


def parse_table_records(table):
    """把课表 table 解析成字典列表。"""
    rows = table.find_all("tr")
    if not rows:
        return []

    headers = get_table_headers(table)
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
            key = headers[index] if index < len(headers) and headers[index] else f"字段{index + 1}"
            record[key] = value
        records.append(record)
    return records


def normalize_course(record):
    """按网页课表表头保存字段，不猜测、不改名。"""
    return {field: record.get(field, "") for field in COURSE_FIELDS}


def make_course_key(record):
    """用一整行字段内容做去重键。"""
    return "|".join(record.get(field, "") for field in COURSE_FIELDS)


def fetch_all_courses(session):
    """逐页请求、解析、整理并去重。"""
    all_records = []
    seen = set()

    for page in range(1, MAX_PAGE + 1):
        html = fetch_course_page(session, build_page_params(page))
        if is_login_page(html):
            raise SystemExit("当前响应像登录页，请检查 COOKIE 是否过期。")

        table = find_course_table(html)
        raw_records = parse_table_records(table) if table else []
        page_courses = [normalize_course(record) for record in raw_records]
        print(f"第 {page} 页：{len(page_courses)} 条")

        for record in page_courses:
            key = make_course_key(record)
            if key not in seen:
                seen.add(key)
                all_records.append(record)

        sleep(SLEEP_SECONDS)

    return all_records


def save_csv(records, filename):
    """把课程记录保存成 Excel 友好的 CSV。"""
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COURSE_FIELDS)
        writer.writeheader()
        writer.writerows(records)


def main():
    session = build_session(COOKIE)
    records = fetch_all_courses(session)
    if not records:
        raise SystemExit("没有提取到课程记录，请检查登录态、分页参数和表格结构。")
    save_csv(records, OUTPUT_FILE)
    print(f"已保存 {len(records)} 条记录到 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

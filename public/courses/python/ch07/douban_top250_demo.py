"""
Chapter 7 · Section 6 配套示例
============================

用 Selenium 抓取豆瓣电影 Top250，导出 CSV。

这是 Section 6 的"能跑通的版本"。Section 6.8 那张拉勾验证截图说明了
为什么我们没有把招聘网站做成可下载的 demo —— 反爬命中的概率太高，
不适合作为教学的第一个跑通案例。

教学要点
--------
* 反检测三件套（在 build_driver 里）
* WebDriverWait 等条件成立而不是死睡
* CSS 选择器：.title / .rating_num / em / p.quote span
* 翻页：直接构造 ?start=N，比模拟点击稳定
* 字段隔离 try/except：单部电影解析失败不会拖垮整批

合规边界
--------
* 豆瓣 Top250 是公开榜单，不是个人页或登录态内容
* 默认 MAX_PAGES=2（共 50 部），单次抓取上限不要加大太多
* 页与页之间随机睡眠 2-4 秒，模拟正常用户翻页节奏
* 不抓登录后才能看的短评、想看、私人主页

依赖
----
    pip install selenium

运行
----
    python douban_top250_demo.py

输出
----
    douban_top250.csv  （utf-8-sig，Excel 可直接打开）
"""

from __future__ import annotations

import csv
import io
import random
import re
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

# Windows 默认控制台编码是 GBK，碰到 Unicode 符号会抛 UnicodeEncodeError。
# 这一行让 print 强制走 UTF-8，跑脚本前不需要再 chcp 65001。
if sys.platform == "win32" and isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ---------- 1. 可调参数 ----------
MAX_PAGES = 2  # 每页 25 部，2 页 = 50 部
PAGE_SLEEP_RANGE = (2.0, 4.0)
OUT_PATH = Path(__file__).with_name("douban_top250.csv")
BASE_URL = "https://movie.douban.com/top250"


# ---------- 2. 数据结构 ----------
@dataclass
class Movie:
    rank: str
    title_cn: str
    title_en: str
    rating: str
    rating_count: str
    year: str
    country: str
    genre: str
    director_actor: str
    quote: str
    detail_url: str


# ---------- 3. 浏览器：反检测设置 ----------
def build_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--window-size=1366,900")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/147.0.0.0 Safari/537.36"
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=opts)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"},
    )
    return driver


# ---------- 4. 单页电影抽取 ----------
def parse_page(driver: webdriver.Chrome) -> list[Movie]:
    items = driver.find_elements(By.CSS_SELECTOR, "ol.grid_view li")
    movies: list[Movie] = []
    for it in items:
        try:
            movies.append(parse_one(it))
        except (NoSuchElementException, IndexError):
            # 个别条目结构异常时跳过，不让它拖垮整批
            continue
    return movies


def parse_one(card) -> Movie:
    rank = card.find_element(By.CSS_SELECTOR, "em").text.strip()

    titles = card.find_elements(By.CSS_SELECTOR, ".title")
    title_cn = titles[0].text.strip()
    # 第二个 .title 形如 " / The Shawshank Redemption"，去掉前导斜杠
    title_en = (
        titles[1].text.strip().lstrip("/").strip() if len(titles) > 1 else ""
    )

    rating = card.find_element(By.CSS_SELECTOR, ".rating_num").text.strip()

    # 评分人数：在 .rating_num 同级的 span 里，文本含"人评价"
    rating_count = ""
    for sp in card.find_elements(By.CSS_SELECTOR, ".bd > div span"):
        m = re.search(r"(\d+)人评价", sp.text or "")
        if m:
            rating_count = m.group(1)
            break

    # info 文本格式：
    #   导演: ... 主演: ...
    #   1994 / 美国 / 犯罪 剧情
    info_text = card.find_element(By.CSS_SELECTOR, ".bd p").text
    director_actor, year, country, genre = split_info(info_text)

    # 引言（部分电影没有）
    quote = ""
    quote_nodes = card.find_elements(By.CSS_SELECTOR, "p.quote span")
    if quote_nodes:
        quote = quote_nodes[0].text.strip()

    detail_url = card.find_element(By.CSS_SELECTOR, ".hd a").get_attribute("href") or ""

    return Movie(
        rank=rank,
        title_cn=title_cn,
        title_en=title_en,
        rating=rating,
        rating_count=rating_count,
        year=year,
        country=country,
        genre=genre,
        director_actor=director_actor,
        quote=quote,
        detail_url=detail_url,
    )


def split_info(text: str) -> tuple[str, str, str, str]:
    """把 .bd p 的两行文本拆成 4 个字段。"""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    director_actor = lines[0] if lines else ""
    year = country = genre = ""
    if len(lines) >= 2:
        parts = [p.strip() for p in lines[1].split("/")]
        if len(parts) >= 1:
            year = parts[0]
        if len(parts) >= 2:
            country = parts[1]
        if len(parts) >= 3:
            genre = parts[2]
    return director_actor, year, country, genre


# ---------- 5. 翻页 ----------
def open_page(driver: webdriver.Chrome, page_no: int) -> None:
    """页码 1-indexed，对应 ?start=0,25,50,..."""
    start = (page_no - 1) * 25
    driver.get(f"{BASE_URL}?start={start}")


def wait_for_list(driver: webdriver.Chrome, timeout: int = 15) -> bool:
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ol.grid_view li .rating_num"))
        )
        return True
    except TimeoutException:
        return False


# ---------- 6. CSV ----------
def write_csv(movies: Iterable[Movie], path: Path) -> None:
    fields = [f.name for f in Movie.__dataclass_fields__.values()]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for m in movies:
            writer.writerow(asdict(m))


# ---------- 7. 主流程 ----------
def main() -> int:
    print(f"[douban] 抓取 Top250 前 {MAX_PAGES} 页（共 {MAX_PAGES * 25} 部）")
    driver = build_driver()
    all_movies: list[Movie] = []
    try:
        for page in range(1, MAX_PAGES + 1):
            print(f"[douban] 第 {page}/{MAX_PAGES} 页 ...")
            open_page(driver, page)

            if not wait_for_list(driver):
                print("  ! 列表加载超时，跳过本页")
                continue

            movies = parse_page(driver)
            print(f"  + 抓到 {len(movies)} 部")
            all_movies.extend(movies)

            if page < MAX_PAGES:
                sleep_for = random.uniform(*PAGE_SLEEP_RANGE)
                print(f"  ~ 礼貌等待 {sleep_for:.1f}s")
                time.sleep(sleep_for)
    except KeyboardInterrupt:
        print("\n[douban] 用户中断")
    finally:
        driver.quit()

    if all_movies:
        write_csv(all_movies, OUT_PATH)
        print(f"[douban] ✓ 共 {len(all_movies)} 部 → {OUT_PATH}")
        return 0
    print("[douban] ✗ 没有抓到任何电影")
    return 1


if __name__ == "__main__":
    sys.exit(main())

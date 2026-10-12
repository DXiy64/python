"""爬虫日报独立入口：在 day30 目录运行 python daily30.py。"""

import csv
import sqlite3
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).parent
DB = HERE / "quotes30.db"
OUT = HERE / "out"
URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "python-learn/30"}


def fetch_page(n):
    """返回 HTML 字符串；请求失败交给调用者处理。"""
    response = requests.get(f"{URL}/page/{n}/", timeout=10, headers=HEADERS)
    response.raise_for_status()
    return response.text


def parse(html):
    """HTML → [(名言, 作者, 标签), ...]。"""
    rows = []
    for quote in BeautifulSoup(html, "html.parser").select(".quote"):
        text = quote.select_one(".text")
        author = quote.select_one(".author")
        if text is None or author is None:
            raise ValueError("网页中的名言缺少正文或作者")
        rows.append((text.get_text(strip=True), author.get_text(strip=True),
                     ",".join(t.get_text(strip=True) for t in quote.select(".tag"))))
    if not rows:
        raise ValueError("没有解析到名言，请检查网页内容")
    return rows


def init_db(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS quotes "
                 "(text TEXT PRIMARY KEY, author TEXT NOT NULL, tags TEXT)")
    conn.commit()


def crawl(conn, pages=2):
    # 先抓齐要求的页面，失败时不提交本轮的部分数据。
    rows = []
    for n in range(1, pages + 1):
        rows.extend(parse(fetch_page(n)))
        if n < pages:
            time.sleep(0.5)
    before = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
    with conn:
        conn.executemany("INSERT OR IGNORE INTO quotes VALUES (?, ?, ?)", rows)
    after = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
    return after - before


def stats(conn):
    return conn.execute("SELECT COUNT(*), COUNT(DISTINCT author) FROM quotes").fetchone()


def top_authors(conn, n=3):
    return conn.execute(
        "SELECT author, COUNT(*) AS amount FROM quotes GROUP BY author "
        "ORDER BY amount DESC, author ASC LIMIT ?", (n,)
    ).fetchall()


def check_counter(conn):
    counts = Counter(author for (author,) in conn.execute("SELECT author FROM quotes"))
    expected = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:3]
    actual = top_authors(conn)
    if expected != actual:
        raise ValueError("Counter 与 SQL 排行不一致")
    return actual


def write_report(conn, out=OUT):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    total, authors = stats(conn)
    lines = [f"日报 {now:%Y-%m-%d}", f"共 {total} 条，{authors} 位作者"]
    lines.extend(f"{author}：{count} 条" for author, count in check_counter(conn))
    # 微秒避免短时间内重跑覆盖同名文件。
    path = out / f"日报_{now:%Y%m%d_%H%M%S_%f}.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def export_csv(conn, out=OUT):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"名言_{datetime.now():%Y%m%d_%H%M%S_%f}.csv"
    rows = conn.execute("SELECT text, author, tags FROM quotes ORDER BY text").fetchall()
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["text", "author", "tags"])
        writer.writerows(rows)
    return path, len(rows) + 1


def main():
    conn = sqlite3.connect(DB)
    try:
        init_db(conn)
        added = crawl(conn)
        total, authors = stats(conn)
        report = write_report(conn)
        csv_path, csv_rows = export_csv(conn)
        print(f"本次新增 {added} 条；共 {total} 条，{authors} 位作者")
        print("Top3：", top_authors(conn))
        print("日报：", report)
        print("CSV：", csv_path, "行数（含表头）：", csv_rows)
    except (requests.RequestException, ValueError, sqlite3.Error, OSError) as error:
        print(f"日报生成失败：{error}")
        return 1
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Day39单文件演示：从终端接收作者ID与报告位置。"""
import argparse
import csv
from pathlib import Path
import sqlite3
import sys

DEFAULT_OUTPUT = Path(__file__).resolve().parent / "out" / "quotes.csv"


def prepare_database(conn):
    """固定样本在本文件提供；已写入三条名言，返回None。"""
    conn.executescript("""
        CREATE TABLE quotes(author_id INTEGER NOT NULL, text TEXT NOT NULL);
    """)
    with conn:
        conn.executemany("INSERT INTO quotes VALUES (?, ?)",
                         [(1, "Keep learning."), (2, "Keep learning."), (1, "Practice helps.")])


def write_report(path, rows):
    """path是Path，rows是二元组列表；创建父目录并覆盖指定CSV。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["author_id", "text"])
        writer.writerows(rows)


def build_demo_parser():
    parser = argparse.ArgumentParser(description="按作者查询固定样本并导出CSV")
    parser.add_argument("--author-id", type=int, default=1, help="作者ID，默认1")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV输出路径")
    return parser


def find_by_author(conn, author_id):
    return conn.execute("SELECT author_id,text FROM quotes WHERE author_id=? ORDER BY text", (author_id,)).fetchall()


def main(argv=None):
    # argv默认None时，从终端读取参数；测试可以传字符串列表。
    parser = build_demo_parser()
    args = parser.parse_args(argv)
    # 参数错误会在上面退出，不会先创建数据库或报告。
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        rows = find_by_author(conn, args.author_id)
    finally:
        conn.close()
    try:
        write_report(args.output, rows)
    except OSError as error:
        print(f"报告写入失败：{error}", file=sys.stderr)
        return 1
    print(f"查询作者{args.author_id}，导出{len(rows)}条：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

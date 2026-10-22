"""Day39作业：仅实现build_parser和末尾一句笔记。"""
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


def build_parser():
    """返回ArgumentParser，不在此函数内parse_args。

    --text：必填字符串；--output：Path类型，默认DEFAULT_OUTPUT。
    保留自动--help；两个选项各写一句help说明。
    """
    raise NotImplementedError("TODO：构造并返回命令行解析器")


def find_by_text(conn, text):
    """已提供的只读参数化查询；返回按作者ID排序的二元组列表。"""
    return conn.execute("SELECT author_id,text FROM quotes WHERE text=? ORDER BY author_id", (text,)).fetchall()


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.text.strip():
        parser.error("--text不能是空字符串或全空格")
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        rows = find_by_text(conn, args.text)
    finally:
        conn.close()
    try:
        write_report(args.output, rows)
    except OSError as error:
        print(f"报告写入失败：{error}", file=sys.stderr)
        return 1
    print(f"导出{len(rows)}条：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# 笔记TODO：parse_args返回什么？终端--text的值如何传到SQL问号和最终CSV？

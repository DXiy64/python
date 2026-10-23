"""Day40单文件起始演示：准备固定数据，关联查询并导出。"""
import argparse
import csv
import json
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parent


def load_rows(source):
    """读取当天JSON，返回[(作者ID,正文), ...]；此时尚未写数据库。"""
    data = json.loads(source.read_text(encoding="utf-8"))
    return [(q["author_id"], q["text"]) for q in data["quotes"]]


def prepare_database(conn):
    """创建不存在的表并确保三位作者存在；不清空已有数据。"""
    conn.execute("PRAGMA foreign_keys = ON")
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS authors(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS quotes(
            id INTEGER PRIMARY KEY,
            author_id INTEGER NOT NULL REFERENCES authors(id),
            text TEXT NOT NULL,
            UNIQUE(author_id,text)
        );
        CREATE INDEX IF NOT EXISTS idx_quotes_text ON quotes(text);
    """)
    with conn:
        conn.executemany("INSERT OR IGNORE INTO authors VALUES (?, ?)",
                         [(1,"Alex"), (2,"Blair"), (3,"Casey")])


def save_quotes(conn, rows):
    """一批一个事务；失败整批回滚并向调用者抛出，不关闭连接。"""
    before = conn.total_changes
    with conn:
        conn.executemany("INSERT OR IGNORE INTO quotes(author_id,text) VALUES (?,?)", rows)
    return conn.total_changes - before


def report_rows(conn):
    """INNER JOIN返回[(作者ID,作者名,正文), ...]；只查询，不关闭连接。"""
    return conn.execute("""
        SELECT a.id, a.name, q.text
        FROM quotes AS q INNER JOIN authors AS a ON q.author_id=a.id
        ORDER BY a.id, q.text
    """).fetchall()


def write_report(output, rows):
    """创建父目录，覆盖指定CSV；rows为三元组列表，空列表只写表头。"""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w",encoding="utf-8-sig",newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["author_id","author","text"])
        writer.writerows(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Day40关联查询与持久化演示")
    parser.add_argument("--db",type=Path,default=ROOT / "out" / "demo.db")
    parser.add_argument("--output",type=Path,default=ROOT / "out" / "demo.csv")
    args = parser.parse_args(argv)
    args.db.parent.mkdir(parents=True,exist_ok=True)
    conn = sqlite3.connect(args.db)
    try:
        prepare_database(conn)
        added = save_quotes(conn, [(1,"Keep learning."),(2,"Ask clearly."),(1,"Practice helps.")])
        rows = report_rows(conn)
    finally:
        conn.close()
    write_report(args.output,rows)
    print(f"本次新增{added}条；报告共{len(rows)}条：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

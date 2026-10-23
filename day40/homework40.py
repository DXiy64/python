"""Day40作业：仅完成run_pipeline及末尾两句笔记。"""
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


def run_pipeline(source, db_path, output):
    """三个参数都是Path，返回{"added":本次新增数, "rows":关联结果列表}。

    依次读取样本、准备数据库目录和连接、初始化、批量保存、查询、关闭、导出。
    谁创建连接谁负责finally关闭；失败向外抛出，写入失败不导出报告。
    不打印，不删除旧数据；辅助代码均已在本文件提供。
    """
    raise NotImplementedError("TODO：把已有辅助函数串成完整流程")


def main(argv=None):
    parser = argparse.ArgumentParser(description="离线名言入库与关联CSV报告")
    parser.add_argument("--source",type=Path,default=ROOT / "samples" / "quotes.json")
    parser.add_argument("--db",type=Path,default=ROOT / "out" / "quotes.db")
    parser.add_argument("--output",type=Path,default=ROOT / "out" / "quotes.csv")
    args = parser.parse_args(argv)
    try:
        result = run_pipeline(args.source,args.db,args.output)
    except (OSError,ValueError,KeyError,sqlite3.Error) as error:
        print(f"处理失败：{error}",file=sys.stderr)
        return 1
    print(f"本次新增{result['added']}条；报告共{len(result['rows'])}条：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# 笔记TODO 1：哪个函数负责关闭连接？为什么关闭后仍可以用rows写CSV？
# 笔记TODO 2：为什么第二次新增0，报告仍有3条？非法作者失败后原数据应怎样？

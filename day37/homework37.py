"""Day37作业入口；只实现store37.py两个目标与本文件末尾一句笔记。"""

import sqlite3
from store37 import save_quotes, list_quotes


def prepare_database(conn):
    """辅助函数完整给出：存作者，返回尚待保存的名言列表。"""
    conn.execute("PRAGMA foreign_keys = ON")
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    conn.executescript("""
        CREATE TABLE authors(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE quotes(
            id INTEGER PRIMARY KEY,
            author_id INTEGER NOT NULL REFERENCES authors(id),
            text TEXT NOT NULL,
            UNIQUE(author_id, text)
        );
    """)
    with conn:
        conn.executemany(
            "INSERT INTO authors VALUES (?, ?)",
            [(1, "Alex"), (2, "Blair"), (3, "Casey")],
        )
    return [(1, "Keep learning."), (1, "Practice helps."), (2, "Ask clearly.")]


def snapshot(conn):
    """仅供检查整张表是否变化，学员不必修改。"""
    return conn.execute(
        "SELECT author_id, text FROM quotes ORDER BY author_id, text"
    ).fetchall()


def main():
    conn = sqlite3.connect(":memory:")
    try:
        rows = prepare_database(conn)
        # 此时作者3位、名言0条；返回rows不会自动写入名言。
        assert list_quotes(conn, 1) == []
        assert save_quotes(conn, rows) == 3
        assert snapshot(conn) == [
            (1, "Keep learning."),
            (1, "Practice helps."),
            (2, "Ask clearly."),
        ]
        assert list_quotes(conn, 1) == [(1, "Keep learning."), (1, "Practice helps.")]
        assert list_quotes(conn, 2) == [(2, "Ask clearly.")]
        assert list_quotes(conn, 3) == []
        assert list_quotes(conn, 999) == []
        print("① 正常与空结果查询通过")
        assert save_quotes(conn, rows) == 0
        assert save_quotes(conn, [(2, "Keep learning.")]) == 1
        assert list_quotes(conn, 2) == [(2, "Ask clearly."), (2, "Keep learning.")]
        print("② 重跑去重与不同作者同正文通过")
        before = snapshot(conn)
        try:
            save_quotes(conn, [(1, "New valid row"), (999, "Invalid author")])
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("非法作者必须抛出IntegrityError")
        assert snapshot(conn) == before
        assert save_quotes(conn, []) == 0
        assert snapshot(conn) == before
        assert not conn.in_transaction
        assert conn.execute("SELECT COUNT(*) FROM authors").fetchone()[0] == 3
        print("③ 整批回滚、空批次及连接仍可使用通过")
    finally:
        conn.close()
    print("Day37代码检查通过；请同时完成末尾笔记")


if __name__ == "__main__":
    main()


# 笔记TODO：谁创建和关闭连接？为什么store里的函数返回数据，而由main打印？

# 答：这里的函数返回数据，而由main打印，是因为main函数是主函数，负责调用store37.py里的函数，并打印函数的返回值。并且是由main函数创建和关闭连接，因为main函数是整个程序的入口，负责整个程序的运行。

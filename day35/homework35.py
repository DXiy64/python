"""Day35：补一个保留零名言作者的统计查询和一句说明。"""

import sqlite3

from tools35 import prepare_database


def author_report(conn):
    # TODO：一条LEFT JOIN分组查询，返回[(作者id, 作者name, 名言条数), ...]。
    # authors应在LEFT JOIN左边；按作者id升序；零名言作者也要保留。
    # 用COUNT统计真正匹配到的名言，不把空匹配占位行误算成一条名言。
    # 返回fetchall得到的列表，不打印、不修改数据、不新建或关闭conn。
    return conn.execute(
        "SELECT a.id, a.name, COUNT(q.id) AS quote_count FROM authors AS a LEFT JOIN quotes AS q ON q.author_id = a.id GROUP BY a.id, a.name ORDER BY a.id ASC"
    ).fetchall()


def main():
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        actual = author_report(conn)
        expected = [(1, "Alex", 2), (2, "Blair", 1), (3, "Casey", 0)]
        assert actual == expected, (actual, expected)
        assert conn.execute("SELECT COUNT(*) FROM authors").fetchone()[0] == 3
        assert conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0] == 3
        print("正常统计通过：Alex两条、Blair一条、Casey零条")
    finally:
        conn.close()

    empty_conn = sqlite3.connect(":memory:")
    try:
        prepare_database(empty_conn, include_quotes=False)
        actual = author_report(empty_conn)
        expected = [(1, "Alex", 0), (2, "Blair", 0), (3, "Casey", 0)]
        assert actual == expected, (actual, expected)
        assert empty_conn.execute("SELECT COUNT(*) FROM authors").fetchone()[0] == 3
        assert empty_conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0] == 0
        print("全空名言场景通过：三位作者均保留，名言数均为0")
    finally:
        empty_conn.close()
    print("Day35代码检查通过；两次连接均由main关闭")


if __name__ == "__main__":
    main()


# 笔记：Casey没有名言时，为什么LEFT JOIN后COUNT(*)是1，而COUNT(q.id)是0？NULL与0有什么区别？

# 答：因为虽然Casey没有名言，但是左关联时，authors表中的Casey行仍然存在，只是quotes表中的q.id是NULL，而不是0。COUNT(q.id)会忽略NULL，所以是0；而COUNT(*)会计算所有行，所以是1。

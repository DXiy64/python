"""Day35：LEFT JOIN保留零名言作者；NULL与COUNT的区别。"""

import sqlite3

from tools35 import prepare_database

DEMO_GROUP_SQL = """
    SELECT a.id, a.name, COUNT(*) AS joined_rows, COUNT(q.id) AS quote_count
    FROM authors AS a
    LEFT JOIN quotes AS q ON q.author_id = a.id
    GROUP BY a.id, a.name
    ORDER BY a.id
"""


def main():
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        print("① 从authors出发，LEFT JOIN保留左边每位作者")
        rows = conn.execute("""
            SELECT a.id, a.name, q.id
            FROM authors AS a
            LEFT JOIN quotes AS q ON q.author_id = a.id
            ORDER BY a.id, q.id
        """).fetchall()
        expected = [(1, "Alex", 101), (1, "Alex", 102), (2, "Blair", 103), (3, "Casey", None)]
        assert rows == expected, (rows, expected)
        print("作者ID、名字、匹配的名言ID：", rows)

        print("② 找不到右表记录时，右表字段是SQL NULL，Python取到None")
        assert rows[-1] == (3, "Casey", None)
        print("Casey真实存在；None表示没匹配到名言，不是名言ID等于0。")
        print("数据库并未插入一条空名言，这只是关联查询的结果。")

        print("③ 按作者分组：COUNT(*)数结果行，COUNT(q.id)只数非NULL名言ID")
        grouped = conn.execute(DEMO_GROUP_SQL).fetchall()
        expected = [(1, "Alex", 2, 2), (2, "Blair", 1, 1), (3, "Casey", 1, 0)]
        assert grouped == expected, (grouped, expected)
        print("作者ID、名字、结果行数、名言条数：", grouped)
        print("Casey被保留为一行，所以COUNT(*)=1；q.id是NULL，所以COUNT(q.id)=0。")
    finally:
        conn.close()

    print("④ 名言表全空时，三位作者仍保留，每人的名言数都是0")
    empty_conn = sqlite3.connect(":memory:")
    try:
        prepare_database(empty_conn, include_quotes=False)
        grouped = empty_conn.execute(DEMO_GROUP_SQL).fetchall()
        expected = [(1, "Alex", 1, 0), (2, "Blair", 1, 0), (3, "Casey", 1, 0)]
        assert grouped == expected, (grouped, expected)
        print("零名言场景：", grouped)
        assert empty_conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0] == 0
    finally:
        empty_conn.close()
    print("连接已关闭；只读样本，没有生成正式数据库。")


if __name__ == "__main__":
    main()

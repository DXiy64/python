"""Day34：INNER JOIN用外键对应主键，返回两表匹配后的查询结果。"""

import sqlite3

from tools34 import prepare_database

DEMO_SQL = """
    SELECT q.id, a.name
    FROM quotes AS q
    INNER JOIN authors AS a
        ON q.author_id = a.id
    ORDER BY q.id
"""


def main():
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        print("① 两张表分别存什么：名言保存作者ID，名字在作者表")
        print("作者：", conn.execute("SELECT id, name FROM authors ORDER BY id").fetchall())
        print("名言：", conn.execute("SELECT id, author_id, text FROM quotes ORDER BY id").fetchall())

        print("② ON说明怎样配对，不能把两张表各自的主键直接当关系")
        print("名言101的author_id=1，对应authors.id=1，所以作者是Alex。")
        print("q是quotes的别名，a是authors的别名；q.id是名言ID，a.id是作者ID。")
        print("关系是q.author_id = a.id；不是q.id = a.id。")

        print("③ INNER JOIN把匹配行的字段放进同一结果行")
        rows = conn.execute(DEMO_SQL).fetchall()
        assert rows == [(101, "Alex"), (102, "Alex"), (103, "Blair")], rows
        print("名言ID与作者名：", rows)
        print("SELECT列顺序决定元组内容；ORDER BY q.id决定各行的排列。")
        print("Casey没有名言，因此这次INNER JOIN结果里没有Casey。")
    finally:
        conn.close()

    print("④ 没有能配对的名言时，返回空列表，不是报错")
    empty_conn = sqlite3.connect(":memory:")
    try:
        prepare_database(empty_conn, include_quotes=False)
        rows = empty_conn.execute(DEMO_SQL).fetchall()
        assert rows == [], rows
        assert empty_conn.execute("SELECT COUNT(*) FROM authors").fetchone()[0] == 3
        print("作者表仍有3人，名言表为空，关联结果：", rows)
    finally:
        empty_conn.close()
    print("两次连接均已关闭；样本未改写，没有生成数据库文件。")


if __name__ == "__main__":
    main()

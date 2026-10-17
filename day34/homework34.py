"""Day34：补一个INNER JOIN查询函数和一句关系说明；辅助工具随课。"""

import sqlite3

from tools34 import prepare_database


def list_quotes(conn):
    # TODO：使用INNER JOIN关联quotes与authors。
    # 返回[(名言id, 正文text, 作者name), ...]，按名言id升序。
    # 用传入conn查询，不打印、不写数据、不新建或关闭连接。
    # 正常返回行元组列表；无匹配记录时返回[]。
    return conn.execute("""
        SELECT q.id, q.text, a.name
        FROM quotes AS q
        INNER JOIN authors AS a 
        ON q.author_id = a.id
        ORDER BY q.id ASC
        """).fetchall()


def main():
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        actual = list_quotes(conn)
        expected = [
            (101, "Keep learning.", "Alex"),
            (102, "Practice helps.", "Alex"),
            (103, "Ask clearly.", "Blair"),
        ]
        assert actual == expected, (actual, expected)
        assert conn.execute("SELECT COUNT(*) FROM authors").fetchone()[0] == 3
        assert conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0] == 3
        print("正常关联查询与结果顺序检查通过")
    finally:
        conn.close()

    empty_conn = sqlite3.connect(":memory:")
    try:
        prepare_database(empty_conn, include_quotes=False)
        actual = list_quotes(empty_conn)
        assert actual == [], actual
        assert empty_conn.execute("SELECT COUNT(*) FROM authors").fetchone()[0] == 3
        print("无匹配名言时返回空列表，作者记录保留")
    finally:
        empty_conn.close()
    print("Day34代码检查通过；两次连接均由main关闭")


if __name__ == "__main__":
    main()


# 笔记：用自己的话说明ON应该比较哪两个字段，为什么不能只比较两张表各自的id。

# 答：因为两张表中的id字段可能不是同一个id，所以需要用ON关键字来指定比较的关联字段。而authors表中的id字段是作者的唯一标识，所以应该比较  quotes表  中的author_id字段  和  authors表  中的id字段，以确保关联正确。

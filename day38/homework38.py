"""Day38作业：只实现ensure_text_index及末尾笔记。"""
import sqlite3
from tools38 import prepare_database, find_quotes, query_plan, index_columns


def ensure_text_index(conn):
    """确保quotes(text)有名为idx_quotes_text的普通索引。

    可重复调用；不新增author_id索引，不改数据、不打印、不关闭连接。
    无需返回值。入口没有待提交事务。
    """
    raise NotImplementedError("TODO：创建可重复调用的正文索引")


def main():
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        before = conn.execute("SELECT id, author_id, text FROM quotes ORDER BY id").fetchall()
        changes = conn.total_changes
        print("① 已有索引：", index_columns(conn))
        print("② 正文过滤的原计划：", query_plan(conn, "Keep learning."))
        ensure_text_index(conn)
        ensure_text_index(conn)
        indexes = index_columns(conn)
        assert ("idx_quotes_text", ["text"]) in indexes
        assert len(indexes) == 2  # 一个原有UNIQUE索引，加一个正文索引
        print("③ 新索引：", indexes)
        print("④ 正文过滤的新计划：", query_plan(conn, "Keep learning."))
        assert find_quotes(conn, "Keep learning.") == [(1, "Keep learning."), (2, "Keep learning.")]
        assert find_quotes(conn, "Practice helps.") == [(1, "Practice helps.")]
        assert find_quotes(conn, "Missing") == []
        assert conn.execute("SELECT id, author_id, text FROM quotes ORDER BY id").fetchall() == before
        assert conn.total_changes == changes
        print("⑤ 查询结果、空结果和数据不变检查通过")
    finally:
        conn.close()
    print("Day38代码检查通过；还需核对末尾计划记录与取舍笔记")


if __name__ == "__main__":
    main()

# 笔记TODO：记录正文查询建索引前后的实际计划关键词及含义；
# 解释为什么已有(author_id,text)索引仍需要检查正文查询计划；
# 写出索引对写入和空间的代价。

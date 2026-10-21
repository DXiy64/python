"""Day38讲义：观察正文过滤查询在建索引前后的计划。"""
import sqlite3
from tools38 import prepare_database, find_quotes, query_plan, index_columns


def main():
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        print("① 已有索引：", index_columns(conn))
        expected = [(1, "Keep learning."), (2, "Keep learning.")]
        before = find_quotes(conn, "Keep learning.")
        assert before == expected
        print("② 建索引前的计划：", query_plan(conn, "Keep learning."))
        # 演示用索引名；作业要自行实现另一个名字。
        conn.execute("CREATE INDEX demo_quotes_text ON quotes(text)")
        print("③ 新索引及其列：", index_columns(conn))
        print("④ 建索引后的计划：", query_plan(conn, "Keep learning."))
        assert find_quotes(conn, "Keep learning.") == before
        assert find_quotes(conn, "Missing") == []
        print("⑤ 结果不变：", before)
    finally:
        conn.close()
    print("Day38讲义通过；请阅读homework38.md后完成作业")


if __name__ == "__main__":
    main()

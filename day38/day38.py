"""Day38独立讲义：辅助函数全文随课可见，不需要打开tools38.py。"""
import sqlite3


QUERY = "SELECT author_id, text FROM quotes WHERE text = ? ORDER BY author_id"


def prepare_database(conn):
    """建表并提交1003条名言；不返回列表，返回值为None。"""
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
        conn.executemany("INSERT INTO authors VALUES (?, ?)", [(1, "Alex"), (2, "Blair")])
        conn.executemany(
            "INSERT INTO quotes(author_id, text) VALUES (?, ?)",
            [(1, "Keep learning."), (2, "Keep learning."), (1, "Practice helps.")]
            + [(1, f"Sample {i:04d}") for i in range(1000)],
        )


def find_quotes(conn, text):
    """返回名言行列表；execute返回游标，fetchall才取出结果。"""
    return conn.execute(QUERY, (text,)).fetchall()


def query_plan(conn, text):
    """返回计划行列表；末列是查找方式的描述，不是名言正文。"""
    return conn.execute("EXPLAIN QUERY PLAN " + QUERY, (text,)).fetchall()


def index_columns(conn):
    """辅助显示已有索引：[(索引名, [列名, ...]), ...]。"""
    result = []
    for row in conn.execute("PRAGMA index_list('quotes')").fetchall():
        name = row[1]
        columns = conn.execute(
            "SELECT name FROM pragma_index_info(?) ORDER BY seqno", (name,)
        ).fetchall()
        result.append((name, [column[0] for column in columns]))
    return result


def main():
    # 文件末尾main()从这里进入。前面的def只是加载定义。
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        # 此时authors有2人、quotes有1003条；准备函数已经提交写入。
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

"""Day38辅助代码：样本、查询和计划读取；不导入旧作业。"""
import sqlite3


QUERY = "SELECT author_id, text FROM quotes WHERE text = ? ORDER BY author_id"


def prepare_database(conn):
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
    return conn.execute(QUERY, (text,)).fetchall()


def query_plan(conn, text):
    """返回[(节点ID, 父节点ID, 辅助整数, 描述), ...]。只供本课人工观察。"""
    return conn.execute("EXPLAIN QUERY PLAN " + QUERY, (text,)).fetchall()


def index_columns(conn):
    """返回[(索引名, [列名, ...]), ...]；本课仅处理普通列索引。"""
    result = []
    for row in conn.execute("PRAGMA index_list('quotes')").fetchall():
        name = row[1]
        columns = conn.execute(
            "SELECT name FROM pragma_index_info(?) ORDER BY seqno", (name,)
        ).fetchall()
        result.append((name, [column[0] for column in columns]))
    return result

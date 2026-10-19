"""Day37演示：把存取SQL放进函数，让main负责调用与显示。"""
import sqlite3


def prepare_database(conn):
    """固定样本直接随课提供，不读取旧作业或其他文件。"""
    conn.execute("CREATE TABLE authors(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    with conn:
        conn.executemany("INSERT INTO authors VALUES (?, ?)", [(1, "Alex"), (2, "Blair")])


def add_author(conn, author_id, name):
    """存取函数：写数据库，返回本次新增数，不打印或关闭连接。"""
    before = conn.total_changes
    with conn:
        conn.execute("INSERT OR IGNORE INTO authors(id, name) VALUES (?, ?)", (author_id, name))
    return conn.total_changes - before


def list_authors(conn):
    """存取函数：返回按ID排序的二元组列表。"""
    return conn.execute("SELECT id, name FROM authors ORDER BY id").fetchall()


def main():
    # 入口调用这里；main创建连接，最后也由main关闭。
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        print("① 准备完成：", list_authors(conn))
        added = add_author(conn, 3, "Casey")
        assert added == 1
        print("② main接收存取函数返回值并显示：新增", added)
        rows = list_authors(conn)
        assert rows == [(1, "Alex"), (2, "Blair"), (3, "Casey")]
        print("③ main显示查询结果：", rows)
        assert add_author(conn, 3, "Casey") == 0
        assert conn.execute("SELECT COUNT(*) FROM authors").fetchone()[0] == 3
        print("④ 重复写入返回0；连接仍由main使用")
    finally:
        conn.close()
    print("Day37讲义通过；main已关闭连接")


if __name__ == "__main__":
    main()

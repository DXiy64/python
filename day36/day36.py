"""Day36：一批写入一起提交，遇到错误一起回滚。仅使用内存库。"""
import sqlite3
import json
from pathlib import Path

# 讲义所需的辅助函数完整放在这里，可以在本文件内从头追踪。
# 作业的tools36提供相同接口；本讲义不会调用homework36.py。
SAMPLE = Path(__file__).resolve().parent / "samples" / "seed.json"


def prepare_database(conn):
    """准备空表、存入作者，返回待写入的名言列表。"""
    # data是整个JSON字典；它只在本函数中使用。
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))
    conn.execute("PRAGMA foreign_keys = ON")
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    conn.executescript("""
        CREATE TABLE authors(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE quotes(
            id INTEGER PRIMARY KEY,
            author_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY(author_id) REFERENCES authors(id),
            UNIQUE(author_id, text)
        );
    """)
    conn.executemany("INSERT INTO authors VALUES (?, ?)",
                     [(a["id"], a["name"]) for a in data["authors"]])
    conn.commit()
    # return交给main的是这个新列表，不是上面的data字典。
    return [(q["author_id"], q["text"]) for q in data["quotes"]]


def snapshot(conn):
    """只查询名言表，返回列表；不新增数据，不关闭连接。"""
    return conn.execute("SELECT author_id, text FROM quotes ORDER BY author_id, text").fetchall()


def main():
    # 运行从文件末尾main()跳到这里；上面的def此前只是定义函数。
    conn = sqlite3.connect(":memory:")
    try:
        rows = prepare_database(conn)
        print("准备完成：作者表3人，名言表0条")
        print("交给后续写入的rows：", rows)
        # 初始化已提交；接下来的演示只向quotes写入。
        print("① 正常提交：with conn正常结束会提交事务")
        with conn:
            conn.executemany("INSERT INTO quotes(author_id, text) VALUES (?, ?)", rows)
        assert len(snapshot(conn)) == 3
        print(snapshot(conn))

        print("② UNIQUE(author_id, text)：同作者同正文不能重复")
        try:
            with conn:
                conn.execute("INSERT INTO quotes(author_id, text) VALUES (?, ?)", rows[0])
        except sqlite3.IntegrityError as error:
            print("预期的唯一约束错误：", error)
        else:
            raise AssertionError("重复记录本应被拒绝")
        assert len(snapshot(conn)) == 3

        print("③ 去重重跑：INSERT OR IGNORE跳过重复，正常结束后提交")
        before = conn.total_changes
        with conn:
            conn.executemany("INSERT OR IGNORE INTO quotes(author_id, text) VALUES (?, ?)", rows)
        assert conn.total_changes - before == 0
        print("本次新增0条")

        print("④ 第二条外键错误：第一条也应回滚")
        old = snapshot(conn)
        try:
            with conn:
                conn.execute("INSERT INTO quotes(author_id, text) VALUES (?, ?)", (1, "Temporary row"))
                conn.execute("INSERT OR IGNORE INTO quotes(author_id, text) VALUES (?, ?)", (999, "Bad author"))
        except sqlite3.IntegrityError as error:
            print("预期的外键错误：", error)
        else:
            raise AssertionError("非法作者本应触发外键错误")
        assert snapshot(conn) == old
        print("整批回滚通过；原有3条保持不变")
        print("注意total_changes不因回滚归零，不能据此判断回滚后实际存量。")
    finally:
        conn.close()
    print("Day36讲义全部通过；连接由main关闭")


if __name__ == "__main__":
    # Python从上往下加载定义后，到这里才真正调用main。
    main()

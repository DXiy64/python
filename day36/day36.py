"""Day36：一批写入一起提交，遇到错误一起回滚。仅使用内存库。"""
import sqlite3
from tools36 import prepare_database, snapshot


def main():
    conn = sqlite3.connect(":memory:")
    try:
        rows = prepare_database(conn)
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
    main()

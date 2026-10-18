"""Day36：只完成批量保存函数和末尾一句事务笔记。"""
import sqlite3
from tools36 import prepare_database, snapshot


def save_batch(conn, rows):
    """rows为[(作者ID, 正文), ...]；成功返回本次新增数。"""
    # TODO：在同一个事务内参数化INSERT OR IGNORE写入整批。
    # 正常完成提交，失败整批回滚且让异常向调用者传播。
    # 连接由main负责；不要逐条commit，也不要关闭conn。
    # 入口保证conn没有未提交事务；可记录total_changes前后差。
    raise NotImplementedError("请实现save_batch")


def main():
    conn = sqlite3.connect(":memory:")
    try:
        rows = prepare_database(conn)
        assert save_batch(conn, rows) == 3
        assert snapshot(conn) == [(1, "Keep learning."), (1, "Practice helps."), (2, "Ask clearly.")]
        assert not conn.in_transaction
        print("首次提交通过：新增3条")
        assert save_batch(conn, rows) == 0
        assert len(snapshot(conn)) == 3
        print("重跑去重通过：新增0条")
        assert save_batch(conn, [(2, "Keep learning.")]) == 1
        print("复合键通过：不同作者可有相同正文")
        before = snapshot(conn)
        try:
            save_batch(conn, [(1, "New valid row"), (999, "Invalid author")])
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("非法作者应抛出IntegrityError")
        assert snapshot(conn) == before
        assert not conn.in_transaction
        print("失败回滚通过：整批未保存，原数据保留")
        assert save_batch(conn, []) == 0
        assert snapshot(conn) == before
        print("空批次通过；连接仍可使用")
    finally:
        conn.close()
    print("Day36代码检查通过；请同时完成笔记")


if __name__ == "__main__":
    main()


# 笔记TODO：为什么不能在每次插入后commit？第二条外键失败时，第一条应怎样处理？

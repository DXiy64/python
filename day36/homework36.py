"""Day36：只完成批量保存函数和末尾一句事务笔记。"""

import sqlite3
from tools36 import prepare_database, snapshot


def save_batch(conn, rows):
    """rows为[(作者ID, 正文), ...]；成功返回本次新增数。"""
    # TODO：在同一个事务内参数化INSERT OR IGNORE写入整批。
    # 正常完成提交，失败整批回滚且让异常向调用者传播。
    # 连接由main负责；不要逐条commit，也不要关闭conn。
    # 入口保证conn没有未提交事务；可记录total_changes前后差。
    before = conn.total_changes
    with conn:
        conn.executemany(
            "INSERT OR IGNORE INTO quotes (author_id, text) VALUES (?, ?)",
            rows,
        )
    return conn.total_changes - before


def main():
    conn = sqlite3.connect(":memory:")
    try:
        rows = prepare_database(conn)
        assert save_batch(conn, rows) == 3
        # 检验插入的条数是否正确
        assert snapshot(conn) == [
            (1, "Keep learning."),
            (1, "Practice helps."),
            (2, "Ask clearly."),
        ]
        # 检验插入的数据是否正确
        assert not conn.in_transaction
        # 检验连接是否处于事务状态
        print("首次提交通过：新增3条")
        assert save_batch(conn, rows) == 0
        # 检验插入的条数是否正确
        assert len(snapshot(conn)) == 3
        # 检验次数插入的数据是否正确
        print("重跑去重通过：新增0条")
        assert save_batch(conn, [(2, "Keep learning.")]) == 1
        # 检验ID为2的作者的名言是否正确
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

# 答：因为每次插入后提交，如果第一条插入成功，第二条插入失败，第一条插入的数据会被提交，但第二条插入的数据不会被提交，这会导致数据的不一致。因此，应该将所有的插入操作放在一个事务中，只有当所有的插入操作都成功时，才提交事务，否则回滚事务，保证数据的一致性。


# 自我理解：
# 1、rows是通过prepare_database函数获取的
# 2、prepare_database第一步先将将文件seed.json中的数据读取成字典，第二步是用PRAGMA foreign_keys = ON;开启外键约束(作用是：当插入数据时，如果外键引用的表中的主键不存在，则插入操作会失败)，第三步通过conn.executemany()将字典中的数据插入到临时的数据库中，并返回插入的数据
# 3、save_batch函数的作用是将rows中的数据插入到临时的数据库中，如果插入的数据已经存在，则不会插入，如果插入的数据不存在，则会插入，并返回插入的数据条数
# 4、次文件中main函数的作用是调用prepare_database函数获取rows，然后调用save_batch函数将rows中的数据插入到临时的数据库中，并打印出插入的数据条数

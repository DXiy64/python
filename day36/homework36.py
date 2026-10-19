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
        # 调用save_batch写入三笔样本，检查返回的“本次新增数”为3，而非连接累计修改数。
        assert snapshot(conn) == [
            (1, "Keep learning."),
            (1, "Practice helps."),
            (2, "Ask clearly."),
        ]
        # 查询实际保存的数据，逐项核对作者ID、正文及排序；结果必须恰好是上面三笔。
        assert not conn.in_transaction
        # not表示取反：要求当前没有未结束的事务，说明函数没有把本次写事务留给调用者。
        # 单看这个状态不能区分提交或回滚；需结合上面的数据检查判断本次成功保存。
        print("首次提交通过：新增3条")
        assert save_batch(conn, rows) == 0
        # 用相同样本再次调用保存函数，检查本次新增数为0：重复记录应被跳过。
        assert len(snapshot(conn)) == 3
        # 只检查重跑后表内仍有3条，确认没有新增重复行；这条断言不逐项核对正文。
        print("重跑去重通过：新增0条")
        assert save_batch(conn, [(2, "Keep learning.")]) == 1
        # 1号作者已有相同正文；改为2号作者后应新增1条，检查去重键是“作者ID+正文”。
        # 这里直接检查的是函数返回值，不是另查数据库核对新记录的所有字段。
        print("复合键通过：不同作者可有相同正文")
        before = snapshot(conn)
        try:
            save_batch(conn, [(1, "New valid row"), (999, "Invalid author")])
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("非法作者应抛出IntegrityError")
        assert snapshot(conn) == before
        # 对比失败前后的实际数据：本批先插入的合法记录也应回滚，旧的4条记录保持不变。
        # before是上面新增第4条后的数据快照，不是save_batch内部的累计修改数。
        assert not conn.in_transaction
        # 外键错误已向外传播并离开with conn；要求回滚后没有遗留未结束的事务。
        print("失败回滚通过：整批未保存，原数据保留")
        assert save_batch(conn, []) == 0
        # 保存空列表，检查本次新增数返回0；空批次不应被当作新增了一条记录。
        assert snapshot(conn) == before
        # 再查表内实际数据，确认空批次没有改变已有4条记录；查询成功也说明连接仍可使用。
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

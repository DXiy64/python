"""Day31作业骨架：只补TODO，不修改Day30正式账本或数据库。"""

import sys
import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
# 让从day31直接启动时，也能找到仓库中的day30模块。
sys.path.insert(0, str(ROOT))
from day30.book30 import ContactBook
from day30.daily30 import init_db


def seed_ledger(book):
    """固定日期，避免按今天时间插入导致跨月检查不稳定。"""
    book.conn.executemany(
        "INSERT INTO ledger(money, sort, note, time) VALUES (?, ?, ?, ?)",
        [
            (12.5, "餐饮", "午饭", "2026-10-01 12:00"),
            (7.5, "交通", "公交", "2026-10-02 08:00"),
            (30.0, "餐饮", "晚饭", "2026-09-30 18:00"),
        ],
    )
    book.conn.commit()


def check_months(book):
    # TODO 1：调用month_report，用assert检查10月、9月、空月。
    # 先保存actual，再比较expected；失败消息包含两者。
    actual = book.month_report("2026-10")
    expected = (2, 20)
    assert actual == expected, f"实际：{actual}，预期：{expected}"
    actual = book.month_report("2026-09")
    expected = (1, 30)
    assert actual == expected, f"实际：{actual}，预期：{expected}"
    actual = book.month_report("2026-08")
    expected = (0, 0)
    assert actual == expected, f"实际：{actual}，预期：{expected}"


def check_persistence(path):
    # TODO 2：新建ContactBook(path)，检查总笔数仍为3。
    # 不要再调用seed_ledger；用try/finally关闭连接。

    book = ContactBook(path)
    try:
        actual = book.conn.execute("SELECT COUNT(*) FROM ledger").fetchone()[0]
        expected = 3
        assert actual == expected, f"实际：{actual}\n期望：{expected}"
    finally:
        book.close()


def check_duplicates(conn):
    # TODO 3：调用init_db(conn)，用INSERT OR IGNORE重复插入同一笔名言。
    # 检查第一次插入后和重复插入后的总数均为1；最后commit。
    # 可用：("同一条名言", "作者甲", "练习")，不联网。
    init_db(conn)
    conn.execute(
        "INSERT OR IGNORE INTO quotes(text, author, tags) VALUES (?, ?, ?)",
        ("同一条名言", "作者甲", "练习"),
    )
    actual = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
    expected = 1
    assert actual == expected, f"实际：{actual}\n期望：{expected}"
    conn.execute(
        "INSERT OR IGNORE INTO quotes(text, author, tags) VALUES (?, ?, ?)",
        ("同一条名言", "作者甲", "练习"),
    )
    actual2 = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
    expected2 = 1
    assert actual2 == expected2, f"实际：{actual2}\n期望：{expected2}"
    conn.commit()


def main():
    import sqlite3

    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="day31-homework-", dir=work) as folder:
        path = Path(folder) / "ledger.db"
        book = ContactBook(path)
        try:
            seed_ledger(book)
            check_months(book)
        finally:
            book.close()
        check_persistence(path)

        conn = sqlite3.connect(Path(folder) / "quotes.db")
        try:
            check_duplicates(conn)
        finally:
            conn.close()
    print("Day31三组检查通过，临时数据已清理")


if __name__ == "__main__":
    main()

"""Day33：只补两个写入函数和两句笔记；工具及样本全部在本目录。"""

import sqlite3

from tools33 import check_unknown_author, load_samples, prepare_database


def save_authors(conn, authors):
    # TODO 1：authors是作者字典列表，遍历并参数化写入authors表。
    # 字段：id、name。使用传入conn，不新建连接、不关闭连接。
    # 本函数只写入，不打印；不要求返回数据，提交由main统一完成。
    raise NotImplementedError("请完成TODO 1：写入作者")


def save_quotes(conn, quotes):
    # TODO 2：quotes是名言字典列表，遍历并参数化写入quotes表。
    # 字段：id、author_id、text；不要把author_id误写成每条名言自己的id。
    # 使用传入conn；提交、关闭和故意错误检查均由main负责。
    raise NotImplementedError("请完成TODO 2：写入名言")


def main():
    data = load_samples()
    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        save_authors(conn, data["authors"])
        save_quotes(conn, data["quotes"])
        conn.commit()

        author_rows = conn.execute("SELECT id, name FROM authors ORDER BY id").fetchall()
        expected_authors = [(1, "Alex"), (2, "Blair"), (3, "Casey")]
        assert author_rows == expected_authors, (author_rows, expected_authors)
        quote_rows = conn.execute(
            "SELECT id, author_id, text FROM quotes ORDER BY id"
        ).fetchall()
        expected_quotes = [
            (101, 1, "Keep learning."),
            (102, 1, "Practice helps."),
            (103, 2, "Ask clearly."),
        ]
        assert quote_rows == expected_quotes, (quote_rows, expected_quotes)
        print("作者与名言固定样本检查通过")

        before = list(quote_rows)
        message = check_unknown_author(conn)
        after = conn.execute("SELECT id, author_id, text FROM quotes ORDER BY id").fetchall()
        assert before == after, (before, after)
        print("不存在的作者被拒绝：", message)
        print("正常数据未受影响；Day33代码检查通过")
    finally:
        conn.close()


if __name__ == "__main__":
    main()


# 笔记1：quotes.id与quotes.author_id分别标识什么？Alex的两条名言为何可以共用author_id=1？
# 笔记2：如果只把Casey的id=3写进名言，却没有authors表中对应的行，为什么会失败？

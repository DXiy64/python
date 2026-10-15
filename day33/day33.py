"""Day33：两张表怎样表示一个作者对应多条名言；离线、内存数据库。"""

import sqlite3

from tools33 import check_unknown_author, load_samples, prepare_database


def main():
    print("① 样本字典、记录字典与行元组")
    data = load_samples()
    first_author = data["authors"][0]
    print("样本顶层键：", list(data))
    print("作者记录：", first_author)
    print("按字段取作者名：", first_author["name"])
    row = (1, "Alex")
    print("SQL行元组示例：", row, "；row[0]是ID，row[1]是名字")
    author_id, author_name = row
    print("解包：", author_id, author_name)

    conn = sqlite3.connect(":memory:")
    try:
        prepare_database(conn)
        print("② 主键标识这一行，外键引用另一张表的行")
        # 课堂只演示一个作者及其两条名言；作业自行遍历JSON中的全部记录。
        conn.execute("INSERT INTO authors(id, name) VALUES (?, ?)", (1, "Alex"))
        conn.execute(
            "INSERT INTO quotes(id, author_id, text) VALUES (?, ?, ?)",
            (201, 1, "One author can write many quotes."),
        )
        conn.execute(
            "INSERT INTO quotes(id, author_id, text) VALUES (?, ?, ?)",
            (202, 1, "The author ID stays the same."),
        )
        conn.commit()
        print("作者表：", conn.execute("SELECT id, name FROM authors ORDER BY id").fetchall())
        quote_rows = conn.execute("SELECT id, author_id FROM quotes ORDER BY id").fetchall()
        assert quote_rows == [(201, 1), (202, 1)]
        print("名言ID与作者ID：", quote_rows)
        print("201/202是两条名言的主键；两个1都引用authors.id=1，不是重复作者。")

        print("③ 先有被引用的作者，再写名言；非法引用明确失败")
        message = check_unknown_author(conn)
        assert "FOREIGN KEY" in message
        assert conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0] == 2
        print("作者999不存在，数据库拒绝：", message)

        print("④ 连接的创建者负责关闭，样本文件不会被修改")
        print("main创建conn并传给工具；工具不另建连接，也不关闭调用者的连接。")
    finally:
        conn.close()
    print("连接已关闭；内存库随之释放，没有生成正式数据库。")


if __name__ == "__main__":
    main()

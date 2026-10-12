import re
import sqlite3

from pathlib import Path
from datetime import datetime

HERE = Path(__file__).parent
OUT = HERE / "out"
DB = OUT / "ledger.db"




MONEY_RE = re.compile(r"\d+(\.\d{1,2})?")



class ContactBook:
    def __init__(self, path=DB):
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS ledger(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        money REAL NOT NULL,
        sort TEXT NOT NULL,
        note TEXT NOT NULL,
        time TEXT NOT NULL
        )""")

    def add(self, money, sort, note):
        if re.fullmatch(MONEY_RE, money) is None or float(money) <= 0:
            print("金额不合法")
            return
        else:
            self.conn.execute(
                "INSERT INTO ledger(money, sort, note, time) VALUES (?, ?, ?, ?)",
                (money, sort, note, datetime.now().strftime("%Y-%m-%d %H:%M")),
            )
        self.conn.commit()
        print("添加成功")

    def show(self):
        if self.conn.execute("SELECT * FROM ledger").fetchone() is None:
            print("账本为空")
        else:
            for row in self.conn.execute("SELECT * FROM ledger"):
                print(row)

    def month_report(self, month):
        count, total = self.conn.execute(
            "SELECT COUNT(*), SUM(money) FROM ledger WHERE time LIKE ?", (month + "%",)
        ).fetchone()
        # SUM 在空月返回 None；数据层返回结果，由界面负责显示。
        return count, total if total is not None else 0

    def delete(self, id):
        if (
            self.conn.execute("SELECT * FROM ledger WHERE id=?", (id,)).fetchone()
            is None
        ):
            print("该记录不存在")
        else:
            self.conn.execute("DELETE FROM ledger WHERE id=?", (id,))
            self.conn.commit()
            print("删除成功")

    def close(self):
        self.conn.close()


def show_menu():
    print("1. 添加记录")
    print("2. 查看记录")
    print("3. 删除记录")
    print("4. 退出")
    print("5. 月报")


def main():
    book = ContactBook()
    try:
        while True:
            show_menu()
            choice = input("请输入选项：")
            if choice == "1":
                money = input("请输入金额：")
                sort = input("请输入类别：")
                note = input("请输入备注：")
                book.add(money, sort, note)
            elif choice == "2":
                book.show()
            elif choice == "3":
                book.show()
                id = input("请输入要删除的记录ID：")
                book.delete(id)
            elif choice == "4":
                break
            elif choice == "5":
                month = input("请输入月份（YYYY-MM）：")
                count, total = book.month_report(month)
                print(f"{month} 共 {count} 笔，总金额 {total:.2f}")
            else:
                print("无效选项，请重新输入")
    finally:
        book.close()


if __name__ == "__main__":
    main()

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
            print("没有找到该条目")
        else:
            self.conn.execute("DELETE FROM ledger WHERE id=?", (id,))
            self.conn.commit()
            print("删除成功")

    def close(self):
        self.conn.close()

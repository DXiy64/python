"""Day33随课工具：只用标准库，不导入旧day，不在导入时写数据。"""

import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "samples" / "seed.json"


def load_samples():
    """读取随课JSON，返回字典；不创建连接或写数据库。"""
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


def prepare_database(conn):
    """给新连接启用外键、建立两张空表；调用者负责关闭连接。"""
    # 必须在开始写入前启用；每个连接都要设置，不能只设置一次就假定永久有效。
    conn.execute("PRAGMA foreign_keys = ON")
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    conn.executescript("""
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE quotes (
            id INTEGER PRIMARY KEY,
            author_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        );
    """)


def check_unknown_author(conn):
    """已提交正常种子数据后调用；确认不存在的作者999不能被引用。"""
    try:
        conn.execute(
            "INSERT INTO quotes(id, author_id, text) VALUES (?, ?, ?)",
            (999, 999, "Invalid reference"),
        )
    except sqlite3.IntegrityError as error:
        conn.rollback()  # 清理本次故意失败；不是让学员在这里再写一套事务工具。
        return str(error)
    else:
        conn.rollback()
        raise AssertionError("非法作者ID竟然入库，请检查外键是否启用")

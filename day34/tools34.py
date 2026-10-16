"""Day34随课建表与样本工具；只用标准库，导入时不读写数据库。"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "samples" / "seed.json"


def prepare_database(conn, include_quotes=True):
    """准备新连接的两张表与样本；False只放作者，连接由调用者关闭。"""
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))
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
    # 沿用普通循环写入；本课只需完成关联查询，不重写Day33作业。
    for author in data["authors"]:
        conn.execute(
            "INSERT INTO authors(id, name) VALUES (?, ?)",
            (author["id"], author["name"]),
        )
    if include_quotes:
        for quote in data["quotes"]:
            conn.execute(
                "INSERT INTO quotes(id, author_id, text) VALUES (?, ?, ?)",
                (quote["id"], quote["author_id"], quote["text"]),
            )
    conn.commit()

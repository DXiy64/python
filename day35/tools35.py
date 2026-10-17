"""Day35随课工具：新连接建表和放样本，不依赖旧作业。"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "samples" / "seed.json"


def prepare_database(conn, include_quotes=True):
    """只使用传入连接；False保留作者样本但不插入名言，调用者负责关闭。"""
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

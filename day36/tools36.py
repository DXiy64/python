"""Day36辅助代码：固定作者样本、复合唯一约束及只读快照。"""
import json
from pathlib import Path

SAMPLE = Path(__file__).resolve().parent / "samples" / "seed.json"


def prepare_database(conn):
    """新连接建表与放入作者；初始化提交完毕，连接由调用者关闭。"""
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))
    conn.execute("PRAGMA foreign_keys = ON")
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    conn.executescript("""
        CREATE TABLE authors(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE quotes(
            id INTEGER PRIMARY KEY,
            author_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY(author_id) REFERENCES authors(id),
            UNIQUE(author_id, text)
        );
    """)
    conn.executemany("INSERT INTO authors VALUES (?, ?)",
                     [(a["id"], a["name"]) for a in data["authors"]])
    conn.commit()
    return [(q["author_id"], q["text"]) for q in data["quotes"]]


def snapshot(conn):
    return conn.execute("SELECT author_id, text FROM quotes ORDER BY author_id, text").fetchall()

"""Day31：运行 python day31/day31.py，无需第三方依赖。"""

import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def sum_positive(numbers):
    total = 0
    for number in numbers:
        if number > 0:
            total += number
    return total


def broken_sum(numbers):
    total = 0
    for number in numbers:
        total += number
        return total  # 故意保留：第一轮就返回，检查应该抓住它。


def main():
    print("① 打印供人观察，assert自动比较实际与预期")
    actual = sum_positive([4, -2, 6])
    expected = 10
    assert actual == expected, f"预期 {expected}，实际 {actual}"
    assert sum_positive([]) == 0
    print("正常与空列表检查通过")

    print("② 检查要有能力抓到错误，而不是只显示通过")
    try:
        actual = broken_sum([4, 6])
        assert actual == 10, f"预期10，实际{actual}"
    except AssertionError as error:
        # 本节有意接住错误，让后续演示能继续；正式验收不要吞掉失败。
        print("检查捕获故意错误：", error)

    print("③ 准备 → 调用 → 比较 → 清理")
    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="day31-demo-", dir=work) as folder:
        path = Path(folder) / "sample.db"
        conn = sqlite3.connect(path)
        try:
            conn.execute("CREATE TABLE sample(value INTEGER)")
            conn.execute("INSERT INTO sample VALUES (?)", (4,))
            conn.commit()
        finally:
            conn.close()

        # 真正重开连接；查询旧连接不能证明保存成功。
        conn = sqlite3.connect(path)
        try:
            actual = conn.execute("SELECT SUM(value) FROM sample").fetchone()[0]
            assert actual == 4, f"重开后预期4，实际{actual}"
            print("跨连接持久化检查通过")
        finally:
            conn.close()
    print("临时目录已清理；没有操作真实账本")

    print("④ 作业：为已有账本写检查，详细要求见homework31.md")


if __name__ == "__main__":
    main()

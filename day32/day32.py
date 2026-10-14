"""Day32：运行本文件只使用本地样本，不访问网站、不写数据库。"""

import sys
from decimal import Decimal
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from day30.daily30 import parse


def fetch_html(url):
    """真实请求写法，今天的main不调用它。"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def main():
    print("① HTTP成功不等于解析成功；缺数据要明确失败")
    html = '<div class="quote"><span class="text">Example</span><small class="author">Alex</small></div>'
    rows = parse(html)
    assert rows == [("Example", "Alex", "")]
    print("本地正常HTML：", rows)

    for label, html in [
        ("空页面", "<html><body>Nothing</body></html>"),
        ("缺作者", '<div class="quote"><span class="text">Example</span></div>'),
    ]:
        try:
            parse(html)
        except ValueError as error:
            print(label, "明确失败：", error)
        else:
            raise AssertionError("坏样本竟然成功，需要检查解析规则")

    print("② raise产生错误，except处理已知错误")
    try:
        # 模拟等待过久；不必真的断网或等待十秒。
        raise requests.Timeout("本地模拟超时")
    except requests.RequestException as error:
        print("抓取失败：", error)
    print("timeout限制连接/读取等待，并非整个任务严格十秒结束。")

    print("③ 去重键决定哪些记录被视为同一笔")
    samples = [("Same quote", "Alex"), ("Same quote", "Blair")]
    text_keys = {text for text, author in samples}
    pair_keys = set(samples)
    assert len(text_keys) == 1
    assert len(pair_keys) == 2
    print("只用正文当键：", len(text_keys), "条；正文+作者：", len(pair_keys), "条")
    print("没有脱离需求的最佳键，需先说明是否保留不同作者的相同正文。")

    print("④ 金额表示：显示两位不等于精确存储")
    print("float：", 0.1 + 0.2)
    print("整数分：", 10 + 20, "分")
    print("从字符串构造Decimal：", Decimal("0.10") + Decimal("0.20"))
    print("本课只认识取舍，不迁移Day30数据库，也不增加记账功能。")


if __name__ == "__main__":
    main()

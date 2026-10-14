"""Day32：补两个错误处理函数，使用给定本地样本验收。"""

import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from day30.daily30 import parse

NORMAL_HTML = '<div class="quote"><span class="text">Example</span><small class="author">Alex</small></div>'
EMPTY_HTML = "<html><body>No quotes</body></html>"
MISSING_AUTHOR_HTML = '<div class="quote"><span class="text">Example</span></div>'


def parse_result(html):
    # TODO 1：调用已有parse(html)，不重写BeautifulSoup逻辑。
    # 成功返回(True, rows)；捕获ValueError后返回(False, str(error))。
    # 不打印，不把失败变成(True, [])。
    raise NotImplementedError("请完成TODO 1")


def fetch_result(fetcher):
    # TODO 2：fetcher是传入的函数，用fetcher()调用并取得HTML。
    # 抓取成功后交给parse_result，返回它的结果。
    # 捕获requests.RequestException，返回(False, str(error))。
    # 不创建目录、连接数据库，也不要重新调用main。
    raise NotImplementedError("请完成TODO 2")


def local_success():
    return NORMAL_HTML


def local_timeout():
    raise requests.Timeout("模拟超时")


def local_http_error():
    raise requests.HTTPError("模拟HTTP 503")


def main():
    ok, data = parse_result(NORMAL_HTML)
    assert ok is True and data == [("Example", "Alex", "")], (ok, data)
    for html in [EMPTY_HTML, MISSING_AUTHOR_HTML]:
        ok, message = parse_result(html)
        assert ok is False and isinstance(message, str) and message, (ok, message)
    print("TODO 1：正常、空页面、缺作者检查通过")

    ok, data = fetch_result(local_success)
    assert ok is True and data == [("Example", "Alex", "")], (ok, data)
    for fetcher in [local_timeout, local_http_error]:
        ok, message = fetch_result(fetcher)
        assert ok is False and isinstance(message, str) and message, (ok, message)
    print("TODO 2：成功、超时、HTTP错误检查通过")


if __name__ == "__main__":
    main()


# 笔记：写两句设计说明即可，不额外做新项目。
# 1. 如果同一正文对应不同作者，text当唯一键会保留几笔？你的业务会选什么键，为什么？
# 2. 固定只支持两位小数的金额，整数分有什么好处？输入小数位超过两位时要明确什么规则？

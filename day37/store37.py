"""学员任务：存取SQL集中在这里，目标函数保留待实现。"""


def save_quotes(conn, rows):
    """rows为[(author_id, text), ...]；一批一事务，返回本次新增数。

    入口无待提交事务；同作者同正文跳过，外键错误整体回滚并向外抛出。
    可查阅自己Day36的save_batch，再把相同职责整理到这里。
    """
    raise NotImplementedError("TODO 1：批量保存名言，不打印，不关闭连接")


def list_quotes(conn, author_id):
    """返回指定作者的[(author_id, text), ...]，按正文升序。

    参数化WHERE；不存在的作者或没有名言的作者返回[]。
    只查询，不修改数据，不打印，不关闭连接。
    """
    raise NotImplementedError("TODO 2：查询指定作者的名言，返回列表")

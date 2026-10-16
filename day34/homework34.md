# Day34：INNER JOIN关联名言与作者

主要目标：根据Day33的作者关系，用一条关联查询同时拿到正文与作者名。约一至两次学习，每次两小时，可跨日。本课不加入LEFT JOIN、GROUP BY、索引、DAO、子查询或新菜单。

## 随课文件与运行

```text
day34/
├─ day34.py           四节课堂演示
├─ homework34.py      一个查询TODO和一句关系说明
├─ homework34.md      本任务书
├─ tools34.py         完整建表、样本读取及入库工具
└─ samples/seed.json  3位作者、3条名言的固定样本
```

仅使用标准库sqlite3、json、pathlib，无第三方依赖。不导入旧day；工具与样本都在当天目录。项目根目录PowerShell：

```powershell
.\.venv\Scripts\python.exe day34\day34.py
.\.venv\Scripts\python.exe day34\homework34.py
```

工具以自身文件位置定位JSON；main创建内存连接并最终关闭，不产生正式.db或报告，不改写样本。骨架首次运行抛NotImplementedError，是待完成状态。先运行讲义，再做作业。

## 前置和类型

Day33已验收一对多、主键与外键；你已问过ORDER BY、连接责任和错误消息，本课继续使用这些概念。

| 表达式 | 类型/含义 |
| --- | --- |
| `conn` | main创建的SQLite连接，传给查询函数 |
| `quotes.id` | 名言本身的主键，如101 |
| `quotes.author_id` | 名言的作者ID，如1 |
| `authors.id` | 作者的主键，如1 |
| `authors.name` | 对应作者名字，如Alex |
| `fetchall()` | 行元组列表，哪怕只有一行也仍是列表 |

这里的`表名.字段名`是SQL中指定字段来源，不是Python字典取值或对象属性访问。两张表都有id时，要说明用哪一张表的id。

## 看懂课堂查询

课堂查询返回名言ID和作者名；作业在此基础上增加正文这一列。SQL各部分的职责：

| 部分 | 作用 |
| --- | --- |
| SELECT | 选择返回哪些列，顺序决定元组内部的先后 |
| FROM quotes AS q | 从名言表开始，q是该表在这条SQL中的别名 |
| INNER JOIN authors AS a | 关联作者表，a是作者表别名 |
| ON q.author_id = a.id | 用名言的作者ID匹配作者主键 |
| ORDER BY q.id | 按名言ID升序排列结果行 |

`AS`取别名只是让这条SQL简短，不会重命名数据库里的表。名言101/102的author_id都为1，因此各自匹配作者1，得到两行Alex；名言主键101本来就不需要等于作者主键1。

INNER JOIN只返回满足ON条件的配对结果。没有名言的Casey仍在作者表中，但不出现在本次名言关联结果里；查询没有删除任何作者。如果名言表为空，结果是空列表，不需要人为抛异常。保留零名言作者的统计留给Day35。

## 学员任务与明确预期

只实现`list_quotes(conn)`：执行一条INNER JOIN查询，返回按名言id升序排列的三元组列表，列顺序为**名言id、正文、作者名**。返回数据，不在该函数中打印；使用传入连接，不重新创建或关闭它。

正常固定预期：

```python
[
    (101, "Keep learning.", "Alex"),
    (102, "Practice helps.", "Alex"),
    (103, "Ask clearly.", "Blair"),
]
```

无匹配场景由main另建一个连接，调用`prepare_database(empty_conn, include_quotes=False)`：False表示只放作者、不放名言。表仍然存在，作者仍是3位，查询应返回`[]`。这是已给定的辅助参数，不要求你再设计建表或入库功能。

调用流程：`main → 创建conn → prepare_database → list_quotes → 比较结果 → close`。第二个场景重复相同流程但使用另一份独立内存库，不能在查询函数里偷换连接或硬编码expected。

通过条件：正常结果的值、列顺序和行顺序正确；空场景为[]；不修改数据或样本；代码末尾一句笔记能解释ON比较的字段。main预置两组断言与连接清理，不重写测试、不增加口头题。没有要求额外写抓取、筛选接口或手工复制每个作者名。

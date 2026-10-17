# Day35：LEFT JOIN与零记录统计

主要目标：统计每位作者的名言数，同时保留没有名言的作者。约一至两次学习，每次两小时，可跨日。只实现一条查询和一句笔记，不增加新菜单、类、抓取器、子查询、窗口函数或索引。

## 文件与运行

```text
day35/
├─ day35.py           四节课堂演示
├─ homework35.py      一个查询TODO和一句笔记
├─ homework35.md      本任务书
├─ tools35.py         完整建表、读取样本和入库辅助工具
└─ samples/seed.json  随课固定输入
```

仅用Python标准库，无需安装第三方库，不导入旧day。根目录PowerShell：

```powershell
.\.venv\Scripts\python.exe day35\day35.py
.\.venv\Scripts\python.exe day35\homework35.py
```

样本按tools35.py所在位置读取。两次连接均为独立内存数据库，由main负责关闭；不修改JSON、不创建正式.db或报告。未完成骨架首次运行报NotImplementedError，属于待完成状态。

## 前置与本课变化

Day34的INNER JOIN只返回匹配到的名言，Casey没有名言，因此不出现在关联结果里。本课从authors表出发，用LEFT JOIN保留左表的全部作者。

| 位置/表达式 | 含义 |
| --- | --- |
| `FROM authors AS a` | 左表是作者，a是作者表别名 |
| `LEFT JOIN quotes AS q` | 寻找对应名言，但保留没有匹配的左表作者 |
| `ON q.author_id = a.id` | 关系仍是名言作者外键对应作者主键 |
| `a.id, a.name` | 作者字段，不会因该作者没有名言就变空 |
| `q.id` | 匹配名言的ID，无匹配时是SQL NULL |
| `None` | sqlite3把SQL NULL取回Python时使用的值 |
| `fetchall()` | 行元组列表，SELECT列顺序决定元组顺序 |

例如Casey的未分组关联结果是`(3, "Casey", None)`。这不是数据库中新建了一条名言，而是LEFT JOIN为了保留作者而产生的查询结果。NULL表示没有对应值，0是一个具体数字；两者不能混为一谈。

## GROUP BY与COUNT就近复习

Day25已接触聚合，本课只复习按作者分组：`GROUP BY a.id, a.name`把同一作者的关联结果归为一组，让COUNT为每位作者各计算一个数量。作者ID与名字一同写出，避免只按姓名把同名作者混在一起。

| 统计方式 | 实际数什么 | Casey结果 |
| --- | --- | --- |
| `COUNT(*)` | 该组关联结果有几行，包括右表为空的占位行 | 1 |
| `COUNT(q.id)` | 该组有多少个非NULL的名言ID | 0 |

名言主键不为NULL，所以COUNT(q.id)可以数匹配到的真实名言。0是统计得到的数量，不是把某条名言的NULL ID改成了0。课堂返回四列用于比较；作业只返回作者ID、作者名、名言条数三列。

## 学员任务与明确预期

只实现`author_report(conn)`：用一条LEFT JOIN分组查询，返回每位作者的名言数，按作者id升序。连接来自main，不另建、不关闭；返回数据，不打印或修改表。正常结果必须为：

```python
[(1, "Alex", 2), (2, "Blair", 1), (3, "Casey", 0)]
```

`include_quotes=False`场景仍有三位作者，但名言表为空，必须返回：

```python
[(1, "Alex", 0), (2, "Blair", 0), (3, "Casey", 0)]
```

这与Day34的空结果不同：这次要求保留左表作者，所以不能直接返回[]。main已提供两组预期、数据未改检查和关闭操作，不需要重写测试或手动补Casey。

在文件末尾写一句自己的解释：Casey的两种COUNT为什么不同，并区分NULL与0。通过标准就是两组结果、原数据/连接可继续使用，以及这句说明；没有额外口头题。需要保留作者时，应把authors放左边，不能只把Day34的JOIN关键字替换掉却不检查左右表。

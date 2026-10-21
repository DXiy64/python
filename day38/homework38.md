# Day38：用查询计划判断索引是否有用

本页是唯一阅读入口。今天的主要目标：对同一个正文过滤查询，检查已有索引，观察新增索引前后的查询计划，并确认结果不变。约两小时，可跨日；核心只有一个索引函数和三句笔记，无额外挑战。

## 1．先运行，再沿调用链阅读

只用Python标准库sqlite3，无第三方依赖，无旧day导入，无外部必读材料。所有样本在tools38.py里生成，数据库只在内存中，没有输入文件或落盘输出。从项目根目录运行：

```powershell
.\.venv\Scripts\python.exe day38/day38.py
```

执行顺序：加载tools38函数定义 → main创建连接 → prepare_database建表并写入样本 → 检查已有索引 → 查询并读取计划 → 建演示索引 → 再读计划并核对结果 → finally关闭连接。导入模块不会自动运行main。

代码按这个顺序阅读：day38.py的main，然后就近查看同目录tools38.py。必要辅助函数全部提供；作业不调用讲义的main，会新建自己的内存库。

## 2．数据与对象先分清

沿用Day33–37的作者与名言两表。作者有Alex(1)、Blair(2)。名言共1003条：

```python
[(1, "Keep learning."), (2, "Keep learning."), (1, "Practice helps.")]
# 另加作者1的1000条正文：Sample 0000 到 Sample 0999
```

UNIQUE(author_id,text)仍然要求同作者同正文不重复。

| 对象/函数 | 类型或输入 | 返回/职责 |
| --- | --- | --- |
| conn | sqlite3.Connection | main创建和关闭的连接 |
| conn.execute(...) | SQL字符串与参数 | sqlite3.Cursor游标 |
| cursor.fetchall() | 无参数 | 所有结果行组成的列表 |
| find_quotes(conn,text) | 连接、正文字符串 | [(author_id,text), ...]，按作者ID升序 |
| query_plan(conn,text) | 同上 | [(整数,整数,整数,描述字符串), ...] |
| index_columns(conn) | 连接 | [(索引名,[列名,...]), ...] |

查询仍用Day37的参数化和fetchall；计划读取也返回行元组列表。它们不是同一种内容：find_quotes返回业务数据，query_plan返回数据库准备怎样查的说明。

## 3．索引解决什么问题

索引像按某列值整理的目录，帮助数据库定位记录；它不会改变你要返回的数据。比如讲义执行：

```sql
CREATE INDEX demo_quotes_text ON quotes(text);
```

语法：CREATE INDEX 索引名 ON 表名(列名)。这创建普通索引，允许不同作者拥有相同正文；不需要UNIQUE INDEX。

作业需要重复运行创建操作。SQLite提供CREATE INDEX IF NOT EXISTS：同名索引已存在时跳过创建。注意它只按名字判断，并不会替你核对一个已有索引的定义；本课用全新内存库，定义通过index_columns核对。

已有UNIQUE(author_id,text)通常会自动产生一个索引。它以author_id为首列，能支持相应作者条件；不能因此断定只按text查也能高效定位。先看实际计划，避免再建一个重复的author_id索引。本课选择的是正文精确匹配：

```sql
SELECT author_id, text FROM quotes WHERE text = ? ORDER BY author_id
```

## 4．怎样读计划

在原SELECT前面加EXPLAIN QUERY PLAN，传入的参数仍然是(text,)。它描述策略，不返回名言，也不是计时器。

tools38.query_plan提供完整读取方式，main打印返回列表。本课只先看每个元组的最后一项描述，不要求背前三个整数。

- SCAN：扫描全部表记录或全部某个索引的条目；看到USING INDEX也不能自动当作按条件定位。
- SEARCH：利用条件只访问部分记录。结合索引名称、text=?判断是否用于正文定位。
- USING COVERING INDEX：所需列可以直接从该索引取得，本课只需认识这个提示。
- USE TEMP B-TREE FOR ORDER BY：可能为排序使用临时结构；不等于正文索引创建失败。

本环境固定样本预期：之前有SCAN，之后有使用demo_quotes_text的SEARCH及text=?。版本、统计信息和样本变化都可能影响计划；不要求逐字匹配整段描述，也不把SEARCH当作任意查询必胜的结论。

终端依次打印①已有索引、②原计划、③新增索引、④新计划、⑤未改变的两条结果，最后显示讲义通过。观察到的计划变化应以你实际输出为准。

## 5．你要完成什么

只修改homework38.py中的ensure_text_index(conn)和末尾笔记，辅助函数与已有断言保持不变。创建名为idx_quotes_text的quotes(text)普通索引，允许重复调用，不再为author_id建索引。函数不打印、不关闭连接、不修改作者或名言；不要求返回值。

```powershell
.\.venv\Scripts\python.exe day38/homework38.py
```

骨架目前会明确报NotImplementedError，表示待完成。实现后输出①至⑤与检查通过提示。原题通过标准：

1. 原有复合唯一索引保留；新增索引名和列正确；调用两次不报错且不新增重复索引。
2. Keep learning.返回[(1,"Keep learning."),(2,"Keep learning.")]，Practice helps.返回[(1,"Practice helps.")]，Missing返回[]。
3. 名言数据及total_changes不变；连接由main关闭，目标函数不打印。
4. 三句笔记：贴出实际建前/建后计划的关键描述并解释；说明为何要检查正文条件而不重复建作者索引；说明写入需维护索引、索引需要额外存储。

索引可能改善特定读取，但插入、删除、修改相关列时要维护索引。本课不测加速倍数，小样本耗时不能证明普遍收益。10分钟闭卷回忆“连接与游标各负责什么”可作为复习，开发阶段允许查本页和代码。

可选查阅：[SQLite查询计划说明](https://www.sqlite.org/eqp.html)、[SQLite索引与查询规划](https://www.sqlite.org/queryplanner.html)，无需读完。

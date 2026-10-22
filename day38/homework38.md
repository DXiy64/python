# Day38：用查询计划判断索引是否有用

本页是唯一阅读入口。今天只研究一件事：给正文建索引后，数据库查找名言的方式有没有变化。先顺着下方步骤理解演示，再做末尾作业。约两小时，可跨日；核心只有一个索引函数和三句笔记，无额外挑战。

## 1．先认清你运行的文件

只用Python标准库sqlite3，无第三方依赖或外部必读材料。演示所需全部函数和样本都在day38.py内，不需要打开tools38.py或旧作业。数据库只在内存中，没有输入文件或落盘输出。从项目根目录运行：

```powershell
.\.venv\Scripts\python.exe day38/day38.py
```

Python先导入sqlite3，设置QUERY字符串，再加载各个def；此时没有建表或写数据。读到文件末尾的main()调用，才进入main函数。讲义与作业是两次独立启动，运行演示不会替你完成作业。

下面直接按main实际执行顺序讲。day38.py里的函数全文用于对照；理解本课不用在多个文件之间找函数。

## 2．main创建连接，准备函数把样本存进去

```python
conn = sqlite3.connect(":memory:")
prepare_database(conn)
```

第一行创建空内存数据库。第二行传入同一个conn，进入prepare_database：开启外键检查 → 创建authors、quotes → 写入作者和名言 → 正常离开with conn并提交。然后回到main，继续下一行。

注意与Day36的区别：本课prepare_database已经写入名言，且没有return，返回None；不能把它当成待保存的rows列表。准备后的状态如下。

沿用Day33–37的作者与名言两表。作者有Alex(1)、Blair(2)。名言共1003条：

```python
[(1, "Keep learning."), (2, "Keep learning."), (1, "Practice helps.")]
# 另加作者1的1000条正文：Sample 0000 到 Sample 0999
```

UNIQUE(author_id,text)仍然要求同作者同正文不重复。

| 对象/函数 | 类型或输入 | 返回/职责 |
| --- | --- | --- |
| conn | sqlite3.Connection | main创建和关闭的连接 |
| prepare_database(conn) | 连接 | 返回None；已写入2位作者和1003条名言 |
| conn.execute(...) | SQL字符串与参数 | sqlite3.Cursor游标 |
| cursor.fetchall() | 无参数 | 所有结果行组成的列表 |
| find_quotes(conn,text) | 连接、正文字符串 | [(author_id,text), ...]，按作者ID升序 |
| query_plan(conn,text) | 同上 | [(整数,整数,整数,描述字符串), ...] |
| index_columns(conn) | 连接 | [(索引名,[列名,...]), ...] |

查询仍用Day37的参数化和fetchall；计划读取也返回行元组列表。它们不是同一种内容：find_quotes返回业务数据，query_plan返回数据库准备怎样查的说明。

## 3．回到main，先看已有索引并查询一次

main先打印index_columns(conn)的结果。这个辅助函数已完整放在day38.py里；它读取quotes的索引名和各索引包含的列，不修改数据。此时预期得到：

```python
[("sqlite_autoindex_quotes_1", ["author_id", "text"])]
```

索引名由SQLite生成，重点看两列的顺序：先author_id，再text。其内部读取语法是辅助展示内容，本课不要求你实现；需要看代码时，函数全文就在同一份讲义里。

随后main调用find_quotes(conn, "Keep learning.")。函数的完整查询逻辑是：

```python
QUERY = "SELECT author_id, text FROM quotes WHERE text = ? ORDER BY author_id"

def find_quotes(conn, text):
    return conn.execute(QUERY, (text,)).fetchall()
```

text收到字符串"Keep learning."；(text,)把它交给SQL的问号。execute执行查询并返回游标，fetchall从游标取出所有结果行，return把列表交回main，保存为before：

```python
[(1, "Keep learning."), (2, "Keep learning.")]
```

这一步只查询，表内仍有1003条名言。main随后用assert核对结果，保存before是为了稍后对比，并未重新写入数据库。

## 4．先看怎么查，再建索引

main接下来调用query_plan(conn, "Keep learning.")，打印建索引前的策略。完整函数只有：

```python
def query_plan(conn, text):
    return conn.execute("EXPLAIN QUERY PLAN " + QUERY, (text,)).fetchall()
```

QUERY仍是上面的SELECT字符串。加号把两个字符串拼成EXPLAIN QUERY PLAN SELECT ...。它让数据库说明准备怎么执行这条查询，返回计划行列表，不返回那两条名言。如何读这个列表，见紧接着的第5节。

读取原计划后，main才执行下面的CREATE INDEX语句。

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

## 5．回到main，再看计划并核对结果

在原SELECT前面加EXPLAIN QUERY PLAN，传入的参数仍然是(text,)。它描述策略，不返回名言，也不是计时器。

query_plan的完整逻辑已在上节给出，main打印它返回的列表。本课只先看每个元组的最后一项描述，不要求背前三个整数。典型的建前/建后结果如下，数字可能不同：

```python
# 建前：即使读的是已有索引，也在扫描全部条目
[(3, 0, 216, "SCAN quotes USING COVERING INDEX sqlite_autoindex_quotes_1")]

# 建后：用新索引按正文条件定位，排序可能还有额外步骤
[(4, 0, 63, "SEARCH quotes USING INDEX demo_quotes_text (text=?)"),
 (16, 0, 0, "USE TEMP B-TREE FOR ORDER BY")]
```

- SCAN：扫描全部表记录或全部某个索引的条目；看到USING INDEX也不能自动当作按条件定位。
- SEARCH：利用条件只访问部分记录。结合索引名称、text=?判断是否用于正文定位。
- USING COVERING INDEX：所需列可以直接从该索引取得，本课只需认识这个提示。
- USE TEMP B-TREE FOR ORDER BY：可能为排序使用临时结构；不等于正文索引创建失败。

本环境固定样本预期：之前有SCAN，之后有使用demo_quotes_text的SEARCH及text=?。版本、统计信息和样本变化都可能影响计划；不要求逐字匹配整段描述，也不把SEARCH当作任意查询必胜的结论。

终端依次打印①已有索引、②原计划、③新增索引、④新计划、⑤未改变的两条结果，最后显示讲义通过。观察到的计划变化应以你实际输出为准。

最后，main再次调用find_quotes，assert它与before相同，并检查查询Missing得到[]。也就是说，新增索引改变了这份样本的查找策略，名言内容和查询结果不变。随后finally调用conn.close()，内存数据库释放。

你现在应该能在本页串起整个过程：**创建空库 → 写入样本 → 查结果和原计划 → 建正文索引 → 查新计划和结果 → 比较 → 关闭。**

## 6．看懂演示后，你要完成什么

作业运行homework38.py，会重新创建内存库。它保留tools38作为辅助模块，但不要求你追进去阅读；准备后的表状态、各辅助函数的输入输出和查询逻辑都与上文相同。执行顺序是：main创建连接 → 准备同样的样本 → 打印原计划 → 调用你实现的ensure_text_index两次 → 核对索引及新计划 → 检查查询和数据不变 → finally关闭。你只需要按下面的接口约定实现目标。

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

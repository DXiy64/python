# Day36：事务与唯一约束

## 从这里顺着学：整节课如何运行

本文件是唯一阅读入口，配合运行day36.py即可。今天不需要打开外部教材，也不需要先读tools36.py。讲义的辅助函数现已完整写在day36.py内，下面按运行顺序讲清楚。后半部分保留原任务要求，难度和通过标准不变。

### 第一步：运行的是哪个文件

在项目根目录运行：

```powershell
.\.venv\Scripts\python.exe day36/day36.py
```

这是看演示。它不会运行你的homework36.py，也不会替你完成作业。

Python先执行import、设置SAMPLE，然后依次读到几个def。读到def只是定义函数，不执行函数体。直到文件末尾：

```python
if __name__ == "__main__":
    main()
```

直接运行这个文件时，条件成立，调用main，跳到main函数内部执行。

### 第二步：main创建一个空的内存数据库

```python
conn = sqlite3.connect(":memory:")
```

此时数据库里没有任何表。conn是操作这一个数据库的连接。

接着执行：

```python
rows = prepare_database(conn)
```

这行先调用右边函数，等它返回后，再把返回值交给左边的rows。此时跳进prepare_database。

### 第三步：prepare_database准备什么，返回什么

它按顺序做五件事，讲义内可以直接看到完整代码：

1. 读取当天samples/seed.json，得到名为data的字典。
2. 开启外键检查，创建authors和quotes两张表。
3. 从data里取作者，写入authors：1号Alex、2号Blair、3号Casey。
4. commit，提交这三位作者。
5. 从data里取出名言的author_id和text，组成新列表并return。

原始data包含两组字典，大致是：

```python
{
    "authors": [{"id": 1, "name": "Alex"}, ...],
    "quotes": [{"id": 101, "author_id": 1, "text": "Keep learning."}, ...],
}
```

其中return这一行进行了转换：

```python
return [(q["author_id"], q["text"]) for q in data["quotes"]]
```

意思是：依次读取每个名言字典，只拿作者ID和正文，组成二元组，再把这些元组放进一个列表。最终main收到的rows完整值是：

```python
[
    (1, "Keep learning."),
    (1, "Practice helps."),
    (2, "Ask clearly."),
]
```

**这里的分界最关键：data是辅助函数内部的字典，rows是它返回的新列表。** rows[0]得到第一笔(1, "Keep learning.")；rows["authors"]会报错，因为列表不能用这个字符串作索引。

此时数据库状态：authors有3人；quotes有0条。返回待保存的列表，并不等于已把列表写进quotes。

### 第四步：回到main，完成第一次写入

```python
with conn:
    conn.executemany("INSERT INTO quotes(author_id, text) VALUES (?, ?)", rows)
```

executemany依次拿rows里的每个二元组填入两个问号：第一个值给author_id，第二个值给text。第一笔就是把1和Keep learning.写入对应两列。

quotes还有id列，但这条SQL明确只提供author_id和text；id由SQLite在省略INTEGER PRIMARY KEY值时分配。因此这里用两个问号即可。

三笔没有错误，正常离开with，提交。名言表由0条变成3条。with不关闭连接，后面的演示仍使用同一个conn。

snapshot(conn)只是SELECT查询，把当前表内数据以列表返回。assert检查它是否符合预期；print负责显示。查询不会再次插入数据。

### 第五步：四段演示连续使用同一个数据库

| 演示 | 做什么 | 结束后quotes条数 |
| --- | --- | --- |
| ① 正常提交 | 写入三笔，正常离开with并提交 | 3 |
| ② 普通INSERT重复数据 | 同作者同正文违反UNIQUE，错误向外离开with，回滚；外层except显示预期错误 | 3 |
| ③ INSERT OR IGNORE重跑 | 三笔都重复，跳过，本次新增0 | 3 |
| ④ 整批失败 | 先插入合法临时记录，再插入不存在的999号作者；外键错误使这次事务整体回滚 | 3 |

②的异常在with外被接住，所以讲义能继续运行③。④回滚的是④这一批，①已提交的三笔仍保留。OR IGNORE不会跳过外键错误。

③的before是执行前conn.total_changes的值。初始化作者累计3次修改，①再新增3条后累计为6；③重跑前后都是6，所以6−6=0。它是累计计数，发生回滚也不会扣回，因此④用snapshot比较真实数据有没有恢复。

最后进入finally执行conn.close()，关闭连接；这个内存数据库随之释放。正常运行会显示准备阶段、①至④的结果，最后显示“Day36讲义全部通过；连接由main关闭”。

### 第六步：看懂演示后，再写作业

运行homework36.py是另一次独立启动：它重新创建内存数据库，不继承讲义里的三条记录。作业的tools36提供上述同样的准备/查询接口，可以先按这里说明使用，不必来回跳文件。

作业的执行路线为：

```text
文件末尾main()
  → 创建空内存库
  → prepare_database(conn)：建表、写作者，返回三笔待保存名言
  → save_batch(conn, rows)：你负责实现
  → main用assert比较函数返回值及表内数据
  → 继续测试重复、不同作者、失败回滚、空列表
  → finally关闭连接
```

你只实现save_batch：记录执行前累计修改数 → 同一事务里批量保存传入的名言 → 成功退出后返回本次新增数。失败时异常向外传播，main负责接住预期错误。不要把初始化作者、读取JSON的步骤复制进来。

本次你已写好的事务笔记可保留。代码只改save_batch，main、工具和样本都不用改。下方是原题细则，需要核对时再看。

---

主要目标：让一批数据库写入成为“全部提交或全部回滚”的整体。约一至两次学习，每次约两小时，可跨日。核心只写一个函数和一句笔记，不加抓取、DAO、并发或复杂隔离级别。

## 前置、类型与调用链

Day33已学外键，Day34–35已学关联查询。本课继续作者—名言场景，辅助工具与JSON全部在day36，不导入旧作业。只用标准库；内存数据库，不落正式数据。

| 名称 | 类型与职责 |
| --- | --- |
| conn | sqlite3.Connection，main创建并关闭 |
| rows | 列表，例如[(1, "Keep learning."), (2, "Ask clearly.")] |
| 单笔row | 二元组：(作者ID整数, 正文字符串)，顺序对应INSERT列 |
| save_batch返回值 | int，成功提交的本次新增条数；失败抛出异常 |
| snapshot返回值 | 按作者ID与正文排序的行元组列表，用于核对真实数据 |

调用链：main → prepare_database建表并提交初始化 → save_batch写入并提交/回滚 → main断言 → main关闭。入口约定没有未提交事务；不处理嵌套事务。

## 1. 什么是事务

同一批两条记录，第一条合法、第二条作者不存在。如果逐条commit，第二条失败时第一条已经保存，产生“半批成功”。本课要求它们一起成功或一起失败；失败后旧数据不变。

在本课sqlite3默认连接模式下：

```python
try:
    with conn:
        # 多次INSERT，放在同一个with里
        ...
except sqlite3.IntegrityError:
    # 异常先离开with，触发回滚，然后在这里处理
    ...
```

with conn正常结束提交；异常向外离开时回滚。它不负责关闭连接，也不是嵌套事务工具。不要在内部吞掉错误后让代码正常离开with；本课函数不捕获错误，由main验证异常。

## 2. UNIQUE与去重边界

UNIQUE(author_id, text)规定“同作者同正文”重复；不同作者即使正文相同也允许。同一批初次保存3条，再次保存同样数据新增0条。

普通INSERT遇到重复会抛IntegrityError。本课在已约定样本类型下使用INSERT OR IGNORE跳过重复；它也可能忽略其他适用约束错误，不能用于替代通用输入校验。外键错误不会因OR IGNORE被跳过，仍抛异常。约束错误是数据库数据问题，不是请求超时等网络失败。

## 3. 本次新增数与失败后的存量

conn.total_changes是该连接累计修改数，不能直接当本次新增。成功路径可保存执行前的值，提交后计算差；失败时不返回新增数。回滚不会扣回total_changes，因此检查回滚要比较真实SELECT结果，而不是看累计计数。

## 4. 作业

完成homework36.py的save_batch及末尾笔记。使用一批一个事务、参数化SQL；不修改main的预期值，不改工具和种子。

通过标准：初次新增3；相同样本重跑新增0；不同作者同正文新增1；合法+非法作者两条组成的一批必须整体回滚并抛IntegrityError；空批次返回0；函数不打印或关闭连接。骨架已有检查，不必另写测试框架。

笔记解释：为何不能逐条commit，以及第二条外键失败时第一条如何处理。目标保留TODO，未实现时报NotImplementedError属于待完成。

## 运行

```powershell
python day36/day36.py
python day36/homework36.py
```

如已按SETUP建立根.venv，使用同一环境的解释器。讲义四节均可独立运行；samples/seed.json是输入，数据库为临时内存数据。今天无需安装依赖、连接网站或修改旧作业。

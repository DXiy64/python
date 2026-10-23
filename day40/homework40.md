# Day40：把离线入库、关联查询和CSV串起来

本页是唯一阅读入口。今天是整合课，主要目标是把已学函数按职责和顺序连接起来，不引入新库或新业务。约两次学习，每次约两小时，可跨日。你只完成一个流程函数和两句笔记，不凭记忆重写SQL、CSV或前面七课。

先读本页、运行day40.py，再做homework40.py。两个入口各自包含完整必要辅助函数，不导入旧作业，不要求跳tools文件或外部教材。标准库即可，输入样本在当天samples目录，输出默认在out目录。

## 1．先运行已经完整提供的起始演示

在项目根目录运行两次同一命令：

```powershell
.\.venv\Scripts\python.exe day40/day40.py
.\.venv\Scripts\python.exe day40/day40.py
```

第一次在尚无演示库时显示“本次新增3条；报告共3条”，第二次显示“本次新增0条；报告共3条”。文件数据库out/demo.db会保留记录；CSV out/demo.csv每次覆盖写出当前全部记录。不要删除数据库来伪造去重结果，也不要把正式数据库路径交给演示。

与先前内存库不同，本课用文件路径连接，关闭程序后数据仍存在。演示和作业默认使用不同的数据库及CSV文件，演示不会替你完成作业。

## 2．按演示main执行顺序理解

文件先导入标准库、设置ROOT、加载def，最后SystemExit(main())进入main。parse_args得到args.db和args.output，都是Path。main创建数据库父目录后，sqlite3.connect(args.db)打开已有库或创建新文件库。

接下来进入try，调用prepare_database(conn)。辅助函数全文就在同一个文件里，它依次：

1. 开启外键检查；
2. 用CREATE TABLE IF NOT EXISTS创建不存在的authors和quotes表；
3. 保留复合唯一约束UNIQUE(author_id,text)，确保正文索引存在；
4. 将三位固定作者Alex(1)、Blair(2)、Casey(3)用INSERT OR IGNORE写入并提交。

它不清空旧表，也不插入名言，返回None。IF NOT EXISTS只在对应对象不存在时创建，不能用来升级任意已有表结构；本课只使用新建的练习库或本课自己生成的库。

然后main调用save_quotes(conn, 固定三笔列表)。它沿用Day36的一批一事务和累计数差值：成功提交返回本次新增数，重复跳过，外键错误向外抛出并回滚这一批。每笔仍然是(作者ID,正文)二元组。

接着report_rows(conn)执行INNER JOIN：

```sql
SELECT a.id, a.name, q.text
FROM quotes AS q INNER JOIN authors AS a ON q.author_id=a.id
ORDER BY a.id, q.text
```

关联依据是名言的author_id引用作者id；结果三列顺序由SELECT决定，行顺序由ORDER BY决定。这次报告只包含有名言的作者，Casey不出现；不是忘记Day35的LEFT JOIN，而是本报告按名言列记录，不做零记录作者统计。

返回rows完整值是：

```python
[(1, "Alex", "Keep learning."),
 (1, "Alex", "Practice helps."),
 (2, "Blair", "Ask clearly.")]
```

main进入finally关闭自己创建的conn。rows已经是fetchall取出的Python列表，不依赖游标继续读取，所以连接关闭后仍可交给write_report写CSV。with负责关闭CSV文件；main最后打印本次新增数与报告总行数并返回0。

## 3．作业要把文件输入接到这些已提供函数上

作业的run_pipeline(source, db_path, output)接收三个Path。除了这一个目标函数，其余辅助函数、命令行选项和错误处理都已在homework40.py完整提供。

| 函数/变量 | 输入 | 返回或作用 |
| --- | --- | --- |
| load_rows(source) | JSON文件Path | [(author_id,text), ...]，未写数据库 |
| prepare_database(conn) | Connection | 返回None；初始化表、索引、作者，保留旧名言 |
| save_quotes(conn, rows) | 连接、二元组列表 | 本次新增数int；成功提交，失败回滚并抛出 |
| report_rows(conn) | 连接 | [(作者ID,作者名,正文), ...] |
| write_report(output, rows) | CSV路径、三元组列表 | 写表头及数据，返回None |
| run_pipeline的结果 | — | {"added":新增数, "rows":三元组列表} |

样本quotes.json包含quotes列表，每项是author_id/text字典。load_rows读取JSON字典，再转换成保存函数需要的二元组列表，不能把它与report_rows返回的三元组混用。

例如样本中的：

```json
{"author_id": 1, "text": "Keep learning."}
```

先变成(1,"Keep learning.")，保存后通过关联查询，才变成(1,"Alex","Keep learning.")。

## 4．目标函数按这条流程实现

在homework40.py里找到run_pipeline，替换它的NotImplementedError，其他辅助函数和main保持不变：

```text
load_rows读取source，接住返回列表
→ 创建db_path的父目录
→ 用db_path创建conn
→ try中初始化、保存样本并记录新增数、查询并接住关联结果
→ finally关闭自己创建的conn
→ 写CSV
→ 返回added和rows组成的字典
```

不在目标函数打印，不捕获并吞掉错误，不清空旧数据。加载样本放在连接之前；连接创建后用try/finally保证失败也关闭。若批量写入失败，异常离开流程，不能继续导出成功报告。CSV导出放在查询和关闭之后。

数据库提交与CSV写文件是两次独立操作：若数据库已经提交、随后CSV路径无法写入，数据库新增记录仍保留。已有main会显示失败并返回1；本课不要求实现数据库与文件的跨资源原子提交。正常导出会覆盖指定CSV，请使用练习路径。

末尾完成两句笔记：谁关闭连接、为什么关闭后rows仍可写文件；为什么重跑新增0但报告仍有3条，以及外键失败后旧名言怎样保留。

## 5．运行和原题通过标准

作业初始骨架在run_pipeline报NotImplementedError，表示待完成。写好后从项目根目录运行：

```powershell
.\.venv\Scripts\python.exe day40/homework40.py
.\.venv\Scripts\python.exe day40/homework40.py
```

默认使用samples/quotes.json、out/quotes.db、out/quotes.csv。新库首次新增3，再次新增0；两次报告都按作者ID和正文排序，内容是：

```csv
author_id,author,text
1,Alex,Keep learning.
1,Alex,Practice helps.
2,Blair,Ask clearly.
```

失败样本用同一个已成功写入的库运行，检查旧数据保留：

```powershell
.\.venv\Scripts\python.exe day40/homework40.py --source day40/samples/invalid_author.json --output day40/out/failed.csv
```

其中第一条合法、第二条999号作者非法，整批回滚。预期显示包含FOREIGN KEY的失败信息，退出1，不创建failed.csv；若这个报告原已存在，失败时保留原内容。旧库仍有原三条，没有留下New valid row。随后重新运行正常样本，仍新增0。

空样本要明确使用另一个新库：

```powershell
.\.venv\Scripts\python.exe day40/homework40.py --source day40/samples/empty.json --db day40/out/empty.db --output day40/out/empty.csv
```

新空库新增0，返回rows=[]，CSV仅表头。把空样本传给已有正常库则不删除旧数据，报告仍含已有记录。正常、重复、跨进程重开、非法作者回滚、空样本及连接关闭是本课验收范围；不追加联网或新框架要求。

阶段复习见[Day31–39分类复习](阶段复习.md)。这是已有知识与误区整理，不增加一组口头考试。Day40仍待你完成，阶段最终验收在本课作业通过后记录。

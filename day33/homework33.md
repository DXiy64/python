# Day33：用两张表表示作者与名言

本单元只学一个主要新难点：**一对多关系，以及主键/外键如何表示这种关系。** 预计两次学习，每次约两小时，可按实际进度调整。不在本课加入JOIN、索引、DAO、ORM、联网采集或新菜单。

## 文件与运行

```text
day33/
├─ day33.py            课堂演示，四节完整运行
├─ homework33.py       学员补两个TODO和两句笔记
├─ homework33.md       本任务书和前置解释
├─ tools33.py          已提供的建表、读样本、非法外键检查工具
└─ samples/seed.json   随课输入，只读
```

只用Python标准库sqlite3、json、pathlib，无需安装第三方库，不导入任何旧day。项目根目录PowerShell：

```powershell
.\.venv\Scripts\python.exe day33\day33.py
.\.venv\Scripts\python.exe day33\homework33.py
```

也可进入day33，用同一个解释器运行文件。默认创建`:memory:`内存库，关闭即释放；不创建正式.db、out目录或报告。程序根据tools33.py的位置读取samples/seed.json，与启动目录无关。骨架首次运行会在TODO 1抛NotImplementedError，这是待完成状态。

## 先看数据形状，再写SQL

| 名字/表达式 | 实际类型与用途 | 示例 |
| --- | --- | --- |
| `data` | 从JSON读到的字典 | 两个键authors、quotes |
| `data["authors"]` | 作者字典列表 | `[{"id": 1, "name": "Alex"}, ...]` |
| `author` | 遍历时的一条作者字典 | `{"id": 1, "name": "Alex"}` |
| `data["quotes"]` | 名言字典列表 | `[{"id": 101, "author_id": 1, "text": "Keep learning."}, ...]` |
| `conn` | SQLite连接对象，执行SQL | 不是路径、字典或函数 |
| `fetchall()` | 查询的行元组列表 | `[(1, "Alex"), (2, "Blair")]` |

字典用字段名取值：`author["name"]`。默认SQL行元组用位置取值：`row[0]`是查询中第一列，不是“字典的第一个字段”。`author_id, name = (1, "Alex")`称为解包，两个值分别赋给两个名字；元素数量应对应。

## 为什么拆两张表

authors表每行表示一个作者，id是该作者的主键。quotes表每行表示一条名言：

| 名言主键quotes.id | 外键quotes.author_id | 正文 |
| --- | --- | --- |
| 101 | 1 | Keep learning. |
| 102 | 1 | Practice helps. |
| 103 | 2 | Ask clearly. |

作者1是Alex，作者2是Blair。101和102是不同名言，所以主键不同；它们都属于Alex，所以作者ID相同。这就是“一个作者对应多条名言”。Casey的ID是3，本样本中没有名言，仍可单独存在于作者表。

`PRIMARY KEY`标识本表中的一行；同一张表不允许重复主键。`FOREIGN KEY (author_id) REFERENCES authors(id)`规定：每条名言的author_id必须引用作者表里已有的id。本课字段还使用NOT NULL，不接受缺失作者ID。主键与外键不是相同职责，也不是看到两个id相同就算违规。

建表代码已在tools33.prepare_database中完整提供，不要求这次凭记忆写DDL。SQLite需要对每个连接启用`PRAGMA foreign_keys = ON`，否则不能只靠建表语句推断外键一定生效；工具已负责设置并检查。

## 你需要完成什么

1. `save_authors(conn, authors)`：遍历传入列表，将id和name写入authors表。
2. `save_quotes(conn, quotes)`：遍历传入列表，将id、author_id和text写入quotes表。先作者后名言，保留样本指定ID，不替换成循环序号。
3. 在原文件末尾写两句关系说明。笔记2是假设没有作者行的情况；正常样本里Casey已经存在，不能把“没有名言”误读成“没有作者”。

SQL值用`?`占位符，实际值以元组传入，不拼接SQL。两个函数只负责执行写入，返回None即可；不是所有函数都必须返回业务结果。main已经准备连接、安排顺序、提交、查询验证及关闭，不要在TODO中重建conn、重置表、再次调用main或关闭调用者连接。

调用顺序：`main → load_samples → 创建conn → prepare_database → save_authors → save_quotes → commit → 已提供的检查 → close`。先沿课堂演示理解一条INSERT如何传值，再自己写遍历；无需增加第三个业务函数。

## 提前明确的验收

- 3位作者、3条名言的字段和值与seed.json一致；Alex对应两条，Blair一条，Casey零条。不使用JOIN，本课直接核对两张表。
- 主键与作者ID没有混用；JSON样本和旧day文件不被修改。
- 给定的作者999不存在，外键检查应得到`FOREIGN KEY constraint failed`；失败后原来的3条名言仍在。
- 直接运行显示“作者与名言固定样本检查通过”“不存在的作者被拒绝”“正常数据未受影响；Day33代码检查通过”。两句笔记另行阅读，不用打印成功代替实际比较。

主键冲突演示或自行增加作者是选做，不影响核心通过。本课不要求处理“重复运行同一个落盘库”、复杂回滚或多个连接；这些留给后面的事务/约束单元。可以查课堂代码与笔记，不要求闭卷重写。

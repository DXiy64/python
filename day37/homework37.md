# Day37：把数据库存取集中到store

今天只有一个新目标：分清调用者main与数据库存取函数的职责。DAO意为数据访问对象，本课先用两个函数理解“集中存取”的职责；不要求写类、继承或ORM。预计约两小时，可分两次学。

## 按这个顺序读和运行

本页是唯一阅读入口，无必读外部教材。先运行讲义，讲义所需函数完整放在day37.py中，再按本页说明完成作业。全部仅用Python标准库及内存数据库，不读取旧作业，不联网，无额外样本文件或正式数据输出。

在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe day37/day37.py
```

程序先导入sqlite3，依次定义prepare_database、add_author、list_authors和main；读到def不会执行函数体。文件末尾main()才让程序进入main。

执行顺序如下，四段演示连续用同一个连接：

1. main创建空内存库，交给prepare_database建作者表并存入Alex、Blair，正常结束with时提交。
2. main调用list_authors(conn)，它执行SELECT并用fetchall返回[(1,"Alex"),(2,"Blair")]，main打印。
3. main调用add_author(conn,3,"Casey")。函数记录修改前累计数，写入后提交，返回差值1。main接到1并打印。
4. main再次查询，得到三位作者；再加同一个3号作者，主键重复被跳过，返回0。
5. 最后进入finally，由main关闭连接。屏幕依次显示①至④，再显示“Day37讲义通过；main已关闭连接”。

重点看三个角色：SQL位于存取函数里；函数通过return交出结果；main拿到结果后才print。函数内不必询问用户，也不必打印。下一步把这些存取函数放进同目录store37.py，就是本课的文件拆分。

## 作业从入口到结束怎样运行

作业与讲义独立运行，会重新建立一个空内存库。作业共两个Python文件，执行时只启动homework37.py，另一个是它导入的模块：

```text
homework37.py启动
  → from store37 import save_quotes, list_quotes：加载函数定义，不写数据库
  → 文件末尾调用main()
  → main创建连接
  → 本文件prepare_database存入作者，返回尚待保存的名言列表
  → main调用store37中的查询/保存函数，拿返回值做断言
  → main打印检查结果
  → finally关闭连接
```

prepare_database和snapshot完整放在作业入口中。你不需要修改或反复研究它们；只需知道准备后authors有3人，quotes有0条，返回的rows完整值是：

```python
[(1, "Keep learning."), (1, "Practice helps."), (2, "Ask clearly.")]
```

这是二元组列表，不是JSON字典。返回列表没有把名言写入数据库。save_quotes接到列表后才负责写入。

| 接口 | 输入 | 返回 | 职责 |
| --- | --- | --- | --- |
| save_quotes(conn, rows) | 连接、上述二元组列表 | int：本次新增条数 | 一个事务整批保存，重复跳过，外键失败回滚并抛出 |
| list_quotes(conn, author_id) | 连接、作者ID整数 | [(author_id,text), ...] | WHERE筛选指定作者，按text升序；无记录返回[] |

## 你具体写什么

先完成store37.py的save_quotes。它和你Day36的save_batch职责相同，允许查自己的Day36作业，整理到新模块中，不再增加新写入规则。

再完成list_quotes：SELECT只选author_id、text两列；FROM quotes；用WHERE author_id = ?和单值元组(author_id,)传入参数；ORDER BY text ASC；fetchall后return。单值元组结尾的逗号不能省略。它不commit、不插入、不关闭conn，也不print。

最后在homework37.py末尾写一句笔记：谁创建和关闭连接；为什么由main显示结果。入口main、辅助函数和已有断言保持不变。初始骨架运行到第一个目标函数时会报NotImplementedError，表示待完成。

## 原题通过标准

- 初次写入新增3，重跑新增0，不同作者同正文新增1。
- 作者1返回[(1,"Keep learning."),(1,"Practice helps.")]；作者2初次返回[(2,"Ask clearly.")]。
- 没有名言的作者3、不存在的作者999、写入前的查询都返回[]。
- 合法记录后跟非法作者的同一批，整体回滚，旧数据保留，异常传到调用者。
- 空批次返回0；两个存取函数不打印，不关闭连接；查询不修改数据。
- 完成连接责任与显示责任的笔记。不增加类、菜单或新框架要求。

完成后运行：

```powershell
.\.venv\Scripts\python.exe day37/homework37.py
```

预期依次显示①正常与空结果、②去重、③回滚与连接检查通过，最后提示完成笔记。今天先学会沿调用链追踪两个接口；独立从零设计模块留到后续项目。

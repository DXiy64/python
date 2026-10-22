# Day39：用命令行参数选择查询条件与报告位置

本页是唯一阅读入口。主要新内容只有argparse：从启动命令接收参数。查询、内存样本和CSV辅助函数完整放在各自的入口文件中，不导入旧作业，不需要去别的文件追实现。约两小时，可跨日；只用Python标准库，无外部必读教材。

## 1．本课解决什么问题

之前改变查询条件，要改Python代码。今天学习在终端指定条件：

```powershell
.\.venv\Scripts\python.exe day39/day39.py --author-id 2 --output day39/out/blair.csv
```

这个命令启动演示，选择作者2，把结果写到指定CSV。演示按作者查询；作业改为按正文查询。两者是两次独立启动，各自创建内存数据库，不共享数据库，也不会互相运行。

报告是运行产出，重复指定同一输出文件会覆盖原报告，请把练习结果放在day39/out或临时目录，不选择需要保留的已有文件。相对输出路径以启动命令所在目录为准；默认路径固定在当天文件所在目录的out/quotes.csv，不随启动目录变化。

## 2．从文件入口进入main

先打开day39.py配合本页，所有必要函数都在其中。Python从上往下导入标准库、设置默认路径并加载def，此时还没查询或生成报告。最后执行：

```python
raise SystemExit(main())
```

先调用main。正常情况下main最后返回0，SystemExit把0作为程序退出码交给终端。本课0表示成功，写报告失败返回1；argparse发现参数错误时会自行以2退出。退出码是给调用程序判断成功失败的数字，不是查询条数。

main的argv参数默认None，表示让parse_args读取终端参数；验证时也可以传列表，例如main(["--author-id", "2"])。你现在不必实现这种测试入口。

## 3．构造解析器，再读取参数

main先执行：

```python
parser = build_demo_parser()
args = parser.parse_args(argv)
```

进入build_demo_parser后，先创建ArgumentParser对象，再用add_argument描述接受哪些选项，最后return这个对象。构造规则与真正读取参数是两步：定义时还不知道用户本次输入了什么。

演示的规则如下，完整代码在同一文件：

```python
parser.add_argument("--author-id", type=int, default=1, help="作者ID，默认1")
parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV输出路径")
```

- 第一个字符串是终端选项名称；它不是Python变量名。
- type=int把输入的字符串"2"转换成整数2；--author-id在args里用args.author_id访问，连字符换成下划线。
- type=Path把输入的路径字符串转换成Path对象，后续write_report才能使用.parent和.open。
- default表示没有提供选项时用什么值；help用于自动帮助说明。
- 本课作业还要使用required=True，表示这个选项必须提供；不要与default混淆。

执行上述启动命令后，args是argparse.Namespace对象，大致相当于一个保存解析结果的对象：args.author_id是整数2，args.output是代表day39/out/blair.csv的Path。它不是字典，不使用args["author_id"]取值。

自动帮助与错误可以分别运行：

```powershell
.\.venv\Scripts\python.exe day39/day39.py --help
.\.venv\Scripts\python.exe day39/day39.py --author-id abc
```

--help显示说明后以0退出；abc无法转为整数，显示错误并以2退出。这两种路径都停在解析阶段，不会创建数据库或报告。没有--author-id时按默认作者1运行。

## 4．参数交给查询函数，查询结果再交给CSV函数

解析成功后，main创建conn，调用prepare_database(conn)，建名言表并写入固定三笔：

```python
[(1, "Keep learning."), (2, "Keep learning."), (1, "Practice helps.")]
```

准备函数已提交写入，返回None。接着：

```python
rows = find_by_author(conn, args.author_id)
```

以作者2为例，整数2交给函数参数author_id，再通过(author_id,)绑定到SQL的WHERE author_id=?；fetchall返回[(2,"Keep learning.")]。先前学过的参数化SQL不变，本课只改变条件来自哪里。

不论查询成功与否，finally都会关闭main创建的连接。成功查询后，rows已是Python列表，关闭数据库不会让这个列表消失。

随后write_report(args.output, rows)：创建父目录，打开CSV文件，先写表头author_id,text，再写列表里的数据。with打开文件，结束时关闭；utf-8-sig与newline=""是已提供的CSV设置，本课不用重写。成功后main显示作者ID、条数和路径，返回0。

上面命令生成的CSV内容为：

```csv
author_id,text
2,Keep learning.
```

作者1会有两条结果，正文升序；不存在的作者999返回[]，报告仍包含表头。若无法写入输出路径，已提供的except OSError显示“报告写入失败”并返回1，不打印成功提示。你不需要实现异常框架或日志系统。

| 名称 | 实际类型 | 来源和去向 |
| --- | --- | --- |
| parser | argparse.ArgumentParser | build_demo_parser返回，负责解析规则 |
| args | argparse.Namespace | parse_args返回，属性保存用户选择 |
| args.author_id | int | 终端字符串经type=int转换，交给查询 |
| args.output | pathlib.Path | 终端路径或默认值，交给CSV函数 |
| conn | sqlite3.Connection | main创建并在finally关闭 |
| rows | 二元组列表 | 查询返回，交给write_report，不是游标 |

## 5．作业只实现解析器和一句笔记

打开homework39.py。它已经完整提供prepare_database、find_by_text、write_report及main，辅助函数与讲义同样在本文件内，不要求打开旧文件。find_by_text用WHERE text=?精确匹配，按author_id升序返回列表。

你只完成build_parser，让它返回一个ArgumentParser，规则如下：

1. --text是必填字符串，保存为args.text；缺少选项或缺少值由argparse报错。
2. --output转换为Path，保存为args.output；不提供时用已经给出的DEFAULT_OUTPUT。
3. 两个选项提供help说明，保留ArgumentParser默认的--help。
4. build_parser只创建并返回解析器，不在其中调用parse_args、查询或写报告。

字符串不写type时默认保持字符串，也可以明确type=str。目标函数保留TODO；初始运行报NotImplementedError，表示尚待完成。main已经提供空字符串/全空格检查，用parser.error给出错误并以2退出。

作业启动后执行顺序完整如下：

```text
末尾调用main
→ build_parser返回你构造的解析器
→ parse_args读取选项，得到args
→ 检查正文不是空白
→ 创建内存库，写入固定样本
→ find_by_text(conn,args.text)：SQL问号接收正文，返回rows
→ 关闭连接
→ write_report(args.output,rows)：创建CSV
→ 显示新增报告的条数和位置，成功返回0
```

末尾写一句笔记：parse_args返回什么，以及命令中的--text值怎样传到SQL问号与最终CSV。不需要写类、菜单、网络采集、配置文件或日志模块，不重新实现SQL或CSV。

## 6．运行与原题通过标准

从项目根目录运行；有空格的正文要用引号包住，形成一个参数值：

```powershell
.\.venv\Scripts\python.exe day39/homework39.py --text "Keep learning." --output day39/out/keep.csv
.\.venv\Scripts\python.exe day39/homework39.py --text "Practice helps."
.\.venv\Scripts\python.exe day39/homework39.py --text "Missing" --output day39/out/missing.csv
.\.venv\Scripts\python.exe day39/homework39.py --help
```

第一条命令显示导出2条，keep.csv内容：

```csv
author_id,text
1,Keep learning.
2,Keep learning.
```

第二条使用默认位置out/quotes.csv，只有作者1的Practice helps.；第三条导出0条但保留表头；--help显示两个选项说明并成功退出。

错误场景：不带--text、只写--text不带值、传入未知选项、正文为空白，都要有清楚错误，退出码2，且不生成报告。输出位置无法写入时，由已提供代码返回1。

允许查讲义完成。验收会核对解析后的属性类型、默认值、上述正常/空结果/错误路径、CSV内容及一句笔记。通过仅表示本课功能和解释符合要求，独立设计命令行工具留待后续应用。

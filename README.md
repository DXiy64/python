# Python 学习记录 🐍

项目式 Python 学习：按学习单元推进，结合短时回忆、独立开发、验证与迁移练习。
**目标：独立拆解需求、开发、验证、维护与交付Python小项目（90个学习单元，可跨日）**

![进度](https://img.shields.io/badge/%E8%BF%9B%E5%BA%A6-38%20%2F%2090%20%E5%A4%A9%20(42.2%25)-orange)
![当前阶段](https://img.shields.io/badge/%E9%98%B6%E6%AE%B5%E2%91%A1-%E9%A1%B9%E7%9B%AE%E4%B8%8E%E6%95%B0%E6%8D%AE%E5%BA%93%E8%BF%9B%E9%98%B6%20Day%2021--40-yellow)
![目标](https://img.shields.io/badge/Python-Projects-blueviolet)

## 学习进度

**已完成 38 / 90 个学习单元（42.2%），Day38提示修正后验收通过，Day39已开课待完成。Day30经AI协助修复、Day36参考完整示例后验收通过；独立掌握与延迟复测另行记录。Day可跨多个实际日。**　🟩 已完成　🟨 进行中　⬜ 未开始

```
Day 01–30  🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
Day 31–60  🟩🟩🟩🟩🟩🟩🟩🟩🟨⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
Day 61–90  ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
```

### 阶段进度

| 阶段 | 天数 | 状态 |
| --- | --- | --- |
| ① 基础收尾（包 / 依赖 / 标准库 / 正则 / 调试） | Day 15–20 | ✅ 已完成（Day 20 复习日三阶段全部验收） |
| ② 项目与数据库进阶（账本 / 采集 / JOIN / DAO / 索引 / 交付） | Day 21–40 | 🟨 Day21–38完成；Day39进行中；40按路线继续 |
| ③ 工程基本功与专题项目（Git / Linux / HTTP / 测试 / 一个技术专题） | Day 41–70 | ⬜ 未开始；Day50做技术体验，由用户明确专题 |
| ④ 语言进阶、维护与综合交付（优先1–2个完整项目） | Day 71–90 | ⬜ 未开始；生成器/装饰器/算法/复现与改需求 |

> 技术路线见 **[ROADMAP.md](ROADMAP.md)**；授课与验收见 **[TEACHING.md](TEACHING.md)**；能力证据见 **[LEARNING_PROGRESS.md](LEARNING_PROGRESS.md)**。地点、岗位选择与投递等由用户自行安排，不计入课程。

2026-10-15课程审查已完成：[审查记录](docs/curriculum/COURSE_AUDIT.md)说明问题、证据与修改；[知识覆盖表](docs/curriculum/COURSE_REFERENCES.md)列出前置与验收位置。Day01–31完成记录和Day32作业保留，后续每单元一个主要新难点。

## 每日记录

第一轮分类笔记见 [Day01–30月度知识笔记](day30/月度知识笔记.md)，含原笔记来源、易错点和工具类设计步骤。

| 状态 | 天数 | 主题 | 课堂代码 | 作业 |
| ---- | ---- | ---- | -------- | ---- |
| ✅ | Day 01 | 第一行代码：print / 变量 / f-string / input | `day01/day01.py` | `day01/homework01.py` — 个人信息输出 |
| ✅ | Day 02 | 条件判断与循环：if / while / break，int 类型转换 | `day02/day02.py` | `day02/homework02.py` — 猜数字游戏 |
| ✅ | Day 03 | 列表与 for 循环：索引、append、range、累加 | `day03/day03.py` | `day03/homework03.py` — 成绩小管家（总分/平均/最高最低） |
| ✅ | Day 04 | 字典与函数：dict 增删改查、def、返回值 | `day04/day04.py` | `day04/homework04.py` — 通讯录小管家 |
| ✅ | Day 05 | 文件读写：w / a / r 模式、with 自动关闭 | `day05/day05.py` | `day05/homework05.py` — 记账本（`account.txt`） |
| ✅ | Day 06 | 异常处理：try/except、ValueError / FileNotFoundError / ZeroDivisionError | `day06/day06.py` | `day06/homework06.py` — 给猜数字游戏穿防弹衣 |
| ✅ | Day 07 | 模块与 JSON：datetime / random、json.dump / load 结构化存档 | `day07/day07.py` | `day07/homework07.py` — 通讯录存档版（`contacts.json`） |
| ✅ | Day 08 | 联网小程序：requests + wttr.in 天气查询，写日志 | `day08/day08.py` | `day08/homework08.py` — 天气小管家（`weather_log.txt`） |
| ✅ | Day 09 | 毕业项目①：通讯录管理系统（while 菜单 + 字典 + 函数 + JSON + try） | `day09/manager.py` | `day09/homework09.py` — 读懂 manager.py：save 调用点、del、strip，加"统计"与电话数字校验 |
| ✅ | Day 10 | 面向对象：class / 对象 / `__init__` / self / 方法，把通讯录装进 `ContactBook` 类 | `day10/day10.py` | `day10/homework10.py` — 加 `count` 统计、电话数字校验、选做模糊搜索 |
| ✅ | Day 11 | 面向对象②：`__str__` 长相 / `__len__` 人数 / update 改电话 / rename 搬家（键不能改名） | `day11/day11.py` | `day11/homework11.py` — 长相、改电话校验、选做改名搬家 |
| ✅ | Day 12 | 毕业项目②：菜单版通讯录（类 + while 菜单 + main，不再递 contacts） | `day12/day12.py` | `day12/homework12.py` — 补模糊搜分支、空名校验、选做看人数 |
| ✅ | Day 13 | 面向对象③：继承 / 父类子类 / `super().__init__` / 方法覆盖 / 多态 / isinstance | `day13/day13.py` | `day13/homework13.py` — 联系人分类：Friend 加备注、Workmate 加公司、多态显示 |
| ✅ | Day 14 | 拆文件：工具箱（类）+ 入口（菜单）、`import` 三种写法、`__pycache__` 与闸门 | `day14/day14.py` | `day14/homework14.md` — 拆分 `big.py` → `hw_contactbook.py` + `hw_main.py`（已验收） |
| ✅ | Day 15 | 模块与包：`__init__.py` 门面、`from 包.模块 import`、相对导入 `.`、`python -m` | `day15/day15.py` | `day15/homework15.md` — 通讯录改造成 `mypkg/` 包（已验收） |
| ✅ | Day 16 | 虚拟环境与依赖：`venv` / `pip` / `requirements.txt` / 环境隔离 | `day16/day16.py` + `commands.md` | `day16/homework16.md` — 建 venv、装 `tabulate`、导出并复现依赖（已验收） |
| ✅ | Day 17 | 标准库四件套：`pathlib` / `csv` / `datetime` / `collections` | `day17/day17.py` | `day17/homework17.py` — 通讯录导出器（CSV + 时间戳报表 + 分组统计，已验收） |
| ✅ | Day 18 | 正则表达式 `re`：search / findall / sub / fullmatch / 分组 / 元字符 | `day18/day18.py` | `day18/homework18.py` — 通讯录数据清洗器（抽取/校验/脱敏手机号，已验收） |
| ✅ | Day 19 | 调试：读 traceback / `print` 打点 / `breakpoint()`+pdb / `logging` 分级 / `assert` | `day19/day19.py` + `crash_demo.py` + `pdb_demo.py` | `day19/homework19.py` — 调试练习台（读错误名 / 修 bug / logging 落盘，已验收） |
| ✅ | Day 20 | 通讯录综合复习（当时的闭卷任务，保留历史记录；后续按现行教学约定） | `day20/homework20.md` + `day20/复习地图.md` | 你自己的 `day20/review.py` + `day20/mypkg/`（三阶段已验收） |
| ✅ | Day 21 | 从零 JSON 命令行记账本：添加、校验、分类金额统计、菜单 | `day21/day21.py` | `day21/homework21.md` + `day21/hw_21.py`（仓库汇总记录已验收） |
| ✅ | Day 22 | 记账本扩展：按分类·日期筛选、月度报表、导出 CSV | `day22/day22.py` | `day22/homework22.md` + `day22/hw_22.py`（已验收：筛选/报表/CSV 落盘） |
| ✅ | Day 23 | 记账本收尾：删除·修改一笔、空月报表、跨月验收 | `day23/day23.py` | `day23/homework23.md` + `day23/hw_23.py`（已验收：删改/空月/跨月） |
| ✅ | Day 24 | sqlite3 第一天：建表 / 增删改查（INSERT·SELECT·UPDATE·DELETE） | `day24/day24.py` | `day24/homework24.py` — 记账本搬进 sqlite（已验收） |
| ✅ | Day 25 | sqlite3 第二天：聚合查询（SUM·COUNT·GROUP BY） | `day25/day25.py` | `day25/homework25.py` — SQL 版分类统计 + 月度报表（已验收） |
| ✅ | Day 26 | sqlite3 第三天：菜单版完整程序 + CSV 导出 | `day26/day26.py` | `day26/homework26.py` — 菜单版 sqlite 记账本（已验收） |
| ✅ | Day 27 | 爬虫第一天：requests 抓网页 + BeautifulSoup 摘内容 | `day27/day27.py` | `day27/homework27.py` — 抓名言存 sqlite（已验收：10 条/去重/日报） |
| ✅ | Day 28 | 爬虫第二天：翻页 + 限速 + 增量入库 | `day28/day28.py` | `day28/homework28.py` — 翻 3 页入库 + 作者排行（已验收：30 条/Top3/重跑 0） |
| ✅ | Day 29 | 爬虫第三天：日报（总数/作者数/排行 + 落盘） | `day29/day29.py` | `day29/homework29.py` — 2 页日报 + 落盘文件（已验收：20 条/15 作者/Einstein 4/日报落盘） |
| ✅ | Day 30 | 综合能力检查（记账本 → 拆包 → 日报与验证） | `day30/homework30.md` + `day30/复习地图.md` | `day30/homework30.py` + `book30/` + `daily30.py`（AI协助修复后验收通过，独立掌握待复测） |
| ✅ | Day 31 | 最小自动化验证：assert、临时数据库、持久化与去重 | `day31/day31.py` | `day31/homework31.py` + `day31/homework31.md`（提示后完成，验收通过） |
| ✅ | Day 32 | 日报可靠性与数据建模：失败说明、本地HTML、去重键与金额取舍 | `day32/day32.py` | `day32/homework32.py` + `day32/homework32.md`（提示后完成，六种情况及两句笔记验收通过） |
| ✅ | Day 33 | 一对多关系、主键与外键：作者和名言两张表 | `day33/day33.py` + `day33/tools33.py` | `day33/homework33.py` + `day33/homework33.md` + `day33/samples/seed.json`（学员实现，写入/外键/笔记验收通过） |
| ✅ | Day 34 | INNER JOIN：按作者关系同时查询名言正文与作者名 | `day34/day34.py` + `day34/tools34.py` | `day34/homework34.py` + `day34/homework34.md` + `day34/samples/seed.json`（提示修正后正常/空结果/连接责任及笔记验收通过） |
| ✅ | Day 35 | LEFT JOIN与零记录统计：COUNT(*)、COUNT(q.id)、NULL与0 | `day35/day35.py` + `day35/tools35.py` | `day35/homework35.py` + `day35/homework35.md` + `day35/samples/seed.json`（提示修正后，正常/全空统计与笔记验收通过） |
| ✅ | Day 36 | 事务与唯一约束：整批提交/回滚、复合去重键 | `day36/day36.py` + `day36/tools36.py` | `day36/homework36.py` + `day36/homework36.md` + `day36/samples/seed.json`（参考完整示例后，写入/去重/回滚与笔记验收通过） |
| ✅ | Day 37 | store接口、调用链与连接责任 | `day37/day37.py` | `day37/homework37.py` + `day37/store37.py` + `day37/homework37.md`（提示后修正，查询/去重/回滚与连接责任隔离复查通过） |
| ✅ | Day 38 | 索引与查询计划、读写及空间取舍 | `day38/day38.py`（完整独立演示，无需追辅助文件） | [教案与任务书](day38/homework38.md) + `day38/homework38.py`（索引函数、实际计划与取舍笔记提示修正后通过） |
| 🟨 | Day 39 | argparse查询条件与报告位置 | `day39/day39.py`（完整单文件演示） | [教案与任务书](day39/homework39.md) + `day39/homework39.py`（解析器及一句笔记待完成） |

Day30作业完成计入进度；帮助程度与独立掌握另行记录，延迟复测不作为新增完成门槛。Day31通过编写检查继续巩固。

### 里程碑

- [x] 基础语法：变量 / 判断 / 循环 / 列表 / 字典 / 函数（Day 01–04）
- [x] 文件与异常：文件读写 / try-except / JSON / 联网（Day 05–08）
- [x] 第一个完整项目：菜单版通讯录（Day 09、12）
- [x] 面向对象：class / self / 双下划线方法 / 继承 / 多态（Day 10–13）
- [x] 阶段① 基础收尾：包 / 虚拟环境 / 标准库 / 正则 / 调试（Day 15–20）
- [ ] 阶段② 项目与数据库进阶：可查文档，自行设计并交付多表采集工具（Day21–40）
- [ ] 阶段③ 工程基本功与专题项目：一个技术专题 + Git/Linux/HTTP/测试（Day41–70）
- [ ] 阶段④ 语言进阶与综合交付：优先1–2个项目，能解释、验证与修改（Day71–90）

## 运行方法

新电脑先按[SETUP.md](SETUP.md)重建项目根目录环境；当前Day31/32按各自任务书从项目根目录启动，保留完整仓库依赖。下面的进入当天目录方式主要用于早期课件，不能代替各任务书指定入口。

```powershell
# 进对应天数目录再运行（部分程序读写同目录下的数据文件）
Set-Location day01
python day01.py
```

联网与爬虫课程需要 `requests`；BeautifulSoup 解析需要 `beautifulsoup4`。优先使用项目虚拟环境，通过同一解释器的 `-m pip` 安装；其他依赖按对应任务记录，Day 16 示例另需 `tabulate`。

菜单类程序（Day 09 起）必须在终端里跑，因为要敲键盘选菜单：

```powershell
Set-Location day14
python main.py
```

## 目录结构

```
day01/  day02/  ...  day15/   # 每天：课堂代码 + 作业 + 程序产生的数据文件
day14/                        # 多文件示例：contactbook.py（工具箱）+ main.py（入口）
day15/mybook/                 # 包示例：__init__.py（门面）+ storage.py + book.py + cli.py
ROADMAP.md                    # 90个学习单元的技术路线
TEACHING.md                   # 当前教学约定
LEARNING_PROGRESS.md          # 当前进度、能力证据与历史记录
SETUP.md                      # 新电脑环境与教学接续
docs/curriculum/              # 课程参考与审查记录
.agents/skills/               # 项目教学、验收及推送技能
```

## 换电脑继续学习

教学规则、路线、能力记录及三个项目技能都随本仓库维护：

- [python-project-tutor](.agents/skills/python-project-tutor/SKILL.md)：解释、授课、课程审查与推进。
- [homework-verify](.agents/skills/homework-verify/SKILL.md)：隔离验收与证据记录。
- [day-push](.agents/skills/day-push/SKILL.md)：按有效授权提交推送、核对远程结果。

提交并推送后，另一台电脑拉取完整仓库，在仓库目录启动AI并读取AGENTS.md即可接续文件中的约定；客户端未发现技能时直接读取对应SKILL.md。无需安装原电脑的全局python-tutor。详细环境和启动检查见[SETUP.md](SETUP.md)。Git不传递聊天记录、全局技能、长期记忆或.venv，也不能保证不同模型的教学表现完全相同。

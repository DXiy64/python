# Python 学习记录 🐍

项目式 Python 学习：按学习单元推进，结合短时回忆、独立开发、验证与迁移练习。
**目标：具备独立开发与验证能力，按岗位需求准备求职（90 天规划窗口）**

![进度](https://img.shields.io/badge/%E8%BF%9B%E5%BA%A6-29%20%2F%2090%20%E5%A4%A9%20(32%25)-orange)
![当前阶段](https://img.shields.io/badge/%E9%98%B6%E6%AE%B5%E2%91%A1-%E4%BB%8E%E9%9B%B6%E5%81%9A%E9%A1%B9%E7%9B%AE%20Day%2021--35-yellow)
![目标](https://img.shields.io/badge/%E7%9B%AE%E6%A0%87-Python%20%E5%B7%A5%E4%BD%9C-blueviolet)

## 学习进度

**仓库记录已完成 29 / 90 个学习单元（32%）；本次未重新验收历史作业。Day 可跨多个实际日。**　🟩 已完成　🟨 进行中　⬜ 未开始

```
Day 01–30  🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟨
Day 31–60  ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
Day 61–90  ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
```

### 阶段进度

| 阶段 | 天数 | 状态 |
| --- | --- | --- |
| ① 基础收尾（包 / 依赖 / 标准库 / 正则 / 调试） | Day 15–20 | ✅ 已完成（Day 20 复习日三阶段全部验收） |
| ② 项目与能力补强（记账本 / sqlite / 爬虫 / 验证 / 迁移） | Day 21–35 | 🟨 进行中（Day 21–29 记账本+sqlite+爬虫日报已验收；Day 30 综合能力检查） |
| ③ 求职核心技能（Git / Linux / HTTP / Web 或数据 / 测试） | Day 36–60 | ⬜ 未开始 |
| ④ 作品与求职（优先 1–2 个完整作品 / 简历 / 面试） | Day 61–90 | ⬜ 未开始 |

> 路线与方向见 **[ROADMAP.md](ROADMAP.md)**；授课与验收见 **[TEACHING.md](TEACHING.md)**；能力证据见 **[LEARNING_PROGRESS.md](LEARNING_PROGRESS.md)**。方向待本人偏好与目标岗位样本确认，不默认后端。

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
| ✅ | Day 20 | 复习日：**不看旧文件，从零重写通讯录**（单文件 → 拆包 → 挂上正则/CSV/日志） | `day20/homework20.md` + `day20/复习地图.md` | 你自己的 `day20/review.py` + `day20/mypkg/`（三阶段已验收） |
| ✅ | Day 21 | 从零 JSON 命令行记账本：添加、校验、分类金额统计、菜单 | `day21/day21.py` | `day21/homework21.md` + `day21/hw_21.py`（仓库汇总记录已验收） |
| ✅ | Day 22 | 记账本扩展：按分类·日期筛选、月度报表、导出 CSV | `day22/day22.py` | `day22/homework22.md` + `day22/hw_22.py`（已验收：筛选/报表/CSV 落盘） |
| ✅ | Day 23 | 记账本收尾：删除·修改一笔、空月报表、跨月验收 | `day23/day23.py` | `day23/homework23.md` + `day23/hw_23.py`（已验收：删改/空月/跨月） |
| ✅ | Day 24 | sqlite3 第一天：建表 / 增删改查（INSERT·SELECT·UPDATE·DELETE） | `day24/day24.py` | `day24/homework24.py` — 记账本搬进 sqlite（已验收） |
| ✅ | Day 25 | sqlite3 第二天：聚合查询（SUM·COUNT·GROUP BY） | `day25/day25.py` | `day25/homework25.py` — SQL 版分类统计 + 月度报表（已验收） |
| ✅ | Day 26 | sqlite3 第三天：菜单版完整程序 + CSV 导出 | `day26/day26.py` | `day26/homework26.py` — 菜单版 sqlite 记账本（已验收） |
| ✅ | Day 27 | 爬虫第一天：requests 抓网页 + BeautifulSoup 摘内容 | `day27/day27.py` | `day27/homework27.py` — 抓名言存 sqlite（已验收：10 条/去重/日报） |
| ✅ | Day 28 | 爬虫第二天：翻页 + 限速 + 增量入库 | `day28/day28.py` | `day28/homework28.py` — 翻 3 页入库 + 作者排行（已验收：30 条/Top3/重跑 0） |
| ✅ | Day 29 | 爬虫第三天：日报（总数/作者数/排行 + 落盘） | `day29/day29.py` | `day29/homework29.py` — 2 页日报 + 落盘文件（已验收：20 条/15 作者/Einstein 4/日报落盘） |
| 🟨 | Day 30 | 综合能力检查：**短时闭卷设计 + 允许查资料的独立开发**（记账本 → 拆包 → 日报与验证） | `day30/homework30.md` + `day30/复习地图.md` | `day30/homework30.py` 或 `review30.py` + `book30/` + `daily30.py`（三阶段待验收，允许跨日） |

### 里程碑

- [x] 基础语法：变量 / 判断 / 循环 / 列表 / 字典 / 函数（Day 01–04）
- [x] 文件与异常：文件读写 / try-except / JSON / 联网（Day 05–08）
- [x] 第一个完整项目：菜单版通讯录（Day 09、12）
- [x] 面向对象：class / self / 双下划线方法 / 继承 / 多态（Day 10–13）
- [x] 阶段① 基础收尾：包 / 虚拟环境 / 标准库 / 正则 / 调试（Day 15–20）
- [ ] 阶段② 从零做项目：能不看教程写出完整程序（Day 21–35）
- [ ] 阶段③ 求职核心技能：Web 或数据处理 + Git + Linux + 测试（Day 36–60）
- [ ] 阶段④ 作品集：优先 1–2 个完整项目 + 简历（Day 61–90）

## 运行方法

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
ROADMAP.md                    # 90 天求职路线图
```

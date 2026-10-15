# 新电脑开工与教学接续

本仓库默认在项目根目录共用一个.venv。换电脑重建环境，不复制原电脑的.venv，也不需要沿用用户名或绝对路径。Day16是历史环境练习，其独立环境与requirements可保留；后续课件默认使用根目录环境。

## 1. 获取完整仓库

已安装Git和Python后，在你选定的父目录执行：

```powershell
git clone https://github.com/dxiy64/python.git
Set-Location python
```

已有仓库时，在项目根目录先检查自己的改动，再更新：

```powershell
git status --short
# 如果有未保存到版本库的作业，先提交或另行备份，再执行下面一行。
git pull --ff-only
```

遇到分叉或冲突先检查原因，不强制覆盖。只有原电脑已提交并推送的文件才能被拉取；本地尚未提交的课程更新不在远程。首次clone无需再pull。

## 2. Windows / PowerShell：根目录建环境并安装

以下命令都在包含README.md、AGENTS.md的项目根目录运行。当前课件在Python 3.14.4验证过，其他版本需实际验证；不把旧指南的“3.9以上”当作已测兼容范围。

```powershell
python --version
git --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -c "import sys, requests, bs4; print(sys.executable); print(requests.__version__, bs4.__version__)"
```

应看到本项目.venv内的解释器，以及requests和BeautifulSoup版本。直接指定解释器无需激活，也不受PowerShell激活脚本策略影响。若编辑器提示缺库，让编辑器选择同一个.venv解释器。

根目录requirements.txt固定本次验证过的requests和beautifulsoup4直接依赖，满足当前Day31/32；没有锁定全部间接依赖，也不代表全部旧课或未来课都只需这两个库。以后新课引入依赖时，按课件说明更新和验证。若复习Day16的tabulate，另用同一个解释器安装：

```powershell
.\.venv\Scripts\python.exe -m pip install -r day16\requirements.txt
```

不要为了证明隔离而卸载全局包或要求“退出环境必须导入失败”；系统Python本来可能已安装同名库。看sys.executable和库来源更可靠。

## 3. macOS / Linux 的对应命令

命令形式如下，本次未在这两类系统实机验证：

```sh
git clone https://github.com/dxiy64/python.git
cd python
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -c "import sys, requests, bs4; print(sys.executable); print(requests.__version__, bs4.__version__)"
```

已有仓库直接进入项目根目录，检查改动后pull，不重复clone。历史代码可能含Windows路径或依赖特定启动目录，按对应任务书核对，不宣称全部历史文件跨系统兼容。

## 4. 让AI接续教学规则

在Codex等支持仓库规则/技能的客户端中打开整个项目目录，开始新会话并读取：

1. AGENTS.md及项目内.agents/skills/python-project-tutor/SKILL.md。
2. TEACHING.md、ROADMAP.md、LEARNING_PROGRESS.md顶部当前状态、README。
3. 正在做的任务书、代码及样本。课程审查时再读docs/curriculum内的[知识覆盖表](docs/curriculum/COURSE_REFERENCES.md)和[审查记录](docs/curriculum/COURSE_AUDIT.md)。

三个技能都放在.agents/skills，不依赖用户全局技能目录。本项目教学技能名为python-project-tutor，避免与原电脑旧python-tutor混淆。客户端没自动发现时，直接读取上述SKILL.md及相邻验收/推送技能，不能因此跳过项目规则。

可发送这句话开始：

> 先读取本项目AGENTS.md、项目教学技能、TEACHING.md、ROADMAP.md、LEARNING_PROGRESS.md、README和当前任务，按文件里的最新进度继续。检查作业时不要代改，指导修改要给当前行号。

读取后应能说清：当前单元及是否已验收、下一步任务、作业帮助程度、新课依赖随课提供，以及通过后自动生成下一课并推送的有效授权。实际进度以文件为准，不在本指南复制计数。

Git同步文件，不同步聊天记录、全局设置、长期记忆、账号权限或.venv。另一台电脑的GitHub登录和推送权限需自行就绪；不同模型仍可能出现理解偏差，需按TEACHING的检查标准核验，不能保证输出完全相同。

## 5. 当前课件的运行检查

以下是当前讲义的离线启动检查，不是学员作业验收；讲义应显示四节演示并正常退出：

```powershell
.\.venv\Scripts\python.exe day32\day32.py
```

Day31/32保留历史跨课依赖，需要完整day30目录；不能只复制day32就宣称独立运行。从后续新课开始，必要业务辅助函数/模块和样本随当天提供，并在隔离目录核验；Python和第三方库仍由环境安装。

作业按自己的任务书运行，TODO未完成时不会通过，不因此重建或覆盖学员文件。后续进度变更时同步更新本节示例。

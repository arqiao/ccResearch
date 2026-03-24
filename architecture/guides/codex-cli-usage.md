# Codex CLI 使用指南
> 更新时间：2026-03-24
> 适用环境：Windows PowerShell

---

## 一、适用场景

这篇文档只写日常使用，不写排障。

适合以下情况：

- 想启动 Codex
- 想在当前仓库里让 Codex 工作
- 想执行一次性任务
- 想知道进入 Codex 对话环境后怎么提需求
- 想查看更多交互界面的历史回显

排障请看：

- `guides/codex-cli-troubleshooting.md`

---

## 二、启动前的最小准备

建议先进入项目根目录：

```powershell
cd D:\workspace\ccResearch\architecture
```

然后检查登录状态：

```powershell
codex login status
```

如果只是想确认 CLI 当前可用，再执行：

```powershell
codex exec --skip-git-repo-check --color never "reply with exactly: OK"
```

---

## 三、外部常用命令

### 3.1 查看版本

```powershell
codex --version
```

### 3.2 查看帮助

```powershell
codex --help
codex exec --help
codex login --help
```

### 3.3 交互式启动

直接启动：

```powershell
codex
```

保留终端滚动历史启动：

```powershell
codex --no-alt-screen
```

带初始提示词启动：

```powershell
codex "先阅读仓库结构，再告诉我这个项目的主要模块"
```

指定工作目录启动：

```powershell
codex -C D:\workspace\ccResearch\architecture
```

推荐在当前仓库里这样启动，便于查看更多历史输出：

```powershell
cd D:\workspace\ccResearch\architecture
codex --no-alt-screen
```

退出 Codex：

- 通常按 `Ctrl+C`
- 如果当前状态没有退出，再按一次 `Ctrl+C`
- 某些情况下也可以尝试 `Ctrl+D`
- 如果仍然无法退出，就关闭当前终端窗口或标签页

### 3.4 非交互执行

执行一次性任务：

```powershell
codex exec "阅读当前仓库并总结主要目录用途"
```

在非 Git 目录执行：

```powershell
codex exec --skip-git-repo-check "解释这个目录里的文件作用"
```

把最终输出写入文件：

```powershell
codex exec -o .\codex-last.txt "总结当前目录"
```

### 3.5 代码评审

```powershell
codex review
```

或：

```powershell
codex exec review
```

### 3.6 恢复最近会话

```powershell
codex resume --last
```

### 3.7 分叉最近会话

```powershell
codex fork --last
```

### 3.8 登出

```powershell
codex logout
```

---

## 四、进入 Codex 对话环境后的常用方式

进入 `codex` 对话环境后，核心交互方式不是记一堆固定 slash 指令，而是直接用自然语言描述任务。

最常用的是下面这些输入模式。

### 4.1 让它先理解项目

```text
先阅读当前仓库结构，再告诉我这个项目的主要模块。
```

```text
先不要改代码，先解释这个仓库的目录职责和主要入口。
```

### 4.2 让它先做分析，不立即改代码

```text
先定位导致这个报错的代码位置，不要修改，先告诉我原因。
```

```text
先找出和登录流程相关的文件，再给我一个修复方案。
```

### 4.3 让它直接改代码

```text
修复当前项目里的 xxx 问题，并自行运行必要的验证命令。
```

```text
在不改变现有接口的前提下，给这个模块补上超时处理。
```

### 4.4 让它只改文档

```text
把刚才结论整理到 guides 目录里，补一份中文操作文档。
```

```text
更新 task-list.md，把这个任务标记为已完成。
```

### 4.5 让它做代码评审

```text
帮我 review 当前改动，优先看 bug、回归风险和缺少的测试。
```

```text
只审查 auth 模块，列出高风险问题。
```

### 4.6 让它解释代码

```text
解释这个函数的执行流程，并指出最容易出错的分支。
```

```text
说明这个模块是怎么处理重试逻辑的。
```

### 4.7 让它限制修改范围

```text
只允许修改 guides 目录，不要碰代码文件。
```

```text
只修改这个文件，别改别的地方。
```

```text
先不要提交，不要删除文件，不要做破坏性操作。
```

### 4.8 让它在执行前说明计划

```text
先给我一个简短计划，再开始改。
```

```text
先列出你准备修改的文件，再执行。
```

### 4.9 让它执行验证

```text
修改后运行测试，并告诉我哪些验证通过了，哪些没跑。
```

```text
完成后用最小命令验证功能可用。
```

---

## 五、推荐的对话写法

### 5.1 任务描述要具体

不推荐：

```text
帮我看一下这个项目。
```

推荐：

```text
先阅读当前仓库，告诉我 API 层、服务层和配置层分别在哪些文件。
```

### 5.2 明确是否允许改代码

不推荐：

```text
看看这个 bug。
```

推荐：

```text
先定位这个 bug，说明原因；确认后你再直接修复。
```

### 5.3 明确边界

推荐附加限制：

- 不要改接口
- 不要改数据库结构
- 只改一个文件
- 先分析后执行
- 改完后跑测试

### 5.4 明确输出形式

例如：

```text
最后用中文总结，给我文件路径和风险点。
```

```text
最后只给结论和修改建议，不要直接改代码。
```

---

## 六、常用工作流

### 6.1 新仓库初次进入

```powershell
cd D:\workspace\ccResearch\architecture
codex --no-alt-screen
```

进入后输入：

```text
先阅读当前仓库结构，再告诉我这个项目的主要模块、核心文档和建议阅读顺序。
```

### 6.2 一次性执行任务

```powershell
codex exec "帮我检查这个仓库里最需要优先处理的问题"
```

### 6.3 连续对话处理复杂任务

```powershell
codex --no-alt-screen
```

建议第一轮输入：

```text
先分析，不要急着改。告诉我你准备怎么做。
```

第二轮再输入更具体要求：

```text
现在开始修改，只改 guides 目录，并在完成后总结变更。
```

### 6.4 从上次会话继续

```powershell
codex resume --last
```

### 6.5 基于上次会话分叉一个新方向

```powershell
codex fork --last
```

---

## 七、查看更多回显

如果你觉得 `codex` 交互界面的显示区域太小，只能看到最后十几行，优先使用：

```powershell
codex --no-alt-screen
```

作用：

- 不使用 alternate screen
- 保留正常终端滚动缓冲区
- 可以直接向上翻看更多历史输出

推荐启动方式：

```powershell
cd D:\workspace\ccResearch\architecture
codex --no-alt-screen
```

如果你用的是 Windows Terminal，还可以额外调大终端 scrollback 缓冲区；但对 Codex CLI 来说，最直接有效的办法仍然是 `--no-alt-screen`。

---

## 八、当前机器的已验证状态

当前这台机器已经确认：

- `@openai/codex` 已全局安装
- `codex --version` 返回 `codex-cli 0.116.0`
- `codex login status` 返回 `Logged in using ChatGPT`
- 当前仓库 `D:\workspace\ccResearch\architecture` 可直接作为 Codex 工作目录
- 最小执行验证已通过

验证命令：

```powershell
codex exec --skip-git-repo-check --color never "reply with exactly: OK"
```

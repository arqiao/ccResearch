# 架构设计决策记录

> 创建时间：2026-02-25
> 说明：记录关键配置的设计思路和决策原因，补充 task-list.md 的"做了什么"，聚焦"为什么这么设计"

---

## 1. 整体架构：CC 本地 + OpenClaw 服务器

### 分工设计

| 角色 | 工具 | 职责 |
|-----|------|------|
| 主动开发 | Claude Code（本地） | 写代码、调研、文件操作 |
| 被动自动化 | OpenClaw（服务器） | 响应飞书消息、定时任务、通知 |

### 决策原因

- CC 需要访问本地文件系统，必须在本地运行
- OpenClaw 需要 7×24 在线响应消息，必须在服务器运行
- 两者通过 GitHub 仓库（ccResearch、arqiao-shared-knowledge）共享状态

---

## 2. API Key 管理规范

### 设计原则

**任何 key 不进入 git 仓库**，按运行环境分两处存放：

| 环境 | 存放位置 | 权限 |
|-----|---------|------|
| 本地（Windows） | `D:\workspace\noshare\env.md` | 不在任何 git 仓库目录下 |
| 服务器（Linux） | `/root/.secrets` | chmod 600 |

### 服务器 key 注入方式

服务器有两种进程需要 key，注入方式不同：

| 进程类型 | 注入方式 | 原因 |
|---------|---------|------|
| 交互式 shell | `~/.bashrc` source `/root/.secrets` | bashrc 在登录时执行 |
| systemd 服务（OpenClaw） | systemd drop-in `Environment=` | systemd 不读 bashrc |

systemd drop-in 路径：
```
/root/.config/systemd/user/openclaw-gateway.service.d/notion.conf
```

### 历史教训

- `skills-dev/.claude/settings.local.json` 曾有明文 BAIDU_API_KEY 上传到 GitHub
- 已用 `git filter-branch` 重写历史清除，强制推送覆盖
- git remote URL 曾嵌入 token（`https://token@github.com/...`），已改为 credential store

---

## 3. Git 同步机制

### 仓库结构

| 仓库 | 本地路径 | 用途 |
|-----|---------|------|
| arqiao-shared-knowledge | `D:\workspace\kbs\arqiao-shared-knowledge` | 知识库、Skills |
| ccResearch | `D:\workspace\ccResearch` | 研究项目、任务清单 |

### 服务器同步方式

服务器只做只读同步，不在服务器上提交：

```
本地 push → GitHub → 服务器 cron git pull（每天凌晨 3 点）
紧急时：手动 ssh 执行 git pull
```

git pull 策略配置为 `pull.ff only`，确保服务器不会产生 merge commit。
若出现分叉（如本地做了 filter-branch），需手动 `git reset --hard origin/main`。

### GitHub 认证

- 本地：token 存在 `~/.git-credentials`（credential store），remote URL 为干净 URL
- 服务器：token 嵌在 remote URL 中（服务器无交互式输入场景，此方式可接受）

---

## 4. OpenClaw 机器人行为配置

### TOOLS.md 设计

OpenClaw 机器人通过 `/home/openclaw/.openclaw/workspace/TOOLS.md` 了解操作规范。

关键规则：**查询项目进度时直接读本地文件，不要去 Notion 搜索**。

原因：模型默认倾向于调用工具（Notion search），需要明确规则才会优先读本地文件。

### Notion 集成

Notion skill 的 API key 需要通过 systemd drop-in 注入（见第 2 节），
仅配置在 openclaw.json 中不够，因为 skill 运行时读取的是进程环境变量。

---

## 5. ccResearch 目录规范

### 目录用途

| 目录 | 用途 |
|-----|------|
| `D:\workspace\devCC` | 产品化项目 |
| `D:\workspace\ccResearch` | 研究性项目、任务清单 |
| `D:\workspace\mytools` | 个人小工具 |
| `D:\workspace\kbs` | 知识库仓库 |
| `D:\workspace\noshare` | 本地敏感信息（不进 git） |

### .gitignore 排除策略

```
plan-research-claw/   # 旧项目，不同步
kbs-dev/              # 不同步
**/tmp/               # 临时文件
**/drafts/            # 草稿
**/node_modules/
**/data/articles_cache/
**/data/articles_fulltext/
```

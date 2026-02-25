# SKILL.md 规范文档

> 整理自 OpenClaw 内置 Skill，更新于 2026-02-19

## 文件结构

```
skill-name/
├── SKILL.md              # 必需，Skill 定义文件
├── scripts/              # 可选，可执行脚本
├── references/           # 可选，参考文档（按需加载到上下文）
└── assets/               # 可选，输出资源（模板、图片等）
```

## SKILL.md 格式

### 1. YAML Frontmatter（必需）

```yaml
---
name: skill-name
description: 简明描述 Skill 功能和触发场景
metadata: { "openclaw": { ... } }  # 可选
---
```

#### 必需字段

| 字段 | 说明 |
|-----|------|
| `name` | Skill 名称，小写字母+数字+连字符 |
| `description` | 功能描述 + 触发场景，这是 AI 决定是否使用该 Skill 的依据 |

#### 可选 metadata

```yaml
metadata:
  openclaw:
    emoji: "🌤️"           # 显示图标
    os: ["darwin", "linux"]  # 支持的操作系统
    requires:
      bins: ["curl", "tmux"]  # 依赖的命令行工具
```

### 2. Markdown Body（必需）

Skill 被触发后加载的指令内容。

## 三种复杂度示例

### 简单型：weather

```yaml
---
name: weather
description: Get current weather and forecasts (no API key required).
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
---
```

特点：
- 简短 description
- 直接给出可用命令和示例
- 无额外资源文件

### 中等型：tmux

```yaml
---
name: tmux
description: Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
metadata: { "openclaw": { "emoji": "🧵", "os": ["darwin", "linux"], "requires": { "bins": ["tmux"] } } }
---
```

特点：
- 包含 Quickstart 快速上手
- 分场景说明（发送输入、监控输出、清理等）
- 引用 `scripts/` 中的辅助脚本

### 复杂型：healthcheck

```yaml
---
name: healthcheck
description: Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening...
---
```

特点：
- 详细的多步骤工作流（Workflow）
- 明确的确认要求（Required confirmations）
- 条件分支和用户选择

## 核心原则

### 1. 简洁优先

> 上下文窗口是公共资源，只添加 AI 不知道的信息。

- 默认假设 AI 已经很聪明
- 用简洁示例代替冗长解释
- 每段内容都要问："这值得占用 token 吗？"

### 2. 自由度匹配任务

| 自由度 | 适用场景 | 形式 |
|-------|---------|------|
| 高 | 多种方法都可行 | 文字指引 |
| 中 | 有推荐模式但允许变化 | 伪代码/带参数脚本 |
| 低 | 操作脆弱、顺序关键 | 具体脚本、少参数 |

### 3. 渐进式加载

1. **Metadata**（始终加载）：name + description，约 100 词
2. **SKILL.md body**（触发后加载）：< 5000 词
3. **Bundled resources**（按需加载）：无限制

## 命名规范

- 只用小写字母、数字、连字符
- 动词开头，描述动作：`pdf-editor`、`code-review`
- 工具相关可加前缀：`gh-address-comments`
- 长度 < 64 字符

## 不要包含的文件

- README.md
- CHANGELOG.md
- INSTALLATION_GUIDE.md
- 任何面向用户的文档

Skill 只为 AI Agent 服务，不需要人类阅读的辅助文档。

## Description 写作技巧

Description 是触发 Skill 的关键，要包含：

1. **做什么**：核心功能
2. **何时用**：触发场景和关键词

示例：
```
Host security hardening and risk-tolerance configuration for OpenClaw deployments.
Use when a user asks for security audits, firewall/SSH/update hardening, risk posture,
exposure review, OpenClaw cron scheduling for periodic checks, or version status checks
on a machine running OpenClaw.
```

## 参考资源

- OpenClaw 文档：https://docs.openclaw.ai
- skill-creator Skill：可辅助创建规范 Skill
- ClawHub：`npx clawhub search <关键词>`

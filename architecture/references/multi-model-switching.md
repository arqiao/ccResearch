# 多模型切换方案

> 创建时间：2026-02-15
> 状态：方案设计中

---

## 一、需求概述

- 使用多个厂商的 API：MiniMax、Claude 中继服务、其他
- 根据问题类型/难度快速切换模型
- 切换动作要方便（一句话或特殊指令）

---

## 二、OpenClaw 原生支持

OpenClaw 已内置多模型管理能力：

### 2.1 支持的模型提供商

| 提供商 | Provider ID | 认证方式 | 说明 |
|-------|-------------|---------|------|
| Anthropic | `anthropic` | API Key | Claude 官方 |
| OpenAI | `openai` | API Key | GPT 系列 |
| Google | `google` | API Key | Gemini 系列 |
| Z.AI (GLM) | `zai` | API Key | 智谱 GLM |
| Moonshot (Kimi) | `moonshot` | API Key | 月之暗面 |
| OpenRouter | `openrouter` | API Key | 多模型聚合 |
| Groq | `groq` | API Key | 快速推理 |
| 自定义 | 自定义 | API Key | 任意 OpenAI 兼容接口 |

### 2.2 快速切换命令

在 OpenClaw 对话中：

```bash
# 查看可用模型
/model list

# 切换到指定模型（数字选择）
/model 3

# 切换到指定模型（完整名称）
/model anthropic/claude-opus-4-6
/model zai/glm-4.7
/model moonshot/kimi-k2.5

# 查看当前模型状态
/model status
```

### 2.3 CLI 管理命令

```bash
# 查看所有配置的模型
openclaw models list

# 设置默认模型
openclaw models set anthropic/claude-opus-4-6

# 添加模型别名（方便记忆）
openclaw models aliases add claude anthropic/claude-opus-4-6
openclaw models aliases add glm zai/glm-4.7
openclaw models aliases add kimi moonshot/kimi-k2.5

# 配置 fallback（主模型不可用时自动切换）
openclaw models fallbacks add zai/glm-4.7
openclaw models fallbacks add moonshot/kimi-k2.5
```

---

## 三、配置示例

### 3.1 多模型配置（openclaw.json）

```json5
{
  // 环境变量（API Keys）
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-xxx",
    "ZAI_API_KEY": "xxx",
    "MOONSHOT_API_KEY": "sk-xxx",
    "MINIMAX_API_KEY": "xxx"
  },

  "agents": {
    "defaults": {
      // 主模型
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["zai/glm-4.7", "moonshot/kimi-k2.5"]
      },
      // 模型白名单 + 别名
      "models": {
        "anthropic/claude-opus-4-6": { "alias": "Claude Opus" },
        "anthropic/claude-sonnet-4-5": { "alias": "Claude Sonnet" },
        "zai/glm-4.7": { "alias": "GLM" },
        "moonshot/kimi-k2.5": { "alias": "Kimi" },
        "minimax/abab6.5": { "alias": "MiniMax" }
      }
    }
  },

  // 自定义提供商（如 MiniMax、Claude 中继）
  "models": {
    "mode": "merge",
    "providers": {
      // MiniMax 配置
      "minimax": {
        "baseUrl": "https://api.minimax.chat/v1",
        "apiKey": "${MINIMAX_API_KEY}",
        "api": "openai-completions",
        "models": [
          { "id": "abab6.5", "name": "MiniMax ABAB 6.5" },
          { "id": "abab5.5", "name": "MiniMax ABAB 5.5" }
        ]
      },
      // Claude 中继服务配置
      "claude-relay": {
        "baseUrl": "https://your-relay-service.com/v1",
        "apiKey": "${CLAUDE_RELAY_API_KEY}",
        "api": "anthropic",
        "models": [
          { "id": "claude-opus-4-6", "name": "Claude Opus (Relay)" }
        ]
      }
    }
  }
}
```

### 3.2 配置别名后的使用

```bash
# 使用别名切换（更简短）
/model claude
/model glm
/model kimi
/model minimax
```

---

## 四、Skill 方案（智能切换）

可以创建一个 Skill，根据问题类型自动推荐或切换模型：

### 4.1 skills/model-switcher/SKILL.md

```markdown
---
name: model-switcher
description: 根据问题类型智能推荐或切换模型
user-invocable: true
---

# 模型切换助手

当用户说"切换模型"、"用 xxx 模型"、"这个问题用什么模型好"时触发。

## 模型推荐规则

| 问题类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 复杂推理、代码架构 | Claude Opus | 推理能力强 |
| 日常编码、快速问答 | Claude Sonnet / GLM | 性价比高 |
| 中文写作、文案 | MiniMax / Kimi | 中文优化好 |
| 长文本处理 | Kimi | 长上下文支持 |

## 快捷指令

- "用强模型" → 切换到 Claude Opus
- "用快模型" → 切换到 GLM
- "用写作模型" → 切换到 MiniMax
- "用长文本模型" → 切换到 Kimi

## 执行

根据用户意图，执行 `/model <provider/model>` 命令。
```

---

## 五、Claude Code 层面

Claude Code 本身也支持模型切换：

```bash
# 查看当前模型
/model

# 切换模型（Claude 系列内部）
/model sonnet
/model opus
```

但 CC 只能切换 Claude 系列，无法切换到其他厂商。如需使用其他厂商，需要通过 OpenClaw。

---

## 六、推荐方案

### 6.1 短期方案（第一阶段）

1. 在 OpenClaw 中配置多个模型提供商
2. 使用 `/model` 命令手动切换
3. 配置别名简化操作

### 6.2 中期方案（第二阶段）

1. 创建 `model-switcher` Skill
2. 支持语义化切换（"用强模型"、"用便宜的"）
3. 根据问题类型自动推荐

### 6.3 长期方案（可选）

1. 开发 MCP Server 统一管理多模型
2. 支持自动路由（根据问题复杂度自动选择）
3. 成本追踪和优化建议

---

## 八、已确认的模型配置

### 8.1 Claude 中继服务

| 配置项 | 值 |
|-------|-----|
| 提供商 | zjz-ai（私有中继） |
| API 格式 | Anthropic 原生 |
| API 端点 | `https://zjz-ai.webtrn.cn` |
| 认证方式 | `ANTHROPIC_AUTH_TOKEN` |

**Claude Code 配置（~/.claude/settings.json）：**

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-xxx",
    "ANTHROPIC_BASE_URL": "https://zjz-ai.webtrn.cn"
  }
}
```

### 8.2 MiniMax

| 配置项 | 值 |
|-------|-----|
| 提供商 | MiniMax |
| API 格式 | Anthropic 兼容 |
| API 端点 | `https://api.minimaxi.com/anthropic` |
| 模型 ID | `MiniMax-M2.5` |
| 认证方式 | MiniMax API Key |

**Claude Code 配置（~/.claude/settings.json）：**

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "你的MiniMax API Key",
    "API_TIMEOUT_MS": "3000000",
    "ANTHROPIC_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_SMALL_FAST_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.5"
  }
}
```

### 8.3 快速切换方案

由于 Claude 中继和 MiniMax 都使用 Anthropic 兼容格式，切换时需要修改环境变量。

**推荐工具：cc-switch**

MiniMax 官方推荐使用 [cc-switch](https://github.com/farion1231/cc-switch) 工具来快速切换配置：

```bash
# macOS / Linux 安装
brew tap farion1231/ccswitch
brew install --cask cc-switch

# Windows
# 从 GitHub Releases 下载安装包
```

cc-switch 可以保存多个配置方案，一键切换。

### 8.4 OpenClaw 多模型配置

在 OpenClaw 中配置多个提供商：

```json5
{
  "env": {
    "CLAUDE_RELAY_API_KEY": "sk-xxx",
    "MINIMAX_API_KEY": "你的MiniMax API Key"
  },

  "models": {
    "mode": "merge",
    "providers": {
      // Claude 中继
      "claude-relay": {
        "baseUrl": "https://zjz-ai.webtrn.cn",
        "apiKey": "${CLAUDE_RELAY_API_KEY}",
        "api": "anthropic",
        "models": [
          { "id": "claude-opus-4-6", "name": "Claude Opus (Relay)" },
          { "id": "claude-sonnet-4-5", "name": "Claude Sonnet (Relay)" }
        ]
      },
      // MiniMax
      "minimax": {
        "baseUrl": "https://api.minimaxi.com/anthropic",
        "apiKey": "${MINIMAX_API_KEY}",
        "api": "anthropic",
        "models": [
          { "id": "MiniMax-M2.5", "name": "MiniMax M2.5" }
        ]
      }
    }
  },

  "agents": {
    "defaults": {
      "model": {
        "primary": "claude-relay/claude-opus-4-6",
        "fallbacks": ["minimax/MiniMax-M2.5"]
      },
      "models": {
        "claude-relay/claude-opus-4-6": { "alias": "Claude" },
        "minimax/MiniMax-M2.5": { "alias": "MiniMax" }
      }
    }
  }
}
```

**切换命令：**

```bash
/model Claude    # 切换到 Claude 中继
/model MiniMax   # 切换到 MiniMax
```

---

## 九、成本追踪方案

### 9.1 需求

- 追踪各模型的 API 调用次数和费用
- 按日/周/月统计
- 支持多提供商汇总

### 9.2 实现方案

**方案 A：OpenClaw 内置（推荐）**

OpenClaw 有 usage tracking 功能：

```bash
# 查看使用统计
openclaw usage

# 查看详细统计
openclaw usage --detailed
```

**方案 B：自建追踪（如需更细粒度）**

可以开发一个 MCP Server 或 Skill 来：
1. 记录每次 API 调用的 token 数
2. 按模型计算费用（需配置各模型单价）
3. 生成报表

### 9.3 各模型定价参考

| 模型 | 输入价格 | 输出价格 | 说明 |
|-----|---------|---------|------|
| Claude Opus | $15/M tokens | $75/M tokens | 最贵，复杂任务用 |
| Claude Sonnet | $3/M tokens | $15/M tokens | 性价比高 |
| GLM-4 | ¥0.1/K tokens | ¥0.1/K tokens | 国内便宜 |
| MiniMax | 按套餐 | 按套餐 | 你已购买套餐 |
| Kimi | ¥0.06/K tokens | ¥0.06/K tokens | 长文本便宜 |

> 注：价格可能变动，以官方为准

---

## 十、待确认事项

- [x] Claude 中继服务提供商及 API 格式 ✅ 已确认：zjz-ai，Anthropic 原生格式
- [x] MiniMax API 端点和模型 ID ✅ 已确认：api.minimaxi.com/anthropic，MiniMax-M2.5
- [ ] 是否需要自建成本追踪（还是 OpenClaw 内置够用）

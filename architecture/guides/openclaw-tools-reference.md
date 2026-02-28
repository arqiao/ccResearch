# OpenClaw Gateway 工具参考

> 更新时间：2026-02-24
> 服务器：39.107.54.166:18789
> Token 位置：`/root/.openclaw/openclaw.json` → `gateway.auth.token`

---

## 一、两个 HTTP 接口概览

| 接口 | 默认状态 | 用途 |
|------|---------|------|
| `POST /tools/invoke` | 始终启用 | 直接调用单个工具，轻量、精准 |
| `POST /v1/chat/completions` | 默认关闭 | 让 agent 执行完整任务，走完整推理链 |

认证方式相同：`Authorization: Bearer <token>`

---

## 二、/tools/invoke 接口

### 请求格式

```json
{
  "tool": "sessions_list",
  "args": {},
  "sessionKey": "main"
}
```

### 可用工具清单

| 工具名 | 必填参数 | 说明 |
|--------|---------|------|
| `sessions_list` | 无 | 列出所有活跃 session |
| `sessions_history` | `sessionKey`, `limit`(可选) | 获取 session 历史消息 |
| `agents_list` | 无 | 列出 agent 配置 |
| `memory_get` | `path` | 读取 memory（需要 OpenAI/Google key） |
| `memory_search` | `query` | 搜索 memory（需要 OpenAI/Google key） |

### 默认 deny 工具（HTTP 接口不可用）

`sessions_spawn`、`sessions_send`、`gateway`、`whatsapp_login`

其他工具（exec、shell、read_file 等）默认 not_found，需在 `openclaw.json` 的 `tools.allow` 里显式开放。

### 使用示例

**列出所有 session：**
```bash
curl -s http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"tool": "sessions_list", "args": {}}'
```

**查看某个 session 的最近消息：**
```bash
curl -s http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "tool": "sessions_history",
    "args": {
      "sessionKey": "agent:main:feishu:group:oc_3204c7360f0b89f350480ac8f7a130c8",
      "limit": 10
    }
  }'
```

**列出 agent 配置：**
```bash
curl -s http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"tool": "agents_list", "args": {}}'
```

### 开放额外工具

在 `openclaw.json` 中配置：
```json5
{
  "gateway": {
    "tools": {
      "allow": ["gateway"],   // 从默认 deny 列表移除
      "deny": ["browser"]     // 额外禁止的工具
    }
  }
}
```

---

## 三、/v1/chat/completions 接口

### 启用方式

在 `/root/.openclaw/openclaw.json` 中添加：
```json5
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```

然后重启 gateway（或等待自动热重载）：`systemctl --user restart openclaw-gateway`

### 使用示例

**非流式（等待完整响应）：**
```bash
curl -s http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openclaw:main",
    "messages": [{"role": "user", "content": "查一下今天的天气"}]
  }'
```

**流式（SSE，实时输出）：**
```bash
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openclaw:main",
    "stream": true,
    "messages": [{"role": "user", "content": "帮我搜索一下 sing-box 最新版本"}]
  }'
```

**指定 session（保持上下文）：**
```bash
curl -s http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openclaw:main",
    "user": "my-session-id",
    "messages": [{"role": "user", "content": "继续上次的任务"}]
  }'
```

> `user` 字段会派生出稳定的 session key，同一 user 值的多次请求共享上下文。

---

## 四、两个接口的选择建议

| 场景 | 推荐接口 | 原因 |
|------|---------|------|
| 查询 session 状态、历史 | `/tools/invoke` | 轻量，直接返回数据 |
| 触发 agent 执行任务（搜索、写 Notion 等） | `/v1/chat/completions` | 走完整推理链，可用所有 skill |
| 本地 CC 触发服务器 OpenClaw 做事 | `/v1/chat/completions` | 相当于"远程发飞书消息"的替代 |
| 监控/自动化脚本 | `/tools/invoke` | 无需 agent 推理，响应快 |

---

## 五、通过 SSH 隧道访问

本地没有直接暴露 18789 端口，需要先建隧道：

```bash
ssh -N openclaw-tunnel  # 建立隧道，保持运行
```

然后本地访问 `http://127.0.0.1:18789/...`（隧道配置见 `~/.ssh/config`）。

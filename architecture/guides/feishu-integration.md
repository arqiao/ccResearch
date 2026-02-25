# 飞书集成指南

> 创建时间：2026-02-19
> 更新时间：2026-02-20
> 状态：✅ 已完成集成并测试通过

## 一、创建飞书应用

### 1.1 创建应用

1. 访问 https://open.feishu.cn
2. 登录后点击"创建应用" → 选择"企业自建应用"
3. 应用名称：arqiaoknow
4. App ID：cli_a91cbf159238dbcb
5. App Secret：保存在服务器配置文件中（不记录在文档）

### 1.2 配置权限（应用身份权限）

| 权限 | 说明 |
|-----|------|
| im:message:readonly | 读取消息 |
| im:chat:readonly | 读取群信息 |
| im:message:send | 发送消息 |
| contact:contact.base:readonly | 读取联系人基本信息（获取发送者名称） |

### 1.3 配置事件订阅

- 订阅方式：长连接（WebSocket）
- 订阅事件：im.message.receive_v1（接收消息）
- 需要开通权限：
  - 读取用户发给机器人的单聊消息
  - 接收群聊中@机器人消息事件

---

## 二、OpenClaw 内置飞书插件

OpenClaw 内置了 `@openclaw/feishu` 插件，无需自定义 MCP Server。

### 2.1 启用插件

```bash
openclaw plugins enable feishu
```

### 2.2 配置文件

路径：`/root/.openclaw/openclaw.json`

```json
{
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      }
    }
  },
  "channels": {
    "feishu": {
      "appId": "cli_a91cbf159238dbcb",
      "appSecret": "<your-app-secret>",
      "enabled": true,
      "domain": "feishu"
    }
  }
}
```

### 2.3 检查状态

```bash
openclaw channels status
# 输出: Feishu default: enabled, configured, running
```

---

## 三、API Key 配置

### 3.1 auth-profiles.json 格式

路径：`/root/.openclaw/agents/main/agent/auth-profiles.json`

```json
{
  "version": 1,
  "profiles": {
    "anthropic:default": {
      "type": "api_key",
      "provider": "anthropic",
      "key": "<your-api-key>"
    }
  }
}
```

关键点：
- 必须有 `version` 字段
- `profiles` 是嵌套结构
- `type` 为 `api_key` 时，使用 `key` 字段（不是 `token`）

### 3.2 自定义 API 代理地址

在 `openclaw.json` 中添加：

```json
{
  "models": {
    "providers": {
      "anthropic": {
        "baseUrl": "https://your-proxy-url.com",
        "models": []
      }
    }
  }
}
```

### 3.3 验证配置

```bash
openclaw models status --json | jq '.auth'
# 确认 missingProvidersInUse 为空
# 确认 providers 中有 anthropic 且 labels 显示 key 信息
```

---

## 四、服务管理

### 4.1 systemd 服务

```bash
# 查看状态
systemctl --user status openclaw-gateway

# 重启服务
systemctl --user restart openclaw-gateway

# 查看日志
journalctl --user -u openclaw-gateway -f
```

### 4.2 详细日志

```bash
cat /tmp/openclaw-0/openclaw-$(date +%Y-%m-%d).log | tail -50
```

---

## 五、踩坑记录

1. **auth-profiles.json 格式错误**：必须包含 `version` 和 `profiles` 嵌套结构
2. **API key 字段名**：`type: "api_key"` 使用 `key` 字段，不是 `token`
3. **HTTP 403 错误**：使用自定义代理时，需在 `models.providers.anthropic.baseUrl` 配置
4. **权限类型**：飞书权限需申请"应用身份权限"，不是"用户身份权限"

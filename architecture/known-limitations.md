# 已知限制与注意事项

> 创建时间：2026-02-26
> 定位：记录系统运行中发现的已知限制、约束条件和注意事项

---

## 一、飞书消息响应

### 1.1 消息丢失场景

模型切换（修改 openclaw.json + auth-profiles.json）后，OpenClaw Gateway 会自动检测配置变更并热重载。

热重载期间（约 2-3 秒），飞书 WebSocket 连接可能短暂断开，此窗口内到达的消息会丢失（`No reply from agent`）。

**已优化**：switch-llm.py 不再主动 `systemctl restart`，改为依赖 OpenClaw 的 config change 自动热重载，大幅缩短中断窗口。

**残留风险**：热重载仍有短暂中断，无法完全消除。

### 1.2 响应延迟

飞书消息从发送到收到回复，通常需要 9-43 秒。

延迟链路：
```
飞书 → OpenClaw Gateway → 代理(sing-box) → zjz-ai.webtrn.cn → Anthropic API → 原路返回
```

瓶颈在代理链路（服务器 → 中转服务 → Anthropic），无法在当前架构下优化。

---

## 二、OpenClaw Gateway

### 2.1 SIGUSR1 行为

向 OpenClaw 进程发送 SIGUSR1 信号，预期是触发配置热重载，但实际行为是 **full process restart**（supervisor restart），等同于 SIGTERM + 重启。

因此不应使用 SIGUSR1 来触发热重载，应依赖 OpenClaw 自身的配置文件变更检测机制。

### 2.2 配置热重载机制

OpenClaw 会自动监测配置文件变更（openclaw.json、auth-profiles.json 等），检测到变更后执行 `config hot reload applied`，进程 PID 不变。

热重载范围：模型配置、API Key、channel 配置等。
不确定范围：Skills 目录变更是否触发热重载（未验证）。

### 2.3 小内存服务器限制

2G 内存服务器（实际可用约 1.6G）：
- npm install 会 OOM，必须用 pnpm（concurrency=1）
- 需要 4G swap（swappiness=10）
- OpenClaw 运行时内存占用约 200-400MB

---

## 三、网络代理

### 3.1 节点不稳定

代理节点可能随时失效，依赖 cron 每小时自动检测切换。
极端情况下（所有节点不可用），GitHub 同步和 API 调用均会失败。

### 3.2 流量限制

订阅服务有流量上限，低于 100MB 时会发飞书通知。
流量耗尽后需要手动续费或更换订阅。

---

## 四、模型切换

### 4.1 账户余额

中转账户余额不足时，API 调用会失败。
switch-llm.py 支持标记账户当天不可用（`--mark-unavailable`），次日自动恢复。

但目前没有自动检测余额不足的机制，需要人工发现后手动标记。

### 4.2 per-channel model 同步

switch-llm.py 切换时会同步更新 `channels.feishu.agents.defaults.model.primary`。
如果 openclaw.json 中新增了其他 channel，需要手动在脚本中添加同步逻辑。

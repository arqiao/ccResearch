# 已知限制与注意事项

> 创建时间：2026-02-26
> 定位：记录系统运行中发现的已知限制、约束条件和注意事项

---

## 一、飞书消息响应

### 1.1 消息丢失场景

模型切换（修改 openclaw.json + auth-profiles.json）后，OpenClaw Gateway 会自动检测配置变更并热重载。

热重载期间（约 2-3 秒），飞书 WebSocket 连接可能短暂断开，此窗口内到达的消息会丢失（`No reply from agent`）。

**已优化**：switch-my-llm.py 不再主动 `systemctl restart`，改为依赖 OpenClaw 的 config change 自动热重载，大幅缩短中断窗口。

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
switch-my-llm.py 支持标记账户当天不可用（`--mark-unavailable`），次日自动恢复。

但目前没有自动检测余额不足的机制，需要人工发现后手动标记。

### 4.2 per-channel model 同步

switch-my-llm.py 切换时会同步更新 `channels.feishu.agents.defaults.model.primary`。
如果 openclaw.json 中新增了其他 channel，需要手动在脚本中添加同步逻辑。

---

## 五、Skill 改名后的会话历史缓存

### 5.1 问题

Skill 或脚本改名后，飞书机器人可能仍然使用旧名称。

根因：`.jsonl` 会话历史文件中保存了 AI 之前的回复，如果历史回复中包含旧名称，模型会参考历史继续使用旧名。`sessions.json` 中的 `skillsSnapshot` 会在重启时自动更新，但 jsonl 历史不会。

### 5.2 解决方案

改名后执行清理脚本：
```bash
bash ~/workspace/arqiao-shared-knowledge/server-scripts/rename-in-sessions.sh "旧名称" "新名称"
```

此规则已写入 TOOLS.md，OpenClaw 在执行改名操作后会自动调用。

---

## 六、WSL1 Tailscale 网络限制

### 6.1 userspace networking 模式

WSL1 不支持 tun 设备，Tailscale 只能以 `--tun=userspace-networking` 模式运行。此模式下：
- 不创建虚拟网卡，常规 TCP/ICMP 流量不走 Tailscale 网络
- `ping 100.x.x.x` 不通，`ssh 100.x.x.x` 也不通
- 只能通过 Tailscale 提供的 SOCKS5 代理（`--socks5-server=localhost:1055`）访问 Tailscale 网络

### 6.2 解决方案

SSH 配置 ProxyCommand 走 SOCKS5：
```
Host aolong
    HostName 100.72.241.16
    User root
    ProxyCommand nc -x localhost:1055 %h %p

Host aolong-oc
    HostName 100.72.241.16
    User openclaw
    ProxyCommand nc -x localhost:1055 %h %p
```

HTTP 请求走 SOCKS5：
```bash
curl -x socks5://localhost:1055 http://100.72.241.16:18789/
```

---

## 七、pnpm 跨用户迁移

### 7.1 shell wrapper 硬编码路径

pnpm 全局安装的命令（如 `openclaw`）会生成 shell wrapper 脚本，其中 `NODE_PATH` 是硬编码的绝对路径。从 root 迁移到 openclaw 用户时，wrapper 中仍指向 `/root/.local/share/pnpm/`，导致命令找不到模块。

修复方式：
```bash
sed -i 's|/root/.local/share/pnpm|/home/openclaw/.local/share/pnpm|g' ~/.local/share/pnpm/openclaw
```

### 7.2 .bashrc 非交互式 guard

Ubuntu 默认 `.bashrc` 开头有非交互式 guard：
```bash
case $- in *i*) ;; *) return;; esac
```

通过 `su - user -c "command"` 或 systemd 执行命令时，shell 是非交互式的，`.bashrc` 会直接 return，其中设置的环境变量（如 PNPM_HOME、代理）不会生效。

解决方案：将非交互式也需要的环境变量放在 `~/.profile` 中。

---

## 八、服务器用户分离

### 8.1 澳龙用户职责

| 用户 | 职责 | 服务 |
|------|------|------|
| openclaw | OpenClaw 服务运行 | openclaw-gateway、account-switcher（systemd user）、frps、switch-proxy.py（cron，sudo 重启 sing-box） |
| root | 系统级服务 | sing-box、tailscaled |

root 下仅保留系统级守护进程（sing-box、tailscaled），其余全部在 openclaw 用户下运行。switch-proxy.py 通过 sudoers 授权重启 sing-box。

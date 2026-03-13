# 我的龙虾资产库

> 创建时间：2026-03-13
> 定位：从资产视角总览——我有哪些龙虾，每只能干什么，怎么连上它

---

## 一、龙虾一览

| 名称 | 定位 | OpenClaw | 状态 |
|------|------|----------|------|
| 云船 | 主力 OpenClaw 服务器 | 已部署（#1） | 运行中 |
| 澳龙 | frp 中继 + 代理出口 + 备用 OpenClaw | 已部署（#2） | 运行中 |
| 草莓派 | 家庭自托管 OpenClaw（零成本长期运行） | 待部署（#3） | 待实施 |
| 笔记本 | 日常开发、Claude Code | 待部署（#4） | 待实施 |
| 手机 | 移动端飞书交互 | 待部署（#5） | 待实施 |

---

## 二、云船——主力龙虾（OpenClaw #1）

### 软硬件配置

| 项目 | 配置 |
|------|------|
| 宿主机 | 联通云智电脑（Windows 10） |
| 公网 IP | 195.64.7.45（入站被平台拦截，无法直接访问） |
| Tailscale IP | 100.115.214.108 |
| CPU | 8 核 |
| 内存 | 16 GB（WSL1 与宿主机共享） |
| 磁盘 | 200 GB（C盘 79G + D盘 119G，WSL1 数据在 D 盘） |
| 带宽 | 100 Mbps 共享 |
| 操作系统 | Ubuntu 24.04 LTS（WSL1） |
| 虚拟化 | WSL1（系统调用翻译层，不支持 Docker/systemd） |
| 用户 | arqiaoclaw |
| Node.js | 22.x |
| 包管理器 | pnpm |

### 能干什么

- 跑 OpenClaw Gateway（飞书机器人的大脑，端口 18789）
- 跑 account-manager 网页（切模型、切账户，端口 19528）
- 给澳龙提供 HTTP 代理（simple-proxy.py，端口 1080）
- frp 客户端（把自己的 SSH 穿透到澳龙公网）
- Tailscale 组网节点
- 定时任务：知识库同步、配置备份、系统/OpenClaw 版本检查

### 怎么连

| 方式 | 命令 |
|------|------|
| SSH（日常首选） | `ssh -p 12222 arqiaoclaw@39.107.54.166` |
| SSH（Tailscale 备用） | `ssh arqiaoclaw@100.115.214.108` |
| OpenClaw 控制台 | 先建隧道，再访问 `http://localhost:18789` |
| account-manager | 先建隧道，再访问 `http://localhost:19528` |

一键建隧道：
```bash
ssh -N -L 18789:localhost:18789 -L 19528:localhost:19528 -p 12222 arqiaoclaw@39.107.54.166
```

> 控制台必须走 localhost 隧道，直接用 IP 会报 device identity 错误。

### 跑了哪些服务

| 服务 | 启动用户 | 端口 | 启动方式 |
|------|---------|------|---------|
| SSH | root | 22 | `service ssh start`（WSL1 无 systemd） |
| tailscaled | root | — | nohup，`--tun=userspace-networking --socks5-server=localhost:1055` |
| frpc | arqiaoclaw | — | nohup，隧道 22→12222，连接澳龙 frps |
| simple-proxy.py | arqiaoclaw | 1080 | nohup，HTTP 代理供澳龙访问云船网络 |
| openclaw gateway | arqiaoclaw | 18789 | nohup，飞书机器人后端 |
| account-manager.js | arqiaoclaw | 19528 | nohup，账户/模型管理网页 |

所有服务由联通云智电脑的 `start-openclaw.bat` 在 Windows 登录后自动启动（详见第八节）。

### 定时任务

| 周期 | 干什么 | 日志 |
|------|--------|------|
| 每天 03:00 | 知识库 git pull | `~/log/cron-kbs-sync.log` |
| 每周日 02:00 | 配置备份 | `~/log/cron-backup.log` |
| 每月1日 04:00 | 系统更新检查 | `~/log/cron-system-update.log` |
| 每周一 03:00 | OpenClaw 版本检查 | `~/log/cron-openclaw-update.log` |

### 日志目录（~/log/）

| 文件 | 来源 |
|------|------|
| `openclaw-gateway.log` | OpenClaw 主服务 |
| `account-manager.log` | 账户/模型管理网页 |
| `frpc.log` | frp 客户端隧道 |
| `tailscaled.log` | Tailscale 守护进程 |
| `simple-proxy.log` | HTTP 代理 |
| `cron-kbs-sync.log` | 知识库同步 |
| `cron-backup.log` | 配置备份 |
| `cron-system-update.log` | 系统更新检查 |
| `cron-openclaw-update.log` | OpenClaw 版本检查 |

### 个性化脚本（~/local/scripts/）

| 脚本 | 用途 |
|------|------|
| simple-proxy.py | HTTP 代理服务（0.0.0.0:1080），供澳龙使用 |
| cloud-ship-switch-proxy.sh | 代理切换（aolong/local/direct） |
| backup_openclaw.sh | 配置备份 |

### OpenClaw 配置

| 文件 | 路径 |
|------|------|
| 主配置 | `~/.openclaw/openclaw.json` |
| 认证配置 | `~/.openclaw/agents/main/agent/auth-profiles.json` |
| Skills 目录 | `~/workspace/arqiao-shared-knowledge/skills/` |
| 密钥文件 | `~/local/.secrets`（chmod 600） |
| 账户数据 | `~/local/.secrets.accounts.json`（chmod 600） |

可用账户：arqiao-tsinghua、arqiao-sina、arqiao-test、arqiao-minimax

### 限制

- WSL1 无 systemd，所有进程用 nohup 管理
- Tailscale 只能走 SOCKS5 代理（localhost:1055），不能直接 TCP
- 联通云平台拦截所有入站端口，必须靠 frp 穿透

---

## 三、澳龙——中继龙虾（OpenClaw #2）

### 软硬件配置

| 项目 | 配置 |
|------|------|
| 平台 | 阿里云轻量应用服务器 |
| 公网 IP | 39.107.54.166（固定） |
| Tailscale IP | 100.72.241.16 |
| CPU | 2 核 |
| 内存 | 2 GB（实际可用约 1.6G，内核预留约 400MB） |
| 磁盘 | 40 GB SSD |
| Swap | 4 GB（swappiness=10） |
| 带宽 | 3 Mbps |
| 操作系统 | Ubuntu |
| 用户 | openclaw（自建服务）、root（仅 sing-box + tailscaled） |
| Node.js | 22.x |
| 包管理器 | pnpm（concurrency=1，内存限制） |

### 能干什么

- frp 服务端（中继云船的 SSH 到公网 12222 端口）
- 代理出口（sing-box，给自己和云船提供翻墙代理）
- 备用 OpenClaw Gateway（云船挂了可以顶上）
- 备用 account-manager（account-switcher 服务）
- Tailscale 组网节点
- 定时任务：知识库同步、配置备份、系统/OpenClaw 版本检查、代理节点自动切换

### 怎么连

| 方式 | 命令 |
|------|------|
| SSH（服务管理） | `ssh openclaw@39.107.54.166` |
| SSH（系统管理） | `ssh root@39.107.54.166` |
| SSH（Tailscale） | `ssh openclaw@100.72.241.16` |
| OpenClaw 控制台 | `http://100.72.241.16:18789`（Tailscale 内直接访问） |

### 跑了哪些服务

| 服务 | 用户 | 端口 | 管理方式 |
|------|------|------|---------|
| openclaw-gateway | openclaw | 18789 | `systemctl --user start/stop/restart openclaw-gateway` |
| account-switcher | openclaw | 19528 | `systemctl --user start/stop/restart account-switcher` |
| frps | openclaw | 7000 | nohup（`~/frp_0.61.0_linux_amd64/`） |
| sing-box | root | 7890(HTTP)/7891(SOCKS5) | `systemctl start/stop sing-box` |
| tailscaled | root | — | `systemctl start/stop tailscaled` |

> openclaw 用户已启用 `loginctl linger`，systemd user 服务在无登录会话时持续运行。
> switch-proxy.py 需重启 sing-box，通过 sudoers 授权：`openclaw ALL=(root) NOPASSWD: /usr/bin/systemctl restart sing-box`

### 定时任务（openclaw 用户）

| 周期 | 干什么 | 日志 |
|------|--------|------|
| 每天 03:00 | 知识库 git pull | `~/log/cron-kbs-sync.log` |
| 每周日 02:00 | 配置备份 | `~/log/cron-backup.log` |
| 每月1日 04:00 | 系统更新检查 | `~/log/cron-system-update.log` |
| 每周一 03:00 | OpenClaw 版本检查 | `~/log/cron-openclaw-update.log` |
| 每小时 | 代理节点自动切换（测速选最优） | `~/log/cron-switch-proxy.log` |

### 日志目录（~/log/）

| 文件 | 来源 |
|------|------|
| `frps.log` | frp 服务端 |
| `cron-kbs-sync.log` | 知识库同步 |
| `cron-backup.log` | 配置备份 |
| `cron-system-update.log` | 系统更新检查 |
| `cron-openclaw-update.log` | OpenClaw 版本检查 |
| `cron-switch-proxy.log` | 代理节点切换 |

> gateway 和 account-switcher 的日志走 systemd journalctl，不在 ~/log/ 中。

### 个性化脚本（~/local/scripts/）

| 脚本 | 用途 |
|------|------|
| switch-proxy.py | 代理节点自动切换（解析订阅、测速、选最优，需 sudo 重启 sing-box） |
| switch-proxy.sh | 手动代理切换（yunchuan/local/direct） |
| backup_openclaw.sh | 配置备份 |

### OpenClaw 配置

| 文件 | 路径 |
|------|------|
| 主配置 | `~/.openclaw/openclaw.json` |
| 认证配置 | `~/.openclaw/agents/main/agent/auth-profiles.json` |
| Skills 目录 | `~/workspace/arqiao-shared-knowledge/skills/` |
| 密钥文件 | `~/local/.secrets`（chmod 600） |
| 账户数据 | `~/local/.secrets.accounts.json`（chmod 600） |
| 环境变量 | `~/.profile`（PNPM_HOME、代理设置） |
| systemd 服务 | `~/.config/systemd/user/openclaw-gateway.service` |
| systemd drop-in | `~/.config/systemd/user/openclaw-gateway.service.d/notion.conf`（Notion API Key 注入） |

### 限制

- 只有 2G 内存，npm install 会 OOM，必须用 pnpm
- 需要 4G swap（swappiness=10）

---

## 四、草莓派——家庭龙虾（OpenClaw #3，待部署）

### 软硬件配置

| 项目 | 配置 |
|------|------|
| 型号 | Raspberry Pi 5 |
| CPU | Broadcom BCM2712，4 核 Cortex-A76 @ 2.4GHz |
| 内存 | 8 GB |
| 存储 | 32 GB MicroSD（建议升级外接 SSD） |
| 电源 | 5V 5A USB-C |
| 网络 | 千兆以太网 + WiFi 6 |
| 操作系统 | 计划安装 Raspberry Pi OS Lite (64-bit) |
| 散热 | 需主动散热（长期运行） |
| 位置 | 家中，通过 Tailscale 组网 |

### 规划用途

- 家庭自托管 OpenClaw（零月租，长期运行）
- 通过 Tailscale 内网穿透，笔记本/手机直连
- 云船稳定后，可能替代澳龙的角色（V19 待定）

### 部署计划

详见 `guides/deploy-raspberry-pi.md`，主要步骤：
1. 烧录系统（Raspberry Pi Imager）
2. 配置 tmpfs（减少 SD 卡写入）
3. 安装 Node.js 22 + pnpm + OpenClaw
4. 安装 Tailscale
5. 从云船迁移配置
6. 配置知识库同步和 cron 任务

---

## 五、笔记本——待部署龙虾（OpenClaw #4）

### 软硬件配置

| 项目 | 配置 |
|------|------|
| 操作系统 | Windows 11 Pro |
| Tailscale IP | 100.100.153.29 |

### 用途

- 日常开发（VS Code、Claude Code）
- 通过 MobaXterm 管理云船和澳龙
- 通过 SSH 隧道访问 OpenClaw 控制台和 account-manager
- 知识库编辑和 git push（ccResearch、arqiao-shared-knowledge）

### 关键工具

| 工具 | 用途 |
|------|------|
| Claude Code | AI 辅助开发 |
| VS Code | 代码编辑 |
| MobaXterm | SSH 会话管理（含端口转发） |
| Tailscale | 内网组网 |
| Git | 知识库同步 |

---

## 六、手机——待部署龙虾（OpenClaw #5）

### 配置

| 项目 | 配置 |
|------|------|
| 操作系统 | Android |
| Tailscale IP | 100.71.142.90 |

### 用途

- 通过飞书 App 与 OpenClaw 机器人对话（自然语言交互）
- 接收飞书通知（系统告警、流量不足等）
- 不直接访问 OpenClaw 控制台（HTTP + 非 localhost 无法生成 device identity）

---

## 七、龙虾们共有的 Skills（30 个）

两台龙虾的 Skills 完全一致，通过 `arqiao-shared-knowledge/skills/` git 同步。

### 飞书相关

| Skill | 说明 |
|-------|------|
| check-feishu-group | 飞书群消息查看 |
| check-feishu-msg | 飞书消息查看 |
| feishu-doc | 飞书文档读取 |
| read-feishu-doc | 飞书文档读取（别名） |
| write-feishu-doc | 飞书文档写入 |
| feishu-sheet | 飞书表格操作 |
| send-feishu-msg | 飞书消息发送 |

### 运维管理

| Skill | 说明 |
|-------|------|
| manage-cron | Cron 任务管理 |
| manage-openclaw-config | OpenClaw 配置管理 |
| manage-skills | Skills 管理 |
| manage-system-service | 系统服务管理 |
| system-info | 系统信息查看 |
| system-status | 系统状态查看 |
| tail-log | 日志查看 |
| update-openclaw | OpenClaw 更新 |
| run-script | 脚本执行 |
| git-sync | Git 仓库同步 |

### 模型与账户

| Skill | 说明 |
|-------|------|
| switch-my-llm | LLM 模型切换 |
| switch-my-account | 账户切换 |
| switch-proxy | 代理切换 |
| proxy-status | 代理状态查看 |

### 信息获取

| Skill | 说明 |
|-------|------|
| baidu-search | 百度搜索 |
| search-web | 网页搜索 |
| read-article | 文章抓取阅读 |
| notion-reader | Notion 读取 |
| my-knowledge | 知识库查询 |
| my-tasks | 任务清单管理 |
| my-files | 文件管理 |
| weather | 天气查询 |

### 创作

| Skill | 说明 |
|-------|------|
| video-gen | 视频生成（火山引擎 Seedance） |

> 目前没有任何龙虾专属的 Skill，所有 Skills 两台龙虾完全一致。

---

## 八、龙虾之间怎么互通

### 网络拓扑

```
笔记本 ──SSH隧道──→ 澳龙:12222 ──frp──→ 云船:22
笔记本 ──Tailscale──→ 云船 / 澳龙
手机   ──飞书App──→ 飞书服务器 ──WebSocket──→ 云船 OpenClaw
云船   ──SOCKS5代理──→ 澳龙（Tailscale userspace networking 限制）
澳龙   ──SSH直连──→ 云船（frp 或 Tailscale）
云船   ←──HTTP代理(1080)──→ 澳龙（双向代理，各用对方的出口）
```

### Tailscale 设备列表

| 设备 | Tailscale IP |
|------|-------------|
| 云船 | 100.115.214.108 |
| 澳龙 | 100.72.241.16 |
| 草莓派 | 待分配 |
| 笔记本 | 100.100.153.29 |
| 手机 | 100.71.142.90 |

### 跨服务器 SSH 配置

云船 `~/.ssh/config`：
```
Host aolong
    HostName 100.72.241.16
    User root
    ProxyCommand nc -x localhost:1055 %h %p

Host aolong-oc
    HostName 100.72.241.16
    User openclaw
    ProxyCommand nc -x localhost:1055 %h %p

Host aolong-pub
    HostName 39.107.54.166
    User root
```

> 云船 WSL1 的 Tailscale 是 userspace-networking 模式，必须走 SOCKS5 代理（localhost:1055）。

澳龙 `~/.ssh/config`（openclaw 用户）：
```
Host yunchuan
    HostName 39.107.54.166
    Port 12222
    User arqiaoclaw

Host yunchuan-ts
    HostName 100.115.214.108
    User arqiaoclaw
```

### 双向代理机制

两台龙虾互为代理出口，各用对方的网络，防止循环：

| 方向 | 命令 | 代理地址 |
|------|------|---------|
| 云船 → 澳龙 | `~/local/scripts/cloud-ship-switch-proxy.sh aolong` | 澳龙 sing-box 出口 |
| 澳龙 → 云船 | `~/local/scripts/switch-proxy.sh yunchuan` | 云船 simple-proxy.py:1080 |

代理设置持久化到 `~/local/.proxy_env`，包括 `http_proxy`/`https_proxy` 环境变量和 `git config`。

---

## 九、联通云智电脑——云船的壳

### 软硬件配置

| 项目 | 配置 |
|------|------|
| 平台 | 联通云智电脑 |
| 公网 IP | 195.64.7.45（入站被平台拦截） |
| CPU | 8 核（与云船共享） |
| 内存 | 16 GB（与云船共享） |
| 磁盘 | C盘 79G + D盘 119G |
| 操作系统 | Windows 10 |
| 访问方式 | 联通专属客户端（无网页版控制台） |

> 仅负责启动 WSL1 和运行 `start-openclaw.bat`，不直接跑 Linux 服务。

### 启动流程

1. 手动打开联通云"云电脑"客户端（无法完全自动化）
2. Windows 自动登录（已配置注册表 AutoAdminLogon）
3. 启动文件夹自动运行 `C:\Users\Administrator\start-openclaw.bat`
4. 脚本等待 WSL 就绪（最多 60 秒，每 5 秒检测一次）
5. WSL 启动后依次启动云船内服务：
   - SSH 服务（root）
   - Tailscale（root，userspace-networking 模式）
   - frpc 隧道（arqiaoclaw）
   - simple-proxy.py（arqiaoclaw）
   - OpenClaw Gateway（arqiaoclaw）
   - account-manager.js（arqiaoclaw）

### 关键文件

| 文件 | 路径 |
|------|------|
| 启动脚本 | `C:\Users\Administrator\start-openclaw.bat` |
| 启动快捷方式 | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw.lnk` |

> 详细部署步骤见 `guides/deploy-cloud-wsl1-frp.md` 第十节。

---

## 十、两台龙虾共有的通用脚本

路径：`~/workspace/arqiao-shared-knowledge/server-scripts/`（git 同步，两台完全一致）

| 脚本 | 用途 |
|------|------|
| feishu_send.py | 飞书消息通知（被其他脚本调用） |
| notify.sh | 通知包装（调用 feishu_send.py） |
| switch-my-llm.py | LLM 模型切换（修改 openclaw.json + auth-profiles.json） |
| switch-my-account.js | 账户切换 |
| account-manager.js | 账户/模型管理网页（端口 19528，含模型切换标签页） |
| check_openclaw_update.sh | OpenClaw 版本检查（cron 调用） |
| check_system_update.sh | 系统更新检查（cron 调用） |
| rename-in-sessions.sh | Skill 改名后清理 .jsonl 会话历史 |
| sync-myskills-list.py | 扫描本机 Skills，生成 ~/local/myskills.json |

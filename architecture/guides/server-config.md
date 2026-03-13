# 服务器配置

> 各服务器的目录规范、密钥存储、脚本路径、账户配置

## 目录规范

### 设计原则

| 目录 | 定位 | 同步策略 |
|------|------|---------|
| `~/workspace/` | 通用内容，各服务器文件名和内容完全一致 | git pull 直接覆盖 |
| `~/local/` | 个性化内容，文件名一致但内容按服务器定制 | 手动维护，不能盲目覆盖 |
| `~/log/` | 服务和 cron 日志，统一存放 | 不同步，各服务器独立 |
| `~/.openclaw/` | OpenClaw 运行时配置和数据 | 脚本自动维护 |

### 通用目录（~/workspace/）

```
~/workspace/
├── arqiao-shared-knowledge/       # 知识库（git 同步）
│   ├── skills/                    # Skills
│   └── server-scripts/            # 通用运维脚本
│       ├── feishu_send.py         # 飞书通知
│       ├── notify.sh              # 通知包装
│       ├── check_openclaw_update.sh # 版本检查
│       ├── check_system_update.sh # 系统更新检查
│       ├── switch-my-llm.py       # LLM 切换
│       ├── switch-my-account.js   # 账户切换
│       ├── rename-in-sessions.sh  # Skill 改名后清理会话历史
│       ├── sync-myskills-list.py  # 生成 ~/local/myskills.json
│       ├── startup-check.sh       # 启动自检+飞书通知
│       └── service-watchdog.sh    # cron 服务守护+自动重启
└── ccResearch/                    # 项目文档（git 同步）
```

### 个性化目录（~/local/）

```
~/local/
├── .secrets                       # API 密钥（chmod 600）
├── .secrets.accounts.json         # 账户数据（chmod 600）
├── .proxy_env                     # 代理环境变量持久化
├── myskills.json                  # 本机 Skills 清单（脚本自动生成）
└── scripts/                       # 个性化脚本
    ├── backup_openclaw.sh         # 配置备份（路径因服务器而异）
    ├── cloud-ship-switch-proxy.sh # 代理切换（云船版）
    ├── simple-proxy.py            # HTTP 代理服务（云船版）
    └── switch-proxy.sh            # 代理切换（澳龙版）
```

> 新增服务器时：`~/workspace/` 直接 git clone 即可；`~/local/` 需要手动创建并填入本机的密钥和脚本。

---

## 云船（联通云 WSL1）

> 公网 IP: 195.64.7.45（被平台拦截，无法直接访问）
> Tailscale IP: 100.115.214.108
> SSH: `ssh -p 12222 arqiaoclaw@39.107.54.166`（通过 frp 隧道）

### 密钥存储

| 文件 | 用途 | 权限 |
|------|------|------|
| `~/local/.secrets` | 第三方 API keys（百度/火山/Notion/飞书/GitHub） | 600 |
| `~/local/.secrets.accounts.json` | 4个 Claude 账户的 baseUrl + apiKey | 600 |

### 账户数据

```
arqiao-tsinghua: zjz-ai 中转（清华大学）
arqiao-sina: zjz-ai 中转（新浪）
arqiao-test: zjz-ai 中转（测试）
arqiao-minimax: MiniMax（sk-cp-...）
```

### 个性化脚本（~/local/scripts/）

- `backup_openclaw.sh` - 配置备份
- `cloud-ship-switch-proxy.sh` - 代理切换（aolong/local/direct）
- `simple-proxy.py` - HTTP 代理服务（0.0.0.0:1080，供澳龙使用）

### cron 任务

```
0 3 * * *    知识库同步          >> ~/log/cron-kbs-sync.log 2>&1
0 2 * * 0    配置备份            >> ~/log/cron-backup.log 2>&1
0 4 1 * *    系统更新检查        >> ~/log/cron-system-update.log 2>&1
0 3 * * 1    OpenClaw 版本检查   >> ~/log/cron-openclaw-update.log 2>&1
*/10 * * * * 服务守护(watchdog)  >> ~/log/cron-watchdog.log 2>&1
```

### 日志目录（~/log/）

| 文件 | 来源 | 说明 |
|------|------|------|
| `openclaw-gateway.log` | start-openclaw.bat | OpenClaw 主服务 |
| `account-manager.log` | start-openclaw.bat | 账户/模型管理网页 |
| `frpc.log` | start-openclaw.bat | frp 客户端隧道 |
| `tailscaled.log` | start-openclaw.bat | Tailscale（root 启动） |
| `simple-proxy.log` | start-openclaw.bat | HTTP 代理 |
| `cron-kbs-sync.log` | crontab | 知识库同步 |
| `cron-backup.log` | crontab | 配置备份 |
| `cron-system-update.log` | crontab | 系统更新检查 |
| `cron-openclaw-update.log` | crontab | OpenClaw 版本检查 |
| `cron-watchdog.log` | crontab | 服务守护（每 10 分钟） |

### 开机自启服务（联通云智电脑 start-openclaw.bat → 启动云船内服务）

> **前提**：联通云智电脑必须先手动打开"云电脑"客户端，云主机才会上线。
> 启动后 startup-check.sh 会自检并发飞书通知，手机上即可确认服务状态。

| 服务 | 用户 | 说明 |
|------|------|------|
| SSH (service ssh start) | root | frp 穿透依赖 |
| tailscaled | root | Tailscale 内网（WSL1 需 userspace-networking） |
| frpc | arqiaoclaw | SSH + 端口穿透到澳龙 |
| simple-proxy.py | arqiaoclaw | HTTP 代理（0.0.0.0:1080），供澳龙使用 |
| openclaw gateway | arqiaoclaw | OpenClaw 主服务 |
| account-manager.js | arqiaoclaw | 账户/模型管理网页（端口 19528） |

### OpenClaw 配置

- 配置文件: `~/.openclaw/openclaw.json`
- 认证文件: `~/.openclaw/agents/main/agent/auth-profiles.json`（运行时由脚本维护）
- Skills 目录: `~/workspace/arqiao-shared-knowledge/skills/`
- 管理工具: `~/workspace/arqiao-shared-knowledge/server-scripts/account-manager.js`（端口 19528）

### 本机信息

- Skills 清单: `~/local/myskills.json`（由 `server-scripts/sync-myskills-list.py` 自动生成）

---

## 澳龙（阿里云）

> 公网 IP: 39.107.54.166
> Tailscale IP: 100.72.241.16
> SSH: `ssh root@39.107.54.166`（系统管理）或 `ssh openclaw@39.107.54.166`（OpenClaw 服务）
> 用户：openclaw（所有自建服务），root（仅 sing-box + tailscaled 等系统级服务）

### 密钥存储

| 文件 | 用途 | 权限 |
|------|------|------|
| `/home/openclaw/local/.secrets` | 第三方 API keys | 600 |
| `/home/openclaw/local/.secrets.accounts.json` | 账户数据 | 600 |

### 服务管理

| 服务 | 用户 | 管理方式 | 说明 |
|------|------|---------|------|
| openclaw-gateway | openclaw | `systemctl --user start/stop/restart openclaw-gateway` | OpenClaw 主服务 |
| account-switcher | openclaw | `systemctl --user start/stop/restart account-switcher` | 账户/模型管理网页 |
| frps | openclaw | nohup（`~/frp_0.61.0_linux_amd64/`） | frp 服务端（中继） |
| sing-box | root | `systemctl start/stop sing-box` | 代理出口 |
| tailscaled | root | `systemctl start/stop tailscaled` | Tailscale 内网 |

> openclaw 用户已启用 loginctl linger，服务在无登录会话时也持续运行。
> switch-proxy.py 需重启 sing-box，通过 sudoers 授权：`openclaw ALL=(root) NOPASSWD: /usr/bin/systemctl restart sing-box`

### 个性化脚本（~/local/scripts/）

- `backup_openclaw.sh` - 配置备份
- `switch-proxy.sh` - 代理切换（yunchuan/local/direct）
- `switch-proxy.py` - 代理节点自动切换（解析订阅，测速选最优，需 sudo 重启 sing-box）

### cron 任务

openclaw 用户：
```
0 3 * * *  知识库同步          >> ~/log/cron-kbs-sync.log 2>&1
0 2 * * 0  配置备份            >> ~/log/cron-backup.log 2>&1
0 4 1 * *  系统更新检查        >> ~/log/cron-system-update.log 2>&1
0 3 * * 1  OpenClaw 版本检查   >> ~/log/cron-openclaw-update.log 2>&1
0 * * * *  代理节点自动切换    >> ~/log/cron-switch-proxy.log 2>&1
```

### 日志目录（~/log/）

| 文件 | 来源 | 说明 |
|------|------|------|
| `frps.log` | nohup | frp 服务端 |
| `cron-kbs-sync.log` | crontab | 知识库同步 |
| `cron-backup.log` | crontab | 配置备份 |
| `cron-system-update.log` | crontab | 系统更新检查 |
| `cron-openclaw-update.log` | crontab | OpenClaw 版本检查 |
| `cron-watchdog.log` | crontab | 服务守护（每 10 分钟） |
| `cron-switch-proxy.log` | crontab | 代理节点切换 |

> gateway 和 account-switcher 的日志走 systemd journalctl，不在 ~/log/ 中。

### OpenClaw 配置

- 配置文件: `~/.openclaw/openclaw.json`
- 认证文件: `~/.openclaw/agents/main/agent/auth-profiles.json`
- Skills 目录: `~/workspace/arqiao-shared-knowledge/skills/`
- 管理工具: `~/workspace/arqiao-shared-knowledge/server-scripts/account-manager.js`（端口 19528）
- 环境变量: `~/.profile`（PNPM_HOME、代理设置）

---

## 同步机制

### 通用脚本同步

通用脚本在 `arqiao-shared-knowledge/server-scripts/` 中，git pull 即可同步：

```bash
cd ~/workspace/arqiao-shared-knowledge && git pull
```

### 密钥同步

密钥文件不在 git 中，需手动同步：

```bash
# 云船 → 澳龙
scp ~/local/.secrets openclaw@39.107.54.166:/home/openclaw/local/.secrets
scp ~/local/.secrets.accounts.json openclaw@39.107.54.166:/home/openclaw/local/.secrets.accounts.json
```

### 代理切换

```bash
# 云船代理切换
~/local/scripts/cloud-ship-switch-proxy.sh aolong   # 切换到澳龙代理
~/local/scripts/cloud-ship-switch-proxy.sh local     # 切换到本地代理
~/local/scripts/cloud-ship-switch-proxy.sh direct    # 不使用代理
~/local/scripts/cloud-ship-switch-proxy.sh status    # 查看当前状态

# 澳龙代理切换
~/local/scripts/switch-proxy.sh yunchuan   # 切换到云船代理
~/local/scripts/switch-proxy.sh local      # 切换到本地代理
~/local/scripts/switch-proxy.sh direct     # 不使用代理
```

# 服务器配置

> 各服务器的密钥存储、脚本路径、账户配置

## 云船（联通云 WSL1）

> 公网 IP: 195.64.7.45（被平台拦截，无法直接访问）
> Tailscale IP: 100.115.214.108
> SSH: `ssh -p 12222 arqiaoclaw@39.107.54.166`（通过 frp 隧道）

### 密钥存储

> 密钥放在 `~/local/` 目录下，与用户目录分离

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

### 脚本目录

- 运维脚本: `~/scripts/`
  - `feishu_send.py` - 飞书通知
  - `notify.sh` - 通知包装
  - `backup_openclaw.sh` - 配置备份
  - `check_openclaw_update.sh` - 版本检查
  - `check_system_update.sh` - 系统更新检查
  - `switch-my-llm.py` - LLM 切换

- 账户切换: `~/.openclaw/`
  - `account-switcher.js` - 账户切换网页（端口 19528）
  - `switch-account.js` - 账户切换脚本

### cron 任务

```
0 3 * * *  知识库同步
0 2 * * 0  配置备份
0 4 1 * *  系统更新检查
0 3 * * 1  OpenClaw 版本检查
```

### OpenClaw 配置

- 配置文件: `~/.openclaw/openclaw.json`
- 认证文件: `~/.openclaw/agents/main/agent/auth-profiles.json`（运行时由脚本维护）
- Skills 目录: `~/workspace/arqiao-shared-knowledge/skills/`

### 共享信息（供 CC 读取）

- Skills 清单: `~/local/share-cc/skills.json`（自动生成）
- 生成脚本: `~/local/share-cc/sync-skills-list.py`

> 详细设计见 [shared-info-design.md](./shared-info-design.md)

---

## 澳龙（阿里云）

> 公网 IP: 39.107.54.166
> Tailscale IP: 100.72.241.16
> SSH: `ssh root@39.107.54.166`

### 密钥存储

| 文件 | 用途 | 权限 |
|------|------|------|
| `/root/local/.secrets` | 第三方 API keys | 600 |
| `/root/local/.secrets.accounts.json` | 账户数据 | 600 |

> ✅ 已完成：accounts.json 已移至 `local/.secrets.accounts.json`，脚本路径已更新

---

## 同步机制

> 两个服务器使用相同的目录结构，修改后只需同步 .secrets 文件即可

### 密钥同步

密钥文件不在 git 中（.secrets 已在 .gitignore），需手动同步：

```bash
# 云船 → 澳龙（云船本地执行）
scp -P 12222 arqiaoclaw@39.107.54.166:~/local/.secrets root@39.107.54.166:/root/local/.secrets
scp -P 12222 arqiaoclaw@39.107.54.166:~/local/.secrets.accounts.json root@39.107.54.166:/root/local/.secrets.accounts.json
```

### 脚本/Skills 同步

| 服务器 | GitHub 访问方式 | 备注 |
|--------|----------------|------|
| 澳龙 | 通过代理（sing-box 127.0.0.1:7890） | source ~/.bashrc 后可 git pull |
| 云船 | 暂无 | 需通过 frp 隧道访问澳龙代理，或使用本地知识库手动同步 |

```bash
# 澳龙（已有代理）
source /root/.bashrc  # 加载代理配置
cd ~/workspace/arqiao-shared-knowledge && git pull

# 云船：目前通过 frp 隧道或本地笔记本手动同步
# 未来可通过 SSH 隧道访问澳龙代理：ssh -D 1080 -CNf user@cloud-ship
```

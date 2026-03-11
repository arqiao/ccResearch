# 服务器共享机制设计

> 各服务器之间的 Skills、配置、信息同步方案

## 设计目标

- 我（CC）对各服务器上安装的 Skills 有准确认知
- 服务器配置变更后可自动同步状态
- 密钥、脚本、Skills 清单分离管理

## 共享目录结构

```
~/local/
├── .secrets              # API 密钥（不进入 git）
├── .secrets.accounts.json # 账户数据
└── share-cc/            # CC 可读取的共享信息
    ├── skills.json       # Skills 清单（自动生成）
    ├── server-info.json  # 服务器信息（可选）
    └── openclaw-config.json # OpenClaw 配置快照（可选）
```

## Skills 清单

### 生成脚本

`~/local/share-cc/sync-skills-list.py`

扫描 Skills 目录，自动生成 `skills.json`：

```json
{
  "updated": "2026-03-11T21:40:00+08:00",
  "skills_dir": "/home/arqiaoclaw/workspace/arqiao-shared-knowledge/skills",
  "skills": [
    {"name": "feishu-doc", "desc": "飞书文档读取"},
    {"name": "switch-my-llm", "desc": "模型切换"},
    {"name": "switch-my-account", "desc": "账户切换"},
    ...
  ]
}
```

### 使用方式

CC 读取 `~/local/share-cc/skills.json` 即可知道当前服务器上有哪些 Skills。

### 自动更新

可在 gateway 启动脚本中加入调用：

```bash
python3 ~/local/share-cc/sync-skills-list.py
```

---

## 各服务器现状

### 云船（联通云 WSL1）

| 项目 | 路径 |
|------|------|
| 密钥 | `~/local/.secrets` |
| 账户 | `~/local/.secrets.accounts.json` |
| Skills 目录 | `~/workspace/arqiao-shared-knowledge/skills` |
| Skills 清单 | `~/local/share-cc/skills.json` |
| OpenClaw 配置 | `~/.openclaw/openclaw.json` |

### 澳龙（阿里云）

| 项目 | 路径 |
|------|------|
| 密钥 | `/root/local/.secrets` |
| 账户 | `/root/local/.secrets.accounts.json` |
| Skills 目录 | `~/workspace/arqiao-shared-knowledge/skills` |
| Skills 清单 | `/root/local/share-cc/skills.json` |
| OpenClaw 配置 | `/root/.openclaw/openclaw.json` |

---

## CC 如何获取服务器信息

### 方式一：直接读取共享文件

CC 可通过 SSH 读取服务器的共享文件：

```bash
# 读取云船的 Skills 清单
ssh -p 12222 arqiaoclaw@39.107.54.166 "cat ~/local/share-cc/skills.json"

# 读取澳龙的 Skills 清单
ssh root@39.107.54.166 "cat /root/local/share-cc/skills.json"
```

### 方式二：同步到本地

可将共享文件同步到本地，方便随时查阅：

```bash
# 同步云船的共享信息到本地
scp -P 12222 arqiaoclaw@39.107.54.166:~/local/share-cc/skills.json ./cloud-ship-skills.json
```

## Skills 配置（重要）

在 `openclaw.json` 顶级添加 `skills.load.extraDirs` 即可让 OpenClaw 加载 Skills：

```json
{
  "skills": {
    "load": {
      "extraDirs": [
        "~/workspace/arqiao-shared-knowledge/skills"
      ],
      "watch": true
    }
  }
}
```

> 注意：只需要在顶级配置，不需要在 channel 配置里重复添加。重启 gateway 后生效。

---

## 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-03-12 | 确认只需要顶级 skills 配置，不需要 channel 级别配置 |
| 2026-03-11 | 创建共享目录结构 `~/local/share-cc/` 和 skills.json 生成脚本 |

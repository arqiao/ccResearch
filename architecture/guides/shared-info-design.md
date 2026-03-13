# 服务器目录规范与共享机制

> 各服务器之间的目录规范、Skills、配置、信息同步方案

## 设计目标

- 通用内容（脚本、Skills、知识库）各服务器完全一致，git pull 即可同步
- 个性化内容（密钥、代理、备份脚本）按服务器定制，文件名一致但内容不同
- 新增服务器时，通用部分直接 clone，个性化部分手动创建

## 目录分类原则

| 目录 | 定位 | 文件名 | 内容 | 同步方式 |
|------|------|--------|------|---------|
| `~/workspace/` | 通用 | 各服务器一致 | 各服务器一致 | git pull |
| `~/local/` | 个性化 | 各服务器一致 | 按服务器定制 | 手动维护 |
| `~/log/` | 日志 | 各服务器一致 | 各服务器独立 | 不同步 |
| `~/.openclaw/` | 运行时 | - | 脚本自动维护 | 不直接同步 |

## 通用目录（~/workspace/）

```
~/workspace/
├── arqiao-shared-knowledge/       # 知识库（git 同步）
│   ├── skills/                    # Skills
│   └── server-scripts/            # 通用运维脚本
│       ├── feishu_send.py         # 飞书通知
│       ├── notify.sh              # 通知包装
│       ├── check_openclaw_update.sh
│       ├── check_system_update.sh
│       ├── switch-my-llm.py       # LLM 切换
│       ├── switch-my-account.js   # 账户切换
│       ├── rename-in-sessions.sh  # Skill 改名后清理会话历史
│       └── sync-myskills-list.py  # 生成 ~/local/myskills.json
└── ccResearch/                    # 项目文档（git 同步）
```

## 个性化目录（~/local/）

```
~/local/
├── .secrets                       # API 密钥（chmod 600）
├── .secrets.accounts.json         # 账户数据（chmod 600）
├── .proxy_env                     # 代理环境变量持久化
├── myskills.json                  # 本机 Skills 清单（脚本自动生成）
└── scripts/                       # 个性化脚本
    ├── backup_openclaw.sh         # 配置备份（路径因服务器而异）
    ├── cloud-ship-switch-proxy.sh # 代理切换（云船）
    ├── simple-proxy.py            # HTTP 代理服务（云船）
    └── switch-proxy.sh            # 代理切换（澳龙）
```

---

## Skills 清单（myskills.json）

### 生成脚本

`~/workspace/arqiao-shared-knowledge/server-scripts/sync-myskills-list.py`

扫描本机 Skills 目录，输出到 `~/local/myskills.json`：

```json
{
  "updated": "2026-03-12T10:00:00+08:00",
  "skills_dir": "/home/arqiaoclaw/workspace/arqiao-shared-knowledge/skills",
  "skills": [
    {"name": "feishu-doc", "desc": "飞书文档读取"},
    {"name": "switch-my-llm", "desc": "模型切换"},
    {"name": "switch-my-account", "desc": "账户切换"}
  ]
}
```

### 使用方式

CC 读取 `~/local/myskills.json` 即可知道当前服务器上有哪些 Skills。

### 自动更新

可在 gateway 启动脚本中加入调用：

```bash
python3 ~/workspace/arqiao-shared-knowledge/server-scripts/sync-myskills-list.py
```

---

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
| 2026-03-12 | 重构：目录规范化——通用脚本移入 server-scripts/（git 同步），个性化脚本移入 ~/local/scripts/，share-cc/ 废弃改为 ~/local/myskills.json |
| 2026-03-12 | 确认只需要顶级 skills 配置，不需要 channel 级别配置 |
| 2026-03-11 | 创建共享目录结构和 skills.json 生成脚本 |

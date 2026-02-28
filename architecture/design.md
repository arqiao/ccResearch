# 实施细节设计

> 创建时间：2026-02-25
> 定位：architecture.md 的实施细节补充，记录关键配置的设计决策和原因

---

## 一、仓库设计

### 两个仓库的职责边界

| 仓库 | 写入方 | 读取方 | 说明 |
|-----|-------|-------|------|
| arqiao-shared-knowledge | CC（本地）、OpenClaw（服务器） | 两端均可 | 共建知识库，解决问题后直接 push |
| ccResearch | CC（本地）only | OpenClaw 只读 | 任务清单由人主导，服务器只做同步 |

### 同步机制

**arqiao-shared-knowledge**：双向读写，任意一端 push 后另一端 pull 获取

**ccResearch**：单向同步
```
CC 本地 push → GitHub → 服务器 cron git pull（每天凌晨 3 点）
紧急同步：飞书发消息触发 webhook → 本地执行 git pull
```

### git pull 策略

服务器配置 `pull.ff only`，确保不产生 merge commit。
若出现分叉（如本地做了 filter-branch 重写历史），需手动：
```bash
git fetch origin && git reset --hard origin/main
```

### GitHub 认证

| 端 | 方式 | 原因 |
|----|------|------|
| 本地 | credential store（`~/.git-credentials`） | remote URL 保持干净，token 单独管理 |
| 服务器 | token 嵌在 remote URL | 服务器无交互式输入场景，此方式可接受 |

---

## 二、本地工作目录规范

| 目录 | 用途 |
|-----|------|
| `D:\workspace\devCC` | 产品化项目 |
| `D:\workspace\ccResearch` | 研究性项目、任务清单 |
| `D:\workspace\mytools` | 个人小工具 |
| `D:\workspace\kbs` | 知识库仓库（arqiao-shared-knowledge） |
| `D:\workspace\noshare` | 本地敏感信息，不进任何 git 仓库 |

### ccResearch .gitignore 排除策略

```
plan-research-claw/   # 旧项目
kbs-dev/              # 不同步
**/tmp/               # 临时文件
**/drafts/            # 草稿
**/node_modules/
**/data/articles_cache/
**/data/articles_fulltext/
```

---

## 三、OpenClaw 服务器配置

### TOOLS.md

路径：`/home/openclaw/.openclaw/workspace/TOOLS.md`

作用：告知 OpenClaw 机器人操作规范，关键规则：
- **查询项目进度时直接读本地文件，禁止去 Notion 搜索**
- 知识库写入后直接 commit push，无需等待人工确认

原因：模型默认倾向于调用工具（Notion search），需要明确规则才会优先读本地文件。

### Notion 集成

Notion skill 的 API key 必须通过 systemd drop-in 注入，仅配置在 openclaw.json 中不够。
原因：systemd 服务启动时不读取 `~/.bashrc`，skill 运行时读取的是进程环境变量。

### 账户切换

脚本：`/root/.openclaw/switch-account.js`
网页：`http://39.107.54.166:19528/`（欠费时手动切换）
可用账户：arqiao-tsinghua、arqiao-sina、arqiao-test、arqiao-minimax

---

## 四、服务器网络代理

### 方案选型

服务器（阿里云）无法直接访问 GitHub，需要代理。
采购的订阅服务为：
    https://msub.xn--m7r52rosihxm.com/api/v1/client/subscribe?token=5a88ba3ed39a1b5dd1c72756f1446e34
选用 sing-box（系统已内置 1.12.22），vmess+ws 协议。

| 端口 | 协议 | 用途 |
|------|------|------|
| 7890 | HTTP | git、curl 等命令行工具 |
| 7891 | SOCKS5 | 备用 |

配置文件：`/etc/sing-box/config.json`，服务：`systemctl status sing-box`

### 节点订阅与自动切换

订阅格式：Clash YAML，包含 27 个可用节点（日本、新加坡、香港、台湾、美国等）。

脚本：`/root/proxy-switch.py`

工作流程：
```
检测当前节点（curl GitHub，超时 5s）
  ↓ 不通
从订阅 URL 拉取节点列表（Clash YAML 解析）
  ↓
逐节点启动临时 sing-box 实例测速
  ↓
选最低延迟节点，更新 /etc/sing-box/config.json，重启 sing-box
  ↓
验证切换结果
```

用法：
```bash
python3 /root/proxy-switch.py          # 检测当前节点，不通则自动切换
python3 /root/proxy-switch.py --force  # 强制重新测速选最优节点
```

### 流量监控

每次节点切换时顺带检查剩余流量（从订阅响应的 `subscription-userinfo` header 解析）。低于 100 MB 时通过飞书 bot 发消息到群（chat_id: oc_42e15484900d10f7f30bcd18d72d1397，群名可能变更但 chat_id 不变）。

### 自动检测 cron

```
0 * * * * python3 /root/proxy-switch.py >> /var/log/proxy-switch.log 2>&1
```

每小时检测一次，节点失效时自动切换，无需人工干预。OpenClaw 也可通过飞书群触发手动切换（见 TOOLS.md）。

---

## 五、API Key 管理

### 设计原则

**任何 key 不进入 git 仓库**，按运行环境分两处存放：

| 环境 | 存放位置 | 权限 |
|-----|---------|------|
| 本地（Windows） | `D:\workspace\noshare\env.md` | 不在任何 git 仓库目录下 |
| 服务器（Linux） | `/root/.secrets` | chmod 600 |

### 当前 Key 清单

| Key | 用途 | 管理地址 |
|-----|------|---------|
| BAIDU_API_KEY | baidu-search skill，中文搜索 | cloud.baidu.com |
| ARK_API_KEY | 火山引擎，Seedance 视频生成 | volcengine.com |
| NOTION_API_KEY | notion skill，读写 Notion | notion.so/my-integrations |
| FEISHU_APP_ID/SECRET | 飞书文档、群消息读取 | open.feishu.cn |
| ANTHROPIC_AUTH_TOKEN | Claude API 中转（zjz-ai） | 中转服务商 |
| GITHUB_TOKEN | 仓库 push/pull | github.com/settings/tokens |

### 服务器 Key 注入方式

服务器有两种进程需要 key，注入方式不同：

| 进程类型 | 注入方式 | 原因 |
|---------|---------|------|
| 交互式 shell | `~/.bashrc` source `/root/.secrets` | bashrc 在登录时执行 |
| systemd 服务（OpenClaw） | systemd drop-in `Environment=` | systemd 不读 bashrc |

systemd drop-in 路径：
```
/root/.config/systemd/user/openclaw-gateway.service.d/notion.conf
```

### 历史教训

- `skills-dev/.claude/settings.local.json` 曾有明文 BAIDU_API_KEY 上传到 GitHub
- 已用 `git filter-branch` 重写历史清除，强制推送覆盖
- git remote URL 曾嵌入 token，已改为 credential store
- `/etc/environment` 曾有明文 BAIDU_API_KEY，已移除（key 已在 `/root/.secrets` 中）

---

## 六、包管理器选择

### npm vs pnpm

2G 内存服务器上 npm install 多次 OOM 失败（即使限制 maxsockets=3），改用 pnpm 后 51 秒完成安装。

| 项目 | npm | pnpm |
|-----|-----|------|
| 安装 OpenClaw | 多次 OOM 失败 | 51 秒成功 |
| 内存占用 | 高（全量解压到 node_modules） | 低（硬链接 + 内容寻址） |
| 并发控制 | `npm config set maxsockets 2` | `pnpm config set concurrency 1` |
| 全局安装路径 | `/usr/lib/node_modules/` | `~/.local/share/pnpm/global/5/node_modules/` |

**结论：小内存服务器（≤4G）必须用 pnpm，且 concurrency 设为 1。**

### pnpm 全局路径注意事项

pnpm 全局安装路径与 npm 不同，需要：
1. `PNPM_HOME` 加入 PATH（`~/.bashrc` 和 `/etc/environment`）
2. systemd 服务的 ExecStart 路径需指向 pnpm 全局目录

---

## 七、Swap 配置经验

### 配置原则

| 物理内存 | 推荐 Swap | swappiness |
|---------|----------|------------|
| ≤2G | 物理内存 × 2（4G） | 10 |
| 2-8G | 物理内存 × 2 | 10 |
| >8G | 物理内存 × 1 | 10 |

### 关键教训

- swappiness 默认 60 对小内存偏高，设为 10 即可
- **切勿设为 100**：会导致系统疯狂换页（thrashing），磁盘 I/O 打满，系统假死
- 2G 物理内存 + 2G swap = 4G 总量不够 npm install 峰值（3-4G），需要 4G swap
- 阿里云 2 核 2G 实际可用内存约 1.6G（内核和 GPU 预留约 400MB）

---

## 八、模型切换方案

### 架构

```
用户（飞书/网页/命令行）
  ↓
switch-llm.py（核心脚本）
  ├── 读取 models-config.json（模型-账户映射）
  ├── 过滤当天不可用账户
  ├── 修改 openclaw.json（全局 + per-channel model）
  ├── 修改 auth-profiles.json（API Key）
  ├── 等待 openclaw-gateway 自动热重载（不重启进程）
  └── 发飞书通知
```

### 配置文件

| 文件 | 路径 | 说明 |
|-----|------|------|
| models-config.json | `/root/.openclaw/` | 模型-账户映射、当前状态、不可用标记 |
| accounts.json | `/root/.openclaw/` | 账户详情（baseUrl、apiKey） |
| switch-llm.py | `/root/scripts/` | 核心切换脚本 |
| account-switcher.js | `/root/.openclaw/` | 网页 UI（端口 19528，含模型切换标签页） |

### per-channel model

openclaw.json 中 `channels.feishu.agents.defaults.model.primary` 可独立于全局模型设置。
switch-llm.py 切换时会同步更新此字段。

### 热重载机制

switch-llm.py 修改配置文件后，不主动重启 openclaw-gateway。OpenClaw 会自动检测配置文件变更并执行热重载（`config hot reload applied`），进程 PID 不变。

仅当 openclaw-gateway 进程不存在时（MainPID=0），才执行 `systemctl --user restart`。

> 早期版本使用 `systemctl restart`，会导致飞书 WebSocket 断连、消息丢失。详见 `known-limitations.md`。

### 网页 UI 交互

网页（account-switcher.js，端口 19528）的模型切换标签页采用两步选择：
1. 点击模型按钮 → 下方动态显示该模型的可用账户列表
2. 点击账户按钮 → 提交切换（model + account）

不可用账户显示为灰色禁用状态。当前账户默认高亮。

# 知识共享与自动化系统方案

> 创建时间：2026-02-15
> 状态：方案确定，待实施

## 一、问题背景

### 1.1 核心痛点

1. **技能复用性差**：同一技术问题（如飞书 API 授权）在多个项目中反复遇到，每次都要重新摸索
2. **团队协作困难**：经验无法跨人员、跨电脑共享
3. **工作空间割裂**：Claude Code 各项目空间独立，共性知识无法流通

### 1.2 目标

- 技术方案一次解决，多项目复用
- 团队成员共享知识，避免重复踩坑
- 自动化知识的获取和更新流程

---

## 二、总体架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                    自动化知识管理架构                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    Git Push     ┌──────────────────┐              │
│  │ 知识仓库      │ ──────────────► │ Webhook 触发      │              │
│  │ (Git)        │                 │ OpenClaw Gateway  │              │
│  └──────────────┘                 └────────┬─────────┘              │
│         ▲                                  │                        │
│         │                                  ▼                        │
│         │                         ┌──────────────────┐              │
│         │                         │ 自动同步 Skill    │              │
│         │                         │ 到各工作空间      │              │
│         │                         └────────┬─────────┘              │
│         │                                  │                        │
│         │         ┌────────────────────────┼────────────────┐       │
│         │         ▼                        ▼                ▼       │
│         │    ┌─────────┐            ┌─────────┐       ┌─────────┐   │
│         │    │ 项目 P1  │            │ 项目 P2  │       │ 项目 P3  │   │
│         │    │ CC/OC   │            │ CC/OC   │       │ CC/OC   │   │
│         │    └────┬────┘            └────┬────┘       └────┬────┘   │
│         │         │                      │                 │        │
│         │         └──────────────────────┴─────────────────┘        │
│         │                        │                                  │
│         │                        ▼                                  │
│         │              ┌──────────────────┐                         │
│         └───────────── │ 解决新问题后      │                         │
│                        │ 自动提交到知识库  │                         │
│                        └──────────────────┘                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1 三层架构

| 层级 | 组件 | 作用 |
|-----|------|------|
| 存储层 | Git 阿乔的共享知识库 | 存储技术方案、接口定义、踩坑记录 |
| 自动化层 | OpenClaw Gateway + Skills | 自动读取/更新知识，跨项目同步 |
| 接入层 | Claude Code / OpenClaw 客户端 | 日常使用入口 |

---

## 三、阿乔的共享知识库结构

```
arqiao-shared-knowledge/
├── README.md                      # 仓库使用说明
├── CLAUDE.md                      # 让 CC 理解仓库结构的指引
│
├── skills/                        # OpenClaw 兼容的 Skill 格式
│   ├── feishu-auth/
│   │   └── SKILL.md              # 飞书授权问题处理
│   ├── knowledge-query/
│   │   └── SKILL.md              # 查询知识库
│   └── knowledge-update/
│       └── SKILL.md              # 更新知识库
│
├── solutions/                     # 技术解决方案
│   ├── feishu/
│   │   ├── auth-refresh.md       # 授权刷新方案
│   │   └── api-best-practices.md
│   └── [其他技术领域]/
│
├── interfaces/                    # 团队共享接口定义
│   ├── api-contracts/
│   └── data-models/
│
├── pitfalls/                      # 踩坑记录
│   ├── feishu-pitfalls.md
│   └── [其他]/
│
├── templates/                     # 文档模板
│   ├── solution-template.md
│   └── pitfall-template.md
│
└── .github/
    └── workflows/
        └── sync-skills.yml       # 自动同步到 ClawHub
```

---

## 四、环境变量约定

为适应多电脑、多平台，采用环境变量统一路径：

```bash
# 阿乔的共享知识库本地路径
SHARED_KNOWLEDGE_PATH=/path/to/arqiao-shared-knowledge

# OpenClaw 配置目录
OPENCLAW_HOME=~/.openclaw
```

### 各平台设置方式

**Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("SHARED_KNOWLEDGE_PATH", "D:\workspace\shared-knowledge", "User")
```

**Linux/macOS (bash/zsh):**
```bash
echo 'export SHARED_KNOWLEDGE_PATH="$HOME/workspace/arqiao-shared-knowledge"' >> ~/.bashrc
source ~/.bashrc
```

---

## 五、部署方案

### 5.1 部署阶段规划

| 阶段 | 时间 | 方案 | 说明 |
|-----|------|------|------|
| 第一阶段 | 现在起 ~1个月 | 云服务器 | 过年期间远程使用 |
| 第二阶段 | 1个月后 | 树莓派 + 内网穿透 | 迁移回家，零成本运行 |

---

## 六、已确认选择

| 项目 | 选择 | 说明 |
|-----|------|------|
| 主力方案 | OpenClaw | 开源、成熟、自主可控 |
| 备选方案 | CoPaw | 阿里通义出品，即将开源，可快速体验 |
| 云服务器 | 阿里云 | 新用户优惠大，国内访问快 |
| Git 托管 | GitHub | 稳定，生态好 |
| 内网穿透 | Tailscale | 免费，无需域名，配置简单 |

---

## 6.1 方案对比：OpenClaw vs CoPaw vs QoderWork

| 对比项 | OpenClaw | CoPaw | QoderWork |
|-------|----------|-------|-----------|
| 开发者 | 社区开源 | 阿里云通义团队 | 阿里 |
| 部署难度 | 需手动配置环境 | 3条命令或云端一键 | 双击安装 |
| 运行位置 | 本地/VPS | 本地/云端均可 | 纯本地 |
| 数据安全 | 本地运行，自主可控 | 本地或云端可选 | 全本地化 |
| 频道接入 | 多频道 | 钉钉/飞书/QQ/Discord | 本地应用调用 |
| Skill扩展 | 支持自定义 | 支持自定义 | 内置+MCP协议 |
| 开源状态 | 已开源 | 即将开源 | 否 |
| 团队共享 | ✅ Gateway 可共享 | ✅ 云端可共享 | ❌ 单机 |
| 远程访问 | ✅ 部署到服务器 | ✅ 魔搭创空间 | ❌ |
| 适合人群 | 技术极客 | 开发者/普通用户 | 普通办公用户 |

**选择理由：**
- **OpenClaw（主力）**：成熟稳定，完全自主可控，适合长期运行
- **CoPaw（备选）**：阿里官方出品，安装更简单，魔搭创空间可零配置体验
- **QoderWork（补充）**：适合本地桌面办公自动化，不适合团队共享场景

---

## 七、实施步骤

### 第一阶段：云服务器部署（现在 ~ 1个月）

| 步骤 | 操作 | 文档 |
|-----|------|------|
| 1 | 购买云服务器 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) 第一章 |
| 2 | 初始化服务器 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) 第二章 |
| 3 | 安装 OpenClaw | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) 第三章 |
| 4 | 创建阿乔的共享知识库 | [init-knowledge-repo.md](./guides/init-knowledge-repo.md) |
| 5 | 配置客户端 | [client-setup.md](./guides/client-setup.md) |

### 第二阶段：MCP 集成

| 步骤 | 功能 | 优先级 | 说明 |
|-----|------|-------|------|
| 1 | 飞书群消息读取 | 最高 | 官方 API 支持好，先做 |
| 2 | 微信群消息读取 | 高 | 需评估封号风险 |
| 3 | OpenClaw Gateway API | 中 | CC 直接调用 Gateway |
| 4 | GitHub 仓库直接访问 | 低 | 无需本地克隆 |

### 第三阶段：树莓派部署（迁移回家）

| 步骤 | 操作 | 文档 |
|-----|------|------|
| 1 | 准备树莓派硬件 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) 第一章 |
| 2 | 安装系统 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) 第二章 |
| 3 | 配置内网穿透 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) 第五章 |
| 4 | 迁移数据和 MCP 服务 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) 第九章 |
| 5 | 更新客户端配置 | [client-setup.md](./guides/client-setup.md) |
| 6 | 释放云服务器 | - |

---

## 八、文档索引

| 文档 | 说明 |
|-----|------|
| [knowledge-sharing-system.md](./knowledge-sharing-system.md) | 本文档，总体方案 |
| [task-list.md](./task-list.md) | 任务清单，跟踪所有待办事项 |
| [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | 云服务器部署指南 |
| [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 树莓派部署指南 |
| [init-knowledge-repo.md](./guides/init-knowledge-repo.md) | 知识仓库初始化 |
| [client-setup.md](./guides/client-setup.md) | 客户端配置指南 |
| [multi-model-switching.md](./references/multi-model-switching.md) | 多模型切换方案 |
| [copaw-alternative.md](./references/copaw-alternative.md) | CoPaw 备选方案 |
| [windows-backup-restore.md](./guides/windows-backup-restore.md) | Windows 换机备份与恢复 |

---

## 附录

### A. 相关文档链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [ClawHub 技能市场](https://clawhub.com)
- [CoPaw 官方文档](http://copaw.agentscope.io/)
- [CoPaw 魔搭创空间](https://modelscope.cn/studios/AgentScope/CoPaw)
- [QoderWork 介绍](https://blog.csdn.net/weixin_43107715/article/details/157585560)

### B. 快速命令参考

```bash
# 同步阿乔的共享知识库
cd $SHARED_KNOWLEDGE_PATH && git pull

# 检查 Gateway 状态
curl http://GATEWAY_IP:18789/health

# SSH 连接服务器
ssh openclaw-cloud  # 云服务器
ssh openclaw-pi     # 树莓派

# 查看 Gateway 日志
ssh openclaw-pi "journalctl -u openclaw-gateway -f"

# OpenClaw 更新（先备份）
tar -czvf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw
npm update -g openclaw@latest
sudo systemctl restart openclaw-gateway
openclaw doctor
```

### C. 常见问题

**Q: 阿乔的共享知识库更新后其他项目怎么获取？**
A: 执行 `git pull` 即可。如果配置了 OpenClaw，Skills 会自动读取最新内容。

**Q: 多人同时修改阿乔的共享知识库怎么办？**
A: 使用 Git 的标准协作流程，小团队可以直接 push，大团队建议用 PR。

**Q: 云服务器到期后数据会丢失吗？**
A: 不会。知识仓库在 Git 远程有备份，OpenClaw 配置在迁移前会导出。

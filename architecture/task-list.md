# 任务清单

> 最后更新：2026-03-13
> 状态说明：⬜ 待办 | 🔄 进行中 | ✅ 已完成 | ⏸️ 暂缓
> 执行者说明：👤 你独立完成 | 🤖 我来协助 | 👥 一起完成

---

## 使用指南

### 文档使用时机

| 文档 | 什么时候看 | 需要看外部资料吗 |
|-----|-----------|-----------------|
| `task-list.md` | **每次开始工作时** | 不需要 |
| `myclaws-inventory.md` | 查看各机器配置和部署状态时 | 不需要 |
| `knowledge-sharing-system.md` | 想了解整体方案时 | 不需要 |
| `guides/deploy-cloud-server.md` | 做任务 #1-9 时 | 阿里云购买页面需要自己操作 |
| `guides/deploy-raspberry-pi.md` | 做任务 #39-64 时 | 树莓派官网下载 Imager |
| `guides/init-knowledge-repo.md` | 做任务 #10-17 时 | GitHub 创建仓库需要自己操作 |
| `guides/client-setup.md` | 做任务 #18-23 时 | 不需要 |
| `known-limitations.md` | 遇到异常行为时 | 不需要 |
| `guides/openclaw-tools-reference.md` | 调用 Gateway API 时 | 不需要 |

### 需要你自己去外部网站的操作

| 任务 | 网站 | 操作 |
|-----|------|------|
| #1-2 | https://www.aliyun.com | 注册账号、购买服务器 |
| #10 | https://github.com | 创建仓库 |
| #24 | https://open.feishu.cn | 创建飞书应用 |
| #36 | https://github.com/settings/tokens | 创建 Personal Access Token |
| #42 | https://www.raspberrypi.com/software/ | 下载 Imager |
| #55 | https://tailscale.com | 注册账号、下载客户端 |

> 这些外部操作 CC 无法代替你做，但当你做完后告诉 CC 结果（如服务器 IP），后续步骤 CC 可以指导。

### 状态更新方式

| 场景 | 谁来更新 | 方式 |
|-----|---------|------|
| 你独立完成的任务（👤） | 你自己 | 直接编辑文件，改 ⬜ 为 ✅ |
| CC 协助的任务（🤖） | CC | 告诉 CC "任务 #X 完成了" |
| 一起完成的任务（👥） | CC | 验证通过后 CC 更新 |
| 遇到问题的任务 | CC | 改为 ⏸️ 并记录原因 |

### 执行者统计

| 执行者 | 数量 | 说明 |
|-------|------|------|
| 👤 你独立完成 | 约 20 项 | 账号注册、购买、硬件准备、授权等 |
| 🤖 CC 协助 | 约 30 项 | 提供命令、写代码、写配置 |
| 👥 一起完成 | 约 14 项 | 需要讨论或共同验证 |

---

## 第一阶段：云服务器部署（紧急，过年期间使用）

### 1.1 基础设施

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 1 | 注册/登录阿里云账号 | ✅ | 👤 | - | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | https://www.aliyun.com |
| 2 | 购买轻量应用服务器 | ✅ | 👤 | #1 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | 2核2G，Ubuntu 24.04 LTS，1年（68元） |
| 3 | 记录服务器 IP 和登录信息 | ✅ | 👤 | #2 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | 公网 IP: 39.107.54.166 |
| 4 | SSH 登录并初始化服务器 | ✅ | 🤖 | #3 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | 系统更新完成 |
| 5 | 安装 Node.js 22 | ✅ | 🤖 | #4 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | v22.22.0 |
| 6 | 安装 OpenClaw | ✅ | 🤖 | #5 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | v2026.2.14 → v2026.2.24（pnpm 安装） |
| 7 | 运行 OpenClaw 引导向导 | ✅ | 👥 | #6 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | 配置完成，使用 claude-sonnet-4-5 |
| 8 | 配置防火墙开放 18789 端口 | ✅ | 🤖 | #7 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | 不需要开放，使用 SSH 隧道更安全 |
| 9 | 验证 Gateway 可访问 | ✅ | 👥 | #8 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | SSH 隧道方式访问成功 |

### 1.2 阿乔的共享知识库

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 10 | 在 GitHub 创建阿乔的共享知识库 | ✅ | 👤 | - | [init-knowledge-repo.md](./guides/init-knowledge-repo.md) | Private 仓库名：arqiao-shared-knowledge |
| 11 | 本地克隆仓库 | ✅ | 👤 | #10 | [init-knowledge-repo.md](./guides/init-knowledge-repo.md) | 已克隆到 D:\workspace\kbs\ |
| 12 | 创建目录结构 | ✅ | 🤖 | #11 | [init-knowledge-repo.md](./guides/init-knowledge-repo.md) | 已创建 |
| 13 | 创建 Skill 文件 | ✅ | 🤖 | #12 | [init-knowledge-repo.md](./guides/init-knowledge-repo.md) | 已创建 |
| 14 | 创建模板文件 | ✅ | 🤖 | #12 | [init-knowledge-repo.md](./guides/init-knowledge-repo.md) | 已创建 |
| 15 | 提交并推送到 GitHub | ✅ | 👤 | #13, #14 | [init-knowledge-repo.md](./guides/init-knowledge-repo.md) | 已推送 |
| 16 | 在服务器上克隆阿乔的共享知识库 | ✅ | 🤖 | #9, #15 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | 通过 scp 传输（服务器无法访问 GitHub） |
| 17 | 链接 Skills 到 OpenClaw | ✅ | 🤖 | #16 | [deploy-cloud-server.md](./guides/deploy-cloud-server.md) | 通过 openclaw.json 的 extraDirs 配置 |

### 1.3 客户端配置

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 18 | Windows 生成 SSH 密钥 | ✅ | 👤 | - | [client-setup.md](./guides/client-setup.md) | ed25519 密钥已生成 |
| 19 | 将公钥添加到服务器 | ✅ | 🤖 | #4, #18 | [client-setup.md](./guides/client-setup.md) | 免密登录已配置 |
| 20 | 配置 SSH config 快捷方式 | ✅ | 🤖 | #19 | [client-setup.md](./guides/client-setup.md) | openclaw-cloud, openclaw-tunnel |
| 21 | 设置 SHARED_KNOWLEDGE_PATH 环境变量 | ✅ | 🤖 | #11 | [client-setup.md](./guides/client-setup.md) | 已设置 |
| 22 | 更新 ~/.claude/CLAUDE.md | ✅ | 🤖 | #21 | [client-setup.md](./guides/client-setup.md) | 已添加知识库路径和使用指引 |
| 23 | 测试 Claude Code 读取阿乔的共享知识库 | ✅ | 👥 | #22 | [client-setup.md](./guides/client-setup.md) | 验证通过 |

---

## 新阶段：联通云智电脑部署（替代阿里云）

> 主机：8核/16GB/200GB，公网 IP 195.64.7.45（固定）
> 参考文档：[deploy-cloud-wsl1-frp.md](./guides/deploy-cloud-wsl1-frp.md)

### V.1 WSL1 + Ubuntu 安装

> 注：联通云智电脑不支持嵌套虚拟化，Hyper-V / WSL2 均不可用，改用 WSL1

| # | 任务 | 状态 | 执行者 | 依赖 | 说明 |
|---|------|------|-------|------|------|
| V1 | 启用 WSL 功能并重启 | ✅ | 👤 | - | dism 启用 Microsoft-Windows-Subsystem-Linux，已重启 |
| V2 | 设置默认版本为 WSL1 | ✅ | 👤 | V1 | `wsl --set-default-version 1` |
| V3 | 安装 Ubuntu 24.04 | ✅ | 👤 | V2 | Ubuntu 24.04.4 LTS，用户名 arqiaoclaw |
| V4 | 迁移 WSL1 数据到 D 盘 | ✅ | 🤖 | V3 | WSL1 数据已在 D:\wsl\ |
| V5 | 开放 Windows 防火墙 18789 端口 | ✅ | 🤖 | V3 | WSL1 共享网络栈，不需要端口转发 |

### V.2 OpenClaw 安装与配置

| # | 任务 | 状态 | 执行者 | 依赖 | 说明 |
|---|------|------|-------|------|------|
| V9 | 安装 Node.js 22 + pnpm | ✅ | 🤖 | V3 | Node.js v22.22.1，pnpm 已安装 |
| V10 | 安装 OpenClaw | ✅ | 🤖 | V9 | openclaw@2026.3.8 已安装 |
| V11 | 运行引导向导 | ✅ | 🤖 | V10 | minimax/MiniMax-M2.5 已配置 |
| V12 | 配置 Gateway 监听 loopback + token | ✅ | 🤖 | V11 | bind: loopback（WSL1网络限制），token 已配置 |
| V13 | 迁移阿里云知识库和配置 | ✅ | 🤖 | V12 | 知识库已克隆（arqiao-shared-knowledge + ccResearch），脚本/账户切换/cron 全部迁移完成 |
| V14 | 验证外网访问（手机/笔记本） | ✅ | 👥 | V5, V12 | 通过 SSH 隧道访问 localhost:18789，飞书群正常响应 |

### V.3 收尾

| # | 任务 | 状态 | 执行者 | 依赖 | 说明 |
|---|------|------|-------|------|------|
| V15 | 联通云开机自启：frpc + openclaw gateway | ✅ | 🤖 | V14 | 启动文件夹方式，WSL等待+SSH服务+frpc+OpenClaw |
| V16 | 笔记本一键连接（MobaXterm） | ✅ | 🤖 | V15 | 会话配置端口转发，双击快捷方式连接 |
| V17 | 更新客户端 SSH config | ✅ | 🤖 | V14 | MobaXterm会话已包含LocalForward |
| V18 | 更新 CLAUDE.md 服务器地址 | ✅ | 🤖 | V14 | 无需更新，CLAUDE.md 中无硬编码 IP，通过 SSH 隧道访问 |
| V19 | 停用/释放阿里云服务器 | ⬜ | 👤 | V14 | 确认新服务器稳定后操作 |
| V20 | 配置 Tailscale 内网访问 | ✅ | 🤖 | V3 | 云船、笔记本、手机已加入 Tailscale 网络（100.115.214.108） |
| V21 | 关闭公网 18789 端口暴露 | ✅ | 🤖 | V20 | frpc 配置已移除 openclaw 代理，仅保留 SSH 隧道 |
| V22 | 配置控制界面访问 | ✅ | 🤖 | V20 | SSH 隧道方式（yunchuan-tunnel），allowedOrigins 已添加 Tailscale IP |
| V23 | 迁移澳龙功能到云船 | ✅ | 🤖 | V13 | 脚本(feishu/notify/backup/update检查)、账户切换(account-manager+switch-my-llm+switch-my-account)、知识库(两个仓库)、cron任务、extraDirs 全部完成；account-manager 已加入开机自启 |

---

## 第二阶段：MCP 集成

> 优先级调整：先飞书，再微信

### 2.1 飞书群消息读取（最高优先级）

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 24 | 创建飞书应用并获取权限 | ✅ | 👤 | - | [feishu-integration.md](./guides/feishu-integration.md) | 应用名：arqiaoknow，已配置应用身份权限 |
| 25 | 配置飞书事件订阅 | ✅ | 👥 | #24 | [feishu-integration.md](./guides/feishu-integration.md) | WebSocket 长连接方式 |
| 26 | 开发飞书 MCP Server | ✅ | 🤖 | #25 | [feishu-integration.md](./guides/feishu-integration.md) | 使用 OpenClaw 内置 feishu 插件，无需自定义 |
| 27 | 集成到 OpenClaw | ✅ | 🤖 | #26 | [feishu-integration.md](./guides/feishu-integration.md) | 已配置 channel 和 API key |

### 2.2 微信群消息读取（高优先级）

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 28 | 调研微信接入方案 | ⬜ | 🤖 | - | - | 我来调研对比 |
| 29 | 评估封号风险和合规性 | ⬜ | 👥 | #28 | - | 一起讨论决策 |
| 30 | 选择并部署微信桥接服务 | ⬜ | 👥 | #29 | - | 根据方案一起实施 |
| 31 | 开发微信 MCP Server | ⬜ | 🤖 | #30 | - | 我来写代码 |
| 32 | 集成到 OpenClaw | ⬜ | 🤖 | #31 | - | 我来配置 |

### 2.3 OpenClaw Gateway API 调用（中优先级）

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 33 | 研究 OpenClaw API 文档 | ✅ | 🤖 | #9 | - | 两个接口：POST /tools/invoke（始终启用）、POST /v1/chat/completions（需开启）；token: root/.openclaw/openclaw.json |
| 34 | 开发 OpenClaw MCP Server | ✅ | 🤖 | #33 | - | openclaw-gateway Skill 已创建（kbs/skills/openclaw-gateway/SKILL.md）；/tools/invoke 和 /v1/chat/completions 均已验证可用；chatCompletions 已在 openclaw.json 中启用 |
| 35 | 测试 CC 触发 OpenClaw 功能 | ✅ | 👥 | #34 | - | /tools/invoke（sessions_list 等）和 /v1/chat/completions（agent 搜索任务）均验证通过；关键修复：models.providers.anthropic 需设 api: anthropic-messages |

### 2.4 GitHub 仓库直接访问（低优先级）

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 36 | 配置 GitHub Personal Access Token | ✅ | 👤 | #10 | - | token 已配置（见 design.md），服务器 gh CLI v2.45.0 已安装 |
| 37 | 部署/配置 GitHub MCP Server | ⏸️ | 🤖 | #36 | - | 暂缓：已通过代理 + git CLI 覆盖，无需额外 MCP Server |
| 38 | 测试 CC 直接读取远程仓库 | ⏸️ | 👥 | #37 | - | 暂缓：同 #37 |

---

## 第三阶段：树莓派部署（迁移回家）⏸️ 低优先级

### 3.1 硬件准备

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 39 | 确认树莓派电源适配器规格 | ⬜ | 👤 | - | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 需要 5V 5A USB-C |
| 40 | 考虑升级存储（可选） | ⬜ | 👤 | - | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 64GB+ SD卡 或 外接 SSD |
| 41 | 准备散热方案 | ⬜ | 👤 | - | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 长期运行建议主动散热 |

### 3.2 系统安装

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 42 | 下载 Raspberry Pi Imager | ⬜ | 👤 | - | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | https://www.raspberrypi.com/software/ |
| 43 | 烧录 Raspberry Pi OS Lite 64-bit | ⬜ | 👤 | #42 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 配置 SSH、用户名、WiFi |
| 44 | 首次启动并 SSH 连接 | ⬜ | 👤 | #43 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | `ssh pi@openclaw-pi.local` |
| 45 | 更新系统 | ⬜ | 🤖 | #44 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供命令 |
| 46 | 配置静态 IP | ⬜ | 🤖 | #45 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供配置 |
| 47 | 优化 SD 卡写入 | ⬜ | 🤖 | #45 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供配置 |

### 3.3 OpenClaw 安装

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 48 | 安装 Node.js 22 | ⬜ | 🤖 | #45 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供命令 |
| 49 | 安装 OpenClaw | ⬜ | 🤖 | #48 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供命令 |
| 50 | 从云服务器导出配置 | ⬜ | 🤖 | #9 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供命令 |
| 51 | 传输配置到树莓派 | ⬜ | 🤖 | #49, #50 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供命令 |
| 52 | 恢复配置并启动 Gateway | ⬜ | 🤖 | #51 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供命令 |

### 3.4 内网穿透

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 53 | 树莓派安装 Tailscale | ⬜ | 🤖 | #45 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我提供命令 |
| 54 | 树莓派登录 Tailscale | ⬜ | 👤 | #53 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 需要你在浏览器授权 |
| 55 | Windows 安装 Tailscale | ⬜ | 👤 | - | [client-setup.md](./guides/client-setup.md) | https://tailscale.com/download/windows |
| 56 | Windows 登录同一 Tailscale 账号 | ⬜ | 👤 | #55 | [client-setup.md](./guides/client-setup.md) | 确保同一账号 |
| 57 | 小米手机安装 Tailscale | ⬜ | 👤 | - | [client-setup.md](./guides/client-setup.md) | 应用商店下载 |
| 58 | 手机登录同一 Tailscale 账号 | ⬜ | 👤 | #57 | [client-setup.md](./guides/client-setup.md) | 确保同一账号 |
| 59 | 验证 Tailscale 网络互通 | ⬜ | 👥 | #54, #56, #58 | [client-setup.md](./guides/client-setup.md) | 一起验证 |

### 3.5 迁移完成

| # | 任务 | 状态 | 执行者 | 依赖 | 参考文档 | 说明 |
|---|------|------|-------|------|---------|------|
| 60 | 更新客户端 SSH config | ⬜ | 🤖 | #59 | [client-setup.md](./guides/client-setup.md) | 我提供配置 |
| 61 | 更新 CLAUDE.md Gateway 地址 | ⬜ | 🤖 | #59 | [client-setup.md](./guides/client-setup.md) | 我来修改 |
| 62 | 迁移 MCP Server 到树莓派 | ⬜ | 🤖 | #52, #59 | [deploy-raspberry-pi.md](./guides/deploy-raspberry-pi.md) | 我来操作 |
| 63 | 验证所有功能正常 | ⬜ | 👥 | #60, #61, #62 | - | 一起验证 |
| 64 | 释放阿里云服务器 | ⬜ | 👤 | #63 | - | 在阿里云控制台操作 |

---

## 基础设施补充

### 服务器网络

| # | 任务 | 状态 | 执行者 | 依赖 | 说明 |
|---|------|------|-------|------|------|
| I1 | 研究阿里云服务器代理方案 | ✅ | 🤖 | - | 选用 sing-box（已内置 1.12.22），vmess+ws 节点 |
| I2 | 配置服务器代理 | ✅ | 👥 | I1 | sing-box 已启动，HTTP 7890 / SOCKS 7891，已写入 ~/.bashrc |
| I3 | 验证 GitHub 访问 | ✅ | 👥 | I2 | git ls-remote 测试通过，HTTP 200 |
| I4 | 配置 GitHub Personal Access Token | ✅ | 👤 | I3 | token 已配置到 git remote URL |
| I5 | 配置知识库 cron 定时同步 | ✅ | 🤖 | I4 | 每天凌晨 3 点自动 git pull，日志写入 /var/log/kbs-sync.log |
| I6 | 配置 systemd linger，防止服务随会话停止 | ✅ | 🤖 | - | loginctl enable-linger root |
| I7 | 配置 requireMention:false，群消息无需 @ 机器人 | ✅ | 🤖 | - | openclaw.json channels.feishu.requireMention=false |
| I8 | 本地 webhook server | ✅ | 🤖 | - | 127.0.0.1:19527，开机自启，支持 sync-kbs 指令 |
| I9 | 反向 SSH 隧道 | ✅ | 🤖 | - | 服务器通过隧道访问本地 19527，开机自启 |
| I10 | 账户切换脚本 | ✅ | 🤖 | - | server-scripts/switch-my-account.js，支持4个账户 |
| I11 | 账户切换网页 | ✅ | 🤖 | - | http://39.107.54.166:19528/，欠费时手动切换 |
| I12 | 配置 TOOLS.md / USER.md | ✅ | 🤖 | - | 机器人知道同步知识库和切换账户的操作方法 |
| I17 | 代理节点自动切换脚本 | ✅ | 🤖 | I2 | ~/local/scripts/switch-proxy.py（澳龙 root cron），解析订阅 Clash YAML，测速选最优节点，cron 每小时检测，流量低于 100 MB 发飞书通知 |
| I18 | 多 LLM 模型切换方案 | ✅ | 🤖 | I10, I11 | models-config.json + switch-my-llm.py + account-manager.js 改造 + switch-my-llm Skill；支持 Opus/Sonnet/Haiku/Thinking/MiniMax 切换，自动选可用账户，余额不足自动跳过 |
| I19 | 模型切换页面：选模型后可选账户 | ✅ | 🤖 | I18 | 模型标签页改为两步选择（选模型→显示账户列表→选账户提交），switch-my-llm.py 增加 --account 参数 |

### 第三方服务集成

| # | 任务 | 状态 | 执行者 | 依赖 | 说明 |
|---|------|------|-------|------|------|
| I13 | 创建 Notion Integration，获取 API Token | ✅ | 👤 | - | https://www.notion.so/my-integrations，token 格式 ntn_xxx |
| I14 | 配置 Notion API Key 到 OpenClaw | ✅ | 🤖 | I13 | openclaw.json + systemd drop-in 注入 NOTION_API_KEY |
| I15 | 将目标页面/数据库共享给 Integration | ✅ | 👤 | I13 | 在 Notion 页面点击「...」→「Connect to」→ 选择 Integration |
| I16 | 验证 Notion 读写功能 | ✅ | 👥 | I14, I15 | 飞书群测试通过 |

---

## 持续任务

| # | 任务 | 状态 | 执行者 | 频率 | 说明 |
|---|------|------|-------|------|------|
| C1 | 同步阿乔的共享知识库（本地） | 🔄 | 👤 | 每次工作前 | `git pull`（服务器端已 cron 自动同步） |
| C2 | 更新阿乔的共享知识库内容 | 🔄 | 👥 | 解决问题后 | 记录方案和踩坑，推送后服务器次日自动同步 |
| C3 | 备份 OpenClaw 配置 | ✅ | 🤖 | 每周日 2:00 | cron 已部署，~/local/scripts/backup_openclaw.sh，备份到 ~/backups/openclaw，保留 30 天，飞书通知 |
| C4 | 检查系统更新 | ✅ | 🤖 | 每月 1 号 4:00 | cron 已部署，server-scripts/check_system_update.sh，检查 apt 可更新包，飞书通知 |
| C5 | 检查 OpenClaw 更新 | ✅ | 🤖 | 每周一 3:00 | cron 已部署，server-scripts/check_openclaw_update.sh，比较 npm 版本，飞书通知 |
| C6 | Skill 学习与扩展 | ➡️ | 👥 | 持续 | 已转移到 skills-dev 项目管理 |
| C7 | 同步 Skill 到服务器 | ➡️ | 👤 | 开发完成后 | 已转移到 skills-dev 项目管理 |

---

## 待讨论/待定事项

| # | 事项 | 状态 | 优先级 | 说明 |
|---|------|------|-------|------|
| D12 | 手机远程控制 Claude Code（Remote Control） | ⏸️ | 中 | 暂缓：①当前版本 2.1.56 尚未包含 `remote-control` 命令 ②需直接登录 claude.ai 的 Pro/Max 账号，目前无此类账号。方案文档：[mobile-remote-control.md](./guides/mobile-remote-control.md) |
| D1 | 飞书授权方案最终确认 | ⬜ | 中 | 需要在实际项目中验证 |
| D2 | 团队成员 Tailscale 邀请 | ⬜ | 低 | 团队扩展时处理 |
| D3 | ClawHub 私有仓库设置 | ⬜ | 低 | 可选，用于 Skill 分发 |
| D4 | Mac Mini 购买评估 | ⏸️ | 低 | 当树莓派性能不足或需要本地运行 LLM 时再考虑 |
| D5 | 多模型配置详情 | ✅ | - | 已确认：Claude 中继（zjz-ai）、MiniMax（api.minimaxi.com/anthropic） |
| D6 | 配置 Gemini API | ⬜ | 低 | 用于 nano-banana-pro 等 Skills，需申请 Google API Key |
| D7 | 配置 Google Places API | ⬜ | 低 | 用于 goplaces Skill，需申请 Google API Key |
| D8 | 配置 Notion API | ✅ | 中 | 已迁移为正式任务 I13-I16 |
| D9 | 配置 OpenAI API | ⬜ | 低 | 用于 openai-image-gen Skill（图片生成），可选 |
| D10 | 配置 Brave Search API | ⏸️ | 中 | 已有 ddg-web-search + baidu-search 覆盖，Brave 已无免费套餐，暂缓 |
| D11 | 阿里云服务器配置代理 | ✅ | 中 | sing-box 代理已运行（127.0.0.1:7890），git 全局代理已配置，GitHub token 已配置，知识库可正常 git pull |
| D13 | 云船 simple-proxy.py 开机自启 | ✅ | 中 | start-openclaw.bat 已更新并替换，含 Tailscale + simple-proxy + account-manager |
| D14 | 云船 Tailscale 开机自启 | ✅ | 中 | start-openclaw.bat 已更新并替换，含 Tailscale + simple-proxy + account-manager |
| D15 | 澳龙用户迁移：root → openclaw | ✅ | 高 | OpenClaw 全部迁移到 /home/openclaw/；systemd user services（gateway + account-switcher）+ loginctl linger；cron 迁移到 openclaw 用户；root 仅保留 frps + switch-proxy.py |
| D16 | 澳龙 root 旧文件清理 | ✅ | 中 | 已删除：.openclaw/、backups/、workspace 符号链接、systemd user 服务文件、杂项文档、frp tar.gz；frps + switch-proxy.py 已迁移到 openclaw 用户，root 仅保留系统级服务 |
| D17 | 笔记本部署 OpenClaw | ⬜ | 低 | Windows 11 本地安装 OpenClaw Gateway，Tailscale 已就绪 |
| D18 | 手机部署 OpenClaw | ⬜ | 低 | Android 端 OpenClaw 部署方案待调研 |

---

## 变更记录

| 日期 | 变更内容 |
|-----|---------|
| 2026-03-13 | 新建 myclaws-inventory.md：龙虾资产库——各台机器软硬件配置、访问方式、运行服务、cron 任务、Skills 部署状态一览；含草莓派/笔记本/手机（待部署）规划 |
| 2026-03-13 | 日志统一到 ~/log/：云船 5 个服务日志从 /tmp/ 和 ~/local/ 迁入 ~/log/，两台服务器 cron 任务加日志输出（cron-*.log），澳龙 frps + switch-proxy.py 从 root 迁到 openclaw 用户（sudoers 授权 sing-box 重启）；更新 deploy-cloud-wsl1-frp.md、server-config.md、shared-info-design.md |
| 2026-03-13 | account-manager.js 迁移到 server-scripts/：从 ~/.openclaw/ 移至 ~/workspace/arqiao-shared-knowledge/server-scripts/，更新 design.md、server-config.md、deploy-cloud-wsl1-frp.md、post-install-checklist.md 中的路径引用，修正澳龙 account-switcher.js 旧名 |
| 2026-03-12 | D15/D16 完成：澳龙用户迁移（root→openclaw）全部完成——OpenClaw binary/config/services/cron/SSH 密钥迁移到 /home/openclaw/，systemd user services 启用（gateway+account-switcher），root 旧文件清理完成（保留 frps + switch-proxy.py） |
| 2026-03-12 | 澳龙目录迁移完成：~/workspace 软链接→/home/openclaw/workspace；通用脚本从 /root/scripts/ 迁入 server-scripts/（scp 同步）；个性化脚本(backup_openclaw.sh, switch-proxy.py/sh)迁入 ~/local/scripts/；share-cc/skills.json→~/local/myskills.json；cron 路径全部更新；通用脚本 notify.sh/check_*.sh 改为相对路径（dirname $0），两台服务器同步 |
| 2026-03-12 | D13/D14 完成：start-openclaw.bat 已在联通云智电脑上替换，含 6 项服务自启（SSH→Tailscale→frpc→simple-proxy→OpenClaw→account-manager） |
| 2026-03-12 | 目录规范化：通用脚本从 ~/scripts/ 移入 arqiao-shared-knowledge/server-scripts/（git 同步）；个性化脚本移入 ~/local/scripts/；share-cc/ 废弃，改为 ~/local/myskills.json；start-openclaw.bat 补充 Tailscale + simple-proxy.py + account-manager.js 开机自启 |
| 2026-03-12 | Skill 改名：switch-account → switch-my-account, model-switcher → switch-my-llm；脚本改名：switch-llm.py → switch-my-llm.py, account-switcher.js → account-manager.js；脚本统一迁移到 ~/scripts/（switch-my-account.js）；所有文档引用同步更新 |
| 2026-03-12 | 修复飞书机器人显示旧 skill 名称：根因是 .jsonl 会话历史中 AI 旧回复包含旧名称，模型参考历史继续使用旧名；修复方式：sed 替换 jsonl 文件中旧名称 |
| 2026-03-12 | 新增 ~/scripts/rename-in-sessions.sh 脚本：Skill/脚本改名后自动清理会话历史中的旧名称；TOOLS.md 已添加强制规则 |
| 2026-03-12 | 云船↔澳龙双向代理机制：云船 simple-proxy.py（0.0.0.0:1080）、cloud-ship-switch-proxy.sh；澳龙 switch-proxy.sh（yunchuan 选项）；系统级代理（http_proxy/https_proxy 环境变量 + git config），持久化到 ~/local/.proxy_env |
| 2026-03-11 | V23 完成：澳龙功能全部迁移到云船——脚本(feishu_send/notify/backup/update检查)、账户切换(account-manager.js+switch-llm.py+switch-account.js)、知识库(arqiao-shared-knowledge+ccResearch)、cron任务(知识库同步/备份/更新检查)、OpenClaw extraDirs 配置；account-manager 已加入 start-openclaw.bat 开机自启 |
| 2026-03-11 | V13 完成：知识库克隆到云船 ~/workspace/，OpenClaw extraDirs 指向 arqiao-shared-knowledge/skills |
| 2026-03-11 | V20-V22 完成：Tailscale 内网访问配置（云船、笔记本、手机已加入网络）、关闭公网 18789 端口（frpc 仅保留 SSH 隧道）、控制界面通过 SSH 隧道访问（yunchuan-tunnel） |
| 2026-03-10 | V15-V18 完成：联通云开机自启配置（frpc + OpenClaw Gateway）、MobaXterm 一键连接配置、SSH config 更新、CLAUDE.md 确认无需更新 |
| 2026-03-10 | 文档更新：deploy-cloud-vm.md 重命名为 deploy-cloud-wsl1-frp.md，补充终端标注和故障排查章节 |
| 2026-02-26 | 文档整理：新建 known-limitations.md（已知限制），更新 design.md（热重载机制、网页 UI 交互）、architecture.md（文档索引补全）、deploy-cloud-server.md（重启注意事项）、openclaw-tools-reference.md、task-list.md（文档索引补全）；临时脚本移入 tmptools/ 子目录 |
| 2026-02-26 | I19 完成：模型切换页面改为两步选择（选模型→显示账户列表→选账户提交），switch-llm.py 增加 --account 可选参数，account-manager.js 模型标签页 UI 改造 |
| 2026-02-26 | OpenClaw 升级到 v2026.2.24：pnpm 安装成功（51s），swap 扩到 4G + swappiness=10，systemd 服务路径更新到 pnpm 全局目录，Gateway 正常运行；deploy-cloud-server.md 已更新安装经验 |
| 2026-02-25 | I18 完成：多 LLM 模型切换方案。新建 models-config.json（模型-账户映射）、switch-llm.py（核心切换脚本）、改造 account-manager.js（增加模型切换标签页，默认显示）、创建 model-switcher Skill（飞书群自然语言切换）。支持 5 个模型、余额不足自动跳过、次日自动恢复 |
| 2026-02-25 | C3/C4/C5 完成：4 个 cron 脚本部署到服务器（feishu_send.py + notify.sh + 3 个业务脚本），全部验证通过，飞书通知正常；另发现 OpenClaw 有新版 2026.2.24 |
| 2026-02-25 | D12：手机远程控制 Claude Code 方案调研，官方 Remote Control 功能当前版本未包含，加入待办；方案文档 guides/mobile-remote-control.md 已创建 |
| 2026-02-25 | #37、#38 暂缓：已通过代理 + git CLI 覆盖 GitHub 访问需求，无需额外 MCP Server |
| 2026-02-25 | #35 完成：两个接口本地→服务器验证通过；关键修复 models.providers.anthropic.api 需设为 anthropic-messages（中转服务用 Anthropic 原生格式） |
| 2026-02-25 | #34 完成：openclaw-gateway Skill 创建，/tools/invoke 和 /v1/chat/completions 均验证可用，chatCompletions 已在 openclaw.json 启用 |
| 2026-02-25 | #33 完成：OpenClaw Gateway API 研究，/tools/invoke 已验证可用，token 在 /root/.openclaw/openclaw.json |
| 2026-02-25 | 树莓派第三阶段改为低优先级；#36 标记为已完成（token 已配置，gh CLI 已装） |
| 2026-02-25 | proxy-switch.py 新增流量监控（低于 100 MB 发飞书通知），cron 检测间隔改为 60 分钟 |
| 2026-02-25 | I17：代理节点自动切换脚本，解析订阅 Clash YAML，cron 每 10 分钟自动检测切换，TOOLS.md 已更新 |
| 2026-02-25 | 新建 design.md，记录架构设计决策（key 管理、git 同步、systemd 注入、目录规范） |
| 2026-02-25 | API Key 安全整改：git filter-branch 清除历史明文 key，服务器 key 迁移到 /root/.secrets，本地 key 迁移到 noshare/env.md，git credential store 替代 remote URL 嵌 token |
| 2026-02-25 | I13-I16：Notion 集成完成，systemd drop-in 注入 NOTION_API_KEY，飞书群验证通过 |
| 2026-02-24 | 新增第三方服务集成章节（I13-I16）：Notion 集成，从 skills-dev #9/#10 迁移过来 |
| 2026-02-24 | I6-I12：linger配置、无需@机器人、本地webhook、反向隧道、账户切换脚本+网页、TOOLS.md配置 |
| 2026-02-23 | 新增基础设施补充章节（I1-I5）：服务器代理、GitHub token、cron 自动同步；新增持续任务 C7；C1 说明更新 |
| 2026-02-23 | D11 完成：服务器代理配置完成，GitHub token 配置，知识库 cron 定时同步已启用 |
| 2026-02-20 | 飞书集成完成（#24-27），使用 OpenClaw 内置插件 |
| 2026-02-15 | 初始创建任务清单 |
| 2026-02-15 | 新增 MCP 集成任务，调整为第二阶段（树莓派之前） |
| 2026-03-10 | 方案调整：Hyper-V / WSL2 均因嵌套虚拟化不可用，改为 WSL1 方案；文档和任务清单同步更新 |
| 2026-03-10 | 新增联通云智电脑部署阶段（V1-V18）：WSL1 + Ubuntu，公网 IP 195.64.7.45，替代阿里云轻量服务器；新建 guides/deploy-cloud-vm.md |
| 2026-03-10 | 服务器命名方案确定：阿里云（frp中继，39.107.54.166）命名为"澳龙"，联通云（OpenClaw主机，195.64.7.45）命名为"云船" |
| 2026-03-11 | 云船OpenClaw配置迁移完成：飞书配置已迁移，Gateway bind改为loopback解决WSL1网络问题，frp隧道正常工作，澳龙OpenClaw已停止仅作frp中继 |
| 2026-03-11 | SSH配置优化：云船SSH密钥认证已配置（免密登录），添加yunchuan快捷方式（端口12222） |
| 2026-02-15 | MCP 优先级调整：飞书优先于微信（官方 API 支持好，风险低） |


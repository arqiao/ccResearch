# CoPaw 备选方案

> 创建时间：2026-02-15
> 状态：备选方案，可快速体验

---

## 一、CoPaw 简介

CoPaw 是阿里云通义团队推出的个人智能助理，对标 OpenClaw，由 AgentScope 团队基于其生态构建。

- **名称含义**：Co Personal Agent Workstation（协同个人智能体工作台）
- **开源状态**：即将在 GitHub 开源
- **官方文档**：http://copaw.agentscope.io/

---

## 二、核心特点

### 2.1 安装极简

**本地安装（3条命令）：**

```bash
pip install copaw
copaw init
copaw start
```

**云端一键部署：**

直接在魔搭创空间部署，无需本地安装：
https://modelscope.cn/studios/AgentScope/CoPaw

> 注意：使用创空间时请将空间设为非公开

### 2.2 多频道接入

支持的频道：
- 钉钉
- 飞书
- QQ
- Discord
- iMessage
- 原生 Console

### 2.3 Skill 扩展

- 内置 Skills：cron、file_reader、pdf、docx、pptx、xlsx、news 等
- 支持自定义 Skill（SKILL.md + 描述）
- 通过控制台启用/禁用、编辑

### 2.4 长期记忆

- PROFILE.md 定义 CoPaw 的"灵魂"
- 自动记录对话中的重要决策、偏好、待办
- 心跳期间做记忆维护

---

## 三、与 OpenClaw 对比

| 对比项 | CoPaw | OpenClaw |
|-------|-------|----------|
| 安装难度 | 极简（3条命令） | 需配置环境 |
| 云端部署 | 魔搭创空间一键 | 需自建服务器 |
| 频道支持 | 钉钉/飞书/QQ等 | 多频道 |
| Skill 兼容 | AgentScope 生态 | ClawHub 生态 |
| 成熟度 | 新发布 | 较成熟 |
| 自主可控 | 云端有依赖 | 完全自主 |

---

## 四、适用场景

**推荐使用 CoPaw 的情况：**

1. 想快速体验，不想折腾环境配置
2. 临时需要 AI 助理，不需要长期运行
3. 主要使用钉钉/飞书沟通
4. 想尝试 AgentScope 生态

**继续使用 OpenClaw 的情况：**

1. 需要长期稳定运行
2. 需要完全自主可控
3. 已有 OpenClaw 部署经验
4. 团队共享场景

---

## 五、快速体验步骤

### 5.1 魔搭创空间（零配置）

1. 访问 https://modelscope.cn/studios/AgentScope/CoPaw
2. 登录魔搭账号
3. Fork 空间到自己账号
4. 将空间设为非公开
5. 在浏览器中直接使用

### 5.2 本地安装

```bash
# 环境要求：Python 3.10-3.13

# 安装
pip install copaw

# 初始化（配置频道、API Key 等）
copaw init

# 启动
copaw start

# 访问 http://127.0.0.1:8088
```

---

## 六、与现有方案的整合

CoPaw 可以作为 OpenClaw 的补充：

| 场景 | 使用方案 |
|-----|---------|
| 长期运行的 Gateway | OpenClaw（部署到服务器/树莓派） |
| 快速体验/临时使用 | CoPaw（魔搭创空间） |
| 本地桌面自动化 | QoderWork |

---

## 附录：相关链接

- [CoPaw 官方文档](http://copaw.agentscope.io/)
- [魔搭创空间](https://modelscope.cn/studios/AgentScope/CoPaw)
- [AgentScope GitHub](https://github.com/modelscope/agentscope)
- [IT之家报道](https://www.ithome.com/0/921/812.htm)

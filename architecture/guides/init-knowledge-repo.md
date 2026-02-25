# 知识仓库初始化指南

> 本文档指导如何创建和初始化共享知识仓库

---

## 一、创建 Git 仓库

### 1.1 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名称：`shared-knowledge`
3. 可见性：Private（推荐，团队使用）
4. 勾选 "Add a README file"
5. 点击 "Create repository"

**注意：** 已确认使用 GitHub 作为 Git 托管平台。

### 1.2 克隆到本地

```bash
# Windows
cd D:\workspace
git clone https://github.com/YOUR_USERNAME/shared-knowledge.git
cd shared-knowledge

# Linux/macOS
cd ~/workspace
git clone https://github.com/YOUR_USERNAME/shared-knowledge.git
cd shared-knowledge
```

---

## 二、创建目录结构

```bash
# 创建目录
mkdir -p skills/feishu-auth
mkdir -p skills/knowledge-query
mkdir -p skills/knowledge-update
mkdir -p solutions/feishu
mkdir -p interfaces/api-contracts
mkdir -p interfaces/data-models
mkdir -p pitfalls
mkdir -p templates
```

---

## 三、创建核心文件

### 3.1 仓库 README.md

```markdown
# 共享知识库

团队共享的技术方案、接口定义、踩坑记录。

## 目录结构

- `skills/` - OpenClaw 兼容的 Skill 定义
- `solutions/` - 技术解决方案
- `interfaces/` - 接口定义
- `pitfalls/` - 踩坑记录
- `templates/` - 文档模板

## 使用方式

### Claude Code 用户

在对话中说：
- "查一下飞书授权的方案" → 会读取 solutions/feishu/
- "更新知识库" → 会引导你添加新内容

### OpenClaw 用户

Skills 会自动加载，使用 `/feishu-auth-helper` 等命令。

## 贡献指南

1. 解决问题后，使用对应模板记录
2. 提交 PR 或直接 push（小团队）
3. 重要变更请通知相关人员
```

### 3.2 CLAUDE.md（让 CC 理解仓库）

```markdown
# 知识仓库使用指南

这是一个共享知识仓库，包含团队积累的技术方案和经验。

## 目录说明

- `solutions/` - 已验证的技术解决方案，按领域分类
- `interfaces/` - 团队共享的接口定义和数据模型
- `pitfalls/` - 踩过的坑和解决方法
- `skills/` - OpenClaw Skill 定义（可忽略）

## 使用规则

1. 遇到技术问题时，先在 solutions/ 和 pitfalls/ 中搜索
2. 解决新问题后，提醒用户更新到对应目录
3. 使用 templates/ 中的模板保持格式统一

## 文件命名约定

- 使用小写字母和连字符：`auth-refresh.md`
- 按功能而非时间命名
```

---

## 四、创建 Skill 文件

### 4.1 skills/feishu-auth/SKILL.md

```markdown
---
name: feishu-auth-helper
description: 飞书 API 授权问题的标准解决方案
user-invocable: true
metadata: {"openclaw": {"requires": {"env": ["FEISHU_APP_ID"]}}}
---

# 飞书授权问题处理

当用户遇到飞书 API 授权相关问题时，按以下流程处理：

## 步骤

1. **读取现有方案**
   - 查看 {baseDir}/../solutions/feishu/auth-refresh.md
   - 确认是否有适用的解决方案

2. **诊断问题**
   - 授权过期（2小时限制）→ 使用 refresh_token 方案
   - 权限不足 → 检查应用权限配置
   - 其他问题 → 查看 pitfalls/feishu-pitfalls.md

3. **实施方案**
   - 按文档步骤操作
   - 记录遇到的新问题

4. **更新知识库**
   - 如果遇到新问题，添加到 pitfalls/
   - 如果有更好的方案，更新 solutions/
```

### 4.2 skills/knowledge-query/SKILL.md

```markdown
---
name: knowledge-query
description: 查询共享知识库中的技术方案和经验
user-invocable: true
---

# 知识库查询

帮助用户在共享知识库中查找信息。

## 触发词

- "查知识库"
- "有没有 xxx 的方案"
- "之前怎么解决 xxx 的"

## 流程

1. **确定查询类型**
   - 技术方案 → solutions/
   - 接口定义 → interfaces/
   - 踩坑记录 → pitfalls/

2. **搜索相关文件**
   - 在对应目录中搜索关键词
   - 列出匹配的文件

3. **展示内容**
   - 读取并展示相关文档
   - 如果没找到，告知用户并建议创建
```

### 4.3 skills/knowledge-update/SKILL.md

```markdown
---
name: knowledge-update
description: 将新解决的问题更新到共享知识库
user-invocable: true
---

# 知识库更新

当用户解决了一个可复用的技术问题时，帮助记录到知识库。

## 触发词

- "更新知识库"
- "记录一下这个方案"
- "把这个坑记下来"

## 流程

1. **确定内容类型**
   询问用户：这是什么类型的内容？
   - 技术解决方案 → solutions/
   - 踩坑记录 → pitfalls/
   - 接口定义 → interfaces/

2. **收集信息**
   - 问题描述
   - 解决方案
   - 注意事项

3. **生成文档**
   - 使用 templates/ 中的模板
   - 生成标准格式的文档

4. **保存并提交**
   - 写入对应目录
   - 执行 git add && git commit && git push
   - 通知用户更新完成
```

---

## 五、创建模板文件

### 5.1 templates/solution-template.md

```markdown
# [问题标题]

> 创建时间：YYYY-MM-DD
> 最后更新：YYYY-MM-DD
> 状态：已验证 / 待验证

## 问题描述

[简要描述遇到的问题]

## 解决方案

### 方案概述

[一句话描述解决思路]

### 实施步骤

1. 步骤一
2. 步骤二
3. 步骤三

### 代码示例

```[language]
// 代码示例
```

## 注意事项

- 注意点 1
- 注意点 2

## 相关链接

- [官方文档](url)
- [相关 Issue](url)
```

### 5.2 templates/pitfall-template.md

```markdown
# [坑的标题]

> 发现时间：YYYY-MM-DD
> 影响范围：[项目/模块]

## 现象

[描述遇到的问题现象]

## 原因

[分析问题的根本原因]

## 解决方法

[如何解决或规避]

## 教训

[从这个坑中学到了什么]
```

---

## 六、创建示例内容

### 6.1 solutions/feishu/auth-refresh.md

```markdown
# 飞书 API 授权刷新方案

> 创建时间：2026-02-15
> 最后更新：2026-02-15
> 状态：已验证

## 问题描述

飞书 API 的 access_token 有效期只有 2 小时，频繁过期导致需要重新授权。

## 解决方案

### 方案概述

使用 refresh_token 机制自动刷新 access_token，避免频繁手动授权。

### 实施步骤

1. 首次授权时保存 refresh_token
2. 在 access_token 过期前（建议提前 10 分钟）使用 refresh_token 获取新 token
3. 更新存储的 token 信息

### 代码示例

```typescript
async function refreshAccessToken(refreshToken: string): Promise<TokenInfo> {
  const response = await fetch('https://open.feishu.cn/open-apis/authen/v1/refresh_access_token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
    }),
  });

  const data = await response.json();
  return {
    accessToken: data.data.access_token,
    refreshToken: data.data.refresh_token,
    expiresIn: data.data.expires_in,
  };
}
```

## 注意事项

- refresh_token 也有有效期（通常 30 天），需要在过期前更新
- 建议将 token 信息持久化存储
- 刷新失败时需要重新走完整授权流程

## 相关链接

- [飞书开放平台文档](https://open.feishu.cn/document/)
```

### 6.2 pitfalls/feishu-pitfalls.md

```markdown
# 飞书 API 踩坑记录

## 1. access_token 2 小时过期

> 发现时间：2026-02-15

### 现象

API 调用突然返回 token 无效错误。

### 原因

飞书 access_token 有效期只有 2 小时。

### 解决方法

参考 solutions/feishu/auth-refresh.md 使用 refresh_token 方案。

---

## 2. [待补充]

> 发现时间：

### 现象

### 原因

### 解决方法
```

---

## 七、提交到 Git

```bash
# 添加所有文件
git add -A

# 提交
git commit -m "初始化知识仓库结构"

# 推送
git push origin main
```

---

## 八、配置环境变量

### Windows

```powershell
[Environment]::SetEnvironmentVariable("SHARED_KNOWLEDGE_PATH", "D:\workspace\shared-knowledge", "User")
```

### Linux/macOS

```bash
echo 'export SHARED_KNOWLEDGE_PATH="$HOME/workspace/shared-knowledge"' >> ~/.bashrc
source ~/.bashrc
```

---

## 九、配置全局 CLAUDE.md

在 `~/.claude/CLAUDE.md` 中添加：

```markdown
## 共享知识仓库

路径：$SHARED_KNOWLEDGE_PATH（或 D:\workspace\shared-knowledge）

当遇到以下情况时，优先查阅共享知识仓库：
- 飞书相关问题 → solutions/feishu/
- 接口定义问题 → interfaces/
- 不确定的技术选型 → pitfalls/

当解决了一个可复用的技术问题时，提醒我更新到共享知识仓库。
```

---

## 十、验证

1. 在 Claude Code 中测试：
   - "帮我查一下飞书授权的方案"
   - 应该能读取到 solutions/feishu/auth-refresh.md

2. 在 OpenClaw 中测试（如果已部署）：
   - `/feishu-auth-helper`
   - 应该能触发对应 Skill

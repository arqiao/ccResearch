# Skills 清单

> 统一管理所有 Skill 的安装状态，后续安装/更新时同步维护。
> 最后更新：2026-02-25

## 第一部分：自定义 Skill（28 个）

本地路径：`D:\workspace\kbs\arqiao-shared-knowledge\skills\`
服务器路径：`/home/openclaw/workspace/arqiao-shared-knowledge/skills/`
本地和服务器已完全同步。

### 搜索与阅读（3 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| baidu-search | ready | ready | ClawHub | 百度 AI 搜索，需 BAIDU_API_KEY |
| ddg-web-search | ready | ready | ClawHub | DuckDuckGo 搜索，无需 API Key |
| url-reader | ready | ready | ClawHub | 智能读取任意 URL，支持微信/小红书/头条等中国主流平台 |

### 飞书（3 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| feishu-common | ready | ready | 自己开发 | 飞书公共认证和 API 辅助模块 |
| feishu-doc | ready | ready | ClawHub | 读取飞书 Wiki/文档/表格/多维表格，自动转 Markdown |
| feishu-user-auth | ready | ready | 自己开发 | 飞书 OAuth 用户授权，支持 token 自动刷新 |

### 微信（3 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| wechat-article-extractor-skill | ready | ready | ClawHub | 提取微信公众号文章元数据和正文内容 |
| wechat-article-fetcher | ready | ready | 自己开发 | 抓取微信公众号文章正文，支持单篇和批量 |
| wechat-article-search | ready | ready | ClawHub | 搜索微信公众号文章，返回标题/概要/来源等 |

### 经验沉淀（2 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| web-article-parser | ready | ready | 自己开发 | 从 URL 提取文章元信息（标题/日期/来源），支持 15+ 网站 |
| web-article-scraper | ready | ready | 自己开发 | 抓取网页文章正文，支持微信/飞书/腾讯云等 |

### 视频（4 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| seedance-2-prompt-engineering-skill | ready | ready | ClawHub | Seedance 2.0 高控制英文提示词创作 |
| seedance-guide | ready | ready | ClawHub | Seedance 2.0 分镜导演，从创意到专业视频提示词 |
| seedance-storyboard-creator | ready | ready | 自己开发 | Seedance 2.0 多模态分镜提示词创作助手 |
| seedance-video-generation | ready | ready | ClawHub | 字节 Seedance AI 视频生成，支持文生视频/图生视频 |

### 图片（2 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| seedream-image-for-openclaw | ready | ready | 自己开发 | 火山引擎 Seedream-4.5 文生图/图生图 |
| volcengine-ai-image-generation | ready | ready | ClawHub | 火山引擎 AI 图片生成工作流 |

### 文档处理（5 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| docx | ready | ready | GitHub | Word 文档创建/读取/编辑 |
| markdown-converter | ready | ready | GitHub | 多格式转 Markdown（PDF/Word/PPT/Excel/HTML 等） |
| pdf | ready | ready | GitHub | PDF 读取/合并/拆分/水印/OCR 等 |
| pptx | ready | ready | GitHub | PowerPoint 创建/读取/编辑 |
| xlsx | ready | ready | GitHub | Excel 创建/读取/编辑/图表 |

### 设计（1 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| frontend-design | ready | ready | GitHub | 高质量前端界面/组件/页面设计与代码生成 |

### 工具（4 个）

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| knowledge-query | ready | ready | 自己开发 | 查询共享知识库中的技术方案和踩坑记录 |
| local-sync | ready | ready | 自己开发 | 同步本地 Windows 知识库 |
| openclaw-gateway | ready | ready | 自己开发 | 通过 SSH 隧道调用服务器 OpenClaw Gateway HTTP API |
| switch-my-account | ready | ready | 自己开发 | 切换 OpenClaw 使用的模型账户 |
| switch-my-llm | ready | ready | 自己开发 | 切换 OpenClaw 使用的 LLM 模型 |

### yunshu 分享（12 个）

位于 `friends-shared/yunshu_skillshub/` 目录。

| Skill 名称 | 本地状态 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|---|
| image-assistant | ready | ready | yunshu | 配图助手 |
| lesson-builder | ready | ready | yunshu | 课程大纲和课件制作 |
| prd-doc-writer | ready | ready | yunshu | PRD/需求文档撰写 |
| priority-judge | ready | ready | yunshu | 优先级判断 |
| project-map-builder | ready | ready | yunshu | 项目地图构建 |
| req-change-workflow | ready | ready | yunshu | 需求变更工作流 |
| thinking-partner | ready | ready | yunshu | 思维伙伴 |
| thought-mining | ready | ready | yunshu | 思维挖掘，零散想法整理成文 |
| ui-design | ready | ready | yunshu | UI 设计 |
| version-planner | ready | ready | yunshu | 版本规划 |
| weekly-report | ready | ready | yunshu | 周报生成 |
| writing-assistant | ready | ready | yunshu | 写作助手 |

## 第二部分：已安装的内置 Skill（约 14 个）

服务器路径：`/usr/lib/node_modules/openclaw/skills/`
本地不适用（内置 Skill 只在 OpenClaw 服务器运行）。

> ⚠️ 以下基于已有记录整理，待服务器恢复后用 `openclaw skills list` 校验补充。

| Skill 名称 | 服务器状态 | 来源 | 概要说明 |
|---|---|---|---|
| healthcheck | ready | OpenClaw 原生 | 健康检查 |
| skill-creator | ready | OpenClaw 原生 | 辅助创建规范的 Skill |
| tmux | ready | OpenClaw 原生 | 终端会话管理 |
| weather | ready | OpenClaw 原生 | 天气查询 |
| clawhub | ready | OpenClaw 原生 | ClawHub CLI，搜索/安装社区 Skill |
| gh | ready | OpenClaw 原生 | GitHub CLI 集成 |
| mcporter | ready | OpenClaw 原生 | MCP 协议支持 |
| playwright | ready | OpenClaw 原生 | 网页自动化（Chromium，两端已安装） |

> 总计 42 ready - 28 自定义 = 约 14 个内置 ready，上表仅列出已确认的 8 个，剩余待校验。

## 第三部分：Missing Skill（42 个）

> ⚠️ 以下基于已有记录整理，待服务器恢复后用 `openclaw skills list` 校验补充。

### 可安装 — 无需 API Key（约 7 个）

| Skill 名称 | 分类 | 来源 | 概要说明 |
|---|---|---|---|
| session-logs | 日志 | OpenClaw 原生 | 会话日志记录 |
| video-frames | 视频 | OpenClaw 原生 | 视频帧提取 |
| blogwatcher | 监控 | OpenClaw 原生 | 博客更新监控 |

> 其余约 4 个待校验。

### 需 API Key（约 9 个）

| Skill 名称 | 分类 | 来源 | 概要说明 | 所需 Key |
|---|---|---|---|---|
| brave-search | 搜索 | OpenClaw 原生 | Brave 联网搜索 | BRAVE_API_KEY |
| firecrawl | 抓取 | OpenClaw 原生 | 网页抓取服务 | FIRECRAWL_API_KEY |
| tavily-search | 搜索 | OpenClaw 原生 | Tavily AI 搜索 | TAVILY_API_KEY |
| nano-banana-pro | 图片 | OpenClaw 原生 | 图片生成 | Gemini API Key |
| openai-image-gen | 图片 | OpenClaw 原生 | DALL-E 图片生成 | OPENAI_API_KEY |
| goplaces | 地图 | OpenClaw 原生 | Google Places 查询 | GOOGLE_PLACES_API_KEY |

> 其余约 3 个待校验。

### macOS 专属（约 7 个）

| Skill 名称 | 来源 | 概要说明 |
|---|---|---|
| apple-notes | OpenClaw 原生 | Apple Notes 集成 |
| apple-reminders | OpenClaw 原生 | Apple Reminders 集成 |

> 其余约 5 个待校验。Linux 服务器不可用。

### 硬件/服务依赖（约 12 个）

| Skill 名称 | 来源 | 概要说明 |
|---|---|---|
| home-assistant | OpenClaw 原生 | 智能家居控制 |
| linear | OpenClaw 原生 | Linear 项目管理集成 |

> 其余约 10 个待校验。需要对应硬件或第三方服务。

---

## 校验清单

服务器恢复后执行以下命令，对照本文件补充：

```bash
# 获取完整列表
ssh openclaw-cloud "openclaw skills list"

# 筛选内置 ready（排除自定义目录）
ssh openclaw-cloud "openclaw skills list" | grep ready

# 筛选 missing
ssh openclaw-cloud "openclaw skills list" | grep missing
```

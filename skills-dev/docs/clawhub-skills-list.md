# ClawHub 可用 Skill 清单

> 整理于 2026-02-19，基于 clawhub search 结果

## 飞书相关（高优先级）

| Skill | 版本 | 说明 | 需要 API Key |
|-------|------|------|-------------|
| feishu-doc | 1.2.7 | 读取飞书 Wiki、文档、表格、多维表格，自动转 Markdown | ✅ 飞书 |
| feishu-doc-manager | 1.0.0 | 发布 Markdown 到飞书文档，支持表格转换 | ✅ 飞书 |
| feishu-bridge | 1.0.0 | 飞书机器人桥接，WebSocket 长连接 | ✅ 飞书 |
| feishu-messaging | 0.0.3 | 飞书消息发送 | ✅ 飞书 |
| feishu-docx-powerwrite | 0.1.0 | 飞书文档增强写入 | ✅ 飞书 |
| lark-integration | 1.0.0 | Lark（飞书国际版）集成 | ✅ Lark |
| lark-calendar | 1.0.0 | Lark 日历和任务 | ✅ Lark |

### 推荐优先级

1. **feishu-doc** - 读取飞书文档，支持 Wiki/Docs/Sheets/Bitable
2. **feishu-doc-manager** - 写入飞书文档，Markdown 自动转换
3. **feishu-bridge** - 飞书机器人集成

### 飞书 API Key 获取

1. 访问飞书开放平台：https://open.feishu.cn
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 配置相应权限（文档读写、消息等）

## 微信相关（高优先级）

| Skill | 版本 | 说明 | 需要 API Key |
|-------|------|------|-------------|
| wechat-article-extractor-skill | 1.0.1 | 微信公众号文章解析，提取元数据和内容 | ❌ |
| wechat-article-search | 0.1.0 | 搜索微信公众号文章，返回标题、概要、来源 | ❌ |
| wechat-search | 1.0.3 | 微信公众号文章搜索（基于 Tavily） | 视情况 |
| wechat-mp-publisher | 2.0.2 | 微信公众号发布 | ✅ 微信 |
| wechat-publisher | 0.1.0 | 微信内容发布 | ✅ 微信 |

### 推荐优先级

1. **wechat-article-extractor-skill** - 解析公众号文章，无需 API
2. **wechat-article-search** - 搜索公众号文章，无需 API
3. **url-reader**（前面已列）- 也支持微信公众号

## 网页搜索相关

| Skill | 版本 | 说明 | 需要 API Key |
|-------|------|------|-------------|
| ddg-web-search | 1.0.0 | DuckDuckGo 搜索，无需 API Key | ❌ |
| baidu-search | 1.1.0 | 百度 AI 搜索 | ❌ |
| tavily-search | 1.0.0 | Tavily AI 优化搜索 | ✅ Tavily |
| multi-search-engine | 2.0.1 | 多搜索引擎聚合 | 视情况 |
| web-search-pro | 1.0.0 | 专业网页搜索 | 视情况 |
| searxng-local-search | 0.1.0 | SearXNG 本地搜索 | ❌ 需自建 |

### 推荐优先级

1. **ddg-web-search** - 无需 API Key，作为 web_search 的备选方案
2. **baidu-search** - 中文搜索效果好，无需 API Key
3. **tavily-search** - AI 优化结果，需要 Tavily API Key

## 网页阅读/抓取相关

| Skill | 版本 | 说明 | 需要 API Key |
|-------|------|------|-------------|
| url-reader | 0.1.1 | 智能读取 URL，支持微信公众号、小红书、抖音、淘宝等中国平台 | ❌ |
| jina-reader | 1.1.0 | Jina AI 网页提取，支持 read/search/ground 三种模式 | ✅ Jina |
| markdown-fetch | 1.0.0 | 网页转 Markdown | ❌ |
| webfetch-md | 1.1.0 | 网页抓取转 Markdown | ❌ |
| rss-ai-reader | 1.0.0 | RSS AI 阅读器 | 视情况 |

### 推荐优先级

1. **url-reader** - 支持中国主流平台，自动保存 Markdown 和图片
2. **jina-reader** - 功能强大，支持搜索和事实核查
3. **markdown-fetch** - 简单网页转换

## 即梦/火山引擎相关（seeDance/seeDream）

| Skill | 版本 | 说明 | 需要 API Key |
|-------|------|------|-------------|
| seedance-video-generation | 1.0.3 | Seedance 视频生成，支持文生视频、图生视频 | ✅ 火山引擎 |
| seedance2-api | 1.1.0 | Seedance 2.0 API 封装 | ✅ 火山引擎 |
| seedance-2-prompt-engineering-skill | 1.0.0 | Seedance 2.0 提示词工程 | ❌ |
| seedance-prompt-en | 1.0.1 | Seedance 2.0 英文提示词写作 | ❌ |
| seedance-guide | 1.0.0 | Seedance 2.0 使用指南 | ❌ |
| seedance-cog | 1.0.0 | Seedance 认知处理 | 视情况 |
| volcengine-ai-video-generation | 1.0.0 | 火山引擎视频生成（通用） | ✅ 火山引擎 |
| volcengine-ai-image-generation | 1.0.0 | 火山引擎图片生成（通用） | ✅ 火山引擎 |

### 推荐优先级

1. **seedance-video-generation** - 直接对接 Seedance，支持 1.5 Pro（带音频）、1.0 Pro 等
2. **seedance-2-prompt-engineering-skill** - 提示词优化，无需 API
3. **volcengine-ai-video-generation** - 火山引擎通用方案

### 火山引擎 API Key 获取

即梦（Jimeng）基于火山引擎，需要：
1. 注册火山引擎账号：https://www.volcengine.com
2. 开通视觉智能服务
3. 获取 Access Key ID 和 Secret Access Key

## 视频制作相关

| Skill | 版本 | 说明 | 评分 |
|-------|------|------|------|
| ffmpeg-video-editor | 1.0.0 | FFmpeg 视频编辑 | 3.530 |
| ffmpeg-cli | 1.0.0 | FFmpeg 命令行封装 | 3.527 |
| video-frames | 1.0.0 | 视频帧提取 | 3.536 |
| remotion-video-toolkit | 1.4.0 | Remotion 视频工具包（React 视频） | 3.433 |
| demo-video | 1.0.0 | Demo 视频创建 | 3.423 |
| video-subtitles | 1.0.0 | 视频字幕处理 | 3.387 |
| video-cog | 1.0.3 | 视频认知处理 | 3.370 |
| video-generation | 1.0.0 | 视频生成 | 3.294 |
| veo | 1.3.0 | Google Veo 视频生成 | 0.918 |
| grok-imagine-video | 1.0.4 | Grok 视频生成 | 0.795 |

### 推荐优先级

1. **ffmpeg-video-editor** / **ffmpeg-cli** - 基础视频处理，无需 API
2. **video-frames** - 视频帧提取，配合图片处理
3. **remotion-video-toolkit** - 程序化视频生成（需要 Node.js）

## 图片生成相关

| Skill | 版本 | 说明 | 评分 |
|-------|------|------|------|
| antigravity-image-gen | 2.0.0 | Antigravity 图片生成 | 3.495 |
| image-cog | 1.0.2 | 图片认知处理 | 3.469 |
| image | 1.0.3 | 通用图片处理 | 3.449 |
| gemini-image-simple | 1.1.0 | Gemini 简易图片生成 | 3.414 |
| gemini-image-gen | 1.3.1 | Gemini 图片生成（完整版） | 3.407 |
| qwen-image | 1.0.0 | 通义千问图片生成 | 3.406 |
| image-edit | 1.0.0 | 图片编辑 | 3.341 |
| openai-image-gen | 1.0.1 | OpenAI DALL-E 图片生成 | 1.031 |
| bria-ai | 0.0.2 | Bria AI 图片生成和编辑 | 0.794 |

### 推荐优先级

1. **gemini-image-gen** - 需要 Gemini API Key（任务 #11）
2. **qwen-image** - 国内可用，通义千问
3. **openai-image-gen** - 需要 OpenAI API Key（任务 #13）

## 多模态/综合

| Skill | 版本 | 说明 | 评分 |
|-------|------|------|------|
| openclaw-aisa-image-video-models | 1.0.0 | Gemini 3 Pro + Qwen Wan 2.6，一个 Key 搞定图片和视频 | 3.292 |
| gemini | 1.0.0 | Gemini 通用能力 | 3.692 |
| gemini-deep-research | 1.0.0 | Gemini 深度研究 | 3.424 |
| gemini-web-search | 1.0.0 | Gemini 网页搜索 | 3.405 |

## 其他实用 Skill

| Skill | 版本 | 说明 | 评分 |
|-------|------|------|------|
| gemini-yt-video-transcript | 1.0.4 | YouTube 视频转文字 | 3.390 |
| gemini-stt | 1.1.0 | Gemini 语音转文字 | 3.286 |
| table-image | 1.0.0 | 表格转图片 | 3.379 |
| github-image-hosting | 1.0.0 | GitHub 图床 | 3.263 |

## 安装方式

```bash
# 查看 Skill 详情
npx clawhub info <skill-name>

# 安装 Skill
npx clawhub install <skill-name>

# 或在 OpenClaw 中
openclaw skills install <skill-name>
```

## 下一步行动

1. 安装 **ffmpeg-cli** 或 **ffmpeg-video-editor** 作为视频处理基础
2. 配置 Gemini API Key 后安装 **gemini-image-gen**
3. 考虑 **openclaw-aisa-image-video-models** 作为一站式方案

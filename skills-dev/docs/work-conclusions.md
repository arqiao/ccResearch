# 工作结论汇总

> 最后更新：2026-02-23

---

## 一、服务器 Skills 现状

**统计**：42 个 Skills 已就绪（总计 84 个）

**已就绪的核心能力**：
- 飞书文档读取（feishu-user-auth）
- 百度搜索（baidu-search）
- DuckDuckGo 搜索（ddg-web-search，通过代理可用）
- 网页阅读（url-reader，Jina 策略，外网通过代理）
- 微信公众号搜索（wechat-article-search）
- 微信公众号文章抓取（wechat-article-fetcher）
- 网页文章元信息提取（web-article-parser，15+ 网站）
- 网页文章正文抓取（web-article-scraper，含飞书 OAuth 经验）
- Seedance 视频生成（seedance-video-generation）
- 火山引擎图片生成（volcengine-ai-image-generation）
- 文档处理（pdf/docx/pptx/xlsx/markdown-converter）
- Skill 创建工具（skill-creator）

**外网访问**：✅ 已通过 sing-box 代理解决（HTTP 7890 / SOCKS 7891）

**仍缺失的能力**：
- 网页自动化（Playwright 1.58.0 + Chromium，本地和服务器两端已安装）

---

## 二、文档访问能力

### 飞书文档（✅ 已解决）

**方案**：使用自建 feishu-user-auth Skill

**命令**：
```bash
cd /home/openclaw/workspace/arqiao-shared-knowledge/skills/feishu-user-auth/scripts
python3 feishu_client.py read-doc {document_token}
```

**支持的域名**：yitanger.feishu.cn

**详细文档**：`solutions/feishu-doc-access.md`

### yitang.top（⏸️ 暂缓）

**问题**：Vue SPA 架构，内容通过 JavaScript 动态加载，curl 无法直接获取

**可能方案**：
1. 使用 Playwright 无头浏览器
2. 找到对应的飞书文档 token 直接读取
3. 抓包分析 API 端点

**详细文档**：`pitfalls/yitang-spa-scraping.md`

---

## 三、公认必装 Skills

来源：5 篇社区文章研究

| 排名 | Skill | 用途 | 状态 |
|-----|-------|------|------|
| 1 | Agent Browser / Playwright | 网页自动化 | ✅ 两端已安装 |
| 2 | Brave Search | 联网搜索 | ❌ 需 API Key |
| 3 | Shell | 终端命令 | ✅ 已内置 |
| 4 | Cron/Wake | 定时任务 | ❌ 需安装 |
| 5 | McPorter | MCP 协议 | ❌ 需安装 |
| 6 | TranscriptAPI | YouTube 字幕 | ❌ 需安装 |
| 7 | Gmail | 邮件自动化 | ❌ 需 OAuth |
| 8 | nano-pdf | PDF 处理 | ✅ 已安装（pdf skill）|
| 9 | Skill Creator | 创建 Skill | ✅ 已就绪 |
| 10 | frontend-design | 去 AI 味设计 | ✅ 已安装 |

---

## 四、踩坑记录

已记录到知识库 `pitfalls/` 目录：

| 文件 | 问题 |
|-----|------|
| `bash-exit-code-unreliable.md` | Windows 下 Bash 退出码不可靠，需看实际输出 |
| `yitang-spa-scraping.md` | SPA 网站无法用 curl 抓取 |
| `feishu-oauth-authorization.md` | 飞书 OAuth 授权流程 |
| `openclaw-auth-profiles-format.md` | auth-profiles.json 格式要求（version、profiles 嵌套、key 字段） |
| `openclaw-custom-api-proxy.md` | 自定义 API 代理需在 openclaw.json 中配置 baseUrl |

已记录到知识库 `solutions/` 目录：

| 文件 | 方案 |
|-----|------|
| `feishu-doc-access.md` | 飞书文档访问方案（feishu-user-auth OAuth） |
| `server-proxy-singbox.md` | 阿里云服务器 sing-box 代理配置 |

---

## 五、项目分工

| 项目 | 路径 | 职责 |
|-----|------|------|
| skills-dev | `D:\workspace\ccResearch\skills-dev` | Skill 总体架构、安装、研究 |
| multimedia | `D:\workspace\ccResearch\multimedia` | 视频制作专题（FFmpeg、Remotion、Seedance） |
| 知识库 | `D:\workspace\kbs\arqiao-shared-knowledge` | 方案、踩坑记录、自建 Skills |

---

## 六、关键阻塞项

~~**服务器外网访问**（#38-40）是当前最大阻塞~~ ✅ 已解决

**sing-box 代理配置**：
- 配置文件：`/etc/sing-box/config.json`
- HTTP 代理：`http://127.0.0.1:7890`
- SOCKS5 代理：`socks5://127.0.0.1:7891`
- 环境变量已写入 `~/.bashrc`
- 使用时需显式传入：`https_proxy=http://127.0.0.1:7890 curl ...`

**当前待安装**（外网已通，可随时安装）：
- 暂无紧急项

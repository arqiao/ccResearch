# Skill 开发项目

- 使用中文与我交互
- 本项目用于 OpenClaw Skill 的学习、开发和测试
- 专注于 Skill 总体架构、规范研究、生态调研

## 项目结构

```
skills-dev/
├── CLAUDE.md           # 本文件
├── task-list.md        # 任务清单
├── paper_urls.txt      # Skills 相关文章链接（94篇）
├── docs/               # 研究文档
│   ├── skill-md-spec.md        # SKILL.md 规范
│   ├── skill-creator-guide.md  # skill-creator 使用指南
│   ├── clawhub-skills-list.md  # ClawHub 可用 Skill 清单
│   ├── work-conclusions.md     # 工作结论汇总（重要）
│   └── articles/               # 原始文章（89篇已下载）
├── drafts/             # 开发中的 Skill
│   └── feishu-user-auth/       # 飞书用户授权 Skill
└── tmp/                # 临时文件（测试产物）
```

## 相关项目

- 多媒体制作：D:\workspace\ccResearch\multimedia（视频/音频 Skill 开发）
- 共享知识库：D:\workspace\kbs\arqiao-shared-knowledge

## 环境信息

- 阿里云服务器 IP：39.107.54.166，SSH 别名：openclaw-cloud
- OpenClaw 版本：2026.2.14，Ubuntu 24.04 LTS
- 服务器已通过 sing-box 代理访问外网（HTTP 7890 / SOCKS 7891）
- Gateway 通过 SSH 隧道访问（非直接公网）

## Skill 相关路径

- 阿乔的共享知识库（本地）：D:\workspace\kbs\arqiao-shared-knowledge
- 阿乔的共享知识库（服务器）：/home/openclaw/workspace/arqiao-shared-knowledge
- OpenClaw 内置 Skills：/usr/lib/node_modules/openclaw/skills/
- 自定义 Skills 通过 openclaw.json 的 extraDirs 加载
- 开发完成的 Skill 放入知识库 skills/ 目录，再 scp 同步到服务器

## 当前 Skill 现状

服务器上 ready 的 Skill（42个），包括：
- 内置：healthcheck、skill-creator、tmux、weather
- 搜索：baidu-search、ddg-search
- 网页阅读：url-reader（Jina 策略）
- 飞书：feishu-doc、feishu-user-auth、feishu-drive、feishu-perm、feishu-wiki
- 微信：wechat-article-extractor、wechat-article-search、wechat-article-fetcher
- 视频/图片：seedance 系列、seedream、volcengine-ai-image-generation
- 文档处理：pdf、docx、pptx、xlsx、markdown-converter、frontend-design
- yunshu 分享：12 个工作流 Skills
- 经验沉淀：web-article-parser、web-article-scraper
- 自建：knowledge-query、wechat-article-fetcher

其余 42 个内置 Skill 状态为 missing，需要安装依赖或配置 API Key。
总计 84 个 Skill（42 ready / 42 missing）。

## Skill 开发工作流

1. 在 drafts/ 中开发和测试 Skill
2. 参考内置 Skill 的 SKILL.md 格式（见 /usr/lib/node_modules/openclaw/skills/）
3. 测试通过后复制到知识库 skills/ 目录
4. scp 同步到服务器：scp -r skills/xxx openclaw-cloud:/home/openclaw/workspace/arqiao-shared-knowledge/skills/
5. 用 openclaw skills list 验证加载

## 学习资源

- OpenClaw 文档：https://docs.openclaw.ai
- ClawHub（Skill 市场）：搜索命令 npx clawhub search <关键词>
- skill-creator Skill：可用来辅助创建规范的 Skill

## 任务管理

任务清单见 [task-list.md](./task-list.md)

## 知识库记录

已记录到 `D:\workspace\kbs\arqiao-shared-knowledge`：

**solutions/**：
- `feishu-doc-access.md` - 飞书文档访问方案
- `server-proxy-singbox.md` - 服务器代理配置（sing-box）

**pitfalls/**：
- `bash-exit-code-unreliable.md` - Windows 下 Bash 退出码不可靠
- `yitang-spa-scraping.md` - yitang.top SPA 抓取问题
- `feishu-oauth-authorization.md` - 飞书 OAuth 授权流程
- `openclaw-auth-profiles-format.md` - auth-profiles.json 格式要求
- `openclaw-custom-api-proxy.md` - 自定义 API 代理需在 openclaw.json 配置 baseUrl

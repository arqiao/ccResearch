# 多媒体制作项目

- 使用中文与我交互
- 本项目专注于 AI 视频/音频制作的工具链研究和 Skill 开发

## 环境信息

- 阿里云服务器 IP：39.107.54.166，SSH 别名：openclaw-cloud
- OpenClaw 版本：2026.2.14，Ubuntu 24.04 LTS
- 服务器已配置 sing-box 代理（HTTP 7890 / SOCKS 7891），可访问外网
- 文件同步使用 scp
- Skill 开发完成后同步到知识库：/home/openclaw/workspace/arqiao-shared-knowledge/skills/

## 相关项目

- Skill 总体架构项目：D:\workspace\ccResearch\skills-dev
- 阿乔的共享知识库（本地）：D:\workspace\kbs\arqiao-shared-knowledge

## 服务器已有的视频相关 Skills

- seedance-video-generation：Seedance 视频生成（文生视频、图生视频）
- seedance-guide：Seedance 2.0 使用指南
- seedance-2-prompt-engineering：Seedance 提示词优化
- volcengine-ai-image-generation：火山引擎图片生成

## 待安装/配置

- FFmpeg：视频处理基础工具，`sudo apt install ffmpeg`
- Remotion：代码驱动视频生成（需外网）
- MiniMax TTS：语音合成 API
- Mureka MCP：AI 音乐生成（需外网）

## 项目结构

```
multimedia/
├── CLAUDE.md          # 本文件
├── task-list.md       # 任务清单
├── docs/              # 研究文档
│   ├── video-skills-research.md  # 视频 Skill 研究报告
│   └── articles/      # 原始文章（供参考）
│       ├── video_article_16.txt  # AI播客制作
│       ├── video_article_59.txt  # 剧本分镜自进化
│       ├── video_article_62.txt  # AI配乐(Mureka)
│       ├── video_article_82.txt  # Remotion文章转视频
│       ├── video_article_85.txt  # 一键MV生成
│       ├── video_article_86.txt  # Seedance分镜Skill
│       └── video_article_89.txt  # 飞书×Seedance
├── skills/            # 开发中的 Skill
├── drafts/            # 草稿和实验
└── tmp/               # 临时文件
```

## 开发工作流

1. 在 drafts/ 中开发和测试 Skill
2. 测试通过后复制到知识库 skills/ 目录
3. scp 同步到服务器验证

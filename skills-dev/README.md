# Skill 开发与学习

本项目用于 OpenClaw Skill 的学习、开发和测试。

## 目录结构

```
skills-dev/
├── CLAUDE.md          # CC 项目指引
├── README.md          # 本文件
├── docs/              # 学习笔记和最佳实践
└── drafts/            # Skill 草稿（开发中）
```

## 相关资源

- OpenClaw 文档：https://docs.openclaw.ai
- ClawHub（Skill 市场）：https://clawhub.com
- 阿乔的共享知识库：D:\workspace\kbs\arqiao-shared-knowledge

## 工作流

1. 在 `drafts/` 中开发和测试 Skill
2. 测试通过后，复制到知识库 `skills/` 目录
3. scp 同步到服务器，验证 OpenClaw 加载

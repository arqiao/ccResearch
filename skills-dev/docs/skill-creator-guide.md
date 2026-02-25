# skill-creator 使用指南

> 整理自 OpenClaw 内置 skill-creator，更新于 2026-02-19

skill-creator 是 OpenClaw 内置的 Skill 创建辅助工具，提供三个脚本：

## 脚本概览

| 脚本 | 功能 | 使用场景 |
|-----|------|---------|
| `init_skill.py` | 初始化新 Skill 目录 | 创建新 Skill 时 |
| `quick_validate.py` | 快速验证 Skill 格式 | 开发过程中检查 |
| `package_skill.py` | 打包成 .skill 文件 | 发布分发时 |

脚本路径：`/usr/lib/node_modules/openclaw/skills/skill-creator/scripts/`

## init_skill.py - 初始化 Skill

### 基本用法

```bash
python init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets] [--examples]
```

### 参数说明

| 参数 | 必需 | 说明 |
|-----|------|------|
| `skill-name` | 是 | Skill 名称，自动转为小写连字符格式 |
| `--path` | 是 | 输出目录 |
| `--resources` | 否 | 要创建的资源目录，逗号分隔 |
| `--examples` | 否 | 在资源目录中创建示例文件 |

### 示例

```bash
# 最简单：只创建 SKILL.md
python init_skill.py my-skill --path ./drafts

# 带脚本目录
python init_skill.py pdf-editor --path ./drafts --resources scripts

# 完整结构 + 示例文件
python init_skill.py my-api-helper --path ./drafts --resources scripts,references,assets --examples
```

### 生成的模板结构

```
my-skill/
├── SKILL.md          # 带 TODO 占位符的模板
├── scripts/          # 如果指定了 --resources scripts
├── references/       # 如果指定了 --resources references
└── assets/           # 如果指定了 --resources assets
```

### 名称规范化

脚本会自动将名称转为规范格式：
- `"Plan Mode"` → `plan-mode`
- `"My_New_Skill"` → `my-new-skill`
- 最大长度：64 字符

## quick_validate.py - 验证 Skill

### 用法

```bash
python quick_validate.py <skill-directory>
```

### 验证内容

1. SKILL.md 文件存在
2. YAML frontmatter 格式正确
3. 必需字段：`name`、`description`
4. 名称格式：小写字母 + 数字 + 连字符
5. 描述长度：≤ 1024 字符

### 允许的 frontmatter 字段

- `name`（必需）
- `description`（必需）
- `license`（可选）
- `allowed-tools`（可选）
- `metadata`（可选）

## package_skill.py - 打包 Skill

### 用法

```bash
python package_skill.py <skill-folder> [output-directory]
```

### 示例

```bash
# 打包到当前目录
python package_skill.py ./drafts/my-skill

# 打包到指定目录
python package_skill.py ./drafts/my-skill ./dist
```

### 打包流程

1. 自动运行 `quick_validate.py` 验证
2. 验证通过后创建 `.skill` 文件（zip 格式）
3. 输出文件名：`<skill-name>.skill`

## 完整开发流程

```bash
# 1. 初始化
python init_skill.py weather-alert --path ./drafts --resources scripts

# 2. 编辑 SKILL.md，完成 TODO 项

# 3. 验证
python quick_validate.py ./drafts/weather-alert

# 4. 打包（可选，用于分发）
python package_skill.py ./drafts/weather-alert ./dist

# 5. 部署到知识库
cp -r ./drafts/weather-alert /path/to/knowledge-repo/skills/

# 6. 同步到服务器
scp -r ./drafts/weather-alert openclaw-cloud:/home/openclaw/workspace/arqiao-shared-knowledge/skills/
```

## 在 OpenClaw 中使用

也可以直接让 OpenClaw 调用 skill-creator：

```
/skill-creator 帮我创建一个 pdf-editor Skill
```

OpenClaw 会自动调用相关脚本并引导你完成创建过程。

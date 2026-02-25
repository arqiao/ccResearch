# 视频制作 Skills 专题研究报告

> 来源：skills-dev 项目文章研究（2026-02-20）
> 文章编号：#59, #62, #82, #85, #86, #89

---

## 一、主要工具链和技术栈

| 工具/技术 | 用途 | 来源文章 |
|----------|------|---------|
| **Remotion** | 代码驱动视频生成（React组件） | #82 |
| **Seedance 2.0** | 火山引擎视频生成模型（文生视频、图生视频） | #86, #89 |
| **Mureka V8** | 昆仑万维 AI 音乐生成 | #62 |
| **Suno/Udio** | AI 音乐生成 | #62, #85 |
| **MiniMax TTS** | 语音合成（克隆音色） | #82 |
| **FFmpeg** | 视频合成、转场、运镜 | #85 |
| **NotebookLM** | 知识库构建（音乐提示词） | #62 |

---

## 二、典型工作流

### 1. 文章转视频（#82 Remotion）

```
文稿+素材 → 内容策划(45-60秒) → 场景设计(6个) → 音频生成(TTS) → 音视频同步 → 多版本输出
```

- 核心：**视频开发在音频生成之前**
- 工具：Remotion + MiniMax TTS
- 成本：配音约 0.3 元/视频
- 6 个阶段：项目初始化 → 内容策划 → 视频开发 → 音频生成 → 音视频同步 → 多版本输出

**关键经验**：
- 两轮逐字稿确认（生成前 + 生成后）
- 环境隔离：每个 project 独立文件夹
- 视觉风格统一：定义个人品牌视觉语言

### 2. AI 配乐工作流（#62）

```
视频 → Gemini分析画面 → NotebookLM生成音乐描述 → Mureka V8生成音乐 → 合成
```

- 核心：用 AI 分析画面氛围，生成专业音乐提示词
- 关键：Mureka V8 支持 MCP，可做成 Skill 自动调用
- 音乐提示词示例：`Warm nostalgic pop, gentle and dreamy, piano and acoustic guitar...`

### 3. 分镜提示词生成（#86）

```
简单想法 → Skill引导问答 → 电影级分镜提示词 → Seedance 2.0 生成视频
```

- 核心：将 Seedance 官方手册做成 Skill，AI 引导用户完善想法
- 输出格式：
  - 整体风格、色调、时长、比例
  - 分镜描述（画面 + 运镜）
  - 音乐建议、参考风格

**分镜提示词示例**：
```
0-3秒：镜头从远处推近，水墨画风格夕阳西下，溪边古亭若隐若现...
4-6秒：镜头摇入亭内后缓慢环绕半周，古装少女侧卧石桌旁...
```

### 4. 一键 MV 生成（#85）

```
主题 → 歌词创作 → 音乐生成 → 时间戳提取 → 角色设计 → 场景描述 → 图像生成 → 视频合成
```

七阶段流水线，20分钟出完整 MV：

1. **歌词创作**：LLM 生成（20-30行，有韵律）
2. **音乐生成**：六要素公式生成风格描述
3. **时间戳提取**：每个字的精确时间戳
4. **角色设计**：保持一致性的关键（参考图）
5. **场景描述**：视觉化思维，像电影分镜师
6. **图像生成**：3并发批处理 + 重试机制
7. **视频合成**：FFmpeg 运镜、转场、调色

**关键技术**：
- 角色一致性：先生成参考图，后续带图提交
- 智能转场：主歌用溶解，副歌用滑动
- 分屏闪切：副歌高潮部分增强节奏感

### 5. 剧本+分镜自进化（#59）

```
执行者(生成内容) ↔ 审核者(打分反馈) → 自我迭代
```

- 双 Agent 架构：执行者 + 审核者
- 长期记忆：evolution.json 记录偏好
- 自动调整审核标准

---

## 三、关键 Skills 和资源

| Skill 名称 | 功能 | 来源 |
|-----------|------|------|
| **seedance-video-generation** | Seedance 视频生成 | clawhub.ai/JackyCSer/seedance-video-generation |
| **mrgoonie/claudekit-skills** | 视频切片、压缩、上传 | GitHub |
| **Remotion Skills** | 代码生成视频 | GitHub remotion-dev |
| **Mureka MCP** | AI 音乐生成 | github.com/SkyworkAI/Mureka-mcp |
| **music2video** | 一键 MV 生成 | #85 文章作者自建 |

---

## 四、服务器现状

**已有能力**：
- ✅ seedance-video-generation
- ✅ volcengine-ai-image-generation
- ✅ seedance-guide、seedance-2-prompt-engineering

**缺失能力**：
- ❌ FFmpeg（需 `apt install ffmpeg`）
- ❌ Remotion（需 Node.js 环境 + 外网）
- ❌ Mureka MCP（需外网安装）
- ❌ TTS 服务（MiniMax API）

---

## 五、开发路线建议

### 短期（无需外网）

1. 安装 FFmpeg：`sudo apt install ffmpeg`
2. 开发「分镜提示词生成」Skill（参考 #86，纯提示词）
3. 结合已有的 seedance-video-generation 测试完整流程

### 中期（外网调通后）

1. 安装 Remotion 环境
2. 配置 MiniMax TTS API
3. 开发「文章转视频」Skill

### 长期

1. 集成 Mureka MCP 实现自动配乐
2. 开发「一键 MV」完整流水线

---

## 六、原始文章列表

| 编号 | 标题 | 核心内容 |
|-----|------|---------|
| #59 | 无限进化的剧本和分镜 | 双Agent自进化架构 |
| #62 | 给长视频AI配乐的Skills | Mureka V8 + NotebookLM |
| #82 | Remotion把文章一键变成视频 | 6阶段工作流 |
| #85 | 生成超级棒MV的Skills | 七阶段流水线 |
| #86 | Seedance2.0分镜Skill | 引导问答生成提示词 |
| #89 | 飞书聊天直接生视频 | OpenClaw × Seedance |

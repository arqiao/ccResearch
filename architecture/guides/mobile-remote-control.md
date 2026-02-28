# 手机远程控制 Claude Code 方案

> 基于 Claude Code 官方 Remote Control 功能，实现手机端接管电脑上的 Claude Code 会话。
>
> 参考来源：[Anthropic 官方文档](https://docs.anthropic.com/en/docs/claude-code/remote-control) · [XiaoHu.AI 公众号文章](https://mp.weixin.qq.com/s/jibF1iD276m71OhGZY6g3Q)

## 核心概念

Remote Control 让你从手机/浏览器接管电脑上正在运行的 Claude Code 会话：

- 代码始终在本地电脑执行，手机只是"遥控器"
- 本地文件系统、MCP 工具、项目配置全部可用
- 对话在所有连接设备间实时同步
- 电脑不开放任何入站端口，仅发出 HTTPS 请求

## 前提条件

| 条件 | 说明 |
|------|------|
| 订阅 | Claude Pro 或 Max（API key 不支持） |
| 登录 | 终端中已通过 `/login` 登录 claude.ai |
| 手机 App | 安装 Claude App（[iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) / [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)） |
| 目录信任 | 首次使用某项目目录时需运行 `claude` 信任该目录 |

## 使用步骤

### 1. 电脑端启动

**方式 A：新建远程会话**

```bash
cd /your/project
claude remote-control
```

**方式 B：在已有会话中开启**

在 Claude Code 对话中输入：
```
/remote-control
```
简写 `/rc` 也可以。当前对话历史全部保留。

启动后终端会显示一个链接和二维码。

### 2. 手机端连接

三种连接方式（任选其一）：

1. 手机扫描终端上的二维码 → 自动跳转 Claude App
2. 复制终端显示的 URL → 手机浏览器打开
3. 打开 Claude App 或 claude.ai/code → 在会话列表中找到（带绿色状态点）

### 3. 开始操作

手机上直接打字发消息，内容同步到电脑终端，Claude 的回复两边同时出现。

## 实用技巧

- 启动前用 `/rename` 给会话命名，方便在手机会话列表中识别
- 按空格键切换二维码显示/隐藏
- 加 `--verbose` 查看详细连接日志

### 自动开启远程模式

每次手动输入 `/remote-control` 太麻烦的话：

1. 在 Claude Code 中输入 `/config`
2. 找到 "Enable Remote Control for all sessions"
3. 设为 `true`

之后每次启动 Claude Code 都会自动开启远程控制。

## 安全机制

- 仅出站 HTTPS 请求，不开放本机端口
- 所有通信走 TLS 加密（与正常使用 Claude Code 相同）
- 使用多个短期凭证，各自独立过期
- 项目文件始终在本地，手机端只显示对话和接收指令

## 注意事项

| 限制 | 说明 |
|------|------|
| 终端不能关 | 关终端或杀进程 = 远程断开 |
| 单会话限制 | 一个 Claude Code 实例只能开一个远程连接 |
| 断网超时 | 电脑醒着但断网 ~10 分钟会超时，需重新 `claude remote-control` |
| 休眠恢复 | 电脑休眠后唤醒会自动重连 |

**保持运行的建议**：笔记本连电源、关显示器或调暗屏幕即可。也可设置合盖不休眠。

## 与 Claude Code on the Web 的区别

| | Remote Control | Claude Code on the Web |
|---|---|---|
| 代码执行位置 | 本地电脑 | Anthropic 云服务器 |
| 本地文件访问 | 可以 | 不可以 |
| MCP 工具 | 可用 | 不可用 |
| 项目配置 | 全部保留 | 需重新设置 |
| 需要电脑开着 | 是 | 否 |
| 适合场景 | 接着干本地已有的活 | 从零开始新任务 |

## 当前状态：⏸️ 暂缓

需同时满足以下两个条件才能启用：

| # | 条件 | 当前状态 | 说明 |
|---|------|---------|------|
| 1 | Claude Code 版本包含 `remote-control` 命令 | ❌ 不满足 | 当前版本 2.1.56（npm 最新），帮助信息中无此命令，功能可能仍在灰度发布中 |
| 2 | 拥有可直接登录 claude.ai 的 Pro/Max 账号 | ❌ 不满足 | 当前通过中转服务（API 转发）使用，无法直接登录 claude.ai；Remote Control 不支持 API key 认证 |

检查方式：
- 条件 1：升级 Claude Code 后运行 `claude --help`，看是否出现 `remote-control` 子命令
- 条件 2：确认中转服务商是否提供可登录 claude.ai 的账号，或自行购买 Pro/Max 订阅（$20/$100 每月）

## 我们的使用场景

适合阿乔团队的典型场景：

1. 电脑上启动 Claude Code 跑复杂任务 → 手机监控进度、回复问题
2. 书房开着会话 → 移动到其他地方继续操作
3. 电脑 + 手机 + 另一台设备同时查看同一会话

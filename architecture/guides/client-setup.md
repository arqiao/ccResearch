# 客户端配置指南

> 本文档说明如何在各设备上配置客户端连接到 OpenClaw Gateway

---

## 一、设备概览

| 设备 | 角色 | 连接方式 |
|-----|------|---------|
| Windows 笔记本 | 主要工作设备 + Claude Code | SSH 隧道 / Tailscale |
| 小米手机 | 移动端 Node | Tailscale / 直连 |

---

## 二、Windows 笔记本配置

### 2.1 生成 SSH 密钥

在 Windows Terminal (PowerShell) 中执行：

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

一路回车使用默认设置。

### 2.2 将公钥传到服务器

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh root@服务器IP "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

输入一次密码后，以后就免密登录了。

> 注意：Windows 没有 `ssh-copy-id` 命令，用上面的方式代替。

### 2.3 配置 SSH 快捷方式

用记事本创建配置文件：

```powershell
notepad $env:USERPROFILE\.ssh\config
```

> 重要：保存时文件名就是 `config`，不要带 `.txt` 后缀！

粘贴以下内容（替换实际 IP）：

```
# 云服务器直连
Host openclaw-cloud
    HostName 39.107.54.166
    User root
    IdentityFile ~/.ssh/id_ed25519

# 云服务器 + SSH 隧道（用于访问 OpenClaw 控制台）
Host openclaw-tunnel
    HostName 39.107.54.166
    User root
    IdentityFile ~/.ssh/id_ed25519
    LocalForward 18789 127.0.0.1:18789

# 树莓派（第三阶段，通过 Tailscale）
Host openclaw-pi
    HostName 100.x.x.x
    User pi
    IdentityFile ~/.ssh/id_ed25519
```

### 2.4 使用方式

```powershell
# 登录服务器
ssh openclaw-cloud

# 建立隧道访问 OpenClaw 控制台
ssh -N openclaw-tunnel
# 然后浏览器访问 http://localhost:18789/#token=你的token
```

> 注意：`ssh -N openclaw-tunnel` 运行后没有输出是正常的，保持窗口开着即可。

### 2.5 配置 Claude Code

编辑 `~/.claude/CLAUDE.md`，添加：

```markdown
## 阿乔的共享知识库

本地路径：D:\workspace\kbs\arqiao-shared-knowledge

当遇到以下情况时，优先查阅阿乔的共享知识库：
- 飞书相关问题 → solutions/feishu/
- 接口定义问题 → interfaces/
- 不确定的技术选型 → pitfalls/

当解决了一个可复用的技术问题时，提醒我更新到阿乔的共享知识库。

## OpenClaw Gateway

- 地址：http://100.x.x.x:18789（Tailscale）或 http://127.0.0.1:18789（SSH 隧道）
- 需要时可以调用 OpenClaw 的能力
```

### 2.6 克隆阿乔的共享知识库

```bash
cd D:\workspace
git clone https://github.com/YOUR_USERNAME/arqiao-shared-knowledge.git
```

### 2.7 设置环境变量

PowerShell（管理员）：

```powershell
[Environment]::SetEnvironmentVariable("SHARED_KNOWLEDGE_PATH", "D:\workspace\kbs\arqiao-shared-knowledge", "User")
```

---

## 三、小米手机配置

### 3.1 安装 Tailscale

1. 在应用商店搜索 "Tailscale"
2. 安装并登录同一账号
3. 开启 VPN 连接

### 3.2 安装 OpenClaw Android Node（可选）

如果需要手机作为 Node（相机、位置等功能）：

1. 访问 OpenClaw 官网下载 Android 版
2. 或在 Gateway 的 Control UI 中扫码配对

### 3.3 验证连接

在手机浏览器中访问：
```
http://100.x.x.x:18789
```

应该能看到 OpenClaw Control UI。

---

## 四、连接测试

### 4.1 测试 Tailscale 网络

```bash
# 在 Windows 上
ping 100.x.x.x  # 树莓派的 Tailscale IP

# 应该能 ping 通
```

### 4.2 测试 OpenClaw Gateway

```bash
# 健康检查
curl http://100.x.x.x:18789/health

# 或在浏览器中访问
http://100.x.x.x:18789
```

### 4.3 测试 Claude Code 读取阿乔的共享知识库

在 Claude Code 中：
```
帮我查一下飞书授权的方案
```

应该能读取到 `D:\workspace\kbs\arqiao-shared-knowledge\solutions\feishu\auth-refresh.md`

---

## 五、日常使用流程

### 5.1 开始工作前

```bash
# 1. 确保 Tailscale 已连接（查看系统托盘图标）

# 2. 同步知识仓库
cd D:\workspace\kbs\arqiao-shared-knowledge
git pull

# 3. 验证 Gateway 可用
curl http://100.x.x.x:18789/health
```

### 5.2 工作中

- 遇到问题先查知识库
- 使用 Claude Code 时，它会自动参考 CLAUDE.md 中的指引

### 5.3 结束工作时

```bash
# 如果更新了知识库
cd D:\workspace\shared-knowledge
git add -A
git commit -m "更新 xxx"
git push
```

---

## 六、故障排查

### 6.1 Tailscale 连接不上

1. 检查 Tailscale 客户端是否运行
2. 检查是否登录了正确的账号
3. 尝试重新连接：右键托盘图标 → Reconnect

### 6.2 无法访问 Gateway

```bash
# 检查 Gateway 是否运行
ssh openclaw-pi "systemctl status openclaw-gateway"

# 检查端口是否监听
ssh openclaw-pi "netstat -tlnp | grep 18789"
```

### 6.3 阿乔的共享知识库同步失败

```bash
# 检查 Git 状态
cd D:\workspace\shared-knowledge
git status

# 如果有冲突，解决后重新提交
git pull --rebase
git push
```

---

## 七、多设备同步

### 7.1 阿乔的共享知识库同步

所有设备都通过 Git 同步：

```bash
# 获取最新内容
git pull

# 提交本地更改
git add -A && git commit -m "更新" && git push
```

### 7.2 OpenClaw 配置同步

OpenClaw 配置存储在 Gateway 服务器上，所有客户端共享同一配置。

如果需要备份：

```bash
ssh openclaw-pi "tar -czvf ~/openclaw-backup.tar.gz ~/.openclaw"
scp openclaw-pi:~/openclaw-backup.tar.gz ./
```

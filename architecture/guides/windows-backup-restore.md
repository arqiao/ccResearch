# Windows 换机备份与恢复指南

> 本文档帮助你在更换电脑时，快速恢复开发环境和配置

---

## 一、需要备份的文件清单

### 1.1 SSH 配置（重要）

| 文件/目录 | 路径 | 说明 |
|----------|------|------|
| SSH 私钥 | `C:\Users\你的用户名\.ssh\id_ed25519` | 免密登录服务器的密钥 |
| SSH 公钥 | `C:\Users\你的用户名\.ssh\id_ed25519.pub` | 公钥（已在服务器上） |
| SSH 配置 | `C:\Users\你的用户名\.ssh\config` | 快捷连接配置 |

### 1.2 Claude Code 配置

| 文件/目录 | 路径 | 说明 |
|----------|------|------|
| 全局配置 | `C:\Users\你的用户名\.claude\CLAUDE.md` | 个人指令和偏好 |
| 项目配置 | `C:\Users\你的用户名\.claude\projects\` | 各项目的配置 |
| 设置文件 | `C:\Users\你的用户名\.claude\settings.json` | Claude Code 设置 |

### 1.3 Git 配置

| 文件 | 路径 | 说明 |
|-----|------|------|
| Git 全局配置 | `C:\Users\你的用户名\.gitconfig` | 用户名、邮箱等 |

### 1.4 工作目录

| 目录 | 路径 | 说明 |
|-----|------|------|
| 阿乔的共享知识库 | `D:\workspace\kbs\arqiao-shared-knowledge\` | Git 仓库，可重新 clone |
| 项目文件 | `D:\workspace\` | 其他项目代码 |

---

## 二、备份操作

### 2.1 一键备份脚本

在 PowerShell 中运行：

```powershell
# 创建备份目录
$backupDir = "D:\backup-for-new-pc"
New-Item -ItemType Directory -Force -Path $backupDir

# 备份 SSH
Copy-Item -Recurse "$env:USERPROFILE\.ssh" "$backupDir\ssh"

# 备份 Claude Code
Copy-Item -Recurse "$env:USERPROFILE\.claude" "$backupDir\claude"

# 备份 Git 配置
Copy-Item "$env:USERPROFILE\.gitconfig" "$backupDir\gitconfig"

# 显示备份内容
Get-ChildItem $backupDir -Recurse | Select-Object FullName
```

### 2.2 备份结果

备份完成后，`D:\backup-for-new-pc` 目录结构：

```
D:\backup-for-new-pc\
├── ssh\
│   ├── id_ed25519          # SSH 私钥（重要！保密！）
│   ├── id_ed25519.pub      # SSH 公钥
│   └── config              # SSH 快捷配置
├── claude\
│   ├── CLAUDE.md           # 全局指令
│   ├── settings.json       # 设置
│   └── projects\           # 项目配置
└── gitconfig               # Git 配置
```

### 2.3 安全提醒

> ⚠️ **SSH 私钥是敏感文件！**
> - 不要上传到云盘、Git 或任何公开位置
> - 建议用 U 盘或加密方式传输到新电脑
> - 传输完成后删除中间副本

---

## 三、新电脑恢复操作

### 3.1 前置准备

新电脑需要先安装：
- Git for Windows（https://git-scm.com/download/win）
- Claude Code（按官方文档安装）
- Windows Terminal（Microsoft Store）

### 3.2 一键恢复脚本

将备份文件夹复制到新电脑后，在 PowerShell 中运行：

```powershell
# 假设备份文件夹在 D:\backup-for-new-pc
$backupDir = "D:\backup-for-new-pc"

# 恢复 SSH
Copy-Item -Recurse "$backupDir\ssh" "$env:USERPROFILE\.ssh"

# 恢复 Claude Code
Copy-Item -Recurse "$backupDir\claude" "$env:USERPROFILE\.claude"

# 恢复 Git 配置
Copy-Item "$backupDir\gitconfig" "$env:USERPROFILE\.gitconfig"

# 设置 SSH 私钥权限（重要）
icacls "$env:USERPROFILE\.ssh\id_ed25519" /inheritance:r /grant:r "$env:USERNAME:R"
```

### 3.3 验证恢复

```powershell
# 测试 SSH 连接
ssh openclaw-cloud

# 测试 Git 配置
git config --global --list

# 测试 Claude Code
claude --version
```

### 3.4 克隆工作仓库

```powershell
# 创建工作目录
mkdir D:\workspace
cd D:\workspace

# 克隆阿乔的共享知识库
git clone https://github.com/你的用户名/arqiao-shared-knowledge.git
```

---

## 四、环境变量恢复

在 PowerShell（管理员）中运行：

```powershell
[Environment]::SetEnvironmentVariable("SHARED_KNOWLEDGE_PATH", "D:\workspace\kbs\arqiao-shared-knowledge", "User")
```

---

## 五、检查清单

恢复完成后，逐项验证：

| 检查项 | 验证命令 | 预期结果 |
|-------|---------|---------|
| SSH 免密登录 | `ssh openclaw-cloud` | 直接登录，不要求密码 |
| SSH 隧道 | `ssh -N openclaw-tunnel` | 无报错，保持连接 |
| OpenClaw 控制台 | 浏览器访问 `http://localhost:18789` | 能打开页面 |
| Git 用户名 | `git config user.name` | 显示你的用户名 |
| Claude Code | `claude` | 正常启动 |

---

## 六、常见问题

### Q: SSH 连接提示权限错误

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

**解决：** 修复私钥权限

```powershell
icacls "$env:USERPROFILE\.ssh\id_ed25519" /inheritance:r /grant:r "$env:USERNAME:R"
```

### Q: 新电脑用户名不同怎么办

SSH config 中使用 `~/.ssh/` 相对路径，会自动适配新用户名，无需修改。

### Q: 服务器上的公钥需要更新吗

不需要。公钥已经在服务器上了，只要私钥一致就能连接。

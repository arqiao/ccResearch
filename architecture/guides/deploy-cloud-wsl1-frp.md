# 联通云智电脑部署指南

> 主机配置：8核 CPU、16GB 内存、200GB 磁盘（C盘79G + D盘119G）
> 公网 IP：195.64.7.45（固定，但平台拦截所有入站端口，无法直接对外提供服务）
> 虚拟化方案：WSL1 + Ubuntu 24.04 LTS（不支持嵌套虚拟化，Hyper-V / WSL2 均不可用）
> 访问方式：本机只能通过联通专属客户端访问，无网页版控制台
>
> **外网访问方案（双通道）：**
> 1. Tailscale 组网（推荐日常使用）：笔记本/手机通过 Tailscale 虚拟 IP 访问，安全且无需公网端口暴露
>    - 云船 Tailscale IP：100.115.214.108（WSL1 userspace networking 模式，需 SOCKS5 代理中转）
>    - 控制界面：SSH 隧道 → localhost:18789（bind: loopback 限制）
> 2. frp 内网穿透（备用 SSH）：借助阿里云 39.107.54.166 做中转
>    - 外网设备 → 阿里云:12222 → frp隧道 → 联通云WSL1:22（SSH）
>    - 公网 18789 端口已关闭，OpenClaw 仅通过 Tailscale 或 SSH 隧道访问

---

## 一、方案对比（与阿里云轻量服务器）

| 对比项 | 阿里云轻量服务器（之前） | 联通云智电脑 + WSL1 |
|-------|----------------------|---------------------|
| CPU | 2 核 | 8 核（WSL1 可用全部） |
| 内存 | 2-4 GB | 16 GB（WSL1 与宿主机共享） |
| 磁盘 | 40-60 GB SSD | 200 GB（WSL1 数据放 D 盘） |
| 带宽 | 1-3 Mbps 共享 | 100 Mbps 共享 |
| 公网 IP | 固定 | 固定（195.64.7.45） |
| 系统 | Linux 原生 | Win10 + WSL1（翻译层） |

---

## 二、方案选型记录

| 方案 | 结果 | 原因 |
|------|------|------|
| Hyper-V | 不可用 | 云虚拟机不支持嵌套虚拟化（SVM not present） |
| WSL2 | 不可用 | 同上，WSL2 依赖 Hyper-V 虚拟化 |
| Docker Desktop | 不可用 | 依赖 WSL2 / Hyper-V |
| 重装为 Linux | 不可用 | 联通云控制台不支持更换系统 |
| WSL1 | 可行 | 不需要虚拟化，通过系统调用翻译层运行 Linux |
| Win10 原生 | 备选 | WSL1 失败时的降级方案 |

### WSL1 的限制

- 不支持 Docker
- 不支持 systemd（服务管理需用 nohup 或 screen）
- 文件系统性能比原生 Linux 稍差
- 跑 Node.js / OpenClaw 没有问题

---

## 三、启用 WSL1

> 实际操作中先尝试了 Hyper-V 和 WSL2，均因嵌套虚拟化不可用而失败，最终确定 WSL1。
> 启用过程中曾开启 Hyper-V 和 VirtualMachinePlatform，后已关闭 Hyper-V。

```powershell
# 1. 如果之前启用了 Hyper-V，先关闭
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -NoRestart

# 2. 启用 WSL（不需要虚拟机平台）
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 3. 重启电脑
Restart-Computer
```

重启后设置默认版本为 WSL1：

```powershell
wsl --set-default-version 1
```

---

## 四、安装 Ubuntu 24.04

```powershell
wsl --install -d Ubuntu-24.04
```

> 如果在线安装超时（GitHub 连接问题），可手动下载 appx 包：
> 浏览器下载 https://aka.ms/wslubuntu2404 ，然后执行 `Add-AppxPackage .\Ubuntu_2404.appx`

安装过程中会提示创建用户名和密码，用户名设为 `arqiaoclaw`。

验证安装：

```powershell
wsl -l -v
# 应显示：
# * Ubuntu-24.04    Stopped         1
```

---

## 五、迁移 WSL1 到 D 盘

> WSL1 默认装在 C 盘，迁移到 D 盘节省 C 盘空间。已完成，当前 WSL1 数据在 D 盘，占用 120G 分区。
> 注意：迁移后需要重新设置默认用户，因为 wsl --import 会将默认用户重置为 root。

```powershell
# 1. 创建目录
mkdir D:\wsl

# 2. 关闭 WSL
wsl --shutdown

# 3. 导出
wsl --export Ubuntu-24.04 D:\wsl\ubuntu-24.04-backup.tar

# 4. 注销
wsl --unregister Ubuntu-24.04

# 5. 导入到 D 盘
wsl --import Ubuntu-24.04 D:\wsl\Ubuntu-24.04 D:\wsl\ubuntu-24.04-backup.tar

# 6. 设置默认用户（wsl --import 后默认用户变为 root，需手动修复）
# 注意：必须用 printf，echo -e 在此场景下不会解析 \n
wsl -d Ubuntu-24.04 -u root -- bash -c 'printf "[user]\ndefault=arqiaoclaw\n" > /etc/wsl.conf'
wsl --shutdown

# 7. 验证默认用户
wsl -d Ubuntu-24.04
# whoami 应显示 arqiaoclaw

# 8. 确认无误后清理备份
Remove-Item D:\wsl\ubuntu-24.04-backup.tar
```

---

## 六、Linux 系统配置

### 6.1 安装基础依赖

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git wget unzip openssh-server
```

启动 SSH 服务（WSL1 不支持 systemd，需手动启动）：

```bash
sudo service ssh start

# 验证
sudo service ssh status
```

> SSH 服务启动后，frpc 才能穿透 22 端口。每次重启 WSL1 后需重新启动（已通过任务计划自动化，见 10.4）。

### 6.2 安装 Node.js 22

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node -v && npm -v
```

### 6.3 安装 OpenClaw

```bash
# pnpm 全局安装需要 sudo
sudo npm install -g pnpm

# pnpm setup 写入 PATH，source 使其生效
pnpm setup
source ~/.bashrc

# openclaw 用普通用户安装（不要 sudo，否则找不到 global bin dir）
pnpm install -g openclaw@latest

# 批准构建脚本（选 sharp、protobufjs、koffi）
pnpm approve-builds -g

# 验证
openclaw --version
```

### 6.4 手动配置 openclaw.json

> 不要用 `openclaw onboard`，向导会因飞书插件路径验证失败而报错。直接手动创建配置。

```bash
mkdir -p ~/.openclaw

# 生成 token
openssl rand -hex 32

# 创建配置文件
cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "gateway": {
    "port": 18789,
    "mode": "remote",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "YOUR_TOKEN_HERE"
    }
  }
}
EOF

# 自动修复配置格式
openclaw doctor --fix

# 设置 gateway 模式
openclaw config set gateway.mode remote

# 配置 MiniMax API Key
openclaw config set models.providers.minimax.apiKey "YOUR_MINIMAX_KEY"

# 选择模型
openclaw configure --section model
```

> 注意：WSL1 不支持 systemd，OpenClaw 服务需要用 nohup 方式启动（见第八节）。

---

## 七、网络配置（公网访问）

> 联通云平台拦截所有入站端口，无法直接从外网访问。
> 解决方案：用阿里云（39.107.54.166）做 frp 中转服务器，把联通云的端口穿透出去。

### 7.1 frp 穿透方案

```
外网设备 → 阿里云:18789 → frp隧道 → 联通云WSL1:18789（OpenClaw）
外网设备 → 阿里云:12222 → frp隧道 → 联通云WSL1:22（SSH）
```

### 7.2 阿里云安装 frps（服务端）

> 在阿里云服务器上运行（笔记本本地执行）

```bash
# SSH 登录阿里云
ssh root@39.107.54.166

# 以下命令在阿里云服务器上执行：
# 下载 frp（查最新版本：https://github.com/fatedier/frp/releases）
wget https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_amd64.tar.gz
tar -xzf frp_0.61.0_linux_amd64.tar.gz
cd frp_0.61.0_linux_amd64

# 创建配置
cat > frps.toml << 'EOF'
bindPort = 7000
auth.token = "YOUR_FRP_TOKEN"
EOF

# 后台运行
nohup ./frps -c frps.toml > /tmp/frps.log 2>&1 &
```

阿里云安全组需开放：7000（frp控制端口）、18789（OpenClaw）、12222（SSH）。

### 7.3 联通云 WSL1 安装 frpc（客户端）

> 在联通云 WSL1 上运行（通过 SSH 连接到联通云后执行）
> frpc 下载到 Windows 目录下（`C:\Users\Administrator\`），方便任务计划程序调用。

```bash
# 在 WSL1 中，下载到 Windows 目录
cd /mnt/c/Users/Administrator
wget https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_amd64.tar.gz
tar -xzf frp_0.61.0_linux_amd64.tar.gz
cd frp_0.61.0_linux_amd64

cat > frpc.toml << 'EOF'
serverAddr = "39.107.54.166"
serverPort = 7000
auth.token = "YOUR_FRP_TOKEN"

[[proxies]]
name = "openclaw"
type = "tcp"
localIP = "127.0.0.1"
localPort = 18789
remotePort = 18789

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 12222
EOF

nohup ./frpc -c frpc.toml > /tmp/frpc.log 2>&1 &
```

### 7.4 验证

```bash
# 从外网访问 OpenClaw
curl http://39.107.54.166:18789/health

# SSH 到联通云
ssh -p 12222 arqiaoclaw@39.107.54.166
```

### 7.5 Tailscale 内网访问（推荐）

> Tailscale 提供安全的点对点加密连接，无需公网端口暴露，推荐日常使用。
> frp 保留作为备用访问方式（SSH 隧道 12222）。

#### 7.5.1 安装 Tailscale

**云船（WSL1）：**
```bash
# 在 WSL1 中安装
curl -fsSL https://tailscale.com/install.sh | sh

# 启动（WSL1 不支持 systemd，需手动启动守护进程）
sudo tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &
sudo tailscale up
# 浏览器打开认证链接完成授权
```

**澳龙（阿里云）：**
```bash
# 标准 Ubuntu 服务器
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# 浏览器打开认证链接完成授权
```

**笔记本 / 手机：**
- Windows: https://tailscale.com/download/windows
- Android/iOS: 应用商店搜索 Tailscale

#### 7.5.2 设备列表

| 设备 | Tailscale IP | 说明 |
|------|-------------|------|
| 云船（联通云） | 100.115.214.108 | 主 OpenClaw 服务器 |
| 澳龙（阿里云） | 100.72.241.16 | frp 中继 + 备用 OpenClaw |
| 笔记本 | 100.100.153.29 | 日常开发 |
| 手机 | 100.71.142.90 | 移动访问 |

#### 7.5.3 访问方式

**通过 Tailscale 访问云船 OpenClaw：**
- API 访问：`http://100.115.214.108:18789`
- 控制界面：需通过 SSH 隧道（bind: loopback 限制）
  ```bash
  ssh -L 18789:127.0.0.1:18789 arqiaoclaw@100.115.214.108
  # 然后访问 http://localhost:18789
  ```

**通过 Tailscale 访问澳龙 OpenClaw：**
- 直接访问：`http://100.72.241.16:18789`（bind: lan 模式）

**云船 SSH 到澳龙：**

> WSL1 的 Tailscale 使用 userspace-networking 模式，不创建 tun 设备，常规 TCP/ICMP 不走 Tailscale 网络。
> 需要通过 Tailscale 提供的 SOCKS5 代理（localhost:1055）中转。

云船 `~/.ssh/config`：
```
Host aolong
    HostName 100.72.241.16
    User root
    ProxyCommand nc -x localhost:1055 %h %p

Host aolong-oc
    HostName 100.72.241.16
    User openclaw
    ProxyCommand nc -x localhost:1055 %h %p

Host aolong-pub
    HostName 39.107.54.166
    User root
```

使用：`ssh aolong`（root 系统管理）、`ssh aolong-oc`（openclaw 服务管理）

**澳龙 SSH 到云船：**

澳龙 `/home/openclaw/.ssh/config`：
```
Host yunchuan
    HostName 39.107.54.166
    Port 12222
    User arqiaoclaw

Host yunchuan-ts
    HostName 100.115.214.108
    User arqiaoclaw
```

使用：`ssh yunchuan`（frp 隧道）或 `ssh yunchuan-ts`（Tailscale 直连）

#### 7.5.4 安全配置

**关闭公网 18789 端口暴露：**
```bash
# 云船 frpc 配置只保留 SSH 隧道
cat > /mnt/c/Users/Administrator/frp_0.61.0_linux_amd64/frpc.toml << 'EOF'
serverAddr = "39.107.54.166"
serverPort = 7000
auth.token = "YOUR_FRP_TOKEN"

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 12222
EOF

# 重启 frpc
pkill -f frpc
cd /mnt/c/Users/Administrator/frp_0.61.0_linux_amd64
nohup ./frpc -c frpc.toml > frpc.log 2>&1 &
```

**验证公网端口已关闭：**
```bash
curl http://39.107.54.166:18789/  # 应该连接失败
```

---

## 八、服务管理（WSL1 专用）

WSL1 不支持 systemd，使用 nohup + screen 管理服务。

### 8.1 启动 Gateway

```bash
nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &
```

### 8.2 重启 Gateway

> 注意：pkill 后需等待 2 秒，否则端口未释放会导致新进程启动失败（Exit 1）。

```bash
pkill -f "openclaw gateway"
sleep 2
nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &
```

### 8.3 停止 Gateway

```bash
pkill -f "openclaw gateway"
```

### 8.4 查看日志

```bash
tail -f /tmp/openclaw-gateway.log
```

---

## 九、客户端访问

> 联通云平台拦截所有入站端口，外网访问需通过 frp 穿透到阿里云（见第七节）。

### 9.1 手机 / 外网设备

> 说明：直接用 IP 访问会报 `control ui requires device identity` 错误，原因是浏览器安全策略：
> HTTP + 非 localhost 地址不是安全上下文，WebCrypto API 被限制，OpenClaw 无法生成 device identity。
> 手机访问需要配置 HTTPS（见附录），或通过 Tailscale 组网后用虚拟 IP 访问。

### 9.2 本地 Windows 笔记本（推荐方式）

> 在笔记本本地运行

必须通过 SSH 隧道走 localhost 访问，不能直接用 IP：

```powershell
# 在笔记本本地运行（保持此窗口不关）
ssh -N -L 18789:localhost:18789 -p 12222 arqiaoclaw@39.107.54.166
```

然后浏览器访问：`http://localhost:18789`

> 直接访问 `http://39.107.54.166:18789` 会报 `control ui requires device identity` 错误，原因同上。

> 注：若使用 Windows Terminal 而非 MobaXterm，可在 `~/.ssh/config`（Windows 上为 `C:\Users\用户名\.ssh\config`）加入以下配置实现自动建隧道：
>
> ```
> Host openclaw-vm
>     HostName 39.107.54.166
>     Port 12222
>     User arqiaoclaw
>     LocalForward 18789 localhost:18789
> ```

### 9.3 SSH 客户端选型

Windows 默认终端（PowerShell/CMD）没有会话管理，每次都要手敲地址和端口，不适合管理多台服务器。

| 工具 | 优点 | 缺点 | 对你的适用性 |
|------|------|------|------------|
| **MobaXterm**（推荐） | 会话管理、内置SFTP、多标签、X11转发、免费版够用 | 界面稍重，免费版有会话数限制（14个） | ✅ 最适合：同时管理阿里云+联通云两台服务器，SFTP方便传文件 |
| **WindTerm** | 完全免费开源、轻量、现代UI | 社区相对小，功能比MobaXterm少 | ✅ 适合：只需要SSH管理，不需要SFTP的场景 |
| **Windows Terminal + SSH config** | 系统自带、轻量 | 无会话管理，需手动维护SSH config | ⚠️ 勉强够用：配好SSH config后可以用Tab补全，但没有图形化管理 |
| **Xshell** | 功能强大、国内用户多 | 免费版限制多，商业版较贵 | ❌ 不推荐：免费版限制太多，性价比不如MobaXterm |

**结论：** 用 MobaXterm，把阿里云（22端口）和联通云（12222端口）都保存为会话，一键连接。

下载：https://mobaxterm.mobatek.net/download-home-edition.html 选 Installer edition（当前最新版 26.1）。

### MobaXterm 会话配置（含端口转发）

> 坑点记录：直接 SSH 访问 `http://39.107.54.166:18789` 会报 `control ui requires device identity` 错误，必须走 SSH 隧道。

#### 创建联通云会话

1. 打开 MobaXterm → 点击左上角 "Session" → "SSH"
2. 填写：
   - Remote host: `39.107.54.166`
   - Port: `12222`
   - Username: `arqiaoclaw`
3. 切换到 "Advanced" 标签：
   - 勾选 "Don't use SSH gateway"
4. 切换到 "SSH gateway" 标签：
   - 勾选 "Connect to SSH gateway"
   - 不需要填写网关（留空）
   - 找到 "Port forwarding" 或 "Forwarded ports"：
     - 点击 "Add" 添加端口转发
     - Local port: `18789`
     - Remote server: `localhost`
     - Remote port: `18789`
5. 切换到 "Environment" 标签：
   - 勾选 "Login using SSH keys"（如果已配置密钥）
6. 保存会话，命名为"联通云-OpenClaw"

#### 验证

1. 双击会话连接
2. 浏览器访问 http://localhost:18789

> 若访问报错，检查会话的端口转发配置是否正确。确保 LocalForward 18789 → localhost:18789 已添加。

#### 创建桌面快捷方式

> 双击 MobaXterm 会话才能连接，不想每次手动双击可以创建快捷方式。

1. 右键已保存的会话 → "Create shortcut"
2. 快捷方式会创建到桌面
3. 双击桌面快捷方式 → 自动连接 SSH + 建立隧道
4. 然后手动打开浏览器访问 http://localhost:18789

### 9.4 allowedOrigins 配置

首次从外网访问控制台会报 `origin not allowed` 错误，需要把访问地址加入白名单：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://localhost:18789","http://127.0.0.1:18789","http://39.107.54.166:18789"]'
pkill -f "openclaw gateway"
sleep 2
nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &
```

---

## 十、日常运维

> 日常运维操作涉及多个终端：
> - 笔记本本地：通过 MobaXterm SSH 连接到联通云
> - 联通云 WSL1：执行 openclaw、frpc 等命令

### 10.1 进入 WSL1

> 在联通云 Windows 上运行

```powershell
wsl -d Ubuntu-24.04
```

### 10.2 服务状态检查

> 在联通云 WSL1 上运行（通过 SSH 连接后执行）

```bash
# OpenClaw 状态
openclaw status
openclaw health

# frpc 状态
ps aux | grep frpc

# 查看 frpc 日志
cat /tmp/frpc.log
```

### 10.3 查看 OpenClaw 日志

> 在联通云 WSL1 上运行

```bash
tail -f /tmp/openclaw-gateway.log
```

### 10.4 开机自启配置

> 在联通云 Windows 上运行

> 注意：联通云需要手动打开"云电脑"客户端才能让云主机上线，无法完全自动化。

#### 步骤一：创建启动脚本

> 坑点记录：
> - WSL 启动需要时间，直接运行会失败，需要循环检测 WSL 就绪
> - SSH 服务启动需要用 root 用户执行（不要用 sudo，会卡住等待密码输入）

在联通云 Windows 上创建 `C:\Users\Administrator\start-openclaw.bat`，内容如下：

```bat
@echo off
REM Wait for WSL (max 60s, check every 5s)
set "waited=0"
:wait_wsl
timeout /t 5 /nobreak > nul
set /a waited+=5
wsl -d Ubuntu-24.04 exit 2>nul
if %errorlevel% neq 0 (
    if %waited% lss 60 goto wait_wsl
    echo WSL not ready after 60s
    exit /b 1
)
echo WSL ready after %waited% seconds
REM Start services (use root for ssh, no sudo needed)
wsl -d Ubuntu-24.04 -u root -- bash -c "service ssh start"
timeout /t 5 /nobreak > nul
REM Tailscale (WSL1 needs userspace networking)
wsl -d Ubuntu-24.04 -u root -- bash -c "nohup tailscaled --tun=userspace-networking --socks5-server=localhost:1055 > /tmp/tailscaled.log 2>&1 &"
timeout /t 3 /nobreak > nul
wsl -d Ubuntu-24.04 -u root -- bash -c "tailscale up"
REM frpc tunnel
wsl -d Ubuntu-24.04 -u arqiaoclaw -- bash -c "nohup /mnt/c/Users/Administrator/frp_0.61.0_linux_amd64/frpc -c /mnt/c/Users/Administrator/frp_0.61.0_linux_amd64/frpc.toml > /tmp/frpc.log 2>&1 &"
REM HTTP proxy for aolong (bidirectional proxy)
wsl -d Ubuntu-24.04 -u arqiaoclaw -- bash -c "nohup python3 ~/local/scripts/simple-proxy.py > ~/local/proxy.log 2>&1 &"
REM OpenClaw gateway
wsl -d Ubuntu-24.04 -u arqiaoclaw -- bash -c "nohup /home/arqiaoclaw/.local/share/pnpm/openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &"
REM account-manager web UI
wsl -d Ubuntu-24.04 -u arqiaoclaw -- bash -c "nohup node ~/workspace/arqiao-shared-knowledge/server-scripts/account-manager.js > /tmp/account-manager.log 2>&1 &"
```

或者用 PowerShell 命令直接创建：

#### 步骤二：加入启动文件夹

> 坑点记录：任务计划开机启动（AtStartup）需要 SYSTEM 账户权限，会遇到 267011 错误，且 WSL 可能未就绪。改用启动文件夹方式更简单可靠。

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw.lnk")
$Shortcut.TargetPath = "C:\Users\Administrator\start-openclaw.bat"
$Shortcut.WorkingDirectory = "C:\Users\Administrator"
$Shortcut.Save
```

验证：手动运行 `C:\Users\Administrator\start-openclaw.bat`，确认 WSL 启动成功。

#### 步骤三：Windows 自动登录

> 坑点记录：如果 Windows 开机需要输入密码，启动文件夹的脚本不会自动运行（需要用户登录后才触发）。

开启自动登录：

```powershell
$password = Read-Host -AsSecureString
$passwordText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_DWORD /d 1 /f
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d Administrator /f
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d $passwordText /f
```

#### 完整启动流程

1. 手动打开联通云"云电脑"客户端
2. Windows 自动登录（如已配置）
3. 启动文件夹自动运行 `start-openclaw.bat`
4. 脚本等待 WSL 就绪（最多 60 秒）
5. WSL 启动后依次启动：SSH 服务 → Tailscale → frpc 穿透 → simple-proxy → OpenClaw → account-manager
6. SSH 无密码连入：`ssh -p 12222 arqiaoclaw@39.107.54.166`
7. MobaXterm 登录后，浏览器访问 http://localhost:18789

### 10.5 重启后手动恢复（自启动异常时备用）

> 在联通云 WSL1 上运行

```bash
# 进入 WSL1
wsl -d Ubuntu-24.04

# 启动 Tailscale
sudo tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &
sudo tailscale up

# 启动 frpc
cd /mnt/c/Users/Administrator/frp_0.61.0_linux_amd64
nohup ./frpc -c frpc.toml > /tmp/frpc.log 2>&1 &

# 启动 HTTP 代理（供澳龙使用）
nohup python3 ~/local/scripts/simple-proxy.py > ~/local/proxy.log 2>&1 &

# 启动 OpenClaw gateway
nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &

# 启动 account-manager 网页
nohup node ~/workspace/arqiao-shared-knowledge/server-scripts/account-manager.js > /tmp/account-manager.log 2>&1 &
```

---

## 十一、故障排查

### 11.1 外网无法访问（SSH 或 OpenClaw）

> 在联通云 WSL1 上运行

```bash
# 1. 检查 frpc 是否在运行
ps aux | grep frpc

# 2. 查看 frpc 日志
cat /tmp/frpc.log

# 3. 检查 frpc 能否连上阿里云
curl -v telnet://39.107.54.166:7000

# 4. 检查阿里云 frps 是否在运行（在笔记本本地执行）
ssh root@39.107.54.166
# 然后在阿里云上执行：
cat /tmp/frps.log
ps aux | grep frps
```

> 常见原因：frpc 未启动、阿里云安全组未开放 7000/12222/18789 端口、frps 异常退出。

### 11.2 WSL1 无法启动

> 在联通云 Windows 上运行

```powershell
wsl --shutdown
wsl

# 检查 WSL 功能是否启用
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```

### 11.3 OpenClaw 进程异常退出

> 在联通云 WSL1 上运行

```bash
# 查看日志
cat /tmp/openclaw-gateway.log

# 重新启动
nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &
```

### 11.4 联通云自启动未生效

> 在联通云 Windows 上排查（通过远程桌面或云电脑客户端）

```powershell
# 检查启动文件夹内容
dir "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"

# 手动运行启动脚本测试
C:\Users\Administrator\start-openclaw.bat

# 检查任务计划（如果有）
Get-ScheduledTask -TaskName 'OpenClaw-AutoStart' | Get-ScheduledTaskInfo

# 检查 frpc 进程
wsl -d Ubuntu-24.04 -u arqiaoclaw -- bash -c "ps aux | grep frpc"

# 检查 openclaw 进程
wsl -d Ubuntu-24.04 -u arqiaoclaw -- bash -c "ps aux | grep openclaw"
```

### 11.5 SSH 无法连接

> 在笔记本本地排查

```powershell
# 测试 SSH 端口是否可达
telnet 39.107.54.166 12222

# 测试 OpenClaw 是否可达
curl http://39.107.54.166:18789/
```

### 11.6 OpenClaw 控制台无法访问（本地隧道方式）

> 在笔记本本地排查

```powershell
# 确认 SSH 隧道已建立
netstat -ano | findstr 18789

# 确认本地端口可访问
curl http://localhost:18789/
```

### 11.7 MobaXterm 端口转发不生效

检查会话配置：
1. 右键会话 → Edit
2. 确认 "SSH gateway" 标签下已添加端口转发：
   - Local port: 18789
   - Remote server: localhost
   - Remote port: 18789
3. 保存会话后重新连接

---

## 附录：不可用方案记录

### Hyper-V

> 联通云智电脑为云虚拟机，底层不支持嵌套虚拟化（SVM not present），
> Hyper-V Hypervisor 无法启动。
> 错误信息：`Hypervisor launch failed; Either SVM not present or not enabled in BIOS.`

### WSL2

> WSL2 依赖 Hyper-V 虚拟化层，同样因嵌套虚拟化不可用而失败。
> 错误信息：`HCS_E_HYPERV_NOT_INSTALLED`

### Docker Desktop

> 依赖 WSL2 / Hyper-V，同样不可用。

### 重装为 Linux

> 联通云控制台不支持更换系统镜像，无法操作。

---

## 附录二：内网穿透方案选型

### 背景

联通云平台拦截所有入站端口，客服明确不提供开放端口服务。需要借助第三方穿透工具才能从外网访问。

### 方案对比

| 方案 | 优点 | 缺点 | 对你的适用性 |
|------|------|------|------------|
| **frp**（当前方案） | 开源免费、自托管、性能好、配置简单 | 需要自己有公网服务器 | ✅ 最适合：已有阿里云，零额外成本，同时穿透SSH+OpenClaw |
| ngrok | 无需服务器、开箱即用 | 免费版流量限制、域名随机、每次重启地址变 | ❌ 不适合：地址不固定，OpenClaw token URL会失效 |
| Cloudflare Tunnel | 免费、稳定 | 需要域名、国内访问不稳定 | ⚠️ 备选：阿里云停用后的替代方案，但国内访问速度不保证 |
| 花生壳 | 国内产品 | 免费版带宽极低（1Mbps）、收费贵 | ❌ 不适合：1Mbps带宽跑OpenClaw会很卡 |
| ZeroTier/Tailscale | 安全、虚拟局域网 | 不是端口穿透，客户端都要装 | ⚠️ 可考虑：手机/笔记本都装Tailscale后可直连，但每台设备都要配置 |

### 选择 frp 的原因

1. 已有阿里云服务器（39.107.54.166），不需要额外付费
2. 自托管，token 自己控制，安全可靠
3. 性能好，无流量限制
4. 配置简单，同时穿透 SSH（12222）和 OpenClaw（18789）两个端口

### 备选方案

若将来阿里云停用，可改用 **Cloudflare Tunnel**（免费且稳定，需要域名）。

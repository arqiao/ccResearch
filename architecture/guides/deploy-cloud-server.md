# 方案 A：云服务器部署指南

> 适用阶段：第一阶段（过年期间远程使用）
> 预计使用时长：1-2 个月

---

## 一、云服务器选择

### 1.1 配置要求

| 配置项 | 最低要求 | 推荐配置 |
|-------|---------|---------|
| CPU | 1 核 | 2 核 |
| 内存 | 2 GB | 4 GB |
| 存储 | 40 GB SSD | 60 GB SSD |
| 带宽 | 1 Mbps | 3 Mbps |
| 系统 | Ubuntu 24.04 LTS | Ubuntu 24.04 LTS |

### 1.2 厂商对比

| 厂商 | 2核4G 月付价格 | 新用户优惠 | 特点 |
|-----|---------------|-----------|------|
| 阿里云 | ~80 元/月 | 首购低至 1 折 | 稳定，文档全 |
| 腾讯云 | ~70 元/月 | 新用户 2-3 折 | 微信生态好 |
| 火山引擎 | ~60 元/月 | 新用户优惠 | 价格有竞争力 |
| Hetzner | ~€6/月 (~45 元) | 无 | 性价比高，OpenClaw 官方推荐 |

### 1.3 确定选择：阿里云

**推荐产品：轻量应用服务器**

- 新用户首购优惠大（通常 2-3 折）
- 包含固定公网 IP
- 自带安全组，配置简单

**购买步骤：**

1. 访问 https://www.aliyun.com/product/swas
2. 选择地域：就近选择（如华东、华南）
3. 镜像：Ubuntu 24.04 LTS
4. 套餐：2核2G 起步（约 50-80 元/月，新用户更低）
5. 购买时长：1 个月（短期使用）
6. 完成支付

---

## 二、服务器初始化

### 2.1 购买后首次登录

```bash
# 使用 SSH 登录（替换为你的服务器 IP）
ssh root@YOUR_SERVER_IP

# 首次登录建议修改密码
passwd
```

### 2.2 创建普通用户（推荐）

```bash
# 创建用户
adduser openclaw

# 添加 sudo 权限
usermod -aG sudo openclaw

# 切换到新用户
su - openclaw
```

### 2.3 安装基础依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要工具
sudo apt install -y curl git wget unzip

# 安装 Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
node -v  # 应显示 v22.x.x
npm -v
```

### 2.4 安装 Docker（可选，用于沙箱）

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sudo sh

# 将当前用户加入 docker 组
sudo usermod -aG docker $USER

# 重新登录使权限生效
exit
ssh openclaw@YOUR_SERVER_IP

# 验证
docker --version
```

---

## 三、安装 OpenClaw

### 3.1 安装 OpenClaw CLI

```bash
# 全局安装
npm install -g openclaw@latest

# 验证安装
openclaw --version
```

### 3.2 运行引导向导

```bash
# 启动引导向导（会引导你完成所有配置）
openclaw onboard --install-daemon
```

向导会引导你完成：
1. 选择 AI 模型提供商（推荐 Anthropic）
2. 配置 API Key
3. 设置 Gateway 端口（默认 18789）
4. 安装为系统服务

### 3.3 配置远程访问

编辑配置文件：

```bash
nano ~/.openclaw/openclaw.json
```

添加或修改以下配置：

```json
{
  "gateway": {
    "bind": "0.0.0.0",
    "port": 18789,
    "token": "YOUR_SECURE_TOKEN_HERE"
  }
}
```

**重要：** 生成一个安全的 token：

```bash
openssl rand -hex 32
```

### 3.4 防火墙配置

> **注意：** 由于 OpenClaw 控制台要求 HTTPS 或 localhost 访问，我们使用 SSH 隧道方式，**不需要**在公网暴露 18789 端口。这样更安全。

阿里云安全组只需保留 SSH 端口（22）即可，**不要**开放 18789 端口。

如果之前已添加 18789 规则，请在阿里云控制台删除。

### 3.5 启动 Gateway

```bash
# 后台运行 Gateway（推荐）
nohup openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &

# 查看是否启动成功
openclaw status

# 查看日志
tail -f /tmp/openclaw-gateway.log
```

> 注意：阿里云轻量服务器的 systemd 用户服务可能不可用，使用 nohup 方式更可靠。

### 3.6 从本地访问控制台

在 Windows 本地建立 SSH 隧道：

```powershell
ssh -N openclaw-tunnel
```

然后浏览器访问：
```
http://localhost:18789/#token=你的token
```

---

## 四、配置阿乔的共享知识库

### 4.1 克隆阿乔的共享知识库

```bash
# 创建工作目录
mkdir -p ~/workspace
cd ~/workspace

# 克隆阿乔的共享知识库（替换为你的仓库地址）
git clone https://github.com/YOUR_USERNAME/arqiao-shared-knowledge.git

# 设置环境变量
echo 'export SHARED_KNOWLEDGE_PATH="$HOME/workspace/arqiao-shared-knowledge"' >> ~/.bashrc
source ~/.bashrc
```

### 4.2 配置 Git 身份

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4.3 链接 Skills 到 OpenClaw

```bash
# 方法一：软链接到 managed skills 目录
ln -s ~/workspace/arqiao-shared-knowledge/skills ~/.openclaw/skills

# 方法二：在配置中添加额外 skills 目录
# 编辑 ~/.openclaw/openclaw.json，添加：
# "skills": {
#   "load": {
#     "extraDirs": ["/home/openclaw/workspace/arqiao-shared-knowledge/skills"]
#   }
# }
```

---

## 五、客户端连接

### 5.1 从 Windows 笔记本连接

**方法一：直接连接（需要公网 IP）**

```bash
# 测试连接
curl http://YOUR_SERVER_IP:18789/health
```

**方法二：SSH 隧道（更安全）**

```bash
# 在本地创建隧道
ssh -N -L 18789:127.0.0.1:18789 openclaw@YOUR_SERVER_IP

# 然后访问 http://127.0.0.1:18789
```

### 5.2 配置本地 Claude Code

在本地 `~/.claude/CLAUDE.md` 中添加：

```markdown
## 远程知识仓库

当需要查阅共享知识时，通过 SSH 访问远程服务器：
- 服务器：YOUR_SERVER_IP
- 知识库路径：/home/openclaw/workspace/shared-knowledge
```

---

## 六、安全加固

### 6.1 配置 SSH 密钥登录

**Windows 客户端操作（PowerShell）：**

```powershell
# 生成密钥（如果没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥到服务器（Windows 没有 ssh-copy-id，用这个方式）
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh root@服务器IP "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Linux/Mac 客户端操作：**

```bash
# 生成密钥（如果没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥到服务器
ssh-copy-id root@服务器IP
```

**服务器端（可选，禁用密码登录更安全）：**

```bash
sudo nano /etc/ssh/sshd_config
# 设置 PasswordAuthentication no
sudo systemctl restart sshd
```

### 6.2 配置 HTTPS（可选）

使用 Caddy 自动配置 HTTPS：

```bash
# 安装 Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# 配置反向代理
sudo nano /etc/caddy/Caddyfile
```

Caddyfile 内容：

```
your-domain.com {
    reverse_proxy localhost:18789
}
```

---

## 七、日常运维

### 7.1 常用命令

```bash
# 查看 Gateway 状态
openclaw health
openclaw status --deep

# 查看日志
journalctl -u openclaw-gateway -f

# 重启服务
sudo systemctl restart openclaw-gateway
```

### 7.2 OpenClaw 更新策略

**原则：手动更新，先备份后升级**

```bash
# 1. 查看当前版本
openclaw --version

# 2. 查看最新版本和 changelog
npm view openclaw version
# 或访问 https://github.com/openclaw/openclaw/releases

# 3. 备份当前配置
tar -czvf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw

# 4. 更新（确认 changelog 无破坏性变更后）
npm update -g openclaw@latest

# 5. 重启服务
sudo systemctl restart openclaw-gateway

# 6. 验证
openclaw health
openclaw doctor
```

**回滚方法（如果更新出问题）：**

```bash
# 1. 安装指定版本
npm install -g openclaw@<previous-version>

# 2. 恢复配置（如果需要）
tar -xzvf openclaw-backup-YYYYMMDD.tar.gz -C ~/

# 3. 重启
sudo systemctl restart openclaw-gateway
```

**更新检查频率：每周一次**

建议关注：
- GitHub Releases: https://github.com/openclaw/openclaw/releases
- Discord 公告频道

### 7.3 备份

```bash
# 备份配置和数据
tar -czvf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw

# 备份知识仓库（Git 已有版本控制，主要是推送到远程）
cd ~/workspace/shared-knowledge
git push origin main
```

---

## 八、迁移准备

当准备迁移到树莓派时：

1. 确保知识仓库已推送到 Git 远程
2. 导出 OpenClaw 配置：`tar -czvf openclaw-config.tar.gz ~/.openclaw`
3. 记录当前的 API Key 和 Token 配置
4. 参考「方案 B：树莓派部署指南」进行迁移

---

## 九、故障排查

### 9.1 Gateway 无法启动

```bash
# 检查端口占用
sudo lsof -i :18789

# 检查日志
journalctl -u openclaw-gateway --no-pager -n 50
```

### 9.2 无法远程连接

```bash
# 检查防火墙
sudo ufw status

# 检查服务是否监听
sudo netstat -tlnp | grep 18789

# 检查云服务器安全组规则（在云控制台）
```

### 9.3 Skills 未加载

```bash
# 检查 skills 目录
ls -la ~/.openclaw/skills

# 运行诊断
openclaw doctor
```

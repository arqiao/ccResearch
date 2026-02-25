# 方案 B：树莓派部署指南

> 适用阶段：第二阶段（长期运行）
> 预计启用时间：1 个月后

---

## 一、硬件准备

### 1.1 设备清单

| 设备 | 规格 | 状态 |
|-----|------|------|
| Raspberry Pi 5 | 8GB 内存 | 已有 |
| MicroSD 卡 | 32GB（建议升级到 64GB+） | 已有 |
| 电源适配器 | 5V 5A USB-C（官方推荐） | 需确认 |
| 网线 | Cat5e 或更高 | 推荐有线连接 |
| 散热器/风扇 | 主动散热 | 推荐（长期运行） |

### 1.2 存储建议

**推荐升级方案（按优先级）：**

1. **外接 SSD（最推荐）**：通过 USB 3.0 连接，速度快、寿命长
2. **高耐久 MicroSD 卡**：如 SanDisk High Endurance 64GB+
3. **当前 32GB 卡**：可用，但建议尽快升级

---

## 二、系统安装

### 2.1 下载系统镜像

推荐使用 **Raspberry Pi OS Lite (64-bit)**：
- 无桌面环境，资源占用少
- 64 位系统，性能更好

下载地址：https://www.raspberrypi.com/software/operating-systems/

### 2.2 烧录系统

使用 Raspberry Pi Imager：

1. 下载并安装 [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. 选择系统：Raspberry Pi OS Lite (64-bit)
3. 选择存储设备
4. 点击设置图标，配置：
   - 设置主机名：`openclaw-pi`
   - 启用 SSH
   - 设置用户名密码
   - 配置 WiFi（可选，推荐用网线）
   - 设置时区：Asia/Shanghai
5. 烧录

### 2.3 首次启动

```bash
# 通过 SSH 连接（替换为实际 IP）
ssh pi@openclaw-pi.local
# 或
ssh pi@192.168.x.x

# 更新系统
sudo apt update && sudo apt full-upgrade -y

# 重启
sudo reboot
```

---

## 三、系统优化

### 3.1 减少 SD 卡写入

```bash
# 编辑 fstab，将 /tmp 和 /var/log 挂载到内存
sudo nano /etc/fstab

# 添加以下行：
tmpfs /tmp tmpfs defaults,noatime,nosuid,size=100m 0 0
tmpfs /var/log tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0
```

### 3.2 配置 Swap（如果使用 SSD）

```bash
# 如果使用 SD 卡，建议禁用 swap
sudo dphys-swapfile swapoff
sudo systemctl disable dphys-swapfile

# 如果使用 SSD，可以保留或增加 swap
sudo nano /etc/dphys-swapfile
# 设置 CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### 3.3 设置静态 IP（推荐）

```bash
sudo nano /etc/dhcpcd.conf

# 添加以下内容（根据你的网络调整）：
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

重启网络：

```bash
sudo systemctl restart dhcpcd
```

---

## 四、安装 OpenClaw

### 4.1 安装 Node.js 22

```bash
# 使用 NodeSource 安装
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# 验证
node -v
npm -v
```

### 4.2 安装 OpenClaw

```bash
# 全局安装
sudo npm install -g openclaw@latest

# 运行引导向导
openclaw onboard --install-daemon
```

### 4.3 从云服务器迁移配置

```bash
# 在云服务器上导出配置
tar -czvf openclaw-config.tar.gz ~/.openclaw

# 传输到树莓派
scp openclaw-config.tar.gz pi@openclaw-pi.local:~/

# 在树莓派上解压
cd ~
tar -xzvf openclaw-config.tar.gz
```

---

## 五、内网穿透配置

### 5.1 确定选择：Tailscale

**为什么选 Tailscale：**
- 免费（个人使用）
- 无需域名、无需固定公网 IP
- 配置简单，各平台都有客户端
- P2P 直连，延迟低

### 5.2 Tailscale 配置（推荐）

**在树莓派上安装：**

```bash
# 安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# 启动并登录
sudo tailscale up

# 会显示一个链接，在浏览器中打开完成授权
```

**在 Windows 笔记本上安装：**

1. 下载 Tailscale：https://tailscale.com/download/windows
2. 安装并登录同一账号
3. 两台设备会自动组网

**在小米手机上安装：**

1. 在应用商店搜索 Tailscale
2. 安装并登录同一账号

**验证连接：**

```bash
# 查看 Tailscale IP
tailscale ip -4

# 从其他设备 ping 树莓派的 Tailscale IP
ping 100.x.x.x
```

**配置 OpenClaw 监听 Tailscale 网络：**

```bash
nano ~/.openclaw/openclaw.json
```

```json
{
  "gateway": {
    "bind": "0.0.0.0",
    "port": 18789,
    "token": "YOUR_SECURE_TOKEN"
  }
}
```

### 5.3 Cloudflare Tunnel 配置（备选）

**前提：需要一个域名托管在 Cloudflare**

```bash
# 安装 cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# 登录 Cloudflare
cloudflared tunnel login

# 创建隧道
cloudflared tunnel create openclaw-tunnel

# 配置隧道
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

config.yml 内容：

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /home/pi/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: openclaw.your-domain.com
    service: http://localhost:18789
  - service: http_status:404
```

```bash
# 启动隧道
cloudflared tunnel run openclaw-tunnel

# 设置为系统服务
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

---

## 六、配置知识仓库

### 6.1 克隆仓库

```bash
mkdir -p ~/workspace
cd ~/workspace
git clone https://github.com/YOUR_USERNAME/shared-knowledge.git

# 配置 Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 6.2 配置 SSH 密钥（用于 Git 推送）

```bash
# 生成密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 将公钥添加到 GitHub/GitLab
```

### 6.3 链接 Skills

```bash
# 链接到 OpenClaw skills 目录
ln -s ~/workspace/shared-knowledge/skills ~/.openclaw/skills
```

---

## 七、设置开机自启

### 7.1 OpenClaw Gateway

```bash
# 如果使用 onboard --install-daemon，已自动配置
# 检查状态
sudo systemctl status openclaw-gateway

# 如果需要手动创建服务
sudo nano /etc/systemd/system/openclaw-gateway.service
```

服务文件内容：

```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/openclaw gateway --port 18789
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw-gateway
sudo systemctl start openclaw-gateway
```

### 7.2 Tailscale

```bash
# Tailscale 安装后自动设置为开机启动
sudo systemctl enable tailscaled
```

---

## 八、监控与维护

### 8.1 查看系统状态

```bash
# CPU 温度
vcgencmd measure_temp

# 内存使用
free -h

# 磁盘使用
df -h

# 系统负载
htop
```

### 8.2 设置温度监控（可选）

```bash
# 创建监控脚本
nano ~/monitor-temp.sh
```

```bash
#!/bin/bash
TEMP=$(vcgencmd measure_temp | grep -oP '\d+\.\d+')
if (( $(echo "$TEMP > 70" | bc -l) )); then
    echo "Warning: CPU temperature is ${TEMP}°C" | logger
fi
```

```bash
chmod +x ~/monitor-temp.sh

# 添加到 crontab
crontab -e
# 添加：*/5 * * * * /home/pi/monitor-temp.sh
```

### 8.3 OpenClaw 更新策略

**原则：手动更新，先备份后升级**

与云服务器相同的流程：

```bash
# 1. 查看当前版本
openclaw --version

# 2. 备份
tar -czvf ~/openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw

# 3. 查看 changelog 确认无破坏性变更后更新
npm update -g openclaw@latest

# 4. 重启并验证
sudo systemctl restart openclaw-gateway
openclaw health && openclaw doctor
```

**回滚：**

```bash
npm install -g openclaw@<previous-version>
sudo systemctl restart openclaw-gateway
```

### 8.4 自动更新知识仓库

```bash
# 创建同步脚本
nano ~/sync-knowledge.sh
```

```bash
#!/bin/bash
cd ~/workspace/shared-knowledge
git pull origin main
```

```bash
chmod +x ~/sync-knowledge.sh

# 每小时自动同步
crontab -e
# 添加：0 * * * * /home/pi/sync-knowledge.sh
```

---

## 九、从云服务器迁移

### 9.1 迁移清单

- [ ] 导出云服务器 OpenClaw 配置
- [ ] 确保知识仓库已推送到 Git 远程
- [ ] 在树莓派上完成所有安装
- [ ] 测试 Tailscale 连接
- [ ] 验证 OpenClaw Gateway 正常运行
- [ ] 更新本地客户端配置（指向新地址）
- [ ] 释放云服务器

### 9.2 迁移步骤

```bash
# 1. 在云服务器上
cd ~/workspace/shared-knowledge
git add -A && git commit -m "迁移前最终同步" && git push

tar -czvf openclaw-backup.tar.gz ~/.openclaw
scp openclaw-backup.tar.gz pi@TAILSCALE_IP:~/

# 2. 在树莓派上
tar -xzvf openclaw-backup.tar.gz
sudo systemctl restart openclaw-gateway

# 3. 验证
openclaw health
openclaw status --deep

# 4. 更新本地 CLAUDE.md，将服务器地址改为 Tailscale IP
```

---

## 十、故障排查

### 10.1 树莓派无法启动

- 检查电源是否足够（需要 5V 5A）
- 尝试重新烧录系统
- 检查 SD 卡是否损坏

### 10.2 Tailscale 连接不上

```bash
# 检查 Tailscale 状态
tailscale status

# 重新认证
sudo tailscale up --reset
```

### 10.3 OpenClaw 内存不足

```bash
# 检查内存使用
free -h

# 重启 Gateway
sudo systemctl restart openclaw-gateway

# 如果持续不足，考虑增加 swap（仅限 SSD）
```

### 10.4 SD 卡损坏预防

- 定期备份重要数据到 Git
- 使用高耐久 SD 卡
- 考虑升级到 SSD
- 避免频繁写入（已配置 tmpfs）

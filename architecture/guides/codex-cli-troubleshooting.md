# Codex CLI 排障指南
> 更新时间：2026-03-24
> 适用环境：Windows PowerShell

---

## 一、适用场景

这篇文档只写排障，不写日常使用。

适合以下情况：

- `codex` 启动失败
- 登录状态异常
- `codex exec` 无法联网
- 怀疑代理、证书、权限或当前终端环境有问题
- 想查看本地会话日志和运行日志

日常使用请看：

- `guides/codex-cli-usage.md`

---

## 二、快速判断方法

这部分用于快速判断问题到底在：

- Codex 本身
- 登录状态
- 网络 / 代理
- 当前终端环境

### 2.1 第一步：看登录是否正常

```powershell
codex login status
```

正常结果：

```text
Logged in using ChatGPT
```

如果这里失败，先处理登录问题，不要继续排查网络。

### 2.2 第二步：跑最小执行命令

```powershell
codex exec --skip-git-repo-check --color never "reply with exactly: OK"
```

判断标准：

- 成功返回 `OK`：核心链路正常
- 失败：继续看错误类型

### 2.3 第三步：看代理变量

```powershell
Get-ChildItem Env: | Where-Object { $_.Name -match '^(HTTP|HTTPS|ALL)_PROXY$|^NO_PROXY$' }
```

重点观察：

- 是否存在 `HTTP_PROXY`
- 是否存在 `HTTPS_PROXY`
- 是否存在 `ALL_PROXY`
- 值是不是你明确知道的代理地址

如果出现这种值：

```text
127.0.0.1:9
```

或者某个你并没有主动配置的本地代理地址，优先怀疑环境注入了错误代理。

### 2.4 第四步：看是否是网络还是权限报错

常见判断方式：

- 报错包含 `connection refused`、`error sending request`、`websocket`、`https`：优先怀疑网络、代理、证书环境
- 报错包含 `permission denied`、`拒绝访问`：先确认是不是在受限终端、沙箱、远程受控环境里运行

不要在第一时间把“拒绝访问”直接认定为本机目录权限损坏。

---

## 三、Windows 常见代理与证书问题处理

这一节只针对 Windows 本机排障，不针对受限沙箱或远程代跑环境。

### 3.1 先看当前会话里有没有代理变量

```powershell
Get-ChildItem Env: | Where-Object { $_.Name -match '^(HTTP|HTTPS|ALL)_PROXY$|^NO_PROXY$' }
```

如果结果里出现你不认识的代理地址，尤其是这类明显异常值：

```text
http://127.0.0.1:9
```

先在当前 PowerShell 会话里临时清掉，再重试 `codex`：

```powershell
$env:HTTP_PROXY=$null
$env:HTTPS_PROXY=$null
$env:ALL_PROXY=$null
$env:NO_PROXY=$null
codex exec --skip-git-repo-check --color never "reply with exactly: OK"
```

这只影响当前终端窗口，不会修改系统配置。

### 3.2 检查用户或系统环境变量里是否持久化了代理

检查当前用户环境变量：

```powershell
reg query HKCU\Environment
```

检查系统环境变量：

```powershell
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
```

如果这里存在错误的 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`，说明问题不是临时会话，而是机器配置本身。

### 3.3 检查 WinHTTP 代理

```powershell
netsh winhttp show proxy
```

正常情况下常见结果是：

```text
Direct access (no proxy server).
```

如果这里被配置成了错误代理，很多命令行程序都会受影响。

### 3.4 检查 PowerShell 启动脚本有没有偷偷设置代理

```powershell
$profile | ForEach-Object { if (Test-Path $_) { Write-Host "=== $_ ==="; Get-Content $_ } }
```

如果 profile 里写了代理环境变量，每次开新终端都会自动注入。

### 3.5 检查目标站点 443 连通性

```powershell
Test-NetConnection chatgpt.com -Port 443
```

如果 `TcpTestSucceeded` 为 `True`，说明最基础的 TCP 连通性是通的。

注意：

- 443 通，不代表一定能成功完成 TLS 握手
- 443 不通，优先排查网络、防火墙、公司代理或本地代理软件

### 3.6 如果报证书相关错误，先区分“系统坏了”还是“当前环境受限”

如果你看到类似错误：

- `no native root CA certificates found`
- `failed to open current user certificate store`
- `拒绝访问`

不要立刻判断成“Windows 证书库损坏”。先做这两个动作：

1. 直接检查当前用户证书库能否读取

```powershell
Get-ChildItem Cert:\CurrentUser\Root | Select-Object -First 5 Subject,Thumbprint
```

2. 再用系统工具检查一次

```powershell
certutil -user -store Root
```

如果这两条都能正常返回，通常说明 Windows 证书库本身没坏，问题更可能出在：

- 当前终端是受限环境
- 某个沙箱或远程控制环境阻止了证书访问
- 某个代理或中间层破坏了 TLS 链路

---

## 四、本地日志与会话记录

Codex CLI 的本地记录主要在用户目录下：

- 会话记录目录：`C:\Users\qiaolian\.codex\sessions`
- 命令历史文件：`C:\Users\qiaolian\.codex\history.jsonl`
- 运行日志文件：`C:\Users\qiaolian\.codex\log\codex-tui.log`

### 4.1 查看所有会话记录

```powershell
Get-ChildItem $env:USERPROFILE\.codex\sessions -Recurse
```

### 4.2 查看命令历史

```powershell
Get-Content $env:USERPROFILE\.codex\history.jsonl
```

### 4.3 查看运行日志的最后 200 行

```powershell
Get-Content $env:USERPROFILE\.codex\log\codex-tui.log -Tail 200
```

### 4.4 查看最近一次会话的原始记录

最近的会话记录通常位于：

```text
C:\Users\qiaolian\.codex\sessions\年\月\日\
```

里面的 `.jsonl` 文件就是对应会话的原始记录。

如果只想先列出最近的会话文件：

```powershell
Get-ChildItem $env:USERPROFILE\.codex\sessions -Recurse -File | Sort-Object LastWriteTime -Descending | Select-Object -First 10 FullName,LastWriteTime
```

---

## 五、这次问题的实际原因

这次排查里，前期报错来自“检查环境”和“真实使用环境”不一致。

### 5.1 现象

前面的检查里出现了两类错误：

- 无法连接 `chatgpt.com`
- 无法写入 `C:\Users\qiaolian\.codex\skills` 和 `C:\Users\qiaolian\.codex\tmp\arg0`

### 5.2 实际原因

原因不是本机损坏，而是受限执行环境干扰了判断：

- 该环境里存在错误代理变量：

```text
HTTP_PROXY=http://127.0.0.1:9
HTTPS_PROXY=http://127.0.0.1:9
ALL_PROXY=http://127.0.0.1:9
```

- 该环境本身也限制了对 `C:\Users\qiaolian\.codex` 的写入

### 5.3 结果

切到真实用户环境后重新验证，结果全部正常：

- `codex exec` 成功返回 `OK`
- `.codex` 目录可写
- 登录正常
- 当前仓库可直接使用

所以这次不需要修系统，不需要重装 Codex，也不需要改 `.codex` 目录权限。

---

## 六、建议保留的排障命令

### 6.1 基本可用性

```powershell
codex --version
codex login status
codex exec --skip-git-repo-check --color never "reply with exactly: OK"
```

### 6.2 代理检查

```powershell
Get-ChildItem Env: | Where-Object { $_.Name -match '^(HTTP|HTTPS|ALL)_PROXY$|^NO_PROXY$' }
```

### 6.3 目标站点 443 连通性

```powershell
Test-NetConnection chatgpt.com -Port 443
```

### 6.4 WinHTTP 代理检查

```powershell
netsh winhttp show proxy
```

### 6.5 当前目录是否是 Git 仓库

```powershell
git rev-parse --is-inside-work-tree
```

### 6.6 证书库可读性检查

```powershell
Get-ChildItem Cert:\CurrentUser\Root | Select-Object -First 5 Subject,Thumbprint
certutil -user -store Root
```

---

## 七、最实用的最终判断

如果下面三条同时成立：

- `codex login status` 正常
- `Test-NetConnection chatgpt.com -Port 443` 正常
- `codex exec --skip-git-repo-check --color never "reply with exactly: OK"` 成功

那就说明：

- `codex` 安装正常
- 登录正常
- 网络核心链路正常
- 没必要继续怀疑证书库、`.codex` 权限或 CLI 安装本身

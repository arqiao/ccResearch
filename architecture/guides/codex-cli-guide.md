# Codex CLI 指南入口
> 更新时间：2026-03-24
> 适用环境：Windows PowerShell

---

## 一、说明

原先这篇文档同时混合了两类内容：

- 日常使用
- 运维排障

现在已经拆分，便于分别查阅。

---

## 二、使用文档

日常使用、启动方式、常用命令、进入 Codex 对话环境后的常用输入方式，见：

- `guides/codex-cli-usage.md`

---

## 三、排障文档

安装验证、登录检查、最小可用性判断、Windows 代理与证书问题处理，见：

- `guides/codex-cli-troubleshooting.md`

---

## 四、当前机器状态

当前机器已验证可用。最小验证命令：

```powershell
codex exec --skip-git-repo-check --color never "reply with exactly: OK"
```

预期结果：

```text
OK
```

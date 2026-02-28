#!/usr/bin/env python3
"""LLM 模型切换脚本 - 切换模型并自动选择可用账户"""
import json, sys, os, subprocess
from datetime import date

CONFIG_FILE = "/root/.openclaw/models-config.json"
ACCOUNTS_FILE = "/root/.openclaw/accounts.json"
OPENCLAW_JSON = "/root/.openclaw/openclaw.json"
AUTH_PROFILES = "/root/.openclaw/agents/main/agent/auth-profiles.json"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def notify(msg):
    try:
        subprocess.run(["python3", "/root/scripts/feishu_send.py", msg],
                       timeout=15, capture_output=True)
    except Exception:
        pass


def clean_unavailable(config):
    """清除过期的不可用标记（非当天的）"""
    today = date.today().isoformat()
    config["unavailable"] = {
        k: v for k, v in config.get("unavailable", {}).items()
        if v == today
    }
    return config


def cmd_list():
    """列出所有可用模型"""
    config = clean_unavailable(load_json(CONFIG_FILE))
    save_json(CONFIG_FILE, config)
    current = config["current"]
    today = date.today().isoformat()
    lines = ["可用模型列表：", ""]
    for mid, info in config["models"].items():
        marker = " <- 当前" if mid == current["model"] else ""
        avail = [a for a in info["accounts"]
                 if config["unavailable"].get(a) != today]
        lines.append("  {} ({}){}".format(info['name'], mid, marker))
        avail_str = ', '.join(avail) if avail else '无可用账户'
        lines.append("    可用账户: {}".format(avail_str))
    print("\n".join(lines))


def cmd_status():
    """查看当前状态"""
    config = clean_unavailable(load_json(CONFIG_FILE))
    save_json(CONFIG_FILE, config)
    cur = config["current"]
    model_info = config["models"].get(cur["model"], {})
    model_name = model_info.get('name', cur['model'])
    print("当前模型: {} ({})".format(model_name, cur['model']))
    print("当前账户: {}".format(cur['account']))
    if config["unavailable"]:
        print("今日不可用: {}".format(', '.join(config['unavailable'].keys())))
    else:
        print("今日不可用: 无")


def cmd_mark_unavailable(account):
    """标记账户当天不可用"""
    config = clean_unavailable(load_json(CONFIG_FILE))
    config["unavailable"][account] = date.today().isoformat()
    save_json(CONFIG_FILE, config)
    print("已标记 {} 今日不可用".format(account))
    notify("[模型切换] 账户 {} 余额不足，已标记今日不可用".format(account))


def cmd_reset_unavailable(account=None):
    """清除不可用标记。指定账户名则只清除该账户，否则清除全部"""
    config = load_json(CONFIG_FILE)
    if account:
        if account in config.get("unavailable", {}):
            del config["unavailable"][account]
            save_json(CONFIG_FILE, config)
            print("已复位账户 {}".format(account))
        else:
            print("账户 {} 未被标记为不可用".format(account))
    else:
        count = len(config.get("unavailable", {}))
        config["unavailable"] = {}
        save_json(CONFIG_FILE, config)
        print("已复位全部账户（清除 {} 条标记）".format(count))


def cmd_switch(model_id, account=None):
    """切换到指定模型，可选指定账户"""
    config = clean_unavailable(load_json(CONFIG_FILE))

    if model_id not in config["models"]:
        print("未知模型: {}".format(model_id))
        print("可用: {}".format(', '.join(config['models'].keys())))
        return False

    model_info = config["models"][model_id]
    today = date.today().isoformat()
    available = [a for a in model_info["accounts"]
                 if config["unavailable"].get(a) != today]

    if not available:
        msg = "模型 {} 无可用账户（全部余额不足）".format(model_id)
        print(msg)
        notify("[模型切换] {}".format(msg))
        return False

    if account:
        if account not in model_info["accounts"]:
            print("账户 {} 不属于模型 {}".format(account, model_id))
            return False
        if config["unavailable"].get(account) == today:
            print("账户 {} 今日不可用".format(account))
            return False
        account_name = account
    else:
        # 优先保持当前账户，只有不可用时才换
        current_account = config["current"].get("account", "")
        if current_account in available:
            account_name = current_account
        else:
            account_name = available[0]
    accounts = load_json(ACCOUNTS_FILE)
    account = accounts["accounts"].get(account_name)
    if not account:
        print("账户 {} 在 accounts.json 中不存在".format(account_name))
        return False

    # 修改 openclaw.json
    oc = load_json(OPENCLAW_JSON)
    model_full = "anthropic/{}".format(model_id)
    oc["agents"]["defaults"]["model"]["primary"] = model_full
    oc["agents"]["defaults"]["models"] = {model_full: {}}
    oc["models"]["providers"]["anthropic"]["baseUrl"] = account["baseUrl"]
    # 同步更新飞书频道的 per-channel model
    feishu = oc.get("channels", {}).get("feishu", {})
    if "agents" in feishu:
        feishu["agents"]["defaults"]["model"]["primary"] = model_full
    save_json(OPENCLAW_JSON, oc)

    # 修改 auth-profiles.json
    auth = load_json(AUTH_PROFILES)
    if "profiles" in auth:
        auth["profiles"]["anthropic:default"]["key"] = account["apiKey"]
    else:
        for k in auth:
            if "anthropic" in k:
                auth[k]["token"] = account["apiKey"]
                break
    save_json(AUTH_PROFILES, auth)

    # 更新 accounts.json current
    accounts["current"] = account_name
    save_json(ACCOUNTS_FILE, accounts)

    # 更新 models-config.json
    config["current"] = {"model": model_id, "account": account_name}
    save_json(CONFIG_FILE, config)

    # openclaw-gateway 会自动检测 config change 并热重载，无需手动重启
    # 仅当进程不存在时才 restart
    try:
        pid = subprocess.check_output(
            ["systemctl", "--user", "show", "-p", "MainPID", "--value",
             "openclaw-gateway"], timeout=5
        ).decode().strip()
        if not pid or pid == "0":
            subprocess.run(["systemctl", "--user", "restart", "openclaw-gateway"],
                           timeout=15, check=True)
    except Exception as e:
        print("检查服务状态失败: {}".format(e))

    msg = "已切换到 {}（账户: {}）".format(model_id, account_name)
    print(msg)
    notify("[模型切换] {}".format(msg))
    return True


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("用法:")
        print("  switch-llm.py <model-id> [--account <account>]  切换模型（可选指定账户）")
        print("  switch-llm.py --list               列出可用模型")
        print("  switch-llm.py --status             查看当前状态")
        print("  switch-llm.py --mark-unavailable <account>  标记账户不可用")
        print("  switch-llm.py --reset-unavailable [account] 复位账户（不指定则全部复位）")
    elif args[0] == "--list":
        cmd_list()
    elif args[0] == "--status":
        cmd_status()
    elif args[0] == "--mark-unavailable":
        if len(args) < 2:
            print("请指定账户名")
        else:
            cmd_mark_unavailable(args[1])
    elif args[0] == "--reset-unavailable":
        cmd_reset_unavailable(args[1] if len(args) > 1 else None)
    else:
        acct = None
        if "--account" in args:
            idx = args.index("--account")
            if idx + 1 < len(args):
                acct = args[idx + 1]
        cmd_switch(args[0], account=acct)

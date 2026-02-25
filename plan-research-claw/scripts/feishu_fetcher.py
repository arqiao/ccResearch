"""飞书数据拉取模块 - 增量获取多维表格记录"""

import json
import sys
import os

# 复用隔壁项目的飞书客户端
FEISHU_CLIENT_DIR = r"D:\workspace\dev-cc\1_clawbots\feishuMSG-xls\src"
sys.path.insert(0, FEISHU_CLIENT_DIR)
from feishu_client import FeishuClient


def load_existing_records(enriched_path: str) -> dict:
    """加载已有数据，返回 {record_id: article} 字典"""
    if not os.path.exists(enriched_path):
        return {}
    with open(enriched_path, "r", encoding="utf-8") as f:
        articles = json.load(f)
    return {a["record_id"]: a for a in articles}


def parse_raw_record(rec: dict) -> dict:
    """将飞书原始记录解析为标准格式"""
    fields = rec.get("fields", {})
    title_raw = fields.get("标题", "")
    if isinstance(title_raw, list):
        title = "".join(item.get("text", "") for item in title_raw).strip()
    else:
        title = str(title_raw).strip()

    link_raw = fields.get("链接", [])
    url = ""
    if isinstance(link_raw, list) and link_raw:
        url = link_raw[0].get("link", "") or link_raw[0].get("text", "")
    elif isinstance(link_raw, str):
        url = link_raw

    date_raw = fields.get("日期", 0)
    date_str = str(date_raw) if date_raw else ""
    if len(date_str) == 8:
        date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

    return {
        "record_id": rec.get("record_id", ""),
        "title": title,
        "url": url,
        "date": date_str,
        "source": fields.get("来源", ""),
        "weekday": fields.get("星期", ""),
        "topic": fields.get("主题分类", ""),
        "category": "",
        "sub_category": "",
        "depth": "",
        "summary": "",
        "word_count": 0,
        "scrape_status": "",
    }


def fetch_from_raw_json(root_dir: str, config: dict) -> list:
    """从本地 feishu_raw_data.json 加载数据"""
    raw_path = os.path.join(root_dir, config["paths"]["raw_data"])
    if not os.path.exists(raw_path):
        print(f"✗ {raw_path} 不存在")
        return []
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_records = json.load(f)
    return [parse_raw_record(r) for r in raw_records]


def fetch_incremental(config: dict, root_dir: str) -> list:
    """增量拉取：对比已有记录，只追加新的"""
    full_path = os.path.join(root_dir, config["paths"]["enriched_json"])

    existing = load_existing_records(full_path)
    all_records = fetch_from_raw_json(root_dir, config)

    new_count = 0
    for rec in all_records:
        rid = rec["record_id"]
        if rid not in existing:
            existing[rid] = rec
            new_count += 1

    merged = list(existing.values())
    merged.sort(key=lambda x: x.get("date", ""), reverse=True)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"✓ 数据合并完成：已有 {len(existing) - new_count}，新增 {new_count}，总计 {len(merged)}")
    return merged

"""热度计算模块 - 基于来源权重和时效性计算文章热度"""

import json
import os
from datetime import datetime, timedelta


def load_hotness_config(root_dir: str) -> dict:
    """加载热度配置"""
    path = os.path.join(root_dir, "data", "hotness.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_hotness(article: dict, config: dict, today: datetime = None) -> float:
    """计算单篇文章热度分"""
    if today is None:
        today = datetime.now()

    # 来源权重
    source = article.get("source", "")
    weights = config["source_weights"]
    source_weight = weights.get(source, weights.get("default", 2))

    # 时效衰减
    date_str = article.get("date", "")
    decay_factor = config["time_decay"][-1]["factor"]  # 默认最低

    if date_str:
        try:
            article_date = datetime.strptime(date_str, "%Y-%m-%d")
            days_ago = (today - article_date).days
            for rule in config["time_decay"]:
                if days_ago <= rule["days"]:
                    decay_factor = rule["factor"]
                    break
        except ValueError:
            pass

    # 计算热度分，归一化到 max_score
    max_score = config.get("max_score", 5)
    max_weight = max(config["source_weights"].values())
    raw_score = source_weight * decay_factor
    normalized = (raw_score / max_weight) * max_score

    return round(normalized, 1)


def calculate_all_hotness(articles: list, root_dir: str) -> list:
    """批量计算热度，直接修改并返回文章列表"""
    config = load_hotness_config(root_dir)
    today = datetime.now()

    for art in articles:
        art["hotness"] = calculate_hotness(art, config, today)

    print(f"✓ 热度计算完成，共 {len(articles)} 篇", flush=True)
    return articles

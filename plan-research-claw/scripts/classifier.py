"""分类打标模块 - 基于 categories.json 配置进行关键词规则匹配"""

import json
import os


def load_categories(root_dir: str) -> dict:
    """加载分类配置"""
    path = os.path.join(root_dir, "data", "categories.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _match_keywords(title: str, keywords: list) -> bool:
    """检查标题是否包含任一关键词"""
    title_lower = title.lower()
    for kw in keywords:
        if kw.lower() in title_lower:
            return True
    return False


def classify_article(title: str, categories: dict) -> dict:
    """对单篇文章进行分类打标"""
    # 匹配一级分类
    category = categories["default_primary"]
    sub_category = ""
    sub_list = []

    for cat in categories["primary"]:
        if _match_keywords(title, cat["keywords"]):
            category = cat["name"]
            sub_list = cat.get("sub", [])
            break

    # 匹配二级分类（如果有）
    if sub_list:
        for sub in sub_list:
            if _match_keywords(title, sub["keywords"]):
                sub_category = sub["name"]
                break
        if not sub_category:
            sub_category = categories["default_sub"]

    # 匹配内容深度
    depth = categories["default_depth"]
    for d in categories["depth"]:
        if _match_keywords(title, d["keywords"]):
            depth = d["name"]
            break

    return {
        "category": category,
        "sub_category": sub_category,
        "depth": depth,
    }


def classify_all(articles: list, root_dir: str) -> list:
    """批量分类，直接修改并返回文章列表"""
    categories = load_categories(root_dir)
    for art in articles:
        result = classify_article(art.get("title", ""), categories)
        art["category"] = result["category"]
        art["sub_category"] = result["sub_category"]
        art["depth"] = result["depth"]
    print(f"✓ 分类完成，共 {len(articles)} 篇", flush=True)
    return articles

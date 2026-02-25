"""全文提取模块 - 从 HTML 缓存提取完整正文并存储为 .txt"""

import json
import os
import sys

# 复用已有的解析器
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_scraper import scrape_wechat, scrape_feishu, scrape_tencent_cloud


def extract_fulltext(config: dict, root_dir: str):
    """从 HTML 缓存提取全文，保存到 data/articles_fulltext/"""
    enriched_path = os.path.join(root_dir, config["paths"]["enriched_json"])
    cache_dir = os.path.join(root_dir, config["paths"]["cache_dir"])
    fulltext_dir = os.path.join(root_dir, config["paths"].get("fulltext_dir", "data/articles_fulltext"))
    os.makedirs(fulltext_dir, exist_ok=True)

    with open(enriched_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    total = len(articles)
    extracted = 0
    skipped = 0
    failed = 0

    print(f"  共 {total} 篇文章，开始全文提取...", flush=True)

    for i, art in enumerate(articles):
        rid = art.get("record_id", "")
        title = art.get("title", "")[:40]
        url = art.get("url", "")
        txt_path = os.path.join(fulltext_dir, f"{rid}.txt")

        # 跳过已提取的
        if os.path.exists(txt_path) and os.path.getsize(txt_path) > 100:
            skipped += 1
            continue

        cache_path = os.path.join(cache_dir, f"{rid}.html")
        if not os.path.exists(cache_path):
            print(f"  [{i+1}/{total}] {title}... 无缓存", flush=True)
            failed += 1
            continue

        print(f"  [{i+1}/{total}] {title}...", end=" ", flush=True)

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                html = f.read()

            if "feishu.cn" in url:
                text, wc = scrape_feishu(html)
            elif "cloud.tencent.com" in url:
                text, wc = scrape_tencent_cloud(html)
            else:
                text, wc = scrape_wechat(html)

            if text and len(text) > 50:
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(f"# {art.get('title', '')}\n")
                    f.write(f"# URL: {url}\n")
                    f.write(f"# 日期: {art.get('date', '')}\n")
                    f.write(f"# 来源: {art.get('source', '')}\n")
                    f.write(f"# 分类: {art.get('category', '')} / {art.get('sub_category', '')}\n")
                    f.write(f"# 字数: {wc}\n\n")
                    f.write(text)
                extracted += 1
                print(f"ok {wc}字", flush=True)
            else:
                failed += 1
                print("empty", flush=True)
        except Exception as e:
            failed += 1
            print(f"error: {str(e)[:60]}", flush=True)

    print(f"\n  全文提取完成：提取 {extracted}，跳过 {skipped}，失败 {failed}", flush=True)
    print(f"  全文目录: {fulltext_dir}", flush=True)


if __name__ == "__main__":
    import yaml
    import io
    # 独立运行时处理 Windows 编码
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "config.yaml"), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    extract_fulltext(cfg, root)

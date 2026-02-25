"""OpenClaw 知识库 - 主入口"""

import argparse
import yaml
import os
import sys
import io

# Windows GBK 兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 项目根目录 = scripts/ 的上一级
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config():
    config_path = os.path.join(ROOT_DIR, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve(rel_path):
    """将配置中的相对路径转为绝对路径"""
    return os.path.join(ROOT_DIR, rel_path)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw 知识库工具")
    parser.add_argument("--fetch", action="store_true", help="从飞书拉取数据（增量）")
    parser.add_argument("--scrape", action="store_true", help="抓取文章内容")
    parser.add_argument("--classify", action="store_true", help="分类打标")
    parser.add_argument("--hotness", action="store_true", help="计算热度")
    parser.add_argument("--export", action="store_true", help="导出Excel")
    parser.add_argument("--web", action="store_true", help="生成Web数据")
    parser.add_argument("--fulltext", action="store_true", help="提取全文到本地")
    parser.add_argument("--all", action="store_true", help="执行全部流程")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    config = load_config()

    if args.all or args.fetch:
        print("\n[1/5] 拉取飞书数据...")
        from feishu_fetcher import fetch_incremental
        fetch_incremental(config, ROOT_DIR)

    if args.all or args.classify:
        print("\n[2/7] 分类打标...")
        import json
        from classifier import classify_all
        path = resolve(config["paths"]["enriched_json"])
        with open(path, "r", encoding="utf-8") as f:
            articles = json.load(f)
        classify_all(articles, ROOT_DIR)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

    if args.all or args.hotness:
        print("\n[3/7] 计算热度...")
        import json
        from hotness_calculator import calculate_all_hotness
        path = resolve(config["paths"]["enriched_json"])
        with open(path, "r", encoding="utf-8") as f:
            articles = json.load(f)
        calculate_all_hotness(articles, ROOT_DIR)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

    if args.all or args.scrape:
        print("\n[4/7] 抓取文章内容...")
        from article_scraper import scrape_all
        scrape_all(config, ROOT_DIR)

    if args.all or args.export:
        print("\n[5/7] 导出Excel...")
        from excel_exporter import export_excel
        export_excel(config, ROOT_DIR)

    if args.all or args.web:
        print("\n[6/7] 生成Web数据...")
        from excel_exporter import generate_web_data
        generate_web_data(config, ROOT_DIR)

    if args.all or args.fulltext:
        print("\n[7/7] 提取全文...")
        from fulltext_extractor import extract_fulltext
        extract_fulltext(config, ROOT_DIR)

    print("\n✓ 全部完成！")


if __name__ == "__main__":
    main()

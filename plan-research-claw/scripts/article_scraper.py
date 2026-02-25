"""文章内容抓取模块 - 微信/飞书/腾讯云文章正文提取"""

import json
import os
import re
import time
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def load_articles(enriched_path: str) -> list:
    with open(enriched_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_articles(articles: list, enriched_path: str):
    with open(enriched_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


def get_cache_path(cache_dir: str, record_id: str) -> str:
    return os.path.join(cache_dir, f"{record_id}.html")


def _jsdecode(s: str) -> str:
    """模拟微信 JsDecode 函数"""
    return (s.replace("\\x5c", "\\").replace("\\x0d", "\r")
             .replace("\\x22", '"').replace("\\x26", "&")
             .replace("\\x27", "'").replace("\\x3c", "<")
             .replace("\\x3e", ">").replace("\\x0a", "\n"))


def _fetch_html(url: str, cache_path: str) -> str:
    """获取HTML，优先读缓存"""
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    html = resp.text
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html


def scrape_wechat(html: str) -> tuple:
    """抓取微信文章正文，返回 (正文文本, 字数)"""
    soup = BeautifulSoup(html, "lxml")

    # 方式1：标准布局 div#js_content
    content_div = soup.find("div", id="js_content")
    if not content_div:
        content_div = soup.find("div", class_="rich_media_content")
    if content_div:
        text = content_div.get_text(separator="\n", strip=True)
        if text and len(text) > 100:
            return text, len(text)

    # 方式2：全屏布局 - 从 JS 变量 content_noencode 提取
    m = re.search(r"content_noencode:\s*JsDecode\('(.*?)'\)", html, re.S)
    if m:
        decoded = _jsdecode(m.group(1))
        # 去掉 HTML 实体和标签
        decoded = re.sub(r"&nbsp;", " ", decoded)
        decoded = re.sub(r"&amp;", "&", decoded)
        decoded = re.sub(r"<[^>]+>", "", decoded)
        text = decoded.strip()
        if text:
            return text, len(text)

    # 方式3：从 desc 字段提取摘要（兜底）
    m = re.search(r"desc:\s*JsDecode\('(.*?)'\)", html, re.S)
    if m:
        text = _jsdecode(m.group(1)).strip()
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"&amp;", "&", text)
        if len(text) > 50:
            return text, len(text)

    return "", 0


def scrape_feishu(html: str) -> tuple:
    """抓取飞书文档正文，从 window.DATA 中提取"""
    soup = BeautifulSoup(html, "lxml")
    all_text_parts = []

    # 飞书 UI 噪音关键词，用于过滤
    noise_keywords = [
        "協作者超過", "协作者超过", "共同編集者", "允許擁有者",
        "允许所有者", "高频场景所需", "快捷配置使用", "借助多种连接器",
        "多彩なプラグイン", "プラグインで", "カスタマイズ",
        "防止编译混淆", "总结会议里的关键决策",
    ]

    for script in soup.find_all("script"):
        txt = script.string or ""
        if len(txt) < 500:
            continue
        parts = re.findall(r'"([^"]*[\u4e00-\u9fff][^"]{20,})"', txt)
        for p in parts:
            # 过滤飞书 UI 文本
            if any(nk in p for nk in noise_keywords):
                continue
            all_text_parts.append(p)

    if all_text_parts:
        text = "\n".join(all_text_parts)
        return text, len(text)
    return "", 0


def scrape_tencent_cloud(html: str) -> tuple:
    """抓取腾讯云开发者文章"""
    soup = BeautifulSoup(html, "lxml")
    content = soup.select_one("div.rno-markdown") or soup.select_one("div.mod-content")
    if content:
        text = content.get_text(separator="\n", strip=True)
        return text, len(text)
    return "", 0


def scrape_one(article: dict, config: dict, root_dir: str = "") -> dict:
    """抓取单篇文章内容，根据URL自动选择解析器"""
    cache_dir = os.path.join(root_dir, config["paths"]["cache_dir"])
    os.makedirs(cache_dir, exist_ok=True)
    max_chars = config["scraper"]["max_summary_chars"]

    url = article.get("url", "")
    rid = article.get("record_id", "")
    cache_path = get_cache_path(cache_dir, rid)

    if not url:
        article["scrape_status"] = "no_url"
        return article

    try:
        html = _fetch_html(url, cache_path)

        # 根据URL选择解析器
        if "feishu.cn" in url:
            text, wc = scrape_feishu(html)
        elif "cloud.tencent.com" in url:
            text, wc = scrape_tencent_cloud(html)
        else:
            text, wc = scrape_wechat(html)

        if text:
            article["summary"] = text[:max_chars]
            article["word_count"] = wc
            article["scrape_status"] = "ok"
        else:
            article["scrape_status"] = "empty"
    except Exception as e:
        article["scrape_status"] = f"error: {str(e)[:80]}"

    return article


def scrape_all(config: dict, root_dir: str):
    """批量抓取所有文章，支持断点续传"""
    enriched_path = os.path.join(root_dir, config["paths"]["enriched_json"])
    articles = load_articles(enriched_path)
    delay = config["scraper"]["delay"]
    save_interval = config["scraper"]["save_interval"]

    total = len(articles)
    skipped = 0
    scraped = 0
    failed = 0

    print(f"  共 {total} 篇文章，开始抓取...", flush=True)

    for i, art in enumerate(articles):
        if art.get("scrape_status") == "ok":
            skipped += 1
            continue

        print(f"  [{i+1}/{total}] {art.get('title', '')[:40]}...", end=" ", flush=True)
        scrape_one(art, config, root_dir)

        if art["scrape_status"] == "ok":
            scraped += 1
            print(f"✓ {art['word_count']}字", flush=True)
        else:
            failed += 1
            print(f"✗ {art['scrape_status']}", flush=True)

        # 定期保存（断点续传）
        if (scraped + failed) % save_interval == 0:
            save_articles(articles, enriched_path)

        time.sleep(delay)

    save_articles(articles, enriched_path)
    print(f"✓ 抓取完成：成功 {scraped}，跳过 {skipped}，失败 {failed}", flush=True)

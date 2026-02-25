# OpenClaw 知识库项目

## 项目概述

OpenClaw（原 Clawdbot）中文知识库，聚合 142 篇相关文章，提供数据处理管线和网页阅读器。

## 目录结构

```
plan-research-claw/
├── config.yaml              # 项目配置（路径、飞书凭证引用、抓取参数）
├── scripts/                 # Python 数据处理脚本
│   ├── main.py              # 主入口 (--fetch/--scrape/--classify/--export/--web/--all)
│   ├── feishu_fetcher.py    # 飞书多维表格数据拉取（增量合并）
│   ├── article_scraper.py   # 文章正文抓取（微信/飞书/腾讯云）
│   ├── classifier.py        # 分类打标（关键词规则匹配）
│   └── excel_exporter.py    # Excel 导出 + Web 数据生成
├── data/
│   ├── feishu_raw_data.json # 飞书原始导出数据（142条）
│   ├── articles_enriched.json # 完整数据（含摘要、分类、抓取状态）
│   └── articles_cache/      # HTML 缓存（142个文件）
├── output/
│   └── openclaw_kb.xlsx     # Excel 输出
├── web/                     # 简易阅读器（已完成）
│   ├── index.html           # 单文件网页阅读器
│   └── articles_data.js     # 由脚本生成的前端数据
├── site/                    # 知识库网站（已完成）
│   ├── index.html           # 首页
│   ├── nav.json             # 导航配置
│   ├── assets/
│   │   ├── style.css        # 全局样式（响应式、暗色模式）
│   │   ├── i18n.js          # 国际化配置（中/英）
│   │   └── nav.js           # 导航渲染与主题切换
│   ├── articles/            # 精选文章页
│   ├── product/             # 产品认知
│   ├── deploy/              # 安装部署
│   ├── config/              # 配置与技巧
│   ├── integration/         # 生态集成
│   ├── practice/            # 应用实战
│   └── trends/              # 趋势展望
└── docs/
    └── project-notes.md     # 本文件
```

## 数据处理管线

### 使用方式

```bash
# 安装依赖
pip install requests beautifulsoup4 lxml openpyxl pyyaml

# 全流程执行
python scripts/main.py --all

# 单步执行
python scripts/main.py --fetch      # 从本地 JSON 增量合并数据
python scripts/main.py --classify   # 分类打标
python scripts/main.py --scrape     # 抓取文章正文（约3-4分钟，支持断点续传）
python scripts/main.py --export     # 导出 Excel
python scripts/main.py --web        # 生成 web/articles_data.js
```

### 分类体系

一级分类（6个）：产品认知、安装部署、配置与技巧、生态集成、应用实战、趋势展望

安装部署二级分类（8个）：macOS本地、Windows本地、Linux本地、Docker容器、国内云平台、国际云平台、NAS/家庭服务器、手机端远程

内容深度（4个）：入门科普、教程实操、深度分析、行业观察

### 文章抓取

支持三种来源的正文提取：
- 微信公众号（标准布局 `div#js_content` + 全屏布局 `JsDecode` 解码）
- 飞书文档（从 `window.DATA` SSR 数据中提取中文段落）
- 腾讯云开发者社区（`div.rno-markdown`）

142 篇文章全部抓取成功（scrape_status=ok）。

### 数据来源

飞书多维表格，通过隔壁项目 `D:\workspace\dev-cc\1_clawbots\feishuMSG-xls` 的飞书客户端进行认证和 API 调用。

## 已完成工作

1. 从飞书多维表格导出 142 篇 OpenClaw 相关文章
2. 基于标题关键词的自动分类打标
3. 全量文章正文抓取（含微信全屏布局、飞书文档、腾讯云的特殊解析）
4. Excel 格式化导出（蓝色表头、交替行色、超链接）
5. 简易网页阅读器（筛选/搜索/排序/分页/暗色模式）
6. 知识库网站（site/ 目录）
   - 参考 VitePress 蓝色主题风格
   - 6 个一级分类页面 + 子页面框架
   - 精选文章聚合页（筛选/搜索/排序/分页）
   - 国际化支持（中文/英文切换，下拉菜单）
   - 响应式设计（桌面端/移动端适配）
   - 暗色模式支持
   - 移动端汉堡菜单导航

## 网站功能

### 国际化 (i18n)
- 支持中文/英文切换
- 语言偏好保存到 localStorage
- 下拉菜单切换，桌面端显示当前语言文字，移动端仅显示图标

### 响应式设计
- 桌面端：水平导航栏 + 右侧工具栏（语言切换、主题切换）
- 移动端：汉堡菜单下拉导航 + 精简工具栏
- 断点：768px

### 页面结构
- 首页：欢迎信息 + 6 个分类卡片入口 + 精选文章入口
- 分类页：页面标题 + 子分类卡片 + 精选文章入口
- 精选文章页：统计栏 + 筛选栏 + 排序 + 文章卡片列表 + 分页

## 待办

- [ ] 各子页面内容填充
- [ ] SEO 优化

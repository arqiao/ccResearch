"""AI辅助重新打标签 v2 - 为所有分类添加二级分类"""
import json
import sys

# 完整的分类映射表（含二级分类）
# 格式: record_id: (category, sub_category, depth)
RETAG_MAP = {
    # === 产品认知 (32篇) ===
    # 架构原理
    "recvaQc716eBbK": ("产品认知", "架构原理", "深度分析"),  # Pi框架
    "recvaJLbAl5oe9": ("产品认知", "架构原理", "深度分析"),  # Pi-OpenClaw-Palantir演化
    "recvavuBj7sCFS": ("产品认知", "架构原理", "深度分析"),  # 极简范式说明书
    "recvaJKpDA0hhq": ("产品认知", "架构原理", "深度分析"),  # AutoGPT狂欢反思
    "recvaeMzvyje4k": ("产品认知", "架构原理", "深度分析"),  # Pi胜出Cursor
    "recvatcK90DLeC": ("产品认知", "架构原理", "深度分析"),  # 用户深度研究报告
    "recvaeMzvyGhMB": ("产品认知", "架构原理", "深度分析"),  # 工作原理与生态
    "recv9QazyrxIiA": ("产品认知", "架构原理", "深度分析"),  # 范式软肋机会
    "recv8xZVmPcnmG": ("产品认知", "架构原理", "深度分析"),  # 范式演进架构解剖
    "recv9q8x3u2wAd": ("产品认知", "架构原理", "深度分析"),  # 自动化记忆不可能三角
    "recval42YtSNvD": ("产品认知", "架构原理", "深度分析"),  # 网关创新
    "recva4HZIHnEoi": ("产品认知", "架构原理", "深度分析"),  # 活着的本质
    # 产品体验
    "recvaVhRl3lB5B": ("产品认知", "产品体验", "入门科普"),  # 用法离谱
    "recvatcK90kOj1": ("产品认知", "产品体验", "教程实操"),  # 70篇测评使用指引
    "recvaxG2S8UMLZ": ("产品认知", "产品体验", "深度分析"),  # 搭建税
    "recva8GYHr5ZUZ": ("产品认知", "产品体验", "教程实操"),  # 入门站7天教程
    "recvati47IsxOP": ("产品认知", "产品体验", "深度分析"),  # LEONIS泼冷水
    "recv9BwpHcpt1y": ("产品认知", "产品体验", "入门科普"),  # 多花4000元
    "recv9oXdOVoaXH": ("产品认知", "产品体验", "入门科普"),  # 普通人怎么用
    "recv9w1CPLYIoY": ("产品认知", "产品体验", "入门科普"),  # Mac mini卖爆
    "recvaVhRl3XWUk": ("产品认知", "产品体验", "入门科普"),  # 一文看懂
    # 避坑指南
    "recvavuBj7VLK5": ("产品认知", "避坑指南", "入门科普"),  # 认清慎用
    "recva4HZIHt5XU": ("产品认知", "避坑指南", "入门科普"),  # 5分钟烧30美金
    "recvakr25p7rNC": ("产品认知", "避坑指南", "深度分析"),  # 隐形越狱
    "recv9TJ1enaicd": ("产品认知", "避坑指南", "入门科普"),  # 50万假Clawdbot
    "recvaefQUFfp91": ("产品认知", "避坑指南", "深度分析"),  # Vibecoding搞错了
    # 发展历程
    "recv9MEc2KCzL6": ("产品认知", "发展历程", "入门科普"),  # Peter失控更名
    "recv9MEcDR6uVp": ("产品认知", "发展历程", "入门科普"),  # Peter失控更名(重复)
    "recv9w3rBHvnkr": ("产品认知", "发展历程", "入门科普"),  # 改名Moltbot
    "recv9TK95W0rC4": ("产品认知", "发展历程", "入门科普"),  # 改写开源规则
    "recvaa643ihVN2": ("产品认知", "发展历程", "入门科普"),  # 3000台免费领
    "recvaJLbAlAej1": ("产品认知", "发展历程", "入门科普"),  # 换成memU Bot

    # === 安装部署 (39篇) - 已有二级分类，保持不变 ===
    "recvaVhRl3AOVc": ("安装部署", "国内云平台", "教程实操"),
    "recvaVhRl322oH": ("安装部署", "Windows本地", "教程实操"),
    "recvaQc716qlqi": ("安装部署", "国内云平台", "教程实操"),
    "recvaVhRl3Jnzi": ("安装部署", "国内云平台", "教程实操"),
    "recvakr25pde6o": ("安装部署", "Windows本地", "教程实操"),
    "recval42YtFsL7": ("安装部署", "NAS/家庭服务器", "教程实操"),
    "recvati47IZy2U": ("安装部署", "通用部署", "教程实操"),
    "recvaeeMmccPm0": ("安装部署", "Docker容器", "教程实操"),
    "recva4HZIHoHNT": ("安装部署", "国内云平台", "教程实操"),
    "recva4HZIHOofD": ("安装部署", "国内云平台", "教程实操"),
    "recvapVmpH4OTj": ("安装部署", "手机端远程", "教程实操"),
    "recv9TJ1ensLRq": ("安装部署", "通用部署", "入门科普"),
    "recval4i3gXPGi": ("安装部署", "国内云平台", "教程实操"),
    "recv9YQanuMoaC": ("安装部署", "macOS本地", "教程实操"),
    "recva2ljoadQF6": ("安装部署", "国内云平台", "入门科普"),
    "recvatcK90Jy0J": ("安装部署", "NAS/家庭服务器", "教程实操"),
    "recv9QazyrJ7mb": ("安装部署", "国内云平台", "教程实操"),
    "recva8GYHrktfH": ("安装部署", "国内云平台", "教程实操"),
    "recvaa6Cf5uBB2": ("安装部署", "国内云平台", "教程实操"),
    "recvati47IARNT": ("安装部署", "macOS本地", "教程实操"),
    "recv9ErGedaYXx": ("安装部署", "通用部署", "教程实操"),
    "recv9NEgNrgbiw": ("安装部署", "通用部署", "教程实操"),
    "recv9NEhE6xgNJ": ("安装部署", "通用部署", "教程实操"),
    "recvaltt5KLGKS": ("安装部署", "手机端远程", "教程实操"),
    "recv9BwpHctnTE": ("安装部署", "国内云平台", "教程实操"),
    "recv9FmrIxAuhW": ("安装部署", "国内云平台", "入门科普"),
    "recvaeMzvynbOd": ("安装部署", "通用部署", "教程实操"),
    "recv9tbvaWublI": ("安装部署", "通用部署", "教程实操"),
    "recv9w1Qac6qvr": ("安装部署", "国内云平台", "入门科普"),
    "recvapTWRyArDs": ("安装部署", "macOS本地", "教程实操"),
    "recv9tbdAM8neT": ("安装部署", "macOS本地", "入门科普"),
    "recv9vY5hTlF3y": ("安装部署", "通用部署", "教程实操"),
    "recv9w4lBvgztY": ("安装部署", "通用部署", "教程实操"),
    "recv9w4uR9imB4": ("安装部署", "通用部署", "教程实操"),
    "recv9w4RJOLQxq": ("安装部署", "通用部署", "教程实操"),
    "recv9wyFWL6sXG": ("安装部署", "macOS本地", "入门科普"),
    "recv9i23UQd2BZ": ("安装部署", "macOS本地", "教程实操"),
    "recv9q9PHjNvhN": ("安装部署", "通用部署", "教程实操"),
    "recv9w3ZjkFjh5": ("安装部署", "国内云平台", "教程实操"),

    # === 配置与技巧 (15篇) ===
    # Skills配置
    "recvaVhRl375UB": ("配置与技巧", "Skills配置", "教程实操"),  # 必装7个Skill
    "recvapUtih5FIo": ("配置与技巧", "Skills配置", "入门科普"),  # 700+ Skills军火库(移到配置)
    "recvatcK90kEaC": ("配置与技巧", "Skills配置", "教程实操"),  # 6种神级技巧
    "recv9QazyredpR": ("配置与技巧", "Skills配置", "教程实操"),  # 80+技能私人助手
    # 模型切换
    "recvaJKpDASbag": ("配置与技巧", "模型切换", "教程实操"),  # 模型配置切换
    "recv9w3rBHH6y5": ("配置与技巧", "模型切换", "教程实操"),  # 第三方Claude API
    "recv9THBEbq2VO": ("配置与技巧", "模型切换", "教程实操"),  # 第三方Claude API(重复)
    # 记忆管理
    "recvaeMzvyCEFd": ("配置与技巧", "记忆管理", "教程实操"),  # 工作空间同步
    "recva2kGfdFpEt": ("配置与技巧", "记忆管理", "教程实操"),  # MD文档记忆系统
    "recval42Ytueyo": ("配置与技巧", "记忆管理", "入门科普"),  # 内容同步记忆agent
    # 性能优化
    "recvaQc716M47Z": ("配置与技巧", "性能优化", "教程实操"),  # 云上5种打开方式
    "recvaVhRl35dVh": ("配置与技巧", "性能优化", "教程实操"),  # 砍掉60% Token
    "recval42YtJtze": ("配置与技巧", "性能优化", "教程实操"),  # 自动化+记忆+多插件
    "recv9LNNH2ST4E": ("配置与技巧", "性能优化", "入门科普"),  # 升级避坑指南
    "recv9QazyrFIoj": ("配置与技巧", "性能优化", "教程实操"),  # 后台持续运行
    "recv9QazyrHcJg": ("配置与技巧", "性能优化", "教程实操"),  # 自动化工具飞书推送

    # === 生态集成 (16篇) ===
    # 飞书/钉钉
    "recvaJLbAl58uc": ("生态集成", "飞书/钉钉", "教程实操"),  # 火山方舟+飞书
    "recvati47IrCE4": ("生态集成", "飞书/钉钉", "教程实操"),  # 飞书钉钉企微全攻略
    "recvati47IaERW": ("生态集成", "飞书/钉钉", "入门科普"),  # 飞书限额警告
    "recv9w4KMRcdgK": ("生态集成", "飞书/钉钉", "教程实操"),  # 接入飞书
    "recva4FFcD19ds": ("生态集成", "飞书/钉钉", "教程实操"),  # 接入钉钉
    # 微信/QQ
    "recvapVp1mSiHB": ("生态集成", "微信/QQ", "教程实操"),  # 微信合规方案
    "recv9TJ1en93W8": ("生态集成", "微信/QQ", "教程实操"),  # QQ玩转
    "recv9THnIWV9Ca": ("生态集成", "微信/QQ", "教程实操"),  # 微信使用
    "recv9oXdOVeLHW": ("生态集成", "微信/QQ", "教程实操"),  # 微信曲线救国
    "recvati47ITbjs": ("生态集成", "微信/QQ", "入门科普"),  # 微信钉钉全能终端
    # 国际平台
    "recvati47IzDfs": ("生态集成", "国际平台", "教程实操"),  # 微信WhatsApp Telegram
    # 开发工具
    "recvaJKpDAiEEI": ("生态集成", "开发工具", "入门科普"),  # AionUI多Agent
    "recvaxGmGgRA54": ("生态集成", "开发工具", "入门科普"),  # 两个开源神器
    "recvapUatVouXV": ("生态集成", "开发工具", "入门科普"),  # 4个GitHub项目
    "recv9NFAs7ybfQ": ("生态集成", "开发工具", "入门科普"),  # Agent Studio

    # === 应用实战 (11篇) ===
    # 办公自动化
    "recvaVhRl3fV9o": ("应用实战", "办公自动化", "教程实操"),  # 10个人真实场景
    "recva2kGfdh0JK": ("应用实战", "办公自动化", "教程实操"),  # 20个内容营销玩法
    "recval42YtaRSt": ("应用实战", "办公自动化", "教程实操"),  # 飞书分析Moltbook
    # 数据分析
    "recv9ErGedgFuX": ("应用实战", "数据分析", "教程实操"),  # 7×24监听股票
    "recv9BwpHcj0BM": ("应用实战", "数据分析", "深度分析"),  # 飞书股票分析
    # 开发编程
    "recv9QazyrWXWw": ("应用实战", "开发编程", "入门科普"),  # 氛围编程付费产品
    "recvavuAg2Rxg9": ("应用实战", "开发编程", "深度分析"),  # 碎片时间深度学习
    "recv9w1Qac6zIH": ("应用实战", "开发编程", "入门科普"),  # 火山方舟模型服务
    # 创意玩法
    "recvaQc716a7lr": ("应用实战", "创意玩法", "入门科普"),  # AI女友Clawra
    "recva1RDWyJshe": ("应用实战", "创意玩法", "教程实操"),  # 假维斯8个场景
    "recvati47IYtK9": ("应用实战", "创意玩法", "教程实操"),  # 2种变现方式

    # === 趋势展望 (29篇) ===
    # 创业投资
    "recvaVhRl36pi4": ("趋势展望", "创业投资", "行业观察"),  # AI创业逻辑被推翻
    "recvaJLbAlFFyh": ("趋势展望", "创业投资", "行业观察"),  # 王慧文抢人
    "recvapVp1mDkR3": ("趋势展望", "创业投资", "行业观察"),  # 王慧文英雄帖
    "recvaVhRl3PbuB": ("趋势展望", "创业投资", "行业观察"),  # 创业信号第二弹
    "recvati47IuWHH": ("趋势展望", "创业投资", "行业观察"),  # 创业信号
    "recval42YtAinY": ("趋势展望", "创业投资", "行业观察"),  # 130位创业者讨论
    "recvamzG28qNAQ": ("趋势展望", "创业投资", "行业观察"),  # 叶天奇Agent电脑
    "recv9TJ1enj1ho": ("趋势展望", "创业投资", "入门科普"),  # 95后硬件版
    # 行业动态
    "recvaVhRl34LLZ": ("趋势展望", "行业动态", "入门科普"),  # ClawCon龙虾孵化场
    "recvamkGz0lIcc": ("趋势展望", "行业动态", "行业观察"),  # 算力扩到1900张卡
    "recvaa6Cf5WS8G": ("趋势展望", "行业动态", "行业观察"),  # 雇佣人类
    "recvaefQUFvS6f": ("趋势展望", "行业动态", "行业观察"),  # 不招人类员工
    "recval57kcgQaW": ("趋势展望", "行业动态", "行业观察"),  # 赚300万
    "recv9QazyrAB9l": ("趋势展望", "行业动态", "入门科普"),  # 150万挤爆论坛
    "recv9WB3yOAqJ8": ("趋势展望", "行业动态", "入门科普"),  # 14万涌进社交APP
    "recv9QazyrUi8U": ("趋势展望", "行业动态", "入门科普"),  # 14万(重复)
    "recv9WB3yOl2kP": ("趋势展望", "行业动态", "入门科普"),  # 14万(重复)
    "recv9KYSnSVFFO": ("趋势展望", "行业动态", "入门科普"),  # QoderWork开箱即用
    "recv9BwpHcNamO": ("趋势展望", "行业动态", "入门科普"),  # 中国版来了
    # 技术演进
    "recvaQc716TFrR": ("趋势展望", "技术演进", "深度分析"),  # 端云协同
    "recvamjdqTm6jV": ("趋势展望", "技术演进", "深度分析"),  # 10x Token消耗
    "recvaa63bpEXgW": ("趋势展望", "技术演进", "深度分析"),  # Agent规模化落地
    "recva1RrULMyq8": ("趋势展望", "技术演进", "深度分析"),  # 中国模型全球时刻
    "recv9HiNlEjdAj": ("趋势展望", "技术演进", "深度分析"),  # 提示词是新interface
    # 未来畅想
    "recvaJKpDAgIZo": ("趋势展望", "未来畅想", "行业观察"),  # 硅基文明
    "recvaJKpDAUYcv": ("趋势展望", "未来畅想", "行业观察"),  # 无人公司
    "recv9YQanuRwzv": ("趋势展望", "未来畅想", "入门科普"),  # ClawTasks打工赚钱
    "recv9YQanuAA27": ("趋势展望", "未来畅想", "入门科普"),  # 64个集体永生
    "recv9LNNH2sZhi": ("趋势展望", "未来畅想", "入门科普"),  # 天网已来
}


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    json_path = "D:/workspace/cc-work/plan-research-claw/data/articles_enriched.json"

    with open(json_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    updated = 0
    for art in articles:
        rid = art.get('record_id', '')
        if rid in RETAG_MAP:
            cat, sub, depth = RETAG_MAP[rid]
            old = (art.get('category'), art.get('sub_category'), art.get('depth'))
            if old != (cat, sub, depth):
                art['category'] = cat
                art['sub_category'] = sub
                art['depth'] = depth
                updated += 1

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✓ 完成！共更新 {updated} 篇文章的分类")

    # 统计新分类分布
    print("\n=== 分类分布统计 ===")
    cats = {}
    subs = {}
    for art in articles:
        c = art.get('category', '')
        s = art.get('sub_category', '')
        cats[c] = cats.get(c, 0) + 1
        key = f"{c}/{s}" if s else f"{c}/未分类"
        subs[key] = subs.get(key, 0) + 1

    for c in sorted(cats.keys()):
        print(f"\n{c}: {cats[c]}篇")
        for key in sorted(subs.keys()):
            if key.startswith(c + "/"):
                sub_name = key.split("/")[1]
                print(f"  └─ {sub_name}: {subs[key]}")


if __name__ == "__main__":
    main()

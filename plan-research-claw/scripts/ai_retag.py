"""AI辅助重新打标签 - 基于全文内容理解的分类修正"""
import json
import sys

# AI审核后的分类修正映射表
# 格式: record_id: (category, sub_category, depth)
RETAG_MAP = {
    # 第1-30篇
    "recvaVhRl3AOVc": ("安装部署", "国内云平台", "教程实操"),
    "recvaVhRl3fV9o": ("应用实战", "", "教程实操"),
    "recvaVhRl34LLZ": ("趋势展望", "", "入门科普"),
    "recvaVhRl36pi4": ("趋势展望", "", "行业观察"),
    "recvaVhRl322oH": ("安装部署", "Windows本地", "教程实操"),
    "recvaQc716a7lr": ("应用实战", "", "入门科普"),
    "recvaQc716TFrR": ("趋势展望", "", "深度分析"),
    "recvaQc716eBbK": ("产品认知", "", "深度分析"),
    "recvaQc716M47Z": ("配置与技巧", "", "教程实操"),
    "recvaQc716qlqi": ("安装部署", "国内云平台", "教程实操"),
    "recvaVhRl3Jnzi": ("安装部署", "国内云平台", "教程实操"),
    "recvaVhRl3lB5B": ("产品认知", "", "入门科普"),
    "recvaJLbAlFFyh": ("趋势展望", "", "行业观察"),
    "recvaJLbAl5oe9": ("产品认知", "", "深度分析"),
    "recvaJLbAl58uc": ("生态集成", "", "教程实操"),
    "recvavuBj7sCFS": ("产品认知", "", "深度分析"),
    "recvaJKpDAgIZo": ("趋势展望", "", "行业观察"),
    "recvaJKpDAUYcv": ("趋势展望", "", "行业观察"),
    "recvaJKpDA0hhq": ("产品认知", "", "深度分析"),
    "recvaJKpDAiEEI": ("生态集成", "", "入门科普"),
    "recvaVhRl375UB": ("配置与技巧", "", "教程实操"),
    "recvapVp1mDkR3": ("趋势展望", "", "行业观察"),
    "recvati47IsxOP": ("产品认知", "", "深度分析"),
    "recvavuBj7VLK5": ("产品认知", "", "入门科普"),
    "recvaVhRl3PbuB": ("趋势展望", "", "行业观察"),
    "recvaeMzvyje4k": ("产品认知", "", "深度分析"),
    "recvamkGz0lIcc": ("趋势展望", "", "行业观察"),
    "recvatcK90DLeC": ("产品认知", "", "深度分析"),
    "recvatcK90kOj1": ("产品认知", "", "教程实操"),
    "recvati47IzDfs": ("生态集成", "", "教程实操"),
    # 第31-60篇
    "recvaxG2S8UMLZ": ("产品认知", "", "深度分析"),
    "recvaxGmGgRA54": ("生态集成", "", "入门科普"),
    "recvaeMzvyCEFd": ("配置与技巧", "", "教程实操"),
    "recvaeMzvyGhMB": ("产品认知", "", "深度分析"),
    "recvakr25pde6o": ("安装部署", "Windows本地", "教程实操"),
    "recval42YtFsL7": ("安装部署", "NAS/家庭服务器", "教程实操"),
    "recval42YtAinY": ("趋势展望", "", "行业观察"),
    "recval42YtaRSt": ("应用实战", "", "教程实操"),
    "recvamjdqTm6jV": ("趋势展望", "", "深度分析"),
    "recvapVp1mSiHB": ("生态集成", "", "教程实操"),
    "recvati47IuWHH": ("趋势展望", "", "行业观察"),
    "recvati47IZy2U": ("安装部署", "通用部署", "教程实操"),
    "recvaVhRl35dVh": ("配置与技巧", "", "教程实操"),
    "recva8GYHr5ZUZ": ("产品认知", "", "教程实操"),
    "recvaa6Cf5WS8G": ("趋势展望", "", "行业观察"),
    "recvaeeMmccPm0": ("安装部署", "Docker容器", "教程实操"),
    "recvaefQUFvS6f": ("趋势展望", "", "行业观察"),
    "recvaefQUFfp91": ("产品认知", "", "深度分析"),
    "recvakr25p7rNC": ("产品认知", "", "深度分析"),
    "recval57kcgQaW": ("趋势展望", "", "行业观察"),
    "recvamzG28qNAQ": ("趋势展望", "", "行业观察"),
    "recvapUatVouXV": ("生态集成", "", "入门科普"),
    "recvatcK90kEaC": ("配置与技巧", "", "教程实操"),
    "recvati47IrCE4": ("生态集成", "", "教程实操"),
    "recvaJLbAlAej1": ("产品认知", "", "入门科普"),
    "recva4HZIHnEoi": ("产品认知", "", "深度分析"),
    "recva4HZIHt5XU": ("产品认知", "", "入门科普"),
    "recva4HZIHoHNT": ("安装部署", "国内云平台", "教程实操"),
    "recva4HZIHOofD": ("安装部署", "国内云平台", "教程实操"),
    "recvaa63bpEXgW": ("趋势展望", "", "深度分析"),
    # 第61-90篇
    "recvaa643ihVN2": ("产品认知", "", "入门科普"),
    "recval42YtJtze": ("配置与技巧", "", "教程实操"),
    "recvapVmpH4OTj": ("安装部署", "手机端远程", "教程实操"),
    "recvati47IYtK9": ("应用实战", "", "教程实操"),
    "recvavuAg2Rxg9": ("应用实战", "", "深度分析"),
    "recv9TJ1en93W8": ("生态集成", "", "教程实操"),
    "recv9TJ1enaicd": ("产品认知", "", "入门科普"),
    "recv9TJ1ensLRq": ("安装部署", "通用部署", "入门科普"),
    "recva2kGfdFpEt": ("配置与技巧", "", "教程实操"),
    "recva2kGfdh0JK": ("应用实战", "", "教程实操"),
    "recval4i3gXPGi": ("安装部署", "国内云平台", "教程实操"),
    "recvapUtih5FIo": ("生态集成", "", "入门科普"),
    "recvati47IaERW": ("生态集成", "", "入门科普"),
    "recv9QazyrAB9l": ("趋势展望", "", "入门科普"),
    "recv9TJ1enj1ho": ("趋势展望", "", "入门科普"),
    "recv9WB3yOAqJ8": ("趋势展望", "", "入门科普"),
    "recv9YQanuRwzv": ("趋势展望", "", "入门科普"),
    "recv9YQanuMoaC": ("安装部署", "macOS本地", "教程实操"),
    "recv9YQanuAA27": ("趋势展望", "", "入门科普"),
    "recva1RrULMyq8": ("趋势展望", "", "深度分析"),
    "recva1RDWyJshe": ("应用实战", "", "教程实操"),
    "recva2ljoadQF6": ("安装部署", "国内云平台", "入门科普"),
    "recvatcK90Jy0J": ("安装部署", "NAS/家庭服务器", "教程实操"),
    "recvati47ITbjs": ("生态集成", "", "入门科普"),
    "recvaJKpDASbag": ("配置与技巧", "", "教程实操"),
    "recv9LNNH2ST4E": ("配置与技巧", "", "入门科普"),
    "recv9LNNH2sZhi": ("趋势展望", "", "入门科普"),
    "recv9QazyrFIoj": ("配置与技巧", "", "教程实操"),
    "recv9QazyrxIiA": ("产品认知", "", "深度分析"),
    "recv9QazyrWXWw": ("应用实战", "", "入门科普"),
    # 第91-120篇
    "recv9QazyrHcJg": ("配置与技巧", "", "教程实操"),
    "recv9QazyredpR": ("配置与技巧", "", "教程实操"),
    "recv9QazyrJ7mb": ("安装部署", "国内云平台", "教程实操"),
    "recv9QazyrUi8U": ("趋势展望", "", "入门科普"),
    "recv9TK95W0rC4": ("产品认知", "", "入门科普"),
    "recv9WB3yOl2kP": ("趋势展望", "", "入门科普"),
    "recva8GYHrktfH": ("安装部署", "国内云平台", "教程实操"),
    "recvaa6Cf5uBB2": ("安装部署", "国内云平台", "教程实操"),
    "recval42Ytueyo": ("配置与技巧", "", "入门科普"),
    "recvati47IARNT": ("安装部署", "macOS本地", "教程实操"),
    "recv9ErGedaYXx": ("安装部署", "通用部署", "教程实操"),
    "recv9ErGedgFuX": ("应用实战", "", "教程实操"),
    "recv9KYSnSVFFO": ("趋势展望", "", "入门科普"),
    "recv9MEc2KCzL6": ("产品认知", "", "入门科普"),
    "recv9MEcDR6uVp": ("产品认知", "", "入门科普"),
    "recv9NEgNrgbiw": ("安装部署", "通用部署", "教程实操"),
    "recv9NEhE6xgNJ": ("安装部署", "通用部署", "教程实操"),
    "recv9NFAs7ybfQ": ("生态集成", "", "入门科普"),
    "recv9THnIWV9Ca": ("生态集成", "", "教程实操"),
    "recvaltt5KLGKS": ("安装部署", "手机端远程", "教程实操"),
    # 第121-142篇
    "recv9BwpHcpt1y": ("产品认知", "", "入门科普"),
    "recv9BwpHcj0BM": ("应用实战", "", "深度分析"),
    "recv9BwpHctnTE": ("安装部署", "国内云平台", "教程实操"),
    "recv9BwpHcNamO": ("趋势展望", "", "入门科普"),
    "recv9FmrIxAuhW": ("安装部署", "国内云平台", "入门科普"),
    "recv9HiNlEjdAj": ("趋势展望", "", "深度分析"),
    "recva4FFcD19ds": ("生态集成", "", "教程实操"),
    "recvaeMzvynbOd": ("安装部署", "通用部署", "教程实操"),
    "recv9tbvaWublI": ("安装部署", "通用部署", "教程实操"),
    "recv9w1Qac6zIH": ("应用实战", "", "入门科普"),
    "recv9w1Qac6qvr": ("安装部署", "国内云平台", "入门科普"),
    "recv9w3rBHvnkr": ("产品认知", "", "入门科普"),
    "recvapTWRyArDs": ("安装部署", "macOS本地", "教程实操"),
    "recv9oXdOVeLHW": ("生态集成", "", "教程实操"),
    "recv9oXdOVoaXH": ("产品认知", "", "入门科普"),
    "recv9tbdAM8neT": ("安装部署", "macOS本地", "入门科普"),
    "recv9vY5hTlF3y": ("安装部署", "通用部署", "教程实操"),
    "recv9w1CPLYIoY": ("产品认知", "", "入门科普"),
    "recv9w4lBvgztY": ("安装部署", "通用部署", "教程实操"),
    "recv9w4uR9imB4": ("安装部署", "通用部署", "教程实操"),
    "recv9w4KMRcdgK": ("生态集成", "", "教程实操"),
    "recv9w4RJOLQxq": ("安装部署", "通用部署", "教程实操"),
    "recv9wyFWL6sXG": ("安装部署", "macOS本地", "入门科普"),
    "recv8xZVmPcnmG": ("产品认知", "", "深度分析"),
    "recv9i23UQd2BZ": ("安装部署", "macOS本地", "教程实操"),
    "recv9q8x3u2wAd": ("产品认知", "", "深度分析"),
    "recv9q9PHjNvhN": ("安装部署", "通用部署", "教程实操"),
    "recv9w3rBHH6y5": ("配置与技巧", "", "教程实操"),
    "recv9w3ZjkFjh5": ("安装部署", "国内云平台", "教程实操"),
    "recv9THBEbq2VO": ("配置与技巧", "", "教程实操"),
    "recval42YtSNvD": ("产品认知", "", "深度分析"),
    "recvaVhRl3XWUk": ("产品认知", "", "入门科普"),
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
                print(f"更新: {art['title'][:30]}... → {cat}/{sub}/{depth}")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 完成！共更新 {updated} 篇文章的分类")

    # 统计新分类分布
    cats = {}
    for art in articles:
        c = art.get('category', '')
        cats[c] = cats.get(c, 0) + 1
    print("\n新分类分布:")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()

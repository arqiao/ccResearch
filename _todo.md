# 待排期开发

移动端 http://localhost:8088/ 页面的“精选文章”及其图标，应该放在右侧。
（我的手机上有这个问题，浏览器的模拟器上没有问题）

http://localhost:8088/articles/ 这个页面的“142篇原始文章”文字改为“精选原始文章”。这个问题确实还是没改。


让AI重新给每篇文章打标签。



# 策划中

  - 然后我来写萃取脚本，你可以选择：
  - 用哪个 LLM API（OpenAI / Claude / 国内模型）
  - 从哪个板块开始萃取（建议从"安装部署"开始，最实用）

  你想用什么模型来做萃取？




# 常用指令
claude --resume 526115eb-85c9-4b6e-8f35-9aec83a3fa7c

## 数据有变更后，一条命令搞定
python scripts/main.py --classify --hotness --web
## 有新文章入库时
python scripts/main.py --fetch --classify --hotness --scrape --web
## 全量重跑
python scripts/main.py --all

## 启动Web服务器
cd D:\workspace\cc-work\plan-research-claw\site
Start-Process -WindowStyle Hidden python -ArgumentList "-m http.server 8088 -d D:\workspace\cc-work\plan-research-claw\site"
## 停止Web服务器
Stop-Process -Name
python
如果有多个 Python 进程只想停特定的，先用 Get-Process python 查看，再用 Stop-Process -Id <进程ID> 停指定的。

## 模型ID
claude-opus-4-6  │ 最新旗舰，最强推理能力
claude-opus-4-5    │ 上一代旗舰
claude-sonnet-4-5  │ 性能与速度平衡，性价比高
claude-haiku-4-5 │ 最快最轻量
claude-haiku-4.5-20251001



域名：https://openclaw-arqiao.vercel.app/
部署：https://github.com/arqiao/kbs-OpenCLaw.git


git init
git remote add origin https://github.com/arqiao/kbs-OpenCLaw.git
git add .
git commit -m "初始上线：知识库网站框架 + 精选文章阅读器"
git branch -M main
git push -u origin main

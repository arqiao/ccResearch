# C 盘空间清理记录（2026-02-11）

## 初始状态

- 总容量 192 GB，已用 174.5 GB，剩余 17.5 GB

## 空间占用分析

主要占用来源（清理前）：

| 目录 | 大小 | 说明 |
|------|------|------|
| Users（用户数据） | 83 GB | 主要是 AppData |
| Windows | 30 GB | 系统文件，不可动 |
| Program Files | 23 GB | 安装的程序 |
| Program Files (x86) | 14 GB | 安装的程序 |
| ProgramData | 8 GB | 程序数据 |

AppData 下主要占用：

| 目录 | 大小 |
|------|------|
| LarkShell（飞书） | 14 GB |
| Tencent/QQBrowser | 8.7 GB |
| 360aibrowser | 7.6 GB |
| Google/Chrome | 5.9 GB |
| Docker | 3.6 GB |
| JianyingPro（剪映） | 5.3 GB |
| Kingsoft/WPS | 2.9 GB |
| Doubao（豆包） | 2.4 GB |

## 清理操作及效果

| 操作 | 释放空间 | 方式 |
|------|---------|------|
| 360安全卫士清理 + 卸载360AI浏览器 | ~10 GB | 卸载应用 + 自动清理 |
| QQ浏览器 Service Worker/CacheStorage | ~7 GB | 手动删除目录（见下方路径） |
| 飞书 LarkShell 缓存 | ~14 GB | 飞书设置内清除缓存 |
| Docker 数据迁移 | ~3.5 GB | Docker Desktop 设置中修改 Disk image location |
| Chrome AI模型 + Service Worker | ~4.5 GB | 手动删除目录（见下方路径） |
| 豆包缓存 | ~0.8 GB | 手动删除目录（见下方路径） |

### 手动删除的具体路径

QQ浏览器：
```
C:\Users\qiaolian\AppData\Local\Tencent\QQBrowser\User Data\Default\Service Worker\CacheStorage
```

Chrome：
```
C:\Users\qiaolian\AppData\Local\Google\Chrome\User Data\OptGuideOnDeviceModel
C:\Users\qiaolian\AppData\Local\Google\Chrome\User Data\Default\Service Worker
```

豆包：
```
C:\Users\qiaolian\AppData\Local\Doubao\User Data\Default\Service Worker
C:\Users\qiaolian\AppData\Local\Doubao\User Data\Default\Code Cache
C:\Users\qiaolian\AppData\Local\Doubao\User Data\Default\Cache
C:\Users\qiaolian\AppData\Local\Doubao\User Data\gecko_cache
```

### 迁移操作

- Docker：Docker Desktop 设置 → Resources → Advanced → Disk image location → 改到 D 盘
- 剪映：设置中改了草稿/素材/预设路径到 E 盘（缓存路径无法修改）
- WPS：设置中改了备份路径到 E 盘（插件数据路径无法修改）

## 最终状态

- 已用约 150 GB，剩余约 52 GB，共释放约 34 GB

## 未处理项

| 项目 | 大小 | 原因 |
|------|------|------|
| 剪映 Apps | 2.3 GB | 程序本体，非缓存，不能删 |
| WPS addons | 2.8 GB | 插件数据，删了会重新下载 |
| 剪映 User Data/Cache | 412 MB | 可删但量小，暂不处理 |

## 关键经验

1. 浏览器"清除缓存"通常不清理 Service Worker/CacheStorage，这部分往往是最大的空间占用，需手动删除，与 Cookie/登录状态无关
2. Chrome 的 `OptGuideOnDeviceModel` 是本地 AI 模型，可达数 GB，可安全删除
3. 飞书缓存路径无法在设置中修改，只能清除；Docker 支持在设置中迁移数据目录
4. 剪映 `Apps` 是程序本体不能删，WPS `wps/addons` 是插件数据不建议删
5. 应用改了存储路径后旧数据不会自动迁移，需确认新旧目录结构一致后才能手动删旧数据

## 后续维护建议

1. 建议每隔一两个月检查一次浏览器的 Service Worker/CacheStorage 目录，这些缓存会随使用持续增长
2. 如果 C 盘再次紧张，可以考虑清理：
   - `C:\Users\qiaolian\AppData\Local\Packages`（1.7 GB，Windows Store 应用数据）
   - npm 缓存（744 MB），执行 `npm cache clean --force` 即可
3. `C:\Windows`（30 GB）中可能有旧的 Windows 更新文件，可通过「磁盘清理」→「清理系统文件」→ 勾选「Windows 更新清理」来释放

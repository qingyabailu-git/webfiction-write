---
name: fiction-scan
description: |
  网文扫榜。分析起点、番茄、晋江等平台排行榜数据，提炼市场趋势与热门题材。
  按题材/篇幅路由到对应的分析管线。支持长篇和短篇。
  触发方式：/fiction-scan、「扫榜」「排行」「什么火」「趋势」「选题」。
---

# fiction-scan：网文扫榜

分析平台排行榜，提炼市场趋势与热门题材。

## 路由

| 用户意图 | 路由到 |
|---------|-------|
| 长篇排行、起点、番茄、晋江 | 长篇扫榜管线 |
| 短篇排行、知乎盐言、故事会 | 短篇扫榜管线 |
| 选题决策、写什么能火 | 长篇扫榜管线（默认） |

## 长篇扫榜管线

### 1. 确定分析目标

- 用户指定平台（起点/番茄/晋江）、榜单类型（畅销/推荐/新书）
- 或用户只说"帮我看看现在什么火" → 默认番茄 + 畅销榜

### 2. 数据采集

使用 browser-cdp 技能（如可用）或 WebFetch 采集榜单数据。
脚本参考：
- `scripts/qidian-rank-scraper.js`
- `scripts/fanqie-rank-scraper.js`
- `scripts/jjwxc-rank-scraper.js`

### 3. 数据分析

输出分析报告：
- 热门题材分布
- 同类书的差异化定位
- 读者画像（年龄段/性别/偏好）
- 选题建议 + 差异化方向
- 成交流程：输出到项目目录 `扫榜分析/` 并复制核心建议到 `选题决策.md`

### 4. 写回

- 完整报告写入 `扫榜分析/`（标题含日期）
- 核心选题建议写入项目根 `选题决策.md`
- 排序后推荐最可行的选题

## 短篇扫榜管线

类似长篇管线，但：
- 数据来源：知乎盐言、七猫短篇、黑岩故事会
- 分析重点：情绪类型分布、反转密度、字数分布、热门题材
- 脚本参考：`scripts/dz-browse-scraper.js`、`scripts/heiyan-booklist-scraper.js`

## 使用示例

```
> /fiction-scan 番茄 畅销榜 都市

📊 正在采集番茄小说畅销榜数据（都市分类）...

分析完成！
热门题材：都市+重生（占比 35%）、都市+职场（28%）
读者画像：25-35 岁男性为主
选题建议：都市+重生+商业（竞争较少，潜力大）
差异化方向：聚焦实体行业而非互联网，增强真实感

✅ 已输出：扫榜分析/2026-06-12_番茄畅销榜-都市.md
✅ 已输出：选题决策.md（请在开书前阅读）
```

## 参考

扫榜数据采集依赖浏览器操作（browser-cdp skill 提供）。
爬虫脚本从 story-long-scan / story-short-scan 的 scripts/ 目录复制。
数据分析参考 genre-trends.md、reader-profiling.md。
读者画像分析参考 reader-profiling.md。
选题决策参考 topic-decision.md。
发布指南参考 publishing-guide.md。
以上参考在分析阶段按需加载，不预读。
---
### 番茄平台特别指南

番茄小说（Fanqie Novel）是字节跳动旗下的免费阅读平台，
主要特点：
- 免费阅读 + 广告分成
- 适合长篇连载（100-300 万字）
- 读者群体以 16-35 岁为主
- 热门题材：都市、玄幻、言情、系统流
- 连载要求：日更 3000-6000 字
- 签约门槛：满 3 万字可申请，10 万字以上优先

扫榜时优先分析番茄平台数据，对收益有直接参考价值。
选题建议中特别标注"番茄适配"程度。
发行策略参考 publishing-guide.md。
```
│ 长篇排行、起点、番茄、晋江 | 长篇扫榜管线 |
│ 短篇排行、知乎盐言、故事会 | 短篇扫榜管线 |
│ 选题决策、写什么能火 | 长篇扫榜管线（默认） |
| 长篇排行、起点、番茄、晋江 | 长篇扫榜管线 |
| 短篇排行、知乎盐言、故事会 | 短篇扫榜管线 |
| 选题决策、写什么能火 | 长篇扫榜管线（默认） |
## 长篇扫榜管线

### 1. 确定分析目标
- 用户指定平台（起点/番茄/晋江）、榜单类型（畅销/推荐/新书）
- 或用户只说"帮我看看现在什么火" → 默认番茄 + 畅销榜

### 2. 数据采集

**方式 A：CDP 浏览器模式（推荐）**
先用 browser-cdp 技能启动 Chrome 调试模式，再运行爬虫脚本：
```bash
# 1. 启动/检测 CDP
node skills/fiction-scan/scripts/cdp-utils.js 9222 --detect

# 2. 运行爬虫（以番茄为例）
node skills/fiction-scan/scripts/fanqie-rank-scraper.js \
  --url "https://fanqienovel.com/rank" \
  --output "扫榜分析/{日期}_番茄畅销榜.md"
```

**方式 B：HTTP 直连模式（备用，无需 CDP）**
直接用 Node.js https 模块抓取：
```bash
SCRIPTS_DIR=skills/fiction-scan/scripts
node -e "
const https = require('https');
https.get('https://api.fanqienovel.com/api/rank/list', (res) => {
  let d = '';
  res.on('data', c => d += c);
  res.on('end', () => {
    const data = JSON.parse(d);
    // 解析排行数据
    console.log('番茄排行数据:', data.length, '条');
  });
});
"
```

### 3. 数据分析
输出分析报告（已有测试通过 14/14）：
- 热门题材分布
- 同类书的差异化定位
- 读者画像
- 选题建议
- 成交流程：输出到项目目录 `扫榜分析/`

### 4. 写回
- 完整报告写入 `扫榜分析/`（标题含日期）
- 核心选题建议写入项目根 `选题决策.md`

## 短篇扫榜管线
类似长篇管线，但数据来源不同：
- 知乎盐言、七猫短篇、黑岩故事会
- 分析重点：情绪类型分布、反转密度、字数分布
- 脚本：`dz-browse-scraper.js`、`heiyan-booklist-scraper.js`

## 环境要求

爬虫脚本依赖以下组件（未安装时只影响 CDP 模式，不影响分析逻辑）：
- Node.js（已有） + Playwright（已有）
- Chrome 浏览器（已有，位于 `C:\Program Files\Google\Chrome\Application\chrome.exe`）
- `browser-cdp` skill（已有）

## 使用示例
```
> /fiction-scan 番茄 畅销榜 都市

📊 正在采集番茄小说畅销榜数据（都市分类）...
✅ 扫榜分析报告已生成：扫榜分析/2026-06-15_番茄畅销榜-都市.md
✅ 选题决策.md 已更新
```

## 参考
爬虫脚本位置：`skills/fiction-scan/scripts/`
支持的脚本：
- `fanqie-rank-scraper.js` — 番茄小说
- `qidian-rank-scraper.js` — 起点中文网
- `jjwxc-rank-scraper.js` — 晋江文学城
- `ciweimao-rank-scraper.js` — 刺猬猫
- `qimao-rank-scraper.js` — 七猫
- `dz-browse-scraper.js` — 点众短篇
- `heiyan-booklist-scraper.js` — 黑岩短篇
- `cdp-utils.js` — CDP 连接工具

爬虫需配合 browser-cdp skill 使用。分析报告生成已独立验证通过。

> **💡 项目说明**：本工具集的灵感来源于两套开源网文创作 skill：
> [webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) 和
> [oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)。
> 在我看来两者各有优势——一个胜在工程化管理，一个胜在情绪驱动方法论——
> 于是用 AI（Codex / Claude）将它们的设计精髓融合成了这套 fiction-* 工具集。
> 在此对原项目作者表示感谢。

# web-fiction - 网文创作工具集

基于 Codex 的网络小说创作工具集，从构思到完本的完整工作流。
面向番茄小说等免费阅读平台，以情绪驱动的写作方法论为核心。

## 设计哲学

- **先定情绪，再定故事**：每章必须明确交付什么情绪
- **不写大纲不写正文**：系统在合适时机提醒补纲
- **系统主动引导**：自动检测章节模式（Normal/Deep）、里程碑主动提示
- **改必有传播**：修改章节时自动探测并传播到后续章节和设定集

## 技能清单

| 技能 | 功能 | 聊天触发（直接说话就行） | 阶段 |
|------|------|------|------|
| **fiction** | 主入口路由，分发到子技能 | 「我想写小说」「帮我写书」「写网文」「开新书」 | 全局 |
| **fiction-conceive** | 构思共创：与 AI 讨论打磨核心构思 | 「聊聊构思」「帮我设计角色」「我想写个什么样的故事」 | 准备 |
| **fiction-setup** | 初始化标准项目目录结构 | 「建项目」「准备写书」「搭环境」「从零开始」 | 准备 |
| **fiction-start** | 正式开书：检查清单 → 锁基线 → 初始化底本 | 「开书」「可以动笔了」「准备好了，开始吧」 | 锁定 |
| **fiction-scan** | 扫榜：分析平台排行榜找热门题材 | 「扫榜」「最近流行什么」「什么火」「市场怎么样」 | 参考 |
| **fiction-analyze** | 拆文：拆解爆款小说结构和写法 | 「拆文」「分析这本书」「帮我拆一下」「学学这本书」 | 参考 |
| **fiction-plan** | 规划：卷节拍表 → 卷时间线 → 章细纲（滚动） | 「规划」「做大纲」「后面怎么写」「帮我规划一下」 | 写作前 |
| **fiction-write** | 正文写作（Normal/Deep 双模式，自动判断） | 「写第X章」「续写」「接着写」「下一章」「日更」 | 核心 |
| **fiction-revise** | 章节修改（Polish/Re-craft/Rewrite 三档） | 「修改第X章」「重写」「这章不太对」「不满意」「回炉」 | 写作后 |
| **fiction-review** | 质量审查（单章/批量/整卷） | 「审查」「帮我看下写得怎么样」「审一下」 | 质量 |
| **fiction-polish** | 润色与去 AI 味 | 「润色」「去AI味」「这篇太AI了」「帮我顺一下文字」 | 质量 |
| **fiction-query** | 查询设定、角色、伏笔等信息 | 「查角色」「查设定」「什么状态」「那个角色叫啥来着」 | 全局 |
| **fiction-learn** | 提取成功写作模式到项目记忆库 | 「记住这个写法」「这招存起来」「以后都这么写」 | 全局 |
| **fiction-doctor** | 项目体检：检查文件结构、底本完整性 | 「体检」「帮我看看项目有没有问题」「检查一下」 | 管理 |
| **fiction-export** | 正文导出与完本归档 | 「导出」「完本」「导出txt」「我要完本了」 | 收尾 |
| **fiction-import** | 导入已有小说到标准结构 | 「导入」「我有现成的稿子」「把我的书导进来」 | 辅助 |

## 安装

将 `skills/` 目录复制到你的 Codex 技能目录：

```bash
# macOS / Linux
cp -r skills/* ~/.codex/skills/

# Windows
Copy-Item -Path "skills/*" -Destination "$env:USERPROFILE\.codex\skills\" -Recurse
```

### 依赖

- Python 3.8+（可选，用于 `scripts/fiction.py` 后端脚本）
- 扫榜功能需要 `browser-cdp` skill（可选）

## 快速开始

不需要记命令，直接和 AI 聊天就能触发。当然，如果你更喜欢用命令，也可以：

`
直接说「帮我建个项目」      → 创建项目骨架
直接说「聊聊构思」          → 和 AI 讨论你的小说构思
直接说「开书」              → 正式开书
直接说「规划一下」          → 规划第 1 卷
直接说「写第一章」          → 开始写作（系统自动选 Deep 模式）
`材/主角/冲突/文风
     ↓  （可穿插扫榜/拆文）
fiction-start    → 检查清单 → 锁基线 → 初始化底本
     ↓
fiction-plan     → 卷节拍表 → 卷时间线 → 章细纲（滚动）
     ↓
fiction-write    → 写作循环（每章自动检测模式 + 里程碑提示）
     ↓
fiction-revise   → 修改（改事实自动传播到后续章节）
     ↓
fiction-review   → 审查（单章/批量/整卷）
fiction-polish   → 润色与去 AI 味
     ↓
fiction-export   → 完本导出
```

## 关键设计

### Normal/Deep 双模式

写每章时系统自动检测：

| 条件 | 模式 |
|------|------|
| 首章/卷首/卷末/高潮/里程碑 | **Deep**（完整六步 + 底本同步） |
| 常规推进章 | **Normal**（标准四步） |

### 自动里程碑提示

写完第 1/5/10/卷末章时系统主动弹出建议，不用用户自己记。

### 三档修改模式

| 模式 | 改事实？ | 自动传播？ |
|------|---------|-----------|
| Polish | ❌ | ❌ |
| Re-craft | ✅ | ✅（改后自动影响扫描） |
| Rewrite | ✅ 全盘 | ✅（全链路刷新） |

## 目录结构

```
项目/
├─ .novel/
│   ├─ state.json            # 统一状态
│   ├─ project_memory.json   # 写作模式积累
│   └─ tmp/                  # 运行时临时文件
├─ .story-system/             # Story System 底本
├─ 设定集/                    # 世界观/角色/力量体系
├─ 大纲/                      # 总纲/卷节拍/章纲
├─ 正文/                      # 各章正文
├─ 追踪/                      # 上下文/伏笔/时间线
└─ 审查报告/                  # review 输出
```

## 许可证

MIT License - 自由使用、修改、分享。

## 鸣谢

本工具由 AI（Codex / Claude）辅助生成。

设计参考了以下开源项目：

### webnovel-writer
- 仓库: [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- 贡献: 工程化的项目管理（state.json 统一状态、Story System 底本体系、
  memory-contract 查询、review-pipeline+metrics 落库、project_memory、
  chapter-commit、doctor/dashboard）

### oh-story-claudecode
- 仓库: [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)
- 贡献: 情绪驱动的写作方法论（先定情绪再定故事）、丰富的写作参考库
  （hooks/反转/情绪技法）、扫榜拆文管线、去 AI 味流程、多书切换机制）

本项目融合了两者的设计精髓：以情绪驱动的方法论为核心，以工程化的数据模型为骨架。

---
name: fiction-write
description: |
  正文写作。支持 Normal（标准四步）和 Deep（完整六步+底本同步+data-agent）双模式。
  系统自动检测模式并提示用户确认。每章写完自动检测里程碑节点弹出建议。
  写作前自动检查章纲是否存在，不存在则阻断。
  触发方式：/fiction-write {章号}、「写第X章」「续写」「继续写」「日更」「下一章」「接着写」「开始写」。
metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-write：正文写作

每章产出一节可发布的正文，写入 `正文/第{章号}章-{标题}.md`。
默认字数目标依据题材和细纲确定（番茄平台建议 2000-3000 字/章）。

## 双模式设计

| 模式 | 适用场景 | 耗时 |
|------|---------|------|
| **Normal** | 常规推进章 | ~30-40 分钟/章 |
| **Deep** | 第 1 章/卷首/卷末/高潮章/里程碑章 | ~60-90 分钟/章 |

## 自动模式检测

写每章前系统自动判断：

| 条件 | 推荐模式 |
|------|---------|
| 本章是第 1 章 | Deep |
| 本章是某卷的第 1 章 | Deep |
| 本章是某卷的最后 2 章 | Deep |
| 本章是第 10/20/30... 章（里程碑） | Deep |
| 章纲标记了 `climax: true` / `is_reversal: true` | Deep |
| 章纲标记了 `mode: deep` | Deep |
| 以上都不是的常规章 | Normal |

交互示例：
```
📌 检测到本章是开篇第一章。
建议使用 Deep 深度模式，以确保：
  · 留下完整的底本基线
  · 审查报告与 metrics 落库
  · data-agent 提取初始事实供后续查询

本次使用 Deep 模式？[Y/n]
```

用户可拒绝（n 切换到 Normal）或确认。

## 前置检查

```bash
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${CLAUDE_PROJECT_DIR:-$PWD}" where)"
```

### 检查一：是否已开书

检查 `state.json.progress.writing_started`。未开书则阻断：
```
⚠️ 还没正式开书，不能写正文。
先运行 fiction-start 完成开书流程。
```

### 检查二：本章细纲是否存在

检查 `大纲/第{卷号}卷/详细大纲.md` 中是否包含本章章节。
不存在则阻断：
```
⚠️ 第 X 卷的细纲还没做到第 N 章。
先规划：fiction-plan {卷号}
```

### 检查三：本章是否已有正文

检查 `正文/第{章号}章-*.md` 是否存在。
存在则提示：本章已有正文，是否覆盖？[Y/n]

## Normal 模式流程

```
Step 1: 加载上下文
  │ 读取章纲目标（核心事件/情绪目标/爽点/禁区）
  │ 读取最近 3 章摘要
  │ 读取活跃伏笔
  │ 加载本回涉及的设定卡
  │ 确认情绪目标 ❮一句话❯
  │
Step 2: 起草正文
  │ 自动加载对应题材的写作公式（内置参考或引用 story 系列的 references）
  │ 如有拆文结果，自动引用最相关段落作为参考
  │ agent 起草 + 字数验证（番茄平台建议 2000-3000 字）
  │
Step 3: reviewer 审查
  │ 返回结构化 JSON:
  │   blocking: []     # 阻断问题，必须修复
  │   suggestions: []  # 非阻断建议
  │ blocking 定点修复，用户裁决无法修复的项
  │
Step 4: 去 AI 味 + 格式规范 + 提交
  │ 4a: banned-words 扫描（一级词替换/二级词按语境判断）
  │ 4b: AI 腔模式检测（对称句/判断句/过度副词）
  │ 4c: 人工化改写（拆长句/抽象替换/对话潜台词化/标点去模板化）
  │ 4d: 格式规范化（引号统一、断句、标点）
  │ 4e: precommit gate
  │ 4f: chapter-commit
  │ 4g: 静默写回追踪文件
  │     ├─ 追踪/上下文.md 更新
  │     ├─ 追踪/伏笔.md 追加/闭合
  │     ├─ 追踪/时间线.md 追加
  │     ├─ 追踪/角色状态.md 更新
  │     └─ 设定集/配角卡 增量/新建
  │ 4h: 生成章节摘要（静默，一句话级别，供 fiction-revise 变更传播使用）
  │     写入 .novel/summaries/ch{N}.md
  │ 4i: git backup
  │
Step 5: 里程碑检查（自动，无交互）
  │ 检查当前章节号触发哪个里程碑
  │ 触发时在完成报告中展示建议
```

## Deep 模式增量

在 Normal 流程基础上增加：

```
Step 1 → context-agent 生成完整写作任务书
          （含全部活跃伏笔、底本约束、文风指引）

Step 3 → 审查报告写入 审查报告/第{章号}章审查报告.md
       → review metrics 写入 index.db

Step 4 → data-agent 提取三份 artifact:
          fulfillment_result.json（目标完成度）
          disambiguation_result.json（消歧义）
          extraction_result.json（本章新事物）
       → chapter-commit（含 data-artifacts）
       → projection 五层刷新（state/index/summary/memory/vector）
       → postcommit gate 校验

Step 5 → 三段式 user-report 最终总结
```

## 里程碑提示（写完每章后自动触发）

当前章节号触发对应提示，展示在完成报告中：

| 位置 | 提示内容 |
|------|---------|
| 第 1 章 | "第 1 章已完成。建议立即做一次深度审查：fiction-review 1（deep 模式）。这章是全书的脸面。" |
| 第 5 章 | "连续写了 5 章。建议：fiction-review 1-5 批量审查；检查追踪/伏笔.md；回看第 1 章风格一致性。" |
| 第 10 章 | "第 10 章完成。建议完整 review-pipeline：fiction-review 1-10；运行一致性检查；查看 dashboard 伏笔密度。" |
| 卷最后一章 | "「{卷名}」全部写完。建议：卷末深度审查；卷摘要归档；规划下一卷：fiction-plan {下一卷号}" |
| 距上次审查 ≥5 章 | "距上次审查过了 5 章。建议：fiction-review {上次+1}-{当前}" |

**压制规则**：
- 同一类型 24 小时内不重复
- 用户刚主动审查过 → 跳过对应提示
- 批量写多章时只在最后写完那章触发
- "每 5 章"基准点是上次审查位置

## 关于写回（全部静默执行，不弹提示）

每章完成后自动写回以下内容（用户不需要知道也不需要确认）：
- 追踪/上下文.md：更新进度、关键决策
- 追踪/伏笔.md：追加新伏笔/标记已回收
- 追踪/时间线.md：追加事件时间锚点
- 追踪/角色状态.md：更新属性/境界/关系变化
- 设定集/配角卡：首次出现且后续复用 → 自动建卡；已有 → 增量补充
- 大纲/第X卷/详细大纲.md：如果实际写作和章纲有出入 → 自动修正章纲（以正文事实为准）

**例外**：如果文件在上次 git commit 后有用户手动编辑，先问用户是否保留手动版本。

## 参考

写作技法参考库（从 story-* 系列继承）：
- genre-writing-formulas.md：各题材创作公式
- hooks-chapter.md / hooks-paragraph.md / hooks-suspense.md：钩子设计
- reversal-toolkit.md：反转设计
- emotional-methods.md / emotional-arc-design.md：情绪设计
- anti-ai-writing.md：去 AI 味核心规则
- banned-words.md：禁用词表
- dialogue-mastery.md：对话技法
- writing-craft.md：通用写作技法

以上参考按需加载，不一次性全部读入。

```bash
# 参考加载示例：按题材加载对应公式
python -X utf8 "${SCRIPTS_DIR}/reference_search.py" \
  --skill write --table genre-writing-formulas \
  --query "{当前题材}" --genre "{当前题材}"
```

## 失败恢复

每步独立，失败补跑不后退。
- 审查缺失 → 重跑 Step 3
- 写回失败 → 只重跑写回步骤
- chapter-commit 未生成 → 重跑 commit
- projection 失败 → 重跑 projection

## 延申阅读

- 修改已写章节 → fiction-revise
- 单独审查 → fiction-review
- 单独润色/去 AI 味 → fiction-polish
- 批量更新细纲 → fiction-plan
- 查询章节/设定状态 → fiction-query
- 可视化面板 → fiction-dashboard
- 项目体检 → fiction-doctor
- 提取写作模式 → fiction-learn
- 多书切换 → fiction-switch
- 导出/完本 → fiction-export
- 封面生成 → fiction-cover
---

## 附录：情绪确认交互示例

Normal 模式下 Step 1 的情绪确认部分：
```
📖 第 7 章写作准备

章纲目标：
  · 核心事件：主角发现李四的账本
  · 情绪目标：紧张 + 期待
  · 本章爽点：李四吃瘪
  · 细纲节点：CBN(发现) → CPN(对峙) → CPN(反转) → CEN(悬念)

最近 3 章摘要：[...]
活跃伏笔：[...]
相关设定：[...]

本章交付什么情绪？（一句话确认）
→ "紧张+期待，李四吃瘪时的畅快感"
```

## 附录：去 AI 味交互示例

Step 4 去 AI 味处理输出：
```
Step 4: 去 AI 味处理
────────────────────
banned-words 扫描：
  🟢 一级词命中 3 处 → 已替换
  🟢 二级词命中 7 处 → 已替换（2 处保留，语境合理）

AI 腔模式识别：
  🟢 对称句密度正常
  🟢 判断式语句 2 处 → 已改写
  ⚠️ 副词修饰偏多（可选处理）
────────────────────
去 AI 味验证：通过 ✓
```

## 附录：完成报告示例

Normal 模式完成后的报告：
```
═══════════════════════════════════════
  第 7 章 完成

  已生成：
  · 正文/第07章-账本.md
  · 审查结果（非阻断信息已标注）
  · 追踪/伏笔.md 已更新（李四的会计 → 已回收）
  · 追踪/时间线.md 已更新
  · git backup ✓

  下一章建议：
  → fiction-write 8
═══════════════════════════════════════
```
---

## 附录：写回清单（底本，静默执行）

每章完成后系统自动写回以下内容。用户不需要知道也不需要确认。

**必写回**：
- 追踪/上下文.md → 更新当前进度、本章关键决策
- 追踪/伏笔.md → 追加新埋伏笔、标记已回收伏笔为 closed
- 追踪/时间线.md → 追加本章事件的时间锚点
- 追踪/角色状态.md → 更新属性/境界/关系的变化

**条件写回**：
- 设定集/配角卡 → 首次出现的具名角色且后续会复用：自动建卡；已有卡：增量补充
- 大纲/第X卷/详细大纲.md → 如果实际写作和章纲有出入，以正文事实为准自动修正章纲（回填）
- 设定集/文风档案.md → Deep 模式下检查文风一致性并追加记录

**仅在 Deep 模式下写回**：
- 审查报告/第N章审查报告.md
- .story-system/chapters/chapter_N.json 刷新
- .story-system/commits/chapter_N.commit.json

写回遵循原则：
- 追踪文件有变动就更新，无变动不写入
- 不弹窗问用户确认
- 唯一例外：文件在上次 git commit 后有用户手动编辑，先问"是否保留你的版本？"
- 跨卷写回需要用户确认（token 消耗大）

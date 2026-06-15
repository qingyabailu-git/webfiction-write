---
name: fiction-polish
description: |
  润色与去 AI 味。对已有正文执行格式规范化、banned-words 扫描替换、
  AI 腔检测与人工化改写、文风一致性检查。支持单章和批量范围。
  触发方式：/fiction-polish {章号或范围}、「润色」「去AI味」「格式」「标点规范」「这篇太AI了」「帮我顺一下文字」。
metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-polish：润色与去 AI 味

独立于 fiction-write 的 Step 4，专门用于用户想单独润色场景。
通常由里程碑提示触发（写 5/10 章后），也可用户主动运行。

## 执行工序

### ① banned-words 扫描

```bash
# 一级词（高概率 AI 腔）："然而""不禁""仿佛""不禁让"等
# 命中 → 直接替换

# 二级词（语境相关）：根据相邻文本判断
# 高频出现 → 替换；偶发 → 保留
```

对照 `references/banned-words.md`（从 story-* 系列继承）。

### ② AI 腔模式检测与改写

| 模式 | 检测方式 | 改写方式 |
|------|---------|---------|
| 对称句/排比句密度 | 统计每段对称结构数 | 打散为长短交替 |
| "X 是 Y 的"判断句 | 正则匹配 | 改为动作/对话承载 |
| 过度修饰副词 | "突然/竟然/深深地"统计 | 去掉或嵌入动作 |
| 模板化开头 | "就在这时/突然/没想到" | 直接上动作 |
| 标点模板化 | 过多省略号/破折号/感叹号连用 | 简化标点 |

### ③ 人工化改写

- 句子结构打散：长复合句拆短
- 抽象描写替换："她感到一阵悲伤" → "她眼泪掉了下来"
- 对话潜台词化：直白陈述 → "嘴上说不用，手却把杯子推了过来"
- 信息密度调整：删减无信息承载的填充词

### ④ 格式规范化

- 引号风格统一（按项目约定：半角双引号或「」）
- 段落断句：单段 ≤ 5 行，超长则按动作/信息变换拆分
- 标点统一：中文标点优先
- 连续动作按镜号断句

### ⑤ 文风一致性检查（如有文风档案）

- 对照 `设定集/文风档案.md` 的标签逐项核验
- 偏离过大的段落标注建议

## 批量运行

```bash
fiction-polish 1-10        # 润色第 1-10 章
fiction-polish --all        # 全部已写章节
fiction-polish --volume 1  # 整卷
```

批量时逐章执行，每章完成输出状态。

## 写回

直接覆盖修改目标正文文件。不做版本管理，但不覆盖用户手动编辑的文件。

## 参考

去 AI 味核心规则和 banned-words 表从 story-* 系列继承。
格式规范从 story-short-write 的 format-and-structure.md 继承。
文风一致性维度由 fiction-conceive 阶段产出的文风档案.md 定义。
本 skill 不内联上述参考文件内容，运行时按需加载。
转换脚本 normalize-punctuation.js 可从 story-* 系列脚本目录复制使用。

## 与 fiction-write 的关系

fiction-write 的 Step 4 内嵌了相同的润色流程。
fiction-polish 是独立的外置版本，用于单独调用。
两者执行效果一致，不应出现同一内容两个不同结果。
如果 fiction-write 时已执行过 Step 4，再次跑 fiction-polish 不会重复修改。
（但如果用户手动改过正文，fiction-polish 会基于最新版本再次处理。）

<!-- fiction-polish: ��ɫ��ȥ AI ζ�������ֻع���Ȼ -->

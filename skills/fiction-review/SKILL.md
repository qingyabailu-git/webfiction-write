---
name: fiction-review
description: |
  质量审查。使用审查模型评估章节质量，生成审查报告并写回审查指标。
  支持单章、批量（1-5）、整卷（--volume N）审查。
  触发方式：/fiction-review {章号或范围}、「审查」「审一下」「检查质量」「review」「帮我看下写得怎么样」。
---
# fiction-review：质量审查

使用审查模型评估章节质量，生成结构化报告和审查指标。

## 执行流程

### Step 1：解析项目根

```bash
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}" where)"
```

### Step 2：加载审查参考

按需加载：
- 总是加载：核心约束、review-schema
- 涉及爽点/钩子：cool-points-guide
- 涉及多线交织：strand-weave-pattern

### Step 3：调用 reviewer agent

必须通过 Agent 工具调用 reviewer，主线不得伪造审查 JSON。

reviewer 只返回严格结构化 JSON，不评分，不口头总结。主线负责把返回的 JSON 写入 `.novel/tmp/review_results.json`，然后由 review-pipeline 覆盖为标准 review_result artifact。

reviewer 跳过、失败、输出不完整、正文为空 → 记录问题，不等同于已审查。

### Step 4：生成报告并落库

```bash
python -X utf8 "${SCRIPTS_DIR}/fiction.py" review-pipeline \
  --project-root "${PROJECT_ROOT}" \
  --chapter {章节号} \
  --review-results ".novel/tmp/review_results.json" \
  --metrics-out ".novel/tmp/review_metrics.json" \
  --report-file "审查报告/第{章节号}章审查报告.md" \
  --save-metrics
```

### Step 5：处理阻断

存在 blocking issue 时，用有限选项让用户裁决：
- 立即修复（输出返工清单，最小修改）
- 仅保存报告，稍后处理（保留报告和指标，结束流程）

## 批量审查

```bash
fiction-review 1-5       # 批量审查 1-5 章
fiction-review --volume 1  # 整卷审查
```

批量审查逐章执行 reviewer → 逐章生成报告 → 汇总显示。

## 写回

- 审查报告写入 `审查报告/第{章号}章审查报告.md`
- review_metrics 写入 `index.db`（review-pipeline --save-metrics）
- review_results JSON 存入 `.novel/tmp/review_results.json`
- Deep 模式下额外更新 `.story-system/reviews/chapter_{N}.review.json`

## 成功标准

1. 解析真实项目根
2. 通过 reviewer 输出结构化 JSON 并落盘
3. 审查报告已生成，metrics 已写入 index.db
4. 存在阻断问题时用户已明确选择处理策略

## 参考

reviewer schema 由 reviewer agent 自带定义，本 skill 不展开。
阻断覆盖指引见 blocking-override-guidelines（由 reviewer 引用）。
批量审查逐章独立执行，不互相影响结果。
审查报告格式由 review-pipeline 决定，本 skill 不定义。
---

## 致谢

本 skill 的开发参考了以下开源项目的思路与实现：

- [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)

感谢原作者的开源贡献。

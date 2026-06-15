---
name: fiction-learn
description: |
  从当前会话提取成功写作模式并写入 project_memory.json。
  类型包括：hook/pacing/dialogue/payoff/emotion/format/other。
  后续写作时自动参考已积累的模式。
  触发方式：/fiction-learn {写作经验描述}、「记住这个写法」「学习」「这个写法好」。
---

# novel-learn：写作模式提取

从对话中提取可复用的写作模式，追加到 project_memory.json。
让系统越写越懂你，自动积累个人风格。

## 执行流程

### 1. 解析项目根

```bash
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/novel.py" --project-root "${CLAUDE_PROJECT_DIR:-$PWD}" where)"
```

### 2. 解析用户输入

- 用户输入为空 → 取本次对话中被用户认可的写法
- 用户有显式输入 → 直接使用

### 3. 归类 pattern_type

| 类型 | 示例 |
|------|------|
| hook | "开篇用冲突前置，第一句就是矛盾" |
| pacing | "过渡章节用双线并行来保持节奏" |
| dialogue | "对话里用潜台词代替直白" |
| payoff | "伏笔钩子要在 10 章内回收" |
| emotion | "虐点时先建立甜蜜再打破" |
| format | "对话单独成行，不用引号" |
| other | 无法归类的 |

### 4. 写入 project_memory.json

```bash
python -X utf8 "${SCRIPTS_DIR}/novel.py" project-memory add-pattern \
  --pattern-type "{归类}" \
  --description "{完整描述}" \
  --category "{分类，可空}" \
  --importance "{high|medium|low}"
```

要求：
- 只追加，不删除旧记录
- pattern_type + description 完全相同时跳过（去重）
- 部分相似不去重

## 成功标准

- project_memory.json 存在且格式合法
- 新 pattern 已追加到 patterns 数组
- 输出包含 status: success

## 失败恢复

| 故障 | 恢复方式 |
|------|---------|
| project_memory.json 不存在 | 脚本自动初始化 {"patterns": []} |
| JSON 解析失败 | 不写入脏数据，告知用户文件损坏 |
| state.json 缺失无法取章节号 | 用 source_chapter: null 跳过，不阻断 |

## 参考

后续写作时 project_memory.json 由 novel-write 的 context-agent 加载，
作为文风参考和历史模式输入。本 skill 只负责写入，不负责读取。
去重逻辑在 novel.py 脚本的 add-pattern 子命令中实现，
此处不重复实现。

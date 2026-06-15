---
name: novel-doctor
description: |
  项目体检诊断。只读检查项目目录、文件、JSON、合同体系完整性。
  发现缺失或异常项时解释影响和修复建议，不自动修复。
  触发方式：/novel-doctor、「体检」「诊断」「检查项目」「项目状态」。
---

# novel-doctor：项目体检诊断

只读诊断当前项目：确认所处阶段应有的文件是否完整。

## 原则

1. 只读诊断，不写文件，不自动修复，不安装依赖
2. 先 project-status 取短状态，再 doctor 做阶段感知检查
3. 缺失项按阶段解释影响和修复建议

## 执行

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT:?}/scripts"

# 短状态
python -X utf8 "${SCRIPTS_DIR}/novel.py" --project-root "${WORKSPACE_ROOT}" project-status --format summary

# 标准体检
python -X utf8 "${SCRIPTS_DIR}/novel.py" --project-root "${WORKSPACE_ROOT}" doctor --format text

# 指定章节（可选）
# python -X utf8 "${SCRIPTS_DIR}/novel.py" --project-root "${WORKSPACE_ROOT}" doctor --chapter {N} --deep
```

## 输出方式

报告包含：
- 当前 phase 和 target_chapter
- 是否有 blocker、缺失或异常文件路径
- 合同/设定集/追踪/正文完整性
- 每个问题的影响和修复建议

不执行真实修复，不展示或要求粘贴 API key。

## 参考

各阶段的文件完整性标准：
- 开书前：.novel/state.json + 设定集/*.md + 总纲草案.md
- 开书后：上述 + .story-system/ 合同 + 大纲/ + 正文/N章.md
- 写作中：追踪/ 文件齐全、合同版本号匹配
体检阶段感知由 novel.py 脚本的 doctor 子命令自动判断。
本 skill 不重复定义各阶段清单。
如需主动修复，先运行 doctor 查看报告，再按建议执行。
如果 contract_version 不匹配，建议运行 novel-start 刷新合同。
如果追踪文件缺失，重新跑 novel-write 对应章节会自动补全。
---
### 使用示例

```
> /novel-doctor

体检报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
阶段：开书后（已写至第 15 章）

✅ 项目状态正常
  · .novel/state.json ✓
  · 设定集/主角卡.md ✓
  · 设定集/世界观.md ✓
  · 设定集/核心冲突.md ✓
  · 大纲/总纲.md ✓
  · 大纲/第1卷/详细大纲.md ✓
  · 正文/ 1-15 章完整 ✓
  · 追踪/伏笔.md ✓
  · 追踪/时间线.md ✓
  · .story-system/MASTER_SETTING.json ✓
  · 合同版本号一致 ✓

⚠️ 建议注意
  · 距上次审查已过 6 章（第 9 章后未审）
  · 追踪/上下文.md 建议归档（当前 50 条记录）

无需处理。
```

```
> /novel-doctor --deep

体检报告（深度）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...
❌ 问题：设定集/世界观.md 引用了一个未建档的配角"赵铁柱"
  影响：后续查询角色赵铁柱时可能返回空结果
  建议：运行 novel-export characters 检查清单，或手动补卡
...
```

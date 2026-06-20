---
name: fiction-start
description: |
  正式开书。运行开书前检查清单，确认构思充分后锁定基线、初始化 Story System 底本。
  开书后设定集锁定为基线，修改需走 fiction-write 内建的变更传播流程。
  开书前不支持写正文。
  触发方式：/fiction-start、「开书」「正式开始」「锁定基线」「开始写作」「准备好了，开始吧」「可以动笔了」。
---
# fiction-start：正式开书

这是一个心理仪式 + 状态切换。开书前用户可自由调整设定/大纲/扫榜/拆书。
开书后设定锁定为基线，系统正式进入写作阶段。

## 前置条件

以下文件必须存在（由 fiction-setup + fiction-conceive 产生）：
- `.novel/state.json`
- `设定集/主角卡.md`（含欲望/缺陷/能力/代价）
- `设定集/世界观.md`
- `设定集/核心冲突.md`（含一句话梗概）
- `大纲/总纲草案.md`

缺失则提示用户先完成对应步骤，不强开。

## 检查清单

```
═══════════════════════════════════════
          正式开书前检查清单
═══════════════════════════════════════

  ☐ 书名: {读取}
  ☐ 题材: {读取}
  ☐ 主角设定: 欲望({}) + 缺陷({})
  ☐ 世界观框架: {已确立/未完成}
  ☐ 核心冲突: {已定/未定}
  ☐ 总纲草案: {存在/缺失}
  ⬜ 可选: 文风档案 → {存在/缺失}
  ⬜ 可选: 扫榜分析 → {已完成/未做}
  ⬜ 可选: 对标拆书 → {已完成/未做}

─────────────────────────────────
建议项（⬜）可选，不影响开书但建议准备。
必填缺失则提示补完再回来。

你现在可以：
  1. 补完未完成项再回来
  2. 直接跳过，正式开书
  3. 先做扫榜/拆文再回来看市场
```

## 开书执行

用户确认后，系统执行：

### 1. 锁定构思文件

将总纲草案升级为正式总纲：
- `大纲/总纲草案.md` → 去除"草案"标记
- 在 `大纲/总纲.md` 中写入核心主线、创意约束（反套路规则/硬约束/主角缺陷/反派镜像）

### 2. 初始化 Story System 底本

```bash
# 生成 MASTER_SETTING.json（全局调性、核心禁忌、题材映射）
python -X utf8 "${SCRIPTS_DIR}/fiction.py" init-contract \
  --project-root "${PROJECT_ROOT}"
```

### 3. 更新 state.json

```json
{
  "progress": { "writing_started": true },
  "versions": { "baseline_version": 1 }
}
```

### 4. 输出开书报告

```
═══════════════════════════════════════
  🎉 正式开书完成！

  状态：
  · 设定集已锁定为基线
  · 底本已初始化（版本 1）
  · 当前阶段：正文写作就绪

  现在可以规划第 1 卷：
  → fiction-plan 1

  或者继续调整构思：
  → fiction-conceive
═══════════════════════════════════════
```

## 开书前 vs 开书后行为差异

| 维度 | 开书前 | 开书后 |
|------|--------|--------|
| 修改设定 | 随意改 | 改完需传播检测 |
| 写正文 | 不支持 | 正常 |
| 底本 | 不存在 | 已初始化（版本 1）|
| fiction-write | 提示"请先 fiction-start" | 正常 |
| fiction-plan | 只做规划，不同步底本 | 规划 + 同步底本 |

**开书后每次 fiction-plan 会刷新对应卷/章的底本版本号。**

## 参考

Story System 底本初始化由 `scripts/fiction.py` 的 `init-contract` 子命令完成。
底本刷新由 fiction-plan 和 fiction-write 负责，start 只做初始建立。
---

## 致谢

本 skill 的开发参考了以下开源项目的思路与实现：

- [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)

感谢原作者的开源贡献。

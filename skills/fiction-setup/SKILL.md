---
name: fiction-setup
description: |
  网络小说项目初始化。创建标准项目目录结构、初始配置文件(state.json)、
  设定集骨架。在进入构思(fiction-conceive)前运行。
  触发方式：/fiction-setup、「建项目」「初始化」「准备写书」「搭环境」「帮我建个项目」「从零开始」。
metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-setup：项目初始化

创建标准项目骨架。只建目录和初始配置文件，不做深度构思。
构思由 fiction-conceive 完成。

## 执行流程

### Phase 1：确认项目目录

```bash
export PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
```

- 检查是否已存在 `.novel/state.json`
- 存在则提示"该项目已初始化，可直接 fiction-start 或 fiction-conceive"
- 不存在则继续
- 询问用户书名，生成安全化目录名

### Phase 2：创建标准目录结构

```
{项目根}/
├─ .novel/
│   ├─ state.json            # 由后续步骤填充
│   ├─ idea_bank.json        # 由 fiction-conceive 填充
│   └─ tmp/                  # 运行时临时文件
│
├─ 设定集/                    # 世界观、角色、力量体系等
├─ 大纲/                      # 总纲、卷纲、章纲
├─ 正文/                      # 各章正文
├─ 追踪/                      # 上下文、伏笔、时间线、角色状态
├─ 审查报告/                   # review-pipeline 产出
└─ 拆文库/                    # fiction-analyze 的分析产出
```

### Phase 3：初始化 state.json

```json
{
  "project": {
    "book_name": "",
    "genre": "",
    "target_words": 0,
    "target_platform": "fanqie",
    "author": ""
  },
  "progress": {
    "current_chapter": 0,
    "current_volume": 1,
    "total_chapters": 0,
    "total_volumes": 0,
    "writing_started": false
  },
  "versions": {
    "baseline_version": 0,
    "last_review_chapter": 0
  }
}
```

### Phase 4：创建 .novel/active-book

写入当前书目录名，作为多书切换指针。

### Phase 5：输出完成信息

- 列出创建的文件和目录
- 建议下一步：fiction-conceive（构思）或 fiction-start（如果已有想法）

## 参考

详细目录结构约定见 `references/`（暂无，按上述硬编码）。
nove-cover 在需要时单独调用，不在此处生成。
扫榜工具 fiction-scan 需要浏览器操作，详见该 skill。
拆文工具 fiction-analyze 需要提供小说文本，详见该 skill。

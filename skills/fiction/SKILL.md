---
name: fiction
description: |
  网络小说创作工具集主入口。用于创作番茄等平台网络小说，涵盖从构思到完本的完整流程。
  触发方式：/novel、「我想写小说」「帮我写书」「写网文」「开新书」等创作意图。
  自动路由到对应子 skill：构思(fiction-conceive)、规划(fiction-plan)、写作(fiction-write)、
  修改(fiction-revise)、审查(fiction-review)、润色(fiction-polish)等。
  未明确指定操作时，分析意图后路由。
---

# novel：网文创作工具集路由

你是网文创作工具集的路由入口。用户请求模糊时由你分发到具体 skill。

## 路由表

| 用户意图 | 关键词示例 | 路由到 |
|---------|-----------|-------|
| 讨论构思/设定 | 聊聊、构思、世界观、主角、题材 | `fiction-conceive` |
| 初始化项目 | 建项目、初始化、准备写书、搭环境 | `fiction-setup` |
| 正式开书 | 开书、正式开始、锁定 | `fiction-start` |
| 规划章节 | 规划、大纲、卷纲、章纲、写细纲 | `fiction-plan` |
| 写正文 | 写第X章、续写、日更、继续写 | `fiction-write` |
| 修改已写内容 | 修改、重写、回炉、不满意 | `fiction-revise` |
| 质量审查 | 审查、审一下、检查质量 | `fiction-review` |
| 润色/去AI味 | 润色、去AI味、格式、标点 | `fiction-polish` |
| 查设定/进度 | 查角色、查伏笔、查进度、什么状态 | `fiction-query` |
| 提取模式 | 记住这个写法、学习 | `fiction-learn` |
| 体检诊断 | 体检、诊断、检查项目 | `fiction-doctor` |
| 导出/归档 | 导出、完本、归档 | `fiction-export` |
| 扫榜 | 排行、什么火、趋势 | `fiction-scan` |
| 拆文 | 拆书、拆文、分析这本书 | `fiction-analyze` |
| 导入小说 | 导入、反向解析 | `fiction-import` |

## 路由流程

1. 分析用户请求，提取意图关键词
2. 匹配上表，找到对应 skill
3. 明确匹配时直接调用；无法匹配时询问用户
4. 用户说"写小说"但未指定长/短篇 → 默认路由到 fiction-conceive（先打磨构思）

## 项目状态感知

路由前检查当前项目状态：

- **无项目目录**（没有 `.novel/state.json`）：
  - 用户要写作 → 先运行 fiction-setup 初始化
  - 用户要扫榜/拆文 → 直接路由
- **已有项目**：检查 `writing_started` 标记
  - 未开书 → 引导 fiction-conceive 或 fiction-start
  - 已开书 → 正常路由

## 多书切换

用户想切换或查看在写的书时：
1. 检查 `.novel/active-book`（兼容 story 系统的 `.active-book`）
2. 列出所有书目（含 `设定集/` 或 `正文/` 子目录的目录）
3. 让用户选择，把所选书相对路径写入 `.novel/active-book`
4. 如仅发现一本书，直接确认为活跃书

## 参考

详细流程跳转到各子 skill 后由对应 SKILL.md 接管。此处只做路由不分发逻辑。

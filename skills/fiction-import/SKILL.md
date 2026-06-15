---
name: fiction-import
description: |
  逆向导入已有小说。将已写好的半成品或完本小说反向解析为标准项目目录结构，
  兼容后续 fiction-plan、fiction-write 流程。内部复用 fiction-analyze 的拆解管线，
  按篇幅自动分流。
  触发方式：/fiction-import、「导入小说」「反向解析」「导入」「把我的书导进来」「我有现成的稿子」。
metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-import：导入已有小说

将已写好但未按本工具集结构组织的项目反向解析为标准格式。

## 适用场景

- 之前在其他工具或纯文本中写了半本，想迁移过来
- 写作途中才决定用本工具集管理
- 有一本完稿想进来做拆解参考

## 执行流程

### Step 1：确认导入源

询问用户：
- 源文件/目录路径
- 书名和作者
- 大致的题材和篇幅

### Step 2：建立目标目录

```bash
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/fiction.py" init --title "{书名}" --author "{作者}" --genre "{题材}" "${CLAUDE_PROJECT_DIR:-$PWD}")"
```

### Step 3：解析源文件

- 如果是单一文件 → 按章节标记拆分（按"第 X 章"或数字编号）
- 如果是目录 → 按文件名排序逐章导入
- 源文件格式支持：.txt / .md 纯文本

### Step 4：按篇幅路由拆解

自动调用 fiction-analyze 的拆解管线，按字数分流。

### Step 5：生成设定和总纲

基于文本分析，生成初始设定集和总纲草案：
- 主角卡（提取文本中的身份/能力/关系）
- 世界观框架
- 核心冲突推测
- 简化到骨架级别，不做过度推断

### Step 6：标记状态

- state.json 中标记 writing_started: true（如果已有一章以上正文）
- 正文文件逐章写入正文/
- 输出导入完成报告

## 限制

- 纯文本格式，解析依赖章节分隔符识别
- 格式不规范（无章节标记、段落无分隔）时精度下降
- 导入后建议运行 fiction-doctor 确认完整性
- 导入的设定和总纲是"推断"而非"确认"，需要用户审查修改
- 导入完成后建议运行 fiction-conceive 打磨设定

## 参考

拆解管线复用 fiction-analyze 的逻辑。
导入后下一步推荐：fiction-doctor（确认完整性）→ fiction-conceive（打磨设定）→ fiction-plan（正式进入规划）
如果导入对象是别人的作品用于拆解学习，建议直接使用 fiction-analyze，
不需要先导入到项目目录。
---
### 使用示例

```
> /fiction-import D:/旧稿/我的小说.txt

📖 导入中...
检测到：长篇（约 25 万字 / 80 章）
题材：都市重生（推测，请用户确认）

✅ 导入完成！
  · 正文/ 已写入 1-80 章
  · 设定集/ 已生成骨架（请 review）
  · 大纲/ 总纲草案.md 已生成
  · 拆文库/ 已生成拆解报告

建议下一步：
  1. fiction-doctor 检查完整性
  2. fiction-conceive 打磨设定
  3. fiction-plan 1 开始正式规划
```

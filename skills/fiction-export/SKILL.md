---
name: fiction-export
description: |
  导出与完本归档。合并所有正文为 .txt/.docx 格式，
  可选去格式、加目录、生成封面。完本后一键归档项目文件。
  触发方式：/fiction-export、「导出」「完本」「归档」「下载」「导出txt」「我要完本了」。
---
# fiction-export：导出与完本归档

将正文合并为可供发布/备份/分享的格式。

## 导出模式

### 正文合并

- 合并所有已写章节为一个文件
- 可选格式：.txt（纯文本）/ .docx
- 合并时自动：按章编号排序、去 format 标记、可选加章目录
- 输出到 `导出/` 目录

```bash
# 导出全部已写章节
python -X utf8 "${SCRIPTS_DIR}/fiction.py" export \
  --project-root "${PROJECT_ROOT}" \
  --format txt --output "导出/{书名}_完本.txt"
```

### 完本归档

完本后执行：
1. 最终一致性检查（可选 deep doctor）
2. 合并正文文件
3. 归档关键项目文件（设定集/大纲/追踪）到 `归档/` 目录
4. 生成完本元数据（字数/章数/写作历时）

```bash
python -X utf8 "${SCRIPTS_DIR}/fiction.py" export \
  --project-root "${PROJECT_ROOT}" \
  --output "归档/{书名}_完本归档.zip"
```

### 文件清理

- 清理运行时临时文件（`.novel/tmp/`）
- 保留追踪/底本等核心数据

## 使用示例

```
> /fiction-export --format docx

✅ 已导出：导出/剑来_完本.docx（45 章，12.3 万字）
```

```
> /fiction-export --archive

✅ 已归档：归档/剑来_完本归档.zip
包含：正文/设定集/大纲/追踪/底本
总字数：12.3 万字 | 45 章 | 历时 67 天
```

## 参考

合并脚本由 `scripts/fiction.py` 的 `export` 和 `export` 子命令处理。
完本归档后，项目目录可移出活跃工作区。
如需继续写新书，运行 fiction-setup 初始化新项目。
如果使用 `.docx` 格式，依赖 Documents 插件的 docx-js 库。
导出的 .txt 文件可直接用于番茄平台投稿。
导出的 .docx 文件可用于自我归档或打印。
---
### 番茄平台投稿注意事项

番茄小说接受 .txt 格式投稿，要求：
- UTF-8 编码（无 BOM）
- 章标题用 `第 X 章` 格式，顶格写
- 正文段之间空一行
- 每章末尾空两行
- 无额外格式标记

本 skill 的 `export` 子命令默认遵守上述规范。
使用 `--format fanqie` 参数可自动适配番茄平台格式要求。
```
---

## 致谢

本 skill 的开发参考了以下开源项目的思路与实现：

- [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)

感谢原作者的开源贡献。

# Changelog

本项目所有重要变更记录在此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [v1.1.0] - 2026-06-20

### 新增
- **state.json schema 版本化**：新增 `SCHEMA_VERSION = 1` 常量和 `migrate_state()` 函数，旧项目打开时自动迁移 `project_info` → `project` 并写入 `schema_version` 字段
- **环境变量双前缀兼容**：8 个 SKILL.md 支持 `CODEX_PROJECT_DIR` 和 `CLAUDE_PROJECT_DIR` 双前缀，无论用 Codex 还是 Claude Code 都能正常工作
- **README 环境变量兼容性说明**：新增段落说明双前缀查找优先级

### 变更
- **metadata.openclaw.sources 迁移到致谢章节**：14 个 SKILL.md 从 frontmatter 移除非标准字段，改为在文件末尾添加 `## 致谢` 章节
- **fiction-write yaml 描述同步**：更新为含修改模式（"写作 Normal/Deep 双模式 + 修改 Re-craft/Rewrite 双模式"）
- **fiction-start/SKILL.md**：旧 `fiction-revise` 引用改为 `fiction-write 内建变更传播流程`
- **fiction-write/SKILL.md**：移除旧的 `fiction-revise` 变更传播引用

### 修复
- **migrate_state 幂等性 bug**：初版返回单值导致 `load_state` 无法判断是否需要持久化迁移结果，改为返回 `(state, changed)` 元组

## [v1.0.3] - 2026-06-17

### 修复（紧急）
- **15 个 SKILL.md 乱码彻底修复**：从 commit `4ef33fa` 恢复干净 UTF-8 版本（v1.0.2 标榜修复但实际未修干净，导致 skill 不可用）
- **15 个 agents/openai.yaml 乱码修复**：同上
- **scripts/reference_search.py**：去除 UTF-8 BOM
- **fiction.py P0 问题**：
  - `cmd_where` 失败时退出码改为 1（原为 0，错误被掩盖）
  - `cmd_export` 支持 `--format {txt,docx,fanqie}` 和 `--output` 参数
  - `cmd_doctor` 支持 `--chapter N` 和 `--deep` 参数
  - `cmd_review` 支持 list 类型的 results 参数

### 新增
- **fiction-revise 合并到 fiction-write**：fiction/SKILL.md 路由表更新，fiction-write/SKILL.md 新增"章节修改模式（内建）"章节，含 Re-craft 和 Rewrite 两种模式
- **.editorconfig**：强制 UTF-8 无 BOM、LF 换行
- **scripts/check_encoding.py**：编码检测工具，可接入 CI 或 pre-commit hook

### 变更
- **README 同步**：完整写作流程图、三种修改强度表、快速上手示例均同步 fiction-revise 合并

## [v1.0.2] - 2026-06-15

### 变更
- 将 `fiction-revise`（章节修改）合并到 `fiction-write`（正文写作），作为内置的三种修改模式
- 为 7 个 skill 新增"写作视角""工作流清晰度""跨 skill 协作"说明段落

### 修复
- 修复审查报告指出的多项问题（注：UTF-8 编码修复不彻底，v1.0.3 已修复）

## [v1.0.1] - 2026-06-10

### 修复
- 16 个 skill 各自审查修复（fiction、fiction-analyze、fiction-conceive 等）

## [v1.0.0] - 2026-06-08

### 新增
- 初始发布，15 个 skill：fiction（主入口路由）、fiction-analyze、fiction-conceive、fiction-doctor、fiction-export、fiction-import、fiction-learn、fiction-plan、fiction-polish、fiction-query、fiction-review、fiction-scan、fiction-setup、fiction-start、fiction-write

---

## 版本号规则

- **主版本号 (X.0.0)**：不兼容的 API 修改
- **次版本号 (1.X.0)**：向下兼容的功能性新增
- **修订号 (1.0.X)**：向下兼容的问题修复

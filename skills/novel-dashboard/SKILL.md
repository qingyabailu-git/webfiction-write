---
name: novel-dashboard
description: |
  启动只读小说管理面板，查看项目状态、实体图谱与章节内容。
  本地 Web 面板，不修改任何项目文件。
  触发方式：/novel-dashboard、「面板」「状态面板」「看进度」「打开面板」。
---

# novel-dashboard：小说管理面板

启动本地只读 Web 面板，可视化查看写作进度和项目数据。

## 前置条件

依赖 dashboard 模块（从 webnovel-dashboard 的后端复用）：
- Python 后端
- 前端 dist/ 构建产物

## 执行流程

### Step 1：确认环境

```bash
if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/dashboard" ]; then
  echo "dashboard 模块未找到，建议先安装依赖"
  exit 1
fi
```

### Step 2：解析项目根

```bash
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/novel.py" --project-root "${CLAUDE_PROJECT_DIR:-$PWD}" where)"
```

### Step 3：启动 Dashboard

```bash
python -m dashboard.server --project-root "${PROJECT_ROOT}"
```

可选参数：
- `--no-browser`：不自动打开浏览器
- `--port 9000`：自定义端口

### Step 4：确认面板可用

访问：
- `/api/story-runtime/health` 确认健康检查通过
- `/api/preflight` 确认数据源正常

## 面板功能

- 章节列表（进度/字数/状态）
- 实体关系图（角色/势力/关系网络）
- 设定词典
- 写作进度统计（总字数/日更量/剩余估算）
- 合同状态（MASTER_SETTING / volume / chapter）
- 最近审查报告

## 安全边界

- 纯只读面板，不提供修改接口
- 文件访问限制在 PROJECT_ROOT 范围内
- 默认仅监听 localhost

## 失败恢复

| 故障 | 恢复方式 |
|------|---------|
| 缺少依赖 | 手动 pip install -r requirements.txt |
| dist/ 缺失 | 确认插件完整安装 |
| 端口占用 | 用 --port 指定其他端口 |
| 页面空白 | 确认 .novel/ 下有 state.json / index.db |

## 参考

Dashboard 后端从 webnovel-dashboard 的 dashboard 模块复用。
前端接口不修改，只读访问。
如果 dashboard 模块无法使用，考虑后续自行实现轻量面板（可选）。
面板使用过程中不消耗写作上下文窗口，保持创作环境干净。
面板停止后不残留进程或文件。
---
### 使用示例

```
> /novel-dashboard

📊 启动 Dashboard...
✅ Dashboard 已启动：http://localhost:5000
当前项目：剑来（第 2 卷第 8 章 / 总计 15 章 / 4.5 万字）
```

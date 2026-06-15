import argparse, json, os, sys
from pathlib import Path
from datetime import datetime

def root(start):
    """查找项目根目录，仅读取不创建。"""
    c = Path(start).resolve()
    novel_dir = c / ".novel"
    state_file = novel_dir / "state.json"
    if state_file.exists():
        return c
    for child in sorted(c.iterdir()):
        if child.is_dir():
            child_state = child / ".novel" / "state.json"
            if child_state.exists():
                return child
    # 项目不存在时返回错误
    print(f"error: no project found in {c} or subdirectories", file=sys.stderr)
    print("hint: run 'fiction setup' to create a new project", file=sys.stderr)
    sys.exit(1)

def load_state(r):
    f=r/".novel"/"state.json"
    return json.loads(f.read_text("utf-8")) if f.exists() else {}

def save_state(r,s):
    f=r/".novel"/"state.json"
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(s,ensure_ascii=False,indent=2),"utf-8")

def cmd_where(a):print(root(Path(a.project_root)))

def cmd_setup(a):
    """初始化项目。明确的初始化命令，替代 where 的隐式创建行为。"""
    c = Path(a.project_root).resolve()
    novel_dir = c / ".novel"
    state_file = novel_dir / "state.json"
    if state_file.exists():
        print(f"project already exists: {c}", file=sys.stderr)
        return c
    novel_dir.mkdir(parents=True, exist_ok=True)
    init_state = {
        "project": {
            "book_name": getattr(a, 'title', ''),
            "author": getattr(a, 'author', ''),
            "genre": getattr(a, 'genre', '')
        },
        "progress": {"writing_started": False},
        "versions": {"baseline_version": 1}
    }
    state_file.write_text(json.dumps(init_state, ensure_ascii=False, indent=2), "utf-8")
    print(f"project initialized: {c}")
    return c

def cmd_status(a):
    r=root(Path(a.project_root));s=load_state(r)
    if not s:print("no state");return
    pi=s.get("project",s.get("project_info",{}))
    pr=s.get("progress",{})
    print("book:",pi.get("book_name",pi.get("title","?")))
    print("author:",pi.get("author","?"))
    print("genre:",pi.get("genre","?"))
    print("writing_started:",pr.get("writing_started",False))

def cmd_doctor(a):
    r = root(Path(a.project_root))
    issues = []
    try:
        checks = [r / ".novel" / "state.json",
                  r / "设定集" / "主角卡.md",
                  r / "设定集" / "世界观.md",
                  r / "大纲" / "总纲.md"]
        for p in checks:
            if not p.exists():
                issues.append(f"missing: {p.relative_to(r)}")
        td = r / "正文"
        if td.exists():
            chs = sorted(td.glob("第*.md"))
            if chs:
                print(f"chapters: {len(chs)}")
        tracks = ["追踪/上下文.md", "追踪/伏笔.md", "追踪/时间线.md", "追踪/角色状态.md"]
        for t in tracks:
            if not (r / t).exists():
                issues.append(f"missing: {t}")
        if issues:
            for i in issues:
                print(i)
        else:
            print("project structure OK")
    except Exception as e:
        print(f"diagnose error: {e}")
        print("tip: check if project files contain special characters")

def cmd_contract(a):
    r=root(Path(a.project_root));s=load_state(r)
    pi=s.get("project",s.get("project_info",{}))
    d=r/".story-system";d.mkdir(parents=True,exist_ok=True)
    m={"route":{"primary_genre":pi.get("genre",""),"target_platform":"fanqie"},"versions":{"baseline_version":1}}
    (d/"MASTER_SETTING.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),"utf-8")
    print("baseline done")

def cmd_export(a):
    r=root(Path(a.project_root))
    chs=sorted((r/"正文").glob("第*.md"))
    if not chs:print("no chapters");return
    out=r/"导出";out.mkdir(exist_ok=True)
    f=out/f"{r.name}_完本.txt"
    with open(f,"w",encoding="utf-8") as fp:
        for ch in chs:fp.write(ch.read_text("utf-8")+"\n\n")
    print("exported:",f)

def cmd_commit(a):
    r=root(Path(a.project_root));ch=int(a.chapter)
    d=r/".story-system"/"commits";d.mkdir(parents=True,exist_ok=True)
    c={"chapter":ch,"timestamp":datetime.now().isoformat(),"status":"accepted"}
    (d/f"chapter_{ch:04d}.commit.json").write_text(json.dumps(c,ensure_ascii=False,indent=2),"utf-8")
    print(f"章节 {ch} 已提交")
    st=load_state(r)
    st.setdefault("progress",{})["current_chapter"]=ch
    save_state(r,st)

def cmd_review(a):
    """必须读取 --review-results 并处理实际数据。"""
    r=root(Path(a.project_root))
    
    # 读取审查结果
    review_file = Path(a.review_results) if hasattr(a, 'review_results') and a.review_results else None
    review_data = {}
    if review_file and review_file.exists():
        try:
            review_data = json.loads(review_file.read_text("utf-8"))
        except Exception as e:
            print(f"error reading review results: {e}", file=sys.stderr)
            sys.exit(1)
    
    # 生成报告
    rf=r/a.report_file
    rf.parent.mkdir(parents=True,exist_ok=True)
    
    # 构建真实报告内容
    blocking = review_data.get("blocking", [])
    suggestions = review_data.get("suggestions", [])
    
    report_content = f"""# 第 {a.chapter} 章审查报告

生成: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 阻断问题

"""
    if blocking:
        for item in blocking:
            report_content += f"- {item}\n"
    else:
        report_content += "无阻断问题\n"
    
    report_content += "\n## 建议\n\n"
    if suggestions:
        for item in suggestions:
            report_content += f"- {item}\n"
    else:
        report_content += "无建议\n"
    
    rf.write_text(report_content,"utf-8")
    print("审查报告:",rf)
    
    # 保存 metrics 如果指定
    if hasattr(a, 'save_metrics') and a.save_metrics:
        metrics_file = Path(a.metrics_out) if hasattr(a, 'metrics_out') and a.metrics_out else r/".novel"/"tmp"/"review_metrics.json"
        metrics_file.parent.mkdir(parents=True, exist_ok=True)
        metrics = {
            "chapter": a.chapter,
            "timestamp": datetime.now().isoformat(),
            "blocking_count": len(blocking),
            "suggestions_count": len(suggestions)
        }
        metrics_file.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), "utf-8")
        print("metrics saved:", metrics_file)

def cmd_memory(a):
    r=root(Path(a.project_root))
    mf=r/".novel"/"project_memory.json"
    if not mf.exists():
        mf.write_text(json.dumps({"patterns":[]},ensure_ascii=False,indent=2),"utf-8")
    mem=json.loads(mf.read_text("utf-8"))
    p={"pattern_type":a.pattern_type,"description":a.description,"importance":a.importance or "medium"}
    mem["patterns"].append(p)
    mf.write_text(json.dumps(mem,ensure_ascii=False,indent=2),"utf-8")
    print(f"pattern saved: {p['pattern_type']}")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--project-root",default=os.getcwd())
    s=p.add_subparsers(dest="cmd")
    
    s.add_parser("where").set_defaults(func=cmd_where)
    
    setup_parser = s.add_parser("setup")
    setup_parser.add_argument("--title", default="")
    setup_parser.add_argument("--author", default="")
    setup_parser.add_argument("--genre", default="")
    setup_parser.set_defaults(func=cmd_setup)
    
    s.add_parser("project-status").set_defaults(func=cmd_status)
    s.add_parser("doctor").set_defaults(func=cmd_doctor)
    s.add_parser("init-contract").set_defaults(func=cmd_contract)
    s.add_parser("export").set_defaults(func=cmd_export)
    
    p6=s.add_parser("chapter-commit")
    p6.add_argument("--chapter",required=True)
    p6.set_defaults(func=cmd_commit)
    
    p7=s.add_parser("review-pipeline")
    p7.add_argument("--chapter",required=True)
    p7.add_argument("--report-file",required=True)
    p7.add_argument("--review-results")
    p7.add_argument("--metrics-out")
    p7.add_argument("--save-metrics", action="store_true")
    p7.set_defaults(func=cmd_review)
    
    p8=s.add_parser("project-memory")
    p8.add_argument("action",choices=["add-pattern"])
    p8.add_argument("--pattern-type",required=True)
    p8.add_argument("--description",required=True)
    p8.add_argument("--importance")
    p8.set_defaults(func=cmd_memory)
    
    a=p.parse_args()
    if hasattr(a,"func"):a.func(a)
    else:p.print_help()

if __name__=="__main__":
    main()

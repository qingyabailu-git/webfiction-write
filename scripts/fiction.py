import argparse, json, os
from pathlib import Path
from datetime import datetime
def root(start):
    c=Path(start).resolve()
    for p in [c]+list(c.parents):
        if (p/".novel"/"state.json").exists():return p
    return c
def load_state(r):
    f=r/".novel"/"state.json"
    return json.loads(f.read_text("utf-8")) if f.exists() else {}
def save_state(r,s):
    f=r/".novel"/"state.json"
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(s,ensure_ascii=False,indent=2),"utf-8")
def cmd_where(a):print(root(Path(a.project_root)))
def cmd_status(a):
    r=root(Path(a.project_root));s=load_state(r)
    if not s:print("no state");return
    pi=s.get("project",s.get("project_info",{}))
    pr=s.get("progress",{})
    print("book:",pi.get("book_name",pi.get("title","?")))
    print("genre:",pi.get("genre","?"))
    print("writing_started:",pr.get("writing_started",False))
def cmd_doctor(a):
    r=root(Path(a.project_root));issues=[]
    for p in [".novel/state.json","设定集/主角卡.md","设定集/世界观.md","大纲/总纲.md"]:
        if not (r/p).exists():issues.append("missing: "+p)
    td=r/"正文"
    if td.exists():
        chs=sorted(td.glob("第*.md"))
        if chs:print("chapters:",len(chs))
    for t in ["追踪/上下文.md","追踪/伏笔.md","追踪/时间线.md","追踪/角色状态.md"]:
        if not (r/t).exists():issues.append("missing: "+t)
    if issues:
        for i in issues:print(i)
    else:print("project structure OK")
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
    r=root(Path(a.project_root))
    rf=r/a.report_file;rf.parent.mkdir(parents=True,exist_ok=True)
    rf.write_text(f"# 第 {a.chapter} 章审查报告\n\n生成: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n由 reviewer agent 输出。\n","utf-8")
    print("审查报告:",rf)
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
    s.add_parser("project-status").set_defaults(func=cmd_status)
    s.add_parser("doctor").set_defaults(func=cmd_doctor)
    s.add_parser("init-contract").set_defaults(func=cmd_contract)
    s.add_parser("export").set_defaults(func=cmd_export)
    p6=s.add_parser("chapter-commit");p6.add_argument("--chapter",required=True);p6.set_defaults(func=cmd_commit)
    p7=s.add_parser("review-pipeline");p7.add_argument("--chapter",required=True);p7.add_argument("--report-file",required=True);p7.add_argument("--review-results");p7.add_argument("--metrics-out");p7.add_argument("--save-metrics",action="store_true");p7.set_defaults(func=cmd_review)
    p8=s.add_parser("project-memory");p8.add_argument("action",choices=["add-pattern"]);p8.add_argument("--pattern-type",required=True);p8.add_argument("--description",required=True);p8.add_argument("--importance",default="medium");p8.set_defaults(func=cmd_memory)
    a=p.parse_args()
    if hasattr(a,"func"):a.func(a)
    else:p.print_help()
if __name__=="__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""novel.py - 网文创作引擎"""
import argparse, json, os
from pathlib import Path

def root(start):
    c = Path(start).resolve()
    for p in [c] + list(c.parents):
        if (p / ".novel" / "state.json").exists():
            return p
    return c

def load_state(r):
    f = r / ".novel" / "state.json"
    return json.loads(f.read_text("utf-8")) if f.exists() else {}

def write_state(r, s):
    f = r / ".novel" / "state.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(s, ensure_ascii=False, indent=2), "utf-8")

def cmd_where(a):
    print(root(Path(a.project_root)))

def cmd_status(a):
    r = root(Path(a.project_root)); s = load_state(r)
    if not s: print("no state"); return
    pi = s.get("project", s.get("project_info", {}))
    pr = s.get("progress", {})
    print("book:", pi.get("book_name", pi.get("title", "?")))
    print("genre:", pi.get("genre", "?"))
    print("writing_started:", pr.get("writing_started", False))

def cmd_doctor(a):
    r = root(Path(a.project_root)); issues = []
    for p in [".novel/state.json","设定集/主角卡.md","设定集/世界观.md","大纲/总纲.md"]:
        if not (r / p).exists(): issues.append("missing: "+p)
    td = r / "正文"
    if td.exists():
        chs = sorted(td.glob("第*.md"))
        if chs: print("chapters:", len(chs))
    for t in ["追踪/上下文.md","追踪/伏笔.md","追踪/时间线.md","追踪/角色状态.md"]:
        if not (r / t).exists(): issues.append("missing: "+t)
    if issues:
        for i in issues: print(i)

def cmd_contract(a):
    r = root(Path(a.project_root)); s = load_state(r)
    pi = s.get("project", s.get("project_info", {}))
    d = r / ".story-system"; d.mkdir(parents=True, exist_ok=True)
    m = {"route":{"primary_genre":pi.get("genre",""),"target_platform":"fanqie"},"versions":{"contract_version":1}}
    (d / "MASTER_SETTING.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),"utf-8")
    print("contract done")

def cmd_export(a):
    r = root(Path(a.project_root))
    chs = sorted((r / "正文").glob("第*.md"))
    if not chs: print("no chapters"); return
    out = r / "导出"; out.mkdir(exist_ok=True)
    f = out / f"{r.name}_完本.txt"
    with open(f,"w",encoding="utf-8") as fp:
        for ch in chs:
            fp.write(ch.read_text("utf-8")+"\n\n")
    print("exported:", f)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", default=os.getcwd())
    s = p.add_subparsers(dest="cmd")
    s.add_parser("where").set_defaults(func=cmd_where)
    s.add_parser("project-status").set_defaults(func=cmd_status)
    s.add_parser("doctor").set_defaults(func=cmd_doctor)
    s.add_parser("init-contract").set_defaults(func=cmd_contract)
    s.add_parser("export").set_defaults(func=cmd_export)
    a = p.parse_args()
    if hasattr(a,"func"): a.func(a)
    else: p.print_help()

if __name__ == "__main__":
    main()

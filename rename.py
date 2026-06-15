import os, re, shutil, subprocess
from pathlib import Path
BASE = Path("D:/codex测试文件/novel")
SKILLS = BASE / "skills"
SCRIPTS = BASE / "scripts"
renames = {"novel":"fiction","novel-conceive":"fiction-conceive","novel-setup":"fiction-setup","novel-start":"fiction-start","novel-plan":"fiction-plan","novel-write":"fiction-write","novel-revise":"fiction-revise","novel-review":"fiction-review","novel-polish":"fiction-polish","novel-query":"fiction-query","novel-learn":"fiction-learn","novel-doctor":"fiction-doctor","novel-export":"fiction-export","novel-scan":"fiction-scan","novel-analyze":"fiction-analyze","novel-import":"fiction-import"}
print("=== Step 1: Copy dirs ===")
for old_name, new_name in renames.items():
    src = SKILLS / old_name; dst = SKILLS / new_name
    if src.exists() and not dst.exists():
        shutil.copytree(str(src), str(dst))
        print(" ", old_name, "->", new_name)
old_py = SCRIPTS / "novel.py"; new_py = SCRIPTS / "fiction.py"
if old_py.exists() and not new_py.exists():
    shutil.copy2(str(old_py), str(new_py))
    print("  scripts/novel.py -> scripts/fiction.py")
print("=== Step 2: Fix file contents ===")
count = 0
for root, dirs, files in os.walk(str(SKILLS)):
    for f in files:
        if f not in ("SKILL.md", "openai.yaml"):
            continue
        fp = Path(root) / f
        text = fp.read_text("utf-8")
        new_text = text
        # Replace patterns carefully
        new_text = re.sub(r"\$novel-", "$fiction-", new_text)
        new_text = re.sub(r"lnovel-", "lfiction-", new_text)
        new_text = re.sub(r"/novel-", "/fiction-", new_text)
        new_text = re.sub(r"skills/novel/", "skills/fiction/", new_text)
        new_text = re.sub(r"skills/novel-", "skills/fiction-", new_text)
        new_text = re.sub(r"scripts/novel.py", "scripts/fiction.py", new_text)
        new_text = re.sub(r'display_name: "novel ', 'display_name: "fiction ', new_text)
        new_text = re.sub(r"^name: novel$", "name: fiction", new_text, flags=re.MULTILINE)
        new_text = re.sub(r"^name: novel-", "name: fiction-", new_text, flags=re.MULTILINE)
        if new_text != text:
            fp.write_text(new_text, "utf-8")
            count += 1
rm = BASE / "README.md"
text = rm.read_text("utf-8")
text = text.replace("# novel - 网文创作工具集", "# web-fiction - 网文创作工具集")
text = re.sub(r"/novel-", "/fiction-", text)
text = re.sub(r"`novel-", "`fiction-", text)
text = re.sub(r"skills/novel-", "skills/fiction-", text)
text = re.sub(r"skills/novel/", "skills/fiction/", text)
text = text.replace("scripts/novel.py", "scripts/fiction.py")
rm.write_text(text, "utf-8")
count += 1
runner = BASE / "test_run" / "test_runner.py"
if runner.exists():
    runner.write_text(runner.read_text("utf-8").replace("scripts/novel.py", "scripts/fiction.py"), "utf-8")
    count += 1
print("  Updated", count, "files")
print("=== Step 3: Git rename ===")
for old_name in renames.keys():
    p = SKILLS / old_name
    if p.exists():
        subprocess.run(["git", "-C", str(BASE), "rm", "-r", str(p)], capture_output=True)
        print("  git rm", old_name)
if old_py.exists():
    subprocess.run(["git", "-C", str(BASE), "rm", str(old_py)], capture_output=True)
    print("  git rm scripts/novel.py")
subprocess.run(["git", "-C", str(BASE), "add", "-A"], capture_output=True)
print("  git add -A")
print("=== Done ===")

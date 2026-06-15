import re
from pathlib import Path
BASE = Path("D:/codex测试文件/novel")
SKILLS = BASE / "skills"
count = 0
for p in list(SKILLS.glob("fiction*/SKILL.md")) + list(SKILLS.glob("fiction*/openai.yaml")):
    text = p.read_text("utf-8")
    new_text = text.replace("novel-", "fiction-")
    new_text = new_text.replace("webfiction-", "webnovel-")
    if new_text != text:
        p.write_text(new_text, "utf-8")
        count += 1
        print(" fixed:", str(p.relative_to(BASE)))
rm = BASE / "README.md"
txt = rm.read_text("utf-8")
txt = txt.replace("`novel-", "`fiction-")
txt = txt.replace("novel-", "fiction-")
txt = txt.replace("webfiction-writer", "webnovel-writer")
txt = txt.replace("webfiction-dashboard", "webnovel-dashboard")
rm.write_text(txt, "utf-8")
count += 1
print("Fixed", count, "files")
remaining = 0
for p in SKILLS.glob("fiction*/SKILL.md"):
    text = p.read_text("utf-8")
    refs = re.findall(r"\bnovel-", text)
    if refs:
        print("  STILL HAS: " + p.parent.name)
        remaining += 1
if remaining == 0:
    print("All fiction-* files clean!")
else:
    print(remaining, "files still have novel- references")

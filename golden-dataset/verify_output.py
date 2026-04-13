"""Verify output files contain all latest fixes."""
import csv, json, re, os, time

# --- CSV check ---
with open("output/golden_annotations.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

commit_err = [r for r in rows if r["has_task"] == "True" and r["task_sub_class"] == "Commitment"]
print(f"CSV: Commitment+HT=True errors: {len(commit_err)}")

kevin = [r for r in rows if "contract terms" in r["content"].lower() and r["from_user"] == "kevinzhang"]
for r in kevin:
    print(f"CSV: Kevin contract terms: HT={r['has_task']}, Sub={r['task_sub_class']}")

ht = sum(1 for r in rows if r["has_task"] == "True")
imp = sum(1 for r in rows if r["is_important"] == "True")
print(f"CSV: {len(rows)} rows, HT=TRUE={ht}, Imp=TRUE={imp}")

# --- JSON check ---
with open("output/chats.config.json", "r", encoding="utf-8") as f:
    chats = json.load(f)

total = sum(len(c.get("ChatMessages", [])) for c in chats)
rxns = sum(1 for c in chats for m in c.get("ChatMessages", []) if m.get("Reactions"))
fol = sum(1 for c in chats for m in c.get("ChatMessages", []) if m.get("Followed"))
sav = sum(1 for c in chats for m in c.get("ChatMessages", []) if m.get("Saved"))
rem = sum(1 for c in chats for m in c.get("ChatMessages", []) if m.get("Reminder"))
print(f"JSON: {len(chats)} chats, {total} msgs, Reactions={rxns}, Followed={fol}, Saved={sav}, Reminder={rem}")

# Happy emoji on negative msgs?
bad = 0
for c in chats:
    for m in c.get("ChatMessages", []):
        if not m.get("Reactions"):
            continue
        content = re.sub("<[^>]+>", "", m.get("Content", "")).lower()
        emoji = m["Reactions"][0]["Reaction"]
        if any(w in content for w in ["urgent", "outage", "breach", "threatening"]) and emoji in ["🎉", "😊", "❤️", "😂"]:
            bad += 1
print(f"JSON: Happy emoji on negative msgs: {bad}")

# File timestamps
for name in ["golden_annotations.csv", "chats.config.json", "review.html"]:
    t = os.path.getmtime(f"output/{name}")
    print(f"  {name}: {time.strftime('%Y-%m-%d %H:%M', time.localtime(t))}")

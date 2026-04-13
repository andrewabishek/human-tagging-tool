"""Find all messages with HT=True and Sub=Commitment (spec violation)."""
import csv

with open("output/golden_annotations.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

count = 0
for i, r in enumerate(rows):
    if r["has_task"] == "True" and r["task_sub_class"] == "Commitment":
        count += 1
        content = r["content"].replace("\n", " ")[:100]
        print(f"  [{i+1}] {r['from_user']}: {content}")
        print(f"       Conv={r['conversation_topic'][:50]}, Type={r['task_type']}, Attr={r['attribution']}, Imp={r['is_important']}")
        print()

print(f"\nTotal Commitment+HT=True errors: {count}")

"""
Export all 907 messages with their labels in a compact, reviewable format.
Output: audit_labels.txt
"""
import csv

with open("output/golden_annotations.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

with open("audit_labels.txt", "w", encoding="utf-8") as out:
    current_conv = None
    for i, r in enumerate(rows):
        conv_id = r["conversation_id"]
        if conv_id != current_conv:
            current_conv = conv_id
            out.write(f"\n{'='*80}\n")
            out.write(f"CONV: {r['conversation_topic']} ({r['chat_type']}, {r['domain']})\n")
            out.write(f"{'='*80}\n")

        # Compact label line
        ht = "T" if r["has_task"] == "True" else "F"
        imp = "T" if r["is_important"] == "True" else "F"
        sub = r["task_sub_class"] if r["has_task"] == "True" else ""
        tt = r["task_type"] if r["has_task"] == "True" else ""
        attr = r["attribution"] if r["has_task"] == "True" else ""
        assign = r["assignee"] if r["has_task"] == "True" else ""
        edge = r["edge_case"]
        notes = r["notes"]

        content = r["content"].replace("\n", " | ")
        if len(content) > 150:
            content = content[:150] + "..."

        out.write(f"\n[{i+1}] {r['from_user']}: {content}\n")
        label_parts = [f"HT={ht}"]
        if ht == "T":
            label_parts.append(f"Sub={sub}")
            label_parts.append(f"Type={tt}")
            label_parts.append(f"Attr={attr}")
            if assign:
                label_parts.append(f"To={assign}")
        label_parts.append(f"Imp={imp}")
        if edge:
            label_parts.append(f"Edge={edge}")
        if notes:
            short_notes = notes[:80] + "..." if len(notes) > 80 else notes
            label_parts.append(f"Notes={short_notes}")
        out.write(f"     {', '.join(label_parts)}\n")

print(f"Written {len(rows)} messages to audit_labels.txt")

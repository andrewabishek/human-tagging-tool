"""
Fix all Commitment messages incorrectly labeled as has_task=True.
Per spec: Commitment (sender's own plan) = HasTask=FALSE.

This script patches the source Python files in-place.
"""
import re

# All commitment messages to fix, grouped by file
# Format: (line_number, old_pattern_snippet, message_start_text)
FIXES_1ON1 = {
    "conversations_1on1.py": [
        # [119] sofiarodriguez: "Yes, please go ahead..."
        {
            "old": '''m("sofiarodriguez", "Yes, please go ahead. Their legal contact is Rebecca Walsh — I'll send you her email.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Self-initiated action — Sofia commits to sending contact info",
              edge_case="self_initiated_task"),''',
            "new": '''m("sofiarodriguez", "Yes, please go ahead. Their legal contact is Rebecca Walsh — I'll send you her email.",
              notes="Commitment — Sofia commits to sending contact info"),''',
        },
        # [139] lisanakamura: "Got quotes from all three vendors..."
        {
            "old": '''m("lisanakamura", "Got quotes from all three vendors. The Figma renewal is 12% higher than last year. Slack and Zoom are comparable. I'll send you the comparison spreadsheet.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["lisanakamura"],
              notes="Self-initiated action — Lisa commits to sending comparison",
              edge_case="self_initiated_action"),''',
            "new": '''m("lisanakamura", "Got quotes from all three vendors. The Figma renewal is 12% higher than last year. Slack and Zoom are comparable. I'll send you the comparison spreadsheet.",
              notes="Commitment — Lisa commits to sending comparison"),''',
        },
        # [140] kevinzhang: "12% increase on Figma? That's steep..." — change from HT=F to HT=T
        {
            "old": '''m("kevinzhang", "12% increase on Figma? That's steep. Let me know the contract terms — I may want to negotiate.",
              notes="Informational reaction — no specific task assigned"),''',
            "new": '''m("kevinzhang", "12% increase on Figma? That's steep. Let me know the contract terms — I may want to negotiate.",
              has_task=True, sub_class="RfK", task_type="Action Request",
              attribution="Implicit", assignee=["lisanakamura"],
              notes="Requests contract terms — implicit ask to Lisa"),''',
        },
    ],
}

def apply_fixes(filename, fixes):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    applied = 0
    for fix in fixes:
        if fix["old"] in content:
            content = content.replace(fix["old"], fix["new"], 1)
            applied += 1
        else:
            print(f"  WARNING: Could not find pattern in {filename}:")
            print(f"    {fix['old'][:80]}...")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  {filename}: {applied}/{len(fixes)} fixes applied")
    return applied

# Apply 1on1 fixes
total = 0
for fn, fixes in FIXES_1ON1.items():
    total += apply_fixes(fn, fixes)

print(f"\nTotal fixes applied (1on1): {total}")

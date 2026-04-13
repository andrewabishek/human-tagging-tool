"""
Fix all Commitment messages incorrectly labeled as has_task=True.
Per spec: Commitment (sender's own plan) = HasTask=FALSE.

Strategy: Find each line with `has_task=True, sub_class="Commitment"`,
then replace from that line through the closing `notes="..."),` line
with just the notes line (and is_important if present).
"""
import re

def fix_commitment_blocks(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixed = 0
    result = []
    i = 0
    while i < len(lines):
        if 'has_task=True, sub_class="Commitment"' in lines[i]:
            # Collect the block from this line through the line ending with "),"
            block_lines = [lines[i]]
            j = i
            # Check if this line itself ends the block
            if lines[i].rstrip().endswith("),"):
                pass  # block is just this one line
            else:
                j = i + 1
                while j < len(lines):
                    block_lines.append(lines[j])
                    if lines[j].rstrip().rstrip("\n").endswith("),"):
                        break
                    j += 1
            
            block = "".join(block_lines)
            
            # Extract notes
            notes_match = re.search(r'notes="([^"]*)"', block)
            notes = notes_match.group(1) if notes_match else "Commitment"
            
            # Clean up notes
            for old, new in [
                ("Self-assigned commitment → HasTask=TRUE, assignee=sender", "Commitment — sender commits"),
                ("Self-assigned — ", "Commitment — "),
                ("Self-assigned by ", "Commitment — "),
                ("Self-assigned commitment with external dependency", "Commitment — sender commits (with external dependency)"),
                ("Self-assigned commitment triggered by group question", "Commitment — sender commits"),
                ("Self-assigned commitment — accelerated timeline", "Commitment — sender commits with accelerated timeline"),
                ("Self-assigned commitment by QA lead", "Commitment — QA lead commits"),
                ("Self-assigned commitment to share contact", "Commitment — sender commits to share contact"),
                ("Self-assigned commitment to investigate and fix", "Commitment — sender commits to investigate and fix"),
                ("Self-assigned commitment", "Commitment — sender commits"),
                ("Self-directed commitment to act", "Commitment — sender commits"),
                ("Self-directed commitment", "Commitment — sender commits"),
                ("Self-initiated action — ", "Commitment — "),
                ("Self-assigned by replying with commitment", "Commitment — sender commits"),
                ("Self-assigned by acting on it", "Commitment — sender acting on it"),
                ("Self-assigned by volunteering in reply", "Commitment — sender volunteers"),
            ]:
                if old in notes:
                    notes = notes.replace(old, new)
                    break
            
            if not notes.startswith("Commitment"):
                notes = f"Commitment — {notes}"
            
            # Check for is_important and edge_case
            is_imp = "is_important=True" in block
            edge_match = re.search(r'edge_case="([^"]*)"', block)
            
            # Build replacement lines
            indent = "              "
            new_parts = []
            if is_imp:
                new_parts.append(f"{indent}is_important=True,\n")
            if edge_match:
                new_parts.append(f'{indent}edge_case="{edge_match.group(1)}",\n')
            new_parts.append(f'{indent}notes="{notes}"),\n')
            
            result.extend(new_parts)
            i = j + 1
            fixed += 1
        else:
            result.append(lines[i])
            i += 1
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(result)
    
    return fixed


files = [
    "conversations_1on1.py",
    "conversations_supplemental.py",
    "conversations_group.py",
    "conversations_meeting.py",
]

total = 0
for fn in files:
    n = fix_commitment_blocks(fn)
    print(f"  {fn}: {n} fixes")
    total += n

print(f"\nTotal commitment blocks fixed: {total}")

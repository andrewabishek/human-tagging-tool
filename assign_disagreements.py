"""
Find ALL has_task disagreements:
  1. Between any two judges on the same conversation
  2. Between any judge and the ground truth (GT)
Then assign tiebreaker:
  - If Andrew Abishek already tagged → assign to Jo
  - If Jo already tagged (but not Andrew) → assign to Andrew Abishek
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client
from collections import defaultdict

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

tags = db.table('conversation_tags').select(
    'conversation_id, judge_name, has_task, conversations(id, topic, source_row_index, chat_type, ground_truth_has_task)'
).execute()

by_conv = defaultdict(list)
for t in tags.data:
    by_conv[t['conversation_id']].append(t)

# Find all conversations with ANY disagreement (judge-judge or judge-GT)
disagree_convs = []

for conv_id, conv_tags in by_conv.items():
    c = conv_tags[0]['conversations']
    idx = c['source_row_index'] + 1
    gt = c['ground_truth_has_task']
    judge_vals = {t['judge_name']: t['has_task'] for t in conv_tags}

    reasons = []

    # Check judge-judge disagreements
    vals = set(judge_vals.values())
    if len(vals) > 1:
        pairs = []
        names = list(judge_vals.keys())
        for i in range(len(names)):
            for j in range(i+1, len(names)):
                if judge_vals[names[i]] != judge_vals[names[j]]:
                    pairs.append(f"{names[i]}={judge_vals[names[i]]} vs {names[j]}={judge_vals[names[j]]}")
        reasons.append("Judge-Judge: " + "; ".join(pairs))

    # Check judge-GT disagreements
    gt_disagrees = []
    for jname, jval in judge_vals.items():
        if jval != gt:
            gt_disagrees.append(f"{jname}={jval}")
    if gt_disagrees:
        reasons.append(f"Judge-GT (GT={gt}): " + "; ".join(gt_disagrees))

    if reasons:
        has_andrew = 'Andrew Abishek' in judge_vals
        has_jo = 'Jo' in judge_vals
        disagree_convs.append({
            'conv_id': conv_id,
            'idx': idx,
            'topic': c['topic'],
            'gt': gt,
            'judge_vals': judge_vals,
            'reasons': reasons,
            'has_andrew': has_andrew,
            'has_jo': has_jo,
        })

disagree_convs.sort(key=lambda x: x['idx'])

print("=" * 90)
print(f"ALL DISAGREEMENTS: {len(disagree_convs)} conversations")
print("=" * 90)

assign_to_jo = []
assign_to_andrew = []

for d in disagree_convs:
    print(f"\n  #{d['idx']} {d['topic'][:65]}")
    print(f"    GT={d['gt']}  Judges: {d['judge_vals']}")
    for r in d['reasons']:
        print(f"    {r}")

    if d['has_andrew']:
        tiebreaker = 'Jo'
        assign_to_jo.append(d)
    else:
        tiebreaker = 'Andrew Abishek'
        assign_to_andrew.append(d)
    print(f"    → ASSIGN TIEBREAKER TO: {tiebreaker}")

print("\n" + "=" * 90)
print("ASSIGNMENT SUMMARY")
print("=" * 90)
print(f"  Assign to Jo: {len(assign_to_jo)} conversations")
for d in assign_to_jo:
    print(f"    #{d['idx']} {d['topic'][:60]}")
print(f"  Assign to Andrew Abishek: {len(assign_to_andrew)} conversations")
for d in assign_to_andrew:
    print(f"    #{d['idx']} {d['topic'][:60]}")

# Now create assignments
print("\n" + "=" * 90)
print("CREATING TIEBREAKER ASSIGNMENTS")
print("=" * 90)

ok = 0
fail = 0
for d in disagree_convs:
    tiebreaker = 'Jo' if d['has_andrew'] else 'Andrew Abishek'
    try:
        # Check if assignment already exists
        existing = db.table('conversation_assignments').select('id').eq(
            'conversation_id', d['conv_id']
        ).eq('judge_name', tiebreaker).execute()

        if existing.data:
            print(f"  #{d['idx']} → {tiebreaker} (assignment already exists, marking tiebreaker)")
            db.table('conversation_assignments').update({
                'is_tiebreaker': True
            }).eq('id', existing.data[0]['id']).execute()
        else:
            db.table('conversation_assignments').insert({
                'conversation_id': d['conv_id'],
                'judge_name': tiebreaker,
                'is_tiebreaker': True,
            }).execute()
            print(f"  #{d['idx']} → {tiebreaker} (new tiebreaker assignment created)")
        ok += 1
    except Exception as e:
        print(f"  #{d['idx']} → {tiebreaker} FAILED: {e}")
        fail += 1

print(f"\nDone: {ok} succeeded, {fail} failed")

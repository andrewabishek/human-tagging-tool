"""
Identify the trickiest conversations for calibration assignments.
Tricky = GT disagreements + judge-judge disagreements + borderline cases.
Score each conversation by trickiness.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client
from collections import defaultdict

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

tags = db.table('conversation_tags').select(
    'conversation_id, judge_name, has_task, is_important, task_type, attribution, '
    'conversations(id, topic, source_row_index, chat_type, ground_truth_has_task)'
).execute()

by_conv = defaultdict(list)
for t in tags.data:
    by_conv[t['conversation_id']].append(t)

scored = []
for conv_id, conv_tags in by_conv.items():
    c = conv_tags[0]['conversations']
    idx = c['source_row_index'] + 1
    gt = c['ground_truth_has_task']
    judge_vals = {t['judge_name']: t['has_task'] for t in conv_tags}

    score = 0
    reasons = []

    # 1. Judge-GT disagreement (any judge disagrees with GT)
    gt_disagrees = [j for j, v in judge_vals.items() if v != gt]
    if gt_disagrees:
        score += 3 * len(gt_disagrees)
        reasons.append(f"GT-disagree({len(gt_disagrees)} judges)")

    # 2. Judge-judge disagreement
    if len(set(judge_vals.values())) > 1:
        score += 5
        reasons.append("Judge-judge disagree")

    # 3. Borderline: has_task=TRUE but attribution=Implicit (softer signal)
    implicit_true = [t for t in conv_tags if t['has_task'] == True and t.get('attribution') == 'Implicit']
    if implicit_true:
        score += 2
        reasons.append("Implicit+TRUE")

    # 4. is_important disagreement between judges
    imp_vals = set(t['is_important'] for t in conv_tags if t['is_important'] is not None)
    if len(imp_vals) > 1:
        score += 2
        reasons.append("IsImportant-disagree")

    # 5. Task type variety (judges tagged different task types)
    task_types = set(t['task_type'] for t in conv_tags if t['task_type'])
    if len(task_types) > 1:
        score += 2
        reasons.append(f"TaskType-disagree({task_types})")

    # 6. Edge-case chat types
    if c['chat_type'] in ('OneOnOne', 'Meeting'):
        score += 1
        reasons.append(f"ChatType={c['chat_type']}")

    if score > 0:
        scored.append({
            'conv_id': conv_id,
            'idx': idx,
            'topic': c['topic'],
            'gt': gt,
            'score': score,
            'reasons': reasons,
            'judge_vals': judge_vals,
            'num_judges': len(conv_tags),
        })

scored.sort(key=lambda x: (-x['score'], x['idx']))

# Check Utkarsh's current state
utkarsh_tagged = set()
utkarsh_assigned = set()
for t in tags.data:
    if t['judge_name'] == 'Utkarsh Jha':
        utkarsh_tagged.add(t['conversation_id'])

assignments = db.table('conversation_assignments').select('conversation_id, judge_name').eq('judge_name', 'Utkarsh Jha').execute()
for a in assignments.data:
    utkarsh_assigned.add(a['conversation_id'])

print(f"Utkarsh Jha: {len(utkarsh_tagged)} tagged, {len(utkarsh_assigned)} assigned")
print(f"Tricky conversations found: {len(scored)}")
print()

print("TOP 20 TRICKIEST CONVERSATIONS:")
print(f"{'#':>4} {'Score':>5} {'Judges':>6} {'GT':>6} | {'Topic':<55} | Reasons")
print("-" * 120)
for s in scored[:20]:
    tag_str = ", ".join(f"{j}={v}" for j, v in s['judge_vals'].items())
    print(f"#{s['idx']:>3} {s['score']:>5} {s['num_judges']:>6} {str(s['gt']):>6} | {s['topic'][:55]:<55} | {', '.join(s['reasons'])}")

# Pick 10 for Utkarsh: highest score, not already tagged/assigned by Utkarsh
candidates = [s for s in scored if s['conv_id'] not in utkarsh_tagged and s['conv_id'] not in utkarsh_assigned]
pick = candidates[:10]

print(f"\n\nRECOMMENDED 10 FOR UTKARSH (not already tagged/assigned by him):")
print(f"{'#':>4} {'Score':>5} {'Judges':>6} {'GT':>6} | {'Topic':<55} | Reasons")
print("-" * 120)
for s in pick:
    print(f"#{s['idx']:>3} {s['score']:>5} {s['num_judges']:>6} {str(s['gt']):>6} | {s['topic'][:55]:<55} | {', '.join(s['reasons'])}")

# Save the pick list for the next step
import json
with open('tricky_picks.json', 'w', encoding='utf-8') as f:
    json.dump({
        'utkarsh_picks': [{'conv_id': s['conv_id'], 'idx': s['idx'], 'topic': s['topic']} for s in pick],
        'all_tricky_ranked': [{'conv_id': s['conv_id'], 'idx': s['idx'], 'topic': s['topic'], 'score': s['score']} for s in scored],
    }, f, indent=2)
print(f"\nSaved tricky_picks.json with ranked list for future assignments.")

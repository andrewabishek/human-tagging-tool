"""Analyze disagreements and single-judge conversations"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client
from collections import defaultdict

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

# Get all tags with conversation info
tags = db.table('conversation_tags').select('*, conversations(id, topic, source_row_index, chat_type, ground_truth_has_task)').execute()

# Group by conversation
by_conv = defaultdict(list)
for t in tags.data:
    by_conv[t['conversation_id']].append(t)

print("=" * 100)
print("SECTION 1: DISAGREEMENTS (has_task differs between judges)")
print("=" * 100)
disagree_convs = []
for conv_id, conv_tags in sorted(by_conv.items(), key=lambda x: x[1][0]['conversations']['source_row_index']):
    has_task_values = set(t['has_task'] for t in conv_tags)
    if len(has_task_values) > 1:  # disagreement
        c = conv_tags[0]['conversations']
        idx = c['source_row_index'] + 1
        judges_involved = [(t['judge_name'], t['has_task']) for t in conv_tags]
        andrew_involved = any(t['judge_name'] == 'Andrew Abishek' for t in conv_tags)
        print(f"\n  #{idx} [{c['chat_type']}] {c['topic']} (GT={c['ground_truth_has_task']})")
        for jn, ht in judges_involved:
            print(f"    {jn:20s} -> HasTask={ht}")
        print(f"    Andrew already assigned: {andrew_involved}")
        disagree_convs.append((conv_id, idx, c['topic'], andrew_involved))

print(f"\nTotal disagreements: {len(disagree_convs)}")

print("\n" + "=" * 100)
print("SECTION 2: SINGLE-JUDGE CONVERSATIONS (only 1 tag, not by Utkarsh or Andrew)")
print("=" * 100)
single_judge_need_tag = []
for conv_id, conv_tags in sorted(by_conv.items(), key=lambda x: x[1][0]['conversations']['source_row_index']):
    if len(conv_tags) == 1:
        t = conv_tags[0]
        c = t['conversations']
        jn = t['judge_name']
        if jn not in ('Andrew Abishek', 'Utkarsh Jha'):
            idx = c['source_row_index'] + 1
            print(f"  #{idx} [{c['chat_type']}] {c['topic']} | Judge={jn} | HasTask={t['has_task']} | GT={c['ground_truth_has_task']}")
            single_judge_need_tag.append(conv_id)

print(f"\nTotal single-judge needing LLM tag: {len(single_judge_need_tag)}")

print("\n" + "=" * 100)
print("SECTION 3: ALL SINGLE-JUDGE CONVERSATIONS (for reference)")
print("=" * 100)
for conv_id, conv_tags in sorted(by_conv.items(), key=lambda x: x[1][0]['conversations']['source_row_index']):
    if len(conv_tags) == 1:
        t = conv_tags[0]
        c = t['conversations']
        idx = c['source_row_index'] + 1
        print(f"  #{idx} [{c['chat_type']}] {c['topic'][:55]:55s} | Judge={t['judge_name']:20s} | HasTask={t['has_task']}")

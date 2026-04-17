"""Final verification: check all tags, disagreements, and coverage"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client
from collections import defaultdict, Counter

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

tags = db.table('conversation_tags').select('*, conversations(id, topic, source_row_index, chat_type, ground_truth_has_task)').execute()
all_convs = db.table('conversations').select('id, topic, source_row_index').execute()

# Stats
print("=" * 80)
print("FINAL DB STATE")
print("=" * 80)
print(f"Total tags: {len(tags.data)}")
judges = Counter(t['judge_name'] for t in tags.data)
for j, c in sorted(judges.items()):
    print(f"  {j}: {c} tags")

by_conv = defaultdict(list)
for t in tags.data:
    by_conv[t['conversation_id']].append(t)

tagged_ids = set(by_conv.keys())
all_ids = set(c['id'] for c in all_convs.data)
untagged = all_ids - tagged_ids
print(f"\nConversations tagged: {len(tagged_ids)}/{len(all_ids)}")
print(f"Conversations with 0 tags: {len(untagged)}")

# Coverage by tag count
tag_counts = Counter(len(v) for v in by_conv.values())
for cnt in sorted(tag_counts.keys()):
    print(f"  {cnt} judge(s): {tag_counts[cnt]} conversations")

# Disagreements
print("\n" + "=" * 80)
print("HAS_TASK DISAGREEMENTS")
print("=" * 80)
disagree_count = 0
for conv_id, conv_tags in sorted(by_conv.items(), key=lambda x: x[1][0]['conversations']['source_row_index']):
    has_task_values = set(t['has_task'] for t in conv_tags)
    if len(has_task_values) > 1:
        c = conv_tags[0]['conversations']
        idx = c['source_row_index'] + 1
        print(f"\n  #{idx} [{c['chat_type']}] {c['topic']} (GT={c['ground_truth_has_task']})")
        for t in conv_tags:
            print(f"    {t['judge_name']:20s} -> HasTask={t['has_task']}")
        disagree_count += 1

if disagree_count == 0:
    print("  None!")
else:
    print(f"\nTotal disagreements: {disagree_count}")

# Andrew Abishek GT accuracy
print("\n" + "=" * 80)
print("ANDREW ABISHEK GT ACCURACY (all tags)")
print("=" * 80)
andrew_tags = [t for t in tags.data if t['judge_name'] == 'Andrew Abishek']
agree = 0
disagrees = []
for t in andrew_tags:
    gt = t['conversations']['ground_truth_has_task']
    if t['has_task'] == gt:
        agree += 1
    else:
        c = t['conversations']
        disagrees.append((c['source_row_index']+1, c['topic'][:50], t['has_task'], gt))

print(f"Agreement: {agree}/{len(andrew_tags)} ({100*agree/len(andrew_tags):.1f}%)")
for idx, topic, mine, gt in sorted(disagrees):
    print(f"  DISAGREE #{idx}: {topic} | Andrew={mine} GT={gt}")

# Conversations needing tiebreaker (disagreement exists)
print("\n" + "=" * 80)
print("CONVERSATIONS NEEDING TIEBREAKER ASSIGNMENT")
print("=" * 80)
need_tiebreaker = []
for conv_id, conv_tags in sorted(by_conv.items(), key=lambda x: x[1][0]['conversations']['source_row_index']):
    has_task_values = set(t['has_task'] for t in conv_tags)
    if len(has_task_values) > 1:
        c = conv_tags[0]['conversations']
        andrew_in = any(t['judge_name'] == 'Andrew Abishek' for t in conv_tags)
        need_tiebreaker.append((conv_id, c['source_row_index']+1, c['topic'], andrew_in))
        print(f"  #{c['source_row_index']+1} {c['topic'][:60]} | Andrew already in: {andrew_in}")

if not need_tiebreaker:
    print("  None — no disagreements exist!")

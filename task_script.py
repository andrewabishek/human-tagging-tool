from supabase import create_client
import json

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

# 1. Get all human tags with conversation details
tags = db.table('conversation_tags').select('*, conversations(id, conversation_id, topic, chat_type, source_row_index, ground_truth_has_task)').execute()
print(f"=== HUMAN TAGS: {len(tags.data)} ===")
for t in sorted(tags.data, key=lambda x: x['conversations']['source_row_index']):
    c = t['conversations']
    assignees = t.get('task_assignees', '')
    print(f"  #{c['source_row_index']+1} [{c['chat_type']}] {c['topic'][:50]}")
    print(f"    GT={c['ground_truth_has_task']} | Judge={t['judge_name']} | HasTask={t['has_task']} | Important={t['is_important']} | Type={t.get('task_type','')!r} | Attr={t.get('attribution','')!r} | Assignees={assignees!r}")
    print()

# 2. Get tagged conversation IDs
tagged_conv_ids = set(t['conversation_id'] for t in tags.data)
print(f"\n=== TAGGED CONVERSATION IDS: {len(tagged_conv_ids)} unique ===")

# 3. Get all conversations
all_convs = db.table('conversations').select('id, conversation_id, topic, chat_type, source_row_index, ground_truth_has_task').order('source_row_index').execute()
print(f"=== TOTAL CONVERSATIONS: {len(all_convs.data)} ===")

# 4. Find untagged
untagged = [c for c in all_convs.data if c['id'] not in tagged_conv_ids]
print(f"=== UNTAGGED: {len(untagged)} ===")
for c in untagged:
    print(f"  #{c['source_row_index']+1} [{c['chat_type']}] {c['topic'][:60]} | GT={c['ground_truth_has_task']}")

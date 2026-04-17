"""Fetch messages for the 43 non-Jo single-judge conversations"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client
from collections import defaultdict

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

# Get all tags
tags = db.table('conversation_tags').select('conversation_id, judge_name').execute()
by_conv = defaultdict(list)
for t in tags.data:
    by_conv[t['conversation_id']].append(t['judge_name'])

# Find single-judge convs not by Andrew or Utkarsh, and not by Jo (already have those)
target_ids = []
for conv_id, judges in by_conv.items():
    if len(judges) == 1 and judges[0] not in ('Andrew Abishek', 'Utkarsh Jha', 'Jo'):
        target_ids.append(conv_id)

print(f"Need to fetch {len(target_ids)} conversations")

# Fetch conversations + messages
results = []
for cid in sorted(target_ids):
    c = db.table('conversations').select('*').eq('id', cid).execute()
    msgs = db.table('messages').select('message_index, speaker_name, message_text').eq('conversation_id', cid).order('message_index').execute()
    
    conv = c.data[0]
    results.append({
        'db_id': conv['id'],
        'source_row_index': conv['source_row_index'],
        'topic': conv['topic'],
        'chat_type': conv['chat_type'],
        'ground_truth_has_task': conv['ground_truth_has_task'],
        'messages': [{'idx': m['message_index'], 'speaker': m['speaker_name'], 'text': m['message_text']} for m in msgs.data]
    })

results.sort(key=lambda x: x['source_row_index'])

with open('remaining_single_judge.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Saved {len(results)} conversations to remaining_single_judge.json")
for r in results:
    print(f"  #{r['source_row_index']+1} [{r['chat_type']}] {r['topic']} ({len(r['messages'])} msgs)")

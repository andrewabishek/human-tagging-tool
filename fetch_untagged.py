import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

# Get tagged conversation IDs
tags = db.table('conversation_tags').select('conversation_id').execute()
tagged_ids = set(t['conversation_id'] for t in tags.data)

# Get all conversations
all_convs = db.table('conversations').select('*').order('source_row_index').execute()
untagged = [c for c in all_convs.data if c['id'] not in tagged_ids]

print(f"Untagged conversations: {len(untagged)}")

results = []
for c in untagged:
    msgs = db.table('messages').select('message_index, speaker_name, message_text').eq('conversation_id', c['id']).order('message_index').execute()
    
    conv_data = {
        'db_id': c['id'],
        'source_row_index': c['source_row_index'],
        'topic': c['topic'],
        'chat_type': c['chat_type'],
        'ground_truth_has_task': c['ground_truth_has_task'],
        'messages': []
    }
    for m in msgs.data:
        conv_data['messages'].append({
            'idx': m['message_index'],
            'speaker': m['speaker_name'],
            'text': m['message_text']
        })
    results.append(conv_data)

with open('untagged_conversations.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Saved {len(results)} conversations to untagged_conversations.json")
for r in results:
    print(f"  #{r['source_row_index']+1} [{r['chat_type']}] {r['topic']} ({len(r['messages'])} msgs)")

"""Check which conversations have only 1 judge"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client
from collections import defaultdict

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')
tags = db.table('conversation_tags').select('conversation_id, judge_name, has_task, conversations(id, topic, source_row_index, chat_type, ground_truth_has_task)').execute()

by_conv = defaultdict(list)
for t in tags.data:
    by_conv[t['conversation_id']].append(t)

print("Conversations with only 1 judge:")
for conv_id, conv_tags in sorted(by_conv.items(), key=lambda x: x[1][0]['conversations']['source_row_index']):
    if len(conv_tags) == 1:
        c = conv_tags[0]['conversations']
        t = conv_tags[0]
        print(f"  #{c['source_row_index']+1} {c['topic'][:60]} | Judge: {t['judge_name']} | HasTask={t['has_task']}")

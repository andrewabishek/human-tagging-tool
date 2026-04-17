"""Assign 10 tricky conversations to Utkarsh Jha"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

with open('tricky_picks.json', 'r', encoding='utf-8') as f:
    picks = json.load(f)

utkarsh_picks = picks['utkarsh_picks']

# Check existing assignments for Utkarsh
existing = db.table('conversation_assignments').select('conversation_id').eq('judge_name', 'Utkarsh Jha').execute()
existing_ids = set(a['conversation_id'] for a in existing.data)

ok = 0
skip = 0
fail = 0
for p in utkarsh_picks:
    if p['conv_id'] in existing_ids:
        print(f"  SKIP #{p['idx']} {p['topic'][:60]} (already assigned)")
        skip += 1
        continue
    try:
        db.table('conversation_assignments').insert({
            'conversation_id': p['conv_id'],
            'judge_name': 'Utkarsh Jha',
        }).execute()
        print(f"  OK   #{p['idx']} {p['topic'][:60]}")
        ok += 1
    except Exception as e:
        print(f"  FAIL #{p['idx']} {p['topic'][:60]} | {e}")
        fail += 1

print(f"\nDone: {ok} assigned, {skip} skipped (existing), {fail} failed")

# Show Utkarsh's total assignments now
total = db.table('conversation_assignments').select('conversation_id').eq('judge_name', 'Utkarsh Jha').execute()
print(f"Utkarsh Jha now has {len(total.data)} total assignments")

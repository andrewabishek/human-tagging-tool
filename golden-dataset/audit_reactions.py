"""Audit all reactions in the generated dataset for semantic validity."""
import json, re

with open('output/chats.config.json', 'r', encoding='utf-8') as f:
    chats = json.load(f)

def strip_html(s):
    return re.sub(r'<[^>]+>', '', s).strip()

count = 0
for chat in chats:
    topic = chat.get('Topic', 'N/A')
    chat_type = chat.get('ChatType', '?')
    raw_members = chat.get('Members', [])
    members = [m.get('MailNickName','?') if isinstance(m, dict) else m for m in raw_members]
    for msg in chat.get('ChatMessages', []):
        reactions = msg.get('Reactions', [])
        if reactions:
            count += 1
            content = strip_html(msg.get('Content', ''))[:160]
            sender = msg.get('From', '?')
            parts = []
            for r in reactions:
                parts.append(f"{r['Reaction']} {r['Sender']}")
            rxn_str = ', '.join(parts)
            print(f"[{count}] {topic} ({chat_type})")
            print(f"    FROM: {sender}")
            print(f"    MSG:  {content}")
            print(f"    RXN:  {rxn_str}")
            print()

print(f"Total messages with reactions: {count}")

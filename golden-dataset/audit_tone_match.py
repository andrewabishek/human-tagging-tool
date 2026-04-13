"""Quick audit: check that each reaction emoji matches the detected tone."""
import json, re
from interaction_signals import _detect_tone, TONE_EMOJI_MAP

with open("output/chats.config.json", "r", encoding="utf-8") as f:
    chats = json.load(f)

# Build reverse mapping: emoji -> list of acceptable tones
emoji_tones = {}
for tone, emojis in TONE_EMOJI_MAP.items():
    for e in emojis:
        emoji_tones.setdefault(e, []).append(tone)

# Also, 👍 is acceptable for neutral, agreement, completion, volunteering
# (it appears in multiple pools), so we don't flag it unless tone is negative

NEGATIVE_EMOJIS = {"🎉", "🔥", "💯", "❤️", "😂", "😊", "👏"}
# These emojis should NEVER appear on negative-tone messages

issues = []
total = 0
for chat in chats:
    ctype = chat.get("ChatType", "Unknown")
    for msg in chat.get("ChatMessages", []):
        rxns = msg.get("Reactions", [])
        if not rxns:
            continue
        total += 1
        content = re.sub("<[^>]+>", "", msg.get("Content", ""))
        tone = _detect_tone(content)
        emoji = rxns[0].get("Reaction", "")
        sender = msg.get("SenderDisplayName", "?")
        reactor = rxns[0].get("Sender", "?")

        # Flag 1: Happy emoji on negative message
        if tone == "negative" and emoji in NEGATIVE_EMOJIS:
            issues.append({
                "type": "NEGATIVE+HAPPY",
                "tone": tone,
                "emoji": emoji,
                "sender": sender,
                "reactor": reactor,
                "msg": content[:120],
            })

        # Flag 2: 👀 on non-negative message (eyes = concern, shouldn't be on positive)
        if tone not in ("negative",) and emoji == "👀":
            # 👀 on questions or risk-adjacent messages is OK - only flag clearly wrong
            if tone in ("appreciative", "humor", "celebratory"):
                issues.append({
                    "type": "EYES+POSITIVE",
                    "tone": tone,
                    "emoji": emoji,
                    "sender": sender,
                    "reactor": reactor,
                    "msg": content[:120],
                })

print(f"Total reacted messages: {total}")
print(f"Issues found: {len(issues)}")
print()
for i, issue in enumerate(issues, 1):
    print(f"[{i}] {issue['type']}: tone={issue['tone']}, emoji={issue['emoji']}")
    print(f"    FROM: {issue['sender']}")
    print(f"    MSG:  {issue['msg']}")
    print(f"    RXN:  {issue['emoji']} {issue['reactor']}")
    print()

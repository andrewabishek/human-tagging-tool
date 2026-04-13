"""
Full audit of golden dataset:
  1. Followed signals — do they make sense on those messages?
  2. Saved signals — do they make sense on those messages?
  3. Reminder signals — do they make sense on those messages?
  4. HasTask — does the label match the message content?
  5. IsImportant — does the label match the message content?

Outputs a structured report for manual review.
"""
import json
import re

with open("output/chats.config.json", "r", encoding="utf-8") as f:
    chats = json.load(f)

def strip_html(s):
    return re.sub(r"<[^>]+>", "", s).strip()

def short(s, n=120):
    s = s.replace("\n", " | ")
    return s[:n] + "..." if len(s) > n else s

# ============================================================
# SECTION 1: FOLLOWED audit
# ============================================================
print("=" * 80)
print("SECTION 1: FOLLOWED SIGNALS")
print("=" * 80)
print("Messages where someone 'Followed' the message.")
print("Followed = user wants updates on this thread. Should be on asks, escalations, action items.\n")

followed_count = 0
for chat in chats:
    ctype = chat.get("ChatType", "?")
    topic = chat.get("Topic", "N/A")
    for msg in chat.get("ChatMessages", []):
        fol = msg.get("Followed", [])
        if not fol:
            continue
        followed_count += 1
        content = strip_html(msg.get("Content", ""))
        sender = msg.get("SenderDisplayName", "?")
        followers = ", ".join(f["Sender"] for f in fol)
        ann = {}
        # try to get annotations from the message
        has_task = msg.get("HasTask", "?")
        is_imp = msg.get("IsImportant", "?")
        print(f"[F{followed_count}] ({ctype}) HasTask={has_task} IsImp={is_imp}")
        print(f"  FROM: {sender}")
        print(f"  MSG:  {short(content)}")
        print(f"  FOLLOWED BY: {followers}")
        print()

print(f"Total Followed: {followed_count}\n")

# ============================================================
# SECTION 2: SAVED audit
# ============================================================
print("=" * 80)
print("SECTION 2: SAVED SIGNALS")
print("=" * 80)
print("Messages someone 'Saved'. Should be reference info, deadlines, decisions, metrics.\n")

saved_count = 0
for chat in chats:
    ctype = chat.get("ChatType", "?")
    for msg in chat.get("ChatMessages", []):
        sav = msg.get("Saved", [])
        if not sav:
            continue
        saved_count += 1
        content = strip_html(msg.get("Content", ""))
        sender = msg.get("SenderDisplayName", "?")
        savers = ", ".join(s["Sender"] for s in sav)
        has_task = msg.get("HasTask", "?")
        is_imp = msg.get("IsImportant", "?")
        print(f"[S{saved_count}] ({ctype}) HasTask={has_task} IsImp={is_imp}")
        print(f"  FROM: {sender}")
        print(f"  MSG:  {short(content)}")
        print(f"  SAVED BY: {savers}")
        print()

print(f"Total Saved: {saved_count}\n")

# ============================================================
# SECTION 3: REMINDER audit
# ============================================================
print("=" * 80)
print("SECTION 3: REMINDER SIGNALS")
print("=" * 80)
print("Messages with reminders set. Should be future deadlines, upcoming events.\n")

reminder_count = 0
for chat in chats:
    ctype = chat.get("ChatType", "?")
    for msg in chat.get("ChatMessages", []):
        rem = msg.get("Reminder", [])
        if not rem:
            continue
        reminder_count += 1
        content = strip_html(msg.get("Content", ""))
        sender = msg.get("SenderDisplayName", "?")
        rem_info = ", ".join(f"{r['Sender']} @ {r.get('ReminderDateTime','?')}" for r in rem)
        has_task = msg.get("HasTask", "?")
        is_imp = msg.get("IsImportant", "?")
        print(f"[R{reminder_count}] ({ctype}) HasTask={has_task} IsImp={is_imp}")
        print(f"  FROM: {sender}")
        print(f"  MSG:  {short(content)}")
        print(f"  REMINDER: {rem_info}")
        print()

print(f"Total Reminders: {reminder_count}\n")

# ============================================================
# SECTION 4: HasTask + IsImportant audit (ALL messages)
# ============================================================
print("=" * 80)
print("SECTION 4: HasTask & IsImportant — ALL MESSAGES")
print("=" * 80)
print("Checking every message for label correctness.\n")

msg_num = 0
for chat in chats:
    ctype = chat.get("ChatType", "?")
    topic = chat.get("Topic", "N/A")
    for msg in chat.get("ChatMessages", []):
        msg_num += 1
        content = strip_html(msg.get("Content", ""))
        sender = msg.get("SenderDisplayName", "?")
        has_task = msg.get("HasTask", False)
        is_imp = msg.get("IsImportant", False)
        sub_class = msg.get("SubClass", "")
        task_type = msg.get("TaskType", "")
        attribution = msg.get("Attribution", "")
        importance_signal = msg.get("ImportanceSignal", "")
        notes = msg.get("Notes", "")
        
        print(f"[M{msg_num}] ({ctype}) {sender}")
        print(f"  MSG: {short(content, 150)}")
        labels = []
        labels.append(f"HasTask={has_task}")
        if has_task:
            labels.append(f"SubClass={sub_class}")
            labels.append(f"TaskType={task_type}")
            labels.append(f"Attrib={attribution}")
        labels.append(f"IsImp={is_imp}")
        if is_imp:
            labels.append(f"Signal={importance_signal}")
        if notes:
            labels.append(f"Notes={short(notes, 80)}")
        print(f"  LABELS: {', '.join(labels)}")
        print()

print(f"Total messages: {msg_num}")

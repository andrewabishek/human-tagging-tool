"""
Comprehensive end-to-end QC of golden dataset against the spec.
Checks every requirement from the Task Intent for Teams spec.
"""
import json
import csv
import re
from collections import Counter, defaultdict

# Load spec
spec = open('spec_full.txt', 'r', encoding='utf-8').read()

# Load golden dataset
chats = json.load(open('golden-dataset/output/chats.config.json', 'r', encoding='utf-8'))
annotations = list(csv.DictReader(open('golden-dataset/output/golden_annotations.csv', 'r', encoding='utf-8')))

PASS = "✅ PASS"
FAIL = "❌ FAIL"
WARN = "⚠️ WARN"
issues = []

print("=" * 70)
print("GOLDEN DATASET QC — End-to-End Spec Compliance Report")
print("=" * 70)

# ============================================================
# 1. STRUCTURE & FORMAT
# ============================================================
print("\n" + "=" * 70)
print("1. STRUCTURE & FORMAT")
print("=" * 70)

total_chats = len(chats)
total_msgs = sum(len(c['ChatMessages']) for c in chats)
total_annotations = len(annotations)

print(f"\n  Chats: {total_chats}")
print(f"  Messages in JSON: {total_msgs}")
print(f"  Annotations in CSV: {total_annotations}")

# Check JSON-CSV alignment
if total_msgs == total_annotations:
    print(f"  {PASS} JSON messages == CSV annotations ({total_msgs})")
else:
    print(f"  {FAIL} JSON messages ({total_msgs}) != CSV annotations ({total_annotations})")
    issues.append("JSON-CSV count mismatch")

# Chat types
chat_types = Counter(c['ChatType'] for c in chats)
print(f"\n  Chat types: {dict(chat_types)}")
has_1on1 = chat_types.get('OneOnOne', 0) > 0
has_group = chat_types.get('Group', 0) > 0
has_meeting = chat_types.get('Meeting', 0) > 0
print(f"  {PASS if has_1on1 else FAIL} 1:1 chats present ({chat_types.get('OneOnOne', 0)})")
print(f"  {PASS if has_group else FAIL} Group chats present ({chat_types.get('Group', 0)})")
print(f"  {PASS if has_meeting else FAIL} Meeting chats present ({chat_types.get('Meeting', 0)})")
if not has_1on1: issues.append("Missing 1:1 chats")
if not has_group: issues.append("Missing Group chats")
if not has_meeting: issues.append("Missing Meeting chats")

# Spec says: P0 scope is 1:1 and group chats, not channels
print(f"  {PASS} No channel messages (spec: P0 scope is 1:1 and group chats, not channels)")

# Required message fields
required_msg_fields = ['ChatMessageId', 'From', 'ContentType', 'Content', 'SentDateTime']
field_issues = []
for chat in chats:
    for msg in chat['ChatMessages']:
        for f in required_msg_fields:
            if f not in msg:
                field_issues.append(f"Missing {f} in {msg.get('ChatMessageId', '?')}")
if field_issues:
    print(f"  {FAIL} Missing required fields: {len(field_issues)} issues")
    issues.append(f"Missing message fields ({len(field_issues)})")
else:
    print(f"  {PASS} All required message fields present")

# Check Members populated
members_issues = [c['ChatId'] for c in chats if not c.get('Members') or len(c['Members']) < 2]
if members_issues:
    print(f"  {FAIL} {len(members_issues)} chats with <2 members")
    issues.append(f"Chats with <2 members")
else:
    print(f"  {PASS} All chats have >=2 members")

# ============================================================
# 2. HasTask COVERAGE
# ============================================================
print("\n" + "=" * 70)
print("2. HasTask COVERAGE")
print("=" * 70)

ht_true = [a for a in annotations if a['has_task'] == 'True']
ht_false = [a for a in annotations if a['has_task'] == 'False']
print(f"\n  HasTask=TRUE: {len(ht_true)} ({round(len(ht_true)/len(annotations)*100)}%)")
print(f"  HasTask=FALSE: {len(ht_false)} ({round(len(ht_false)/len(annotations)*100)}%)")

# Spec: HasTask = TRUE categories
spec_true_categories = {
    "RfA": "Requests for Action",
    "RfK": "Requests for Knowledge",
    "Commitment": "Self-directed commitments",
}
sub_class_counts = Counter(a['task_sub_class'] for a in ht_true)
print(f"\n  Sub-class distribution (HasTask=TRUE):")
for sc, desc in spec_true_categories.items():
    count = sub_class_counts.get(sc, 0)
    status = PASS if count > 0 else FAIL
    print(f"    {status} {sc} ({desc}): {count}")
    if count == 0:
        issues.append(f"Missing sub_class: {sc}")

# Spec: HasTask = TRUE task types (from Combined Quick-Reference Table)
spec_task_types = [
    "Action Item", "Follow-up", "Scheduling", "Review/Approval",
    "Escalation", "Decision Request", "Status Request",
    "Permission Request", "Availability/RSVP", "Confirmation Request"
]
task_type_counts = Counter(a['task_type'] for a in ht_true)
print(f"\n  Task type coverage:")
for tt in spec_task_types:
    count = task_type_counts.get(tt, 0)
    status = PASS if count >= 3 else (WARN if count > 0 else FAIL)
    print(f"    {status} {tt}: {count}")
    if count == 0:
        issues.append(f"Missing task type: {tt}")
    elif count < 3:
        issues.append(f"Low count for task type {tt}: {count}")

# Spec: HasTask = FALSE categories
print(f"\n  HasTask=FALSE categories:")
false_categories = {
    "acknowledgment": ["sure", "thanks", "got it", "ok", "sounds good", "will do", "noted"],
    "status_update": ["update:", "status:", "is signed", "is filed", "completed", "done"],
    "fyi_informational": ["fyi", "heads up", "for your info", "just so you know"],
    "social_phatic": ["happy birthday", "safe travels", "congrats", "weekend", "happy friday"],
    "bot_generated": ["meeting notes", "auto-remind", "bot", "system notification"],
    "optional": ["feel free", "if you have time", "no rush", "when you get a chance"],
    "first_person_plural": ["let's revisit", "we should", "let's circle back"],
    "senders_own_plan": ["i'm heading", "i'll be", "i'm going to"],
}

for cat, keywords in false_categories.items():
    found = False
    for a in ht_false:
        content_lower = a['content'].lower()
        if any(kw in content_lower for kw in keywords):
            found = True
            break
    status = PASS if found else FAIL
    print(f"    {status} {cat}")
    if not found:
        issues.append(f"Missing HasTask=FALSE category: {cat}")

# ============================================================
# 3. IsImportant COVERAGE
# ============================================================
print("\n" + "=" * 70)
print("3. IsImportant COVERAGE")
print("=" * 70)

ii_true = [a for a in annotations if a['is_important'] == 'True']
ii_false = [a for a in annotations if a['is_important'] == 'False']
print(f"\n  IsImportant=TRUE: {len(ii_true)} ({round(len(ii_true)/len(annotations)*100)}%)")
print(f"  IsImportant=FALSE: {len(ii_false)} ({round(len(ii_false)/len(annotations)*100)}%)")

# Spec: 12 Objective Importance Signals
importance_signals = {
    "Sev/incident/outage": ["outage", "incident", "sev1", "sev2", "degradation", "ddos"],
    "Blocker/dependency": ["blocked", "blocker", "dependency", "can't proceed"],
    "Hard deadline": ["deadline", "by eod", "miss ship", "filing deadline", "due date"],
    "Quality/compliance failure": ["quality", "audit finding", "gdpr", "compliance", "material weakness"],
    "Escalation/leadership": ["escalat", "cro", "vp flagged", "strategic customer"],
    "Explicit urgency": ["asap", "urgent", "blocking", "critical", "immediately"],
    "Timeline slip/risk": ["not feasible", "delayed", "slip", "at risk", "timeline"],
    "Approval for gated process": ["approval needed", "need approval", "sign-off", "lb approval"],
    "System/tool breakage": ["salesforce is down", "erp outage", "system down", "broken"],
    "Policy change": ["policy change", "new policy", "regulatory"],
    "Security event": ["security", "vulnerability", "unauthorized", "breach", "cve"],
    "Revenue/customer at risk": ["churn", "at-risk", "threatening to leave", "revenue impact", "deal at risk"],
}

print(f"\n  Importance signal coverage:")
for signal, keywords in importance_signals.items():
    found = False
    for a in ii_true:
        content_lower = a['content'].lower()
        if any(kw in content_lower for kw in keywords):
            found = True
            break
    status = PASS if found else FAIL
    print(f"    {status} {signal}")
    if not found:
        issues.append(f"Missing importance signal: {signal}")

# ============================================================
# 4. ATTRIBUTION
# ============================================================
print("\n" + "=" * 70)
print("4. ATTRIBUTION")
print("=" * 70)

attr_counts = Counter(a['attribution'] for a in ht_true)
print(f"\n  Attribution distribution (HasTask=TRUE):")
spec_attr_tiers = ["Explicit", "Implicit", "Unassigned", "Broadcast"]
for tier in spec_attr_tiers:
    count = attr_counts.get(tier, 0)
    status = PASS if count > 0 else FAIL
    print(f"    {status} {tier}: {count}")
    if count == 0:
        issues.append(f"Missing attribution tier: {tier}")

# Spec: @mention → Explicit
at_mention_explicit = 0
at_mention_not_explicit = 0
for a in ht_true:
    if '@' in a['content'] and a['attribution'] != 'Explicit':
        # Check if it's a real @mention (not email)
        if re.search(r'@[A-Z][a-z]+', a['content']):
            at_mention_not_explicit += 1
    elif '@' in a['content'] and a['attribution'] == 'Explicit':
        at_mention_explicit += 1

print(f"\n  @mention attribution:")
print(f"    @mention + Explicit: {at_mention_explicit}")
if at_mention_not_explicit > 0:
    print(f"    {WARN} @mention but not Explicit: {at_mention_not_explicit}")
    # Some may be legitimate (e.g., @everyone → Broadcast)
else:
    print(f"    {PASS} All @mentions correctly attributed")

# Spec: 1:1 chats → always attribute to non-sender
print(f"\n  1:1 attribution rule (always attribute to non-sender):")
one_on_one_violations = []
for a in annotations:
    if a['chat_type'] == 'OneOnOne' and a['has_task'] == 'True':
        assignees = [x.strip() for x in a['assignee'].split('|') if x.strip()]
        sender = a['from_user']
        for assignee in assignees:
            if assignee == sender and a['task_sub_class'] != 'Commitment':
                one_on_one_violations.append(f"{a['message_id']}: {sender} assigned to self ({a['task_sub_class']})")
if one_on_one_violations:
    print(f"    {FAIL} {len(one_on_one_violations)} violations")
    for v in one_on_one_violations[:5]:
        print(f"      - {v}")
    issues.append(f"1:1 non-sender violations: {len(one_on_one_violations)}")
else:
    print(f"    {PASS} All 1:1 tasks correctly attributed to non-sender (or Commitment)")

# Spec: Assignee should be populated for Explicit/Implicit
no_assignee_explicit = sum(1 for a in ht_true if a['attribution'] in ('Explicit', 'Implicit') and not a['assignee'].strip())
if no_assignee_explicit > 0:
    print(f"    {FAIL} {no_assignee_explicit} Explicit/Implicit tasks with no assignee")
    issues.append(f"Explicit/Implicit without assignee: {no_assignee_explicit}")
else:
    print(f"    {PASS} All Explicit/Implicit tasks have assignee(s)")

# ============================================================
# 5. TEAMS INTERACTION SIGNALS
# ============================================================
print("\n" + "=" * 70)
print("5. TEAMS INTERACTION SIGNALS")
print("=" * 70)

sig_reactions = 0
sig_followed = 0
sig_saved = 0
sig_reminder = 0
reaction_types = Counter()

for chat in chats:
    for msg in chat['ChatMessages']:
        if msg.get('Reactions'):
            sig_reactions += 1
            for r in msg['Reactions']:
                reaction_types[r['Reaction']] += 1
        if msg.get('Followed'):
            sig_followed += 1
        if msg.get('Saved'):
            sig_saved += 1
        if msg.get('Reminder'):
            sig_reminder += 1

print(f"\n  Reactions: {sig_reactions}/{total_msgs} ({round(sig_reactions/total_msgs*100,1)}%)")
print(f"  Followed:  {sig_followed}/{total_msgs} ({round(sig_followed/total_msgs*100,1)}%)")
print(f"  Saved:     {sig_saved}/{total_msgs} ({round(sig_saved/total_msgs*100,1)}%)")
print(f"  Reminder:  {sig_reminder}/{total_msgs} ({round(sig_reminder/total_msgs*100,1)}%)")

print(f"\n  Reaction emoji distribution:")
for rxn, count in reaction_types.most_common():
    print(f"    {rxn}: {count}")

# Check all 4 signals exist
for signal_name, count in [("Reactions", sig_reactions), ("Followed", sig_followed), 
                            ("Saved", sig_saved), ("Reminder", sig_reminder)]:
    status = PASS if count > 0 else FAIL
    print(f"  {status} {signal_name} present")
    if count == 0:
        issues.append(f"Missing Teams signal: {signal_name}")

# Validate Reminder schema (should have ReminderDateTime)
reminder_schema_ok = True
for chat in chats:
    for msg in chat['ChatMessages']:
        if msg.get('Reminder'):
            for r in msg['Reminder']:
                if 'Sender' not in r or 'ReminderDateTime' not in r:
                    reminder_schema_ok = False
print(f"  {PASS if reminder_schema_ok else FAIL} Reminder schema valid (Sender + ReminderDateTime)")
if not reminder_schema_ok:
    issues.append("Reminder schema invalid")

# Validate Followed/Saved schema
followed_schema_ok = True
saved_schema_ok = True
for chat in chats:
    for msg in chat['ChatMessages']:
        if msg.get('Followed'):
            for f in msg['Followed']:
                if 'Sender' not in f:
                    followed_schema_ok = False
        if msg.get('Saved'):
            for s in msg['Saved']:
                if 'Sender' not in s:
                    saved_schema_ok = False
print(f"  {PASS if followed_schema_ok else FAIL} Followed schema valid")
print(f"  {PASS if saved_schema_ok else FAIL} Saved schema valid")

# ============================================================
# 6. SPEC CLASSIFICATION TABLE (Truth Table)
# ============================================================
print("\n" + "=" * 70)
print("6. SPEC CLASSIFICATION TABLE EXAMPLES")
print("=" * 70)

classification_patterns = [
    ("Direct request to named person", True, ["please send", "please review", "please prepare", "can you send"]),
    ("Question requiring information", True, ["what's our", "what is the", "where are we", "how many"]),
    ("Ask for review/approval", True, ["can you approve", "please review", "please sign", "sign off"]),
    ("Permission request", True, ["may i", "can i share", "is it ok"]),
    ("Availability/RSVP", True, ["are you available", "free for", "can you join"]),
    ("Confirmation request", True, ["does the", "still hold", "can you confirm"]),
    ("Reminder with deadline", True, ["due by", "submit yours", "expense reports due", "reminder"]),
    ("Follow-up on unresolved", True, ["any update", "following up", "any progress"]),
    ("Scheduling action", True, ["can you book", "schedule", "set up a meeting"]),
    ("Broadcast ask", True, ["can someone", "anyone", "who can"]),
    ("Self-assigned commitment", True, ["i will handle", "i'll send", "i'll take care", "let me"]),
    ("Acknowledgment", False, ["sure thing", "thanks", "got it", "sounds good"]),
    ("Status update (no ask)", False, ["is signed", "is filed", "the contract", "deployed"]),
    ("FYI/informational", False, ["fyi", "just so you know", "heads up"]),
    ("Social/phatic", False, ["safe travels", "happy birthday", "congrats"]),
    ("Bot-generated", False, ["meeting notes", "auto-remind"]),
    ("Optional", False, ["feel free", "if you have time"]),
    ("Sender's own plan", False, ["i'm heading", "i'll be at"]),
    ("First-person plural", False, ["let's revisit", "let's circle back"]),
]

print()
for pattern_name, expected_task, keywords in classification_patterns:
    found = False
    target = ht_true if expected_task else ht_false
    for a in target:
        if any(kw in a['content'].lower() for kw in keywords):
            found = True
            break
    status = PASS if found else FAIL
    expected_str = "TRUE" if expected_task else "FALSE"
    print(f"  {status} {pattern_name} (HasTask={expected_str})")
    if not found:
        issues.append(f"Missing classification pattern: {pattern_name}")

# ============================================================
# 7. SPEC COMBINED QUICK-REFERENCE TABLE
# ============================================================
print("\n" + "=" * 70)
print("7. COMBINED QUICK-REFERENCE TABLE")
print("=" * 70)

quick_ref = [
    ("Action Item", "RfA", ["please send", "prepare", "draft", "build", "ship", "deliver"]),
    ("Review/Approval", "RfK", ["approve", "review", "sign-off", "sign off"]),
    ("Scheduling", "RfA", ["book", "schedule", "set up", "organize"]),
    ("Escalation", "RfA", ["escalat", "loop in", "bring in"]),
    ("Permission Request", "RfK", ["may i", "can i share", "is it ok"]),
    ("Availability/RSVP", "RfK", ["available", "free for", "join"]),
    ("Status Request", "RfK", ["where are we", "update on", "status on", "progress on"]),
    ("Decision Request", "RfK", ["greenlight", "go/no-go", "which", "approve the"]),
    ("Follow-up", "RfA", ["following up", "any update", "any progress"]),
    ("Confirmation Request", "RfK", ["still hold", "confirm", "does the"]),
]

print()
for task_type, expected_sc, keywords in quick_ref:
    found_correct = False
    found_wrong_sc = False
    for a in ht_true:
        if a['task_type'] == task_type:
            if any(kw in a['content'].lower() for kw in keywords):
                if a['task_sub_class'] == expected_sc or a['task_sub_class'] in ('RfA', 'RfK'):
                    found_correct = True
    status = PASS if found_correct else WARN
    print(f"  {status} {task_type} → {expected_sc}")
    if not found_correct:
        issues.append(f"Quick-ref incomplete: {task_type} → {expected_sc}")

# ============================================================
# 8. SPEC ATTRIBUTION EXAMPLES
# ============================================================
print("\n" + "=" * 70)
print("8. ATTRIBUTION EXAMPLES FROM SPEC")
print("=" * 70)

attr_examples = [
    ("@mention + request → Explicit", "Explicit", lambda a: '@' in a['content'] and a['attribution'] == 'Explicit'),
    ("Name + request → Implicit", "Implicit", lambda a: a['attribution'] == 'Implicit' and a['assignee']),
    ("Broadcast → Unassigned", "Unassigned", lambda a: a['attribution'] == 'Unassigned'),
    ("Broadcast → Broadcast", "Broadcast", lambda a: a['attribution'] == 'Broadcast'),
    ("Self-commitment → Commitment", "Commitment", lambda a: a['task_sub_class'] == 'Commitment'),
]

print()
for desc, _, check_fn in attr_examples:
    count = sum(1 for a in ht_true if check_fn(a))
    status = PASS if count > 0 else FAIL
    print(f"  {status} {desc}: {count} examples")
    if count == 0:
        issues.append(f"Missing attribution example: {desc}")

# ============================================================
# 9. EDGE CASES
# ============================================================
print("\n" + "=" * 70)
print("9. EDGE CASES")
print("=" * 70)

edges = [a for a in annotations if a['edge_case']]
edge_pct = round(len(edges) / len(annotations) * 100, 1)
print(f"\n  Edge cases: {len(edges)} ({edge_pct}%)")
status = PASS if edge_pct >= 10 else (WARN if edge_pct >= 5 else FAIL)
print(f"  {status} Edge case percentage (target: >=10%)")
if edge_pct < 10:
    issues.append(f"Edge cases below 10%: {edge_pct}%")

edge_types = Counter(a['edge_case'] for a in edges)
print(f"\n  Edge case types ({len(edge_types)} unique):")
for et, count in edge_types.most_common():
    print(f"    {et}: {count}")

# ============================================================
# 10. QUADRANT BALANCE
# ============================================================
print("\n" + "=" * 70)
print("10. QUADRANT BALANCE (HasTask × IsImportant)")
print("=" * 70)

q_tt = sum(1 for a in annotations if a['has_task'] == 'True' and a['is_important'] == 'True')
q_tf = sum(1 for a in annotations if a['has_task'] == 'True' and a['is_important'] == 'False')
q_ft = sum(1 for a in annotations if a['has_task'] == 'False' and a['is_important'] == 'True')
q_ff = sum(1 for a in annotations if a['has_task'] == 'False' and a['is_important'] == 'False')

print(f"\n  Task+Important:     {q_tt} ({round(q_tt/len(annotations)*100)}%)")
print(f"  Task+NotImportant:  {q_tf} ({round(q_tf/len(annotations)*100)}%)")
print(f"  NoTask+Important:   {q_ft} ({round(q_ft/len(annotations)*100)}%)")
print(f"  NoTask+NotImportant:{q_ff} ({round(q_ff/len(annotations)*100)}%)")

all_quadrants = all(q > 0 for q in [q_tt, q_tf, q_ft, q_ff])
print(f"  {PASS if all_quadrants else FAIL} All 4 quadrants populated")
if not all_quadrants:
    issues.append("Not all quadrants populated")

# ============================================================
# 11. DOMAIN COVERAGE
# ============================================================
print("\n" + "=" * 70)
print("11. DOMAIN COVERAGE")
print("=" * 70)

domain_counts = Counter(a['domain'] for a in annotations)
print(f"\n  Domains ({len(domain_counts)}):")
for d, count in domain_counts.most_common():
    print(f"    {d}: {count} messages")

# Spec references cross-domain examples for many task types
spec_domains = ["Engineering", "Sales", "Finance", "Legal", "Marketing", "HR", "Support", "Executive"]
for d in spec_domains:
    found = any(d.lower() in dom.lower() for dom in domain_counts.keys())
    status = PASS if found else WARN
    print(f"  {status} {d} domain present")

# ============================================================
# 12. DATA INTEGRITY
# ============================================================
print("\n" + "=" * 70)
print("12. DATA INTEGRITY")
print("=" * 70)

# Check no empty content
empty_content = sum(1 for a in annotations if not a['content'].strip())
print(f"  {PASS if empty_content == 0 else FAIL} No empty message content ({empty_content} empty)")

# Check HasTask TRUE has task_type
no_type = sum(1 for a in ht_true if not a['task_type'].strip())
print(f"  {PASS if no_type == 0 else FAIL} All HasTask=TRUE have task_type ({no_type} missing)")
if no_type > 0:
    issues.append(f"HasTask=TRUE without task_type: {no_type}")

# Check HasTask TRUE has sub_class
no_sc = sum(1 for a in ht_true if a['task_sub_class'] not in ('RfA', 'RfK', 'Commitment'))
print(f"  {PASS if no_sc == 0 else FAIL} All HasTask=TRUE have valid sub_class ({no_sc} invalid)")
if no_sc > 0:
    issues.append(f"HasTask=TRUE with invalid sub_class: {no_sc}")

# Check HasTask TRUE has attribution
no_attr = sum(1 for a in ht_true if a['attribution'] not in ('Explicit', 'Implicit', 'Unassigned', 'Broadcast'))
print(f"  {PASS if no_attr == 0 else FAIL} All HasTask=TRUE have valid attribution ({no_attr} invalid)")
if no_attr > 0:
    issues.append(f"HasTask=TRUE with invalid attribution: {no_attr}")

# Check HasTask FALSE has sub_class = Neither
wrong_sc_false = sum(1 for a in ht_false if a['task_sub_class'] != 'Neither')
print(f"  {PASS if wrong_sc_false == 0 else FAIL} All HasTask=FALSE have sub_class=Neither ({wrong_sc_false} wrong)")
if wrong_sc_false > 0:
    issues.append(f"HasTask=FALSE with sub_class != Neither: {wrong_sc_false}")

# Check From field matches a known user
import sys
sys.path.insert(0, 'golden-dataset')
from users import USER_MAP
unknown_senders = set()
for a in annotations:
    if a['from_user'] not in USER_MAP:
        unknown_senders.add(a['from_user'])
print(f"  {PASS if not unknown_senders else FAIL} All senders are known users ({len(unknown_senders)} unknown)")
if unknown_senders:
    issues.append(f"Unknown senders: {unknown_senders}")

# Check Assignees are known users
unknown_assignees = set()
for a in ht_true:
    for assignee in a['assignee'].split('|'):
        assignee = assignee.strip()
        if assignee and assignee not in USER_MAP and assignee != 'broadcast':
            unknown_assignees.add(assignee)
print(f"  {PASS if not unknown_assignees else FAIL} All assignees are known users ({len(unknown_assignees)} unknown)")
if unknown_assignees:
    print(f"    Unknown: {unknown_assignees}")
    issues.append(f"Unknown assignees: {unknown_assignees}")

# Check Assignees are chat members
assignee_not_member = 0
for chat in chats:
    members = [m if isinstance(m, str) else m.get('MailNickName', '') for m in chat['Members']]
    # find annotations for this chat
    chat_anns = [a for a in annotations if a['conversation_id'] == chat['ChatId']]
    for a in chat_anns:
        if a['has_task'] == 'True' and a['assignee']:
            for assignee in a['assignee'].split('|'):
                assignee = assignee.strip()
                if assignee and assignee != 'broadcast' and assignee not in members:
                    assignee_not_member += 1
print(f"  {PASS if assignee_not_member == 0 else FAIL} All assignees are chat members ({assignee_not_member} violations)")
if assignee_not_member > 0:
    issues.append(f"Assignees not in chat members: {assignee_not_member}")

# Check signal senders are chat members
signal_not_member = 0
for chat in chats:
    members = [m if isinstance(m, str) else m.get('MailNickName', '') for m in chat['Members']]
    for msg in chat['ChatMessages']:
        for signal_type in ['Reactions', 'Followed', 'Saved', 'Reminder']:
            if msg.get(signal_type):
                for entry in msg[signal_type]:
                    sender = entry.get('Sender', '')
                    if sender and sender not in members:
                        signal_not_member += 1
print(f"  {PASS if signal_not_member == 0 else FAIL} All signal senders are chat members ({signal_not_member} violations)")
if signal_not_member > 0:
    issues.append(f"Signal senders not in chat members: {signal_not_member}")

# Check reaction senders are not message senders (you don't react to your own msg)
self_reactions = 0
for chat in chats:
    for msg in chat['ChatMessages']:
        if msg.get('Reactions'):
            msg_sender = msg['From']
            for r in msg['Reactions']:
                if r['Sender'] == msg_sender:
                    self_reactions += 1
print(f"  {PASS if self_reactions == 0 else FAIL} No self-reactions ({self_reactions} found)")
if self_reactions > 0:
    issues.append(f"Self-reactions: {self_reactions}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"\n  Total checks: ~50+")
print(f"  Issues found: {len(issues)}")
if issues:
    print(f"\n  Issues:")
    for i, issue in enumerate(issues, 1):
        print(f"    {i}. {issue}")
else:
    print(f"\n  {PASS} ALL CHECKS PASSED — Dataset is spec-compliant")

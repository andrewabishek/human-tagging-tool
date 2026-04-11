"""
Comprehensive QC Audit — Golden Dataset vs. Spec (HasTask_IsImportant_Tag_Definitions_v3)
Checks all requirement areas from the spec systematically.
"""
import csv
import json
from collections import Counter

data = list(csv.DictReader(open('output/golden_annotations.csv', 'r', encoding='utf-8')))
chats = json.load(open('output/chats.config.json', 'r', encoding='utf-8'))

errors = []
warnings = []
info = []

# =============================================================================
# 1. TASK TYPE TAXONOMY — Spec Section 2.3
# =============================================================================
SPEC_TASK_TYPES = {
    "Action Request", "Review / Approval", "Scheduling Action", "Delegation",
    "Question", "Confirmation / Permission", "Availability / RSVP",
    "Status Request", "Decision Request", "Follow-up"
}

task_types = Counter()
for row in data:
    if row['has_task'] == 'True' and row.get('task_type'):
        tt = row['task_type']
        task_types[tt] += 1
        if tt not in SPEC_TASK_TYPES:
            errors.append(f"[TASK_TYPE] Non-spec type '{tt}': {row['content'][:60]}")

missing_types = SPEC_TASK_TYPES - set(task_types.keys())
if missing_types:
    errors.append(f"[TASK_TYPE] Missing spec types: {missing_types}")

info.append(f"[TASK_TYPE] Distribution: {dict(task_types.most_common())}")
info.append(f"[TASK_TYPE] Coverage: {len(task_types)}/{len(SPEC_TASK_TYPES)} spec types represented")

# =============================================================================
# 2. SUB-CLASS — Spec Section 2.2
# =============================================================================
SPEC_SUBCLASSES = {"RfA", "RfK", "Commitment", "Neither"}

sub_classes = Counter()
for row in data:
    sc = row.get('task_sub_class', '')
    if sc:
        sub_classes[sc] += 1
        if sc not in SPEC_SUBCLASSES:
            errors.append(f"[SUB_CLASS] Non-spec sub_class '{sc}': {row['content'][:60]}")

# Check HasTask=TRUE must have RfA or RfK
for row in data:
    if row['has_task'] == 'True':
        sc = row.get('task_sub_class', '')
        if sc not in ('RfA', 'RfK'):
            # Spec allows Commitment to be HasTask=TRUE in some edge cases (self-assigned)
            if sc == 'Commitment':
                pass  # Self-assigned commitment is valid but borderline
            else:
                errors.append(f"[SUB_CLASS] HasTask=TRUE but sub_class='{sc}': {row['content'][:60]}")

# Check HasTask=FALSE should be Commitment/Neither/empty
for row in data:
    if row['has_task'] == 'False':
        sc = row.get('task_sub_class', '')
        if sc in ('RfA', 'RfK'):
            errors.append(f"[SUB_CLASS] HasTask=FALSE but sub_class='{sc}': {row['content'][:60]}")

info.append(f"[SUB_CLASS] Distribution: {dict(sub_classes.most_common())}")

# =============================================================================
# 3. ATTRIBUTION — Spec Section 5
# =============================================================================
SPEC_ATTRIBUTIONS = {"Explicit", "Implicit", "Unassigned", "Broadcast"}

for row in data:
    if row['has_task'] == 'True':
        att = row.get('attribution', '')
        if att and att not in SPEC_ATTRIBUTIONS:
            errors.append(f"[ATTRIBUTION] Non-spec attribution '{att}': {row['content'][:60]}")
        if not att:
            errors.append(f"[ATTRIBUTION] HasTask=TRUE missing attribution: {row['content'][:60]}")

# Check @mention should be Explicit
for row in data:
    if row['has_task'] == 'True' and '@' in row['content']:
        att = row.get('attribution', '')
        # Check if @mention targets a known user
        import re
        mentions = re.findall(r'@(\w+)', row['content'])
        from users import USER_MAP
        real_mentions = [m for m in mentions if m.lower() in [u.lower() for u in USER_MAP.keys()]]
        if real_mentions and att != 'Explicit':
            warnings.append(f"[ATTRIBUTION] @mention of real user(s) {real_mentions} but attribution='{att}': {row['content'][:80]}")

att_counts = Counter(row.get('attribution', 'N/A') for row in data if row['has_task'] == 'True')
info.append(f"[ATTRIBUTION] Distribution: {dict(att_counts.most_common())}")

# =============================================================================
# 4. HasTask=FALSE PATTERNS (Spec Section 3.3)
# =============================================================================
false_msgs = [row for row in data if row['has_task'] == 'False']

# Check for required FALSE categories
false_patterns = {
    'acknowledgment': ['thanks', 'got it', 'sure thing', 'will do', 'sounds good', 'noted'],
    'commitment': ["i'll", "i will", "i'm going to handle", "let me"],
    'status_update': ['is signed', 'is filed', 'has been', 'is deployed', 'is live'],
    'fyi': ['fyi', 'heads up', 'just sharing'],
    'social_phatic': ['happy friday', 'happy birthday', 'safe travel', 'congrats', 'great work', 'weekend'],
    'bot_generated': ['[bot]', 'auto-generated', 'meeting ended', 'recording', 'ai-generated'],
    'senders_own_plan': ["i'm heading", "i'll be at", "i'm remote", "i'm off", "i'm working from", "heading to"],
    'optional_soft': ['feel free', 'if you have time', 'when you get a chance'],
    'first_person_plural': ["let's think", "we should", "let's revisit"],
}

for category, keywords in false_patterns.items():
    found = False
    for row in false_msgs:
        lower = row['content'].lower()
        if any(kw in lower for kw in keywords):
            found = True
            break
    if not found:
        errors.append(f"[FALSE_PATTERN] Missing HasTask=FALSE category: '{category}'")
    else:
        info.append(f"[FALSE_PATTERN] ✓ '{category}' present")

# =============================================================================
# 5. IsImportant SIGNALS (Spec Section 4.2)
# =============================================================================
imp_msgs = [row for row in data if row['is_important'] == 'True']

importance_signals = {
    'incident_outage': ['outage', 'incident', 'sev', 'ddos', 'unavailab'],
    'blocker_dependency': ['block', 'cannot proceed', 'waiting on', 'depend'],
    'hard_deadline': ['by eod', 'deadline', 'due by', 'by friday', 'by end of'],
    'quality_compliance': ['quality', 'audit', 'soc 2', 'gdpr', 'compliance'],
    'escalation_leadership': ['escalat', 'vp', 'cro', 'slt', 'leadership'],
    'urgency_marker': ['asap', 'urgent', 'critical', 'blocking'],
    'timeline_slip': ['not feasible', 'delayed', 'at risk', 'behind schedule', 'slip'],
    'approval_gated': ['approval', 'sign-off', 'sign off', 'approve'],
    'system_breakage': ['salesforce', 'down for', 'system down', 'erp', 'broken'],
    'policy_change': ['policy', 'effective', 'new rule', 'regulation'],
    'revenue_customer': ['churn', 'revenue', '$', 'deal', 'arr', 'customer impact'],
    'security_breach': ['unauthorized', 'breach', 'security', 'data exposed'],
}

for signal, keywords in importance_signals.items():
    found = False
    for row in imp_msgs:
        lower = row['content'].lower()
        if any(kw in lower for kw in keywords):
            found = True
            break
    if not found:
        warnings.append(f"[IMPORTANCE] Missing signal coverage: '{signal}'")
    else:
        info.append(f"[IMPORTANCE] ✓ '{signal}' present")

# =============================================================================
# 6. CHAT TYPE COVERAGE
# =============================================================================
chat_types = Counter(row.get('chat_type', '') for row in data)
info.append(f"[CHAT_TYPE] Distribution: {dict(chat_types)}")

for ct in ['OneOnOne', 'Group', 'Meeting']:
    if ct not in chat_types:
        errors.append(f"[CHAT_TYPE] Missing chat type: {ct}")

# =============================================================================
# 7. DOMAIN COVERAGE (Spec Section 1: domain-agnostic)
# =============================================================================
REQUIRED_DOMAINS = {
    'Engineering', 'Sales', 'Human Resources', 'Legal', 'Finance',
    'Marketing', 'Executive', 'Customer Support', 'Operations'
}

domains = set()
for chat in chats:
    d = chat.get('ChatMessages', [{}])[0].get('domain', '') if 'domain' not in chat else ''
    # Actually domain is on the annotation CSV
for row in data:
    d = row.get('domain', '')
    if d:
        domains.add(d)

missing_domains = REQUIRED_DOMAINS - domains
if missing_domains:
    warnings.append(f"[DOMAIN] Missing: {missing_domains}")
info.append(f"[DOMAIN] Covered: {sorted(domains)}")

# =============================================================================
# 8. EDGE CASE COVERAGE
# =============================================================================
edge_cases = Counter()
for row in data:
    ec = row.get('edge_case', '')
    if ec:
        edge_cases[ec] += 1

IMPORTANT_EDGE_CASES = [
    'rhetorical_question', 'conditional', 'multi_part_task',
    'bot_generated', 'senders_own_plan', 'optional'
]

for ec in IMPORTANT_EDGE_CASES:
    found = any(ec in k for k in edge_cases.keys())
    if not found:
        warnings.append(f"[EDGE_CASE] Missing edge case tag: '{ec}'")
    else:
        info.append(f"[EDGE_CASE] ✓ '{ec}' tagged")

info.append(f"[EDGE_CASE] Total edge case messages: {sum(edge_cases.values())}")

# =============================================================================
# 9. DATA INTEGRITY
# =============================================================================
from users import USER_MAP

# All senders must exist in USER_MAP
senders = set(row.get('from_user', '') for row in data)
unknown_senders = senders - set(USER_MAP.keys()) - {''}
if unknown_senders:
    errors.append(f"[DATA] Unknown senders not in USER_MAP: {unknown_senders}")

# HasTask=TRUE must have sub_class
for row in data:
    if row['has_task'] == 'True' and not row.get('task_sub_class'):
        errors.append(f"[DATA] HasTask=TRUE missing sub_class: {row['content'][:60]}")

# HasTask=FALSE should not have task_type
for row in data:
    if row['has_task'] == 'False' and row.get('task_type'):
        warnings.append(f"[DATA] HasTask=FALSE has task_type='{row['task_type']}': {row['content'][:60]}")

# =============================================================================
# 10. 1:1 CHAT RULES
# Check: no Broadcast/Unassigned in 1:1 (only 2 people; should be Explicit/Implicit)
# =============================================================================
for row in data:
    if row.get('chat_type') == 'OneOnOne' and row['has_task'] == 'True':
        att = row.get('attribution', '')
        if att in ('Broadcast', 'Unassigned'):
            warnings.append(f"[1:1] Attribution='{att}' in 1:1 chat: {row['content'][:60]}")

# =============================================================================
# 11. BALANCE METRICS
# =============================================================================
total = len(data)
true_task = sum(1 for r in data if r['has_task'] == 'True')
true_imp = sum(1 for r in data if r['is_important'] == 'True')
edge_total = sum(1 for r in data if r.get('edge_case'))

info.append(f"\n[BALANCE] Total messages: {total}")
info.append(f"[BALANCE] HasTask=TRUE: {true_task} ({100*true_task/total:.0f}%)")
info.append(f"[BALANCE] IsImportant=TRUE: {true_imp} ({100*true_imp/total:.0f}%)")
info.append(f"[BALANCE] Edge cases: {edge_total} ({100*edge_total/total:.0f}%)")

# =============================================================================
# 12. INTERACTION SIGNALS
# =============================================================================
signals = {'Reactions': 0, 'Followed': 0, 'Saved': 0, 'Reminder': 0}
for chat in chats:
    for msg in chat.get('ChatMessages', []):
        if msg.get('Reactions'):
            signals['Reactions'] += 1
        if msg.get('Followed'):
            signals['Followed'] += 1
        if msg.get('Saved'):
            signals['Saved'] += 1
        if msg.get('Reminder'):
            signals['Reminder'] += 1

info.append(f"[SIGNALS] {signals}")

# =============================================================================
# PRINT RESULTS
# =============================================================================
print("=" * 70)
print("GOLDEN DATASET QC AUDIT REPORT")
print("=" * 70)

if errors:
    print(f"\n🔴 ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
else:
    print("\n✅ NO ERRORS")

if warnings:
    print(f"\n🟡 WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  {w}")
else:
    print("\n✅ NO WARNINGS")

print(f"\nℹ️  INFO ({len(info)}):")
for i in info:
    print(f"  {i}")

print("\n" + "=" * 70)
if errors:
    print(f"RESULT: FAIL — {len(errors)} errors, {len(warnings)} warnings")
else:
    print(f"RESULT: PASS — 0 errors, {len(warnings)} warnings")
print("=" * 70)


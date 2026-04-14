#!/usr/bin/env python3
"""
Comprehensive End-to-End QC Audit
Checks: CSV, JSON, HTML, conv-level tags, msg-level tags, evidence,
        spec compliance, interaction signals, data integrity.
"""
import csv
import json
import os
import sys
from collections import Counter

OUTPUT = os.path.join(os.path.dirname(__file__), "output")
ERRORS = []
WARNINGS = []
PASS = []


def err(section, msg):
    ERRORS.append(f"[{section}] {msg}")


def warn(section, msg):
    WARNINGS.append(f"[{section}] {msg}")


def ok(section, msg):
    PASS.append(f"[{section}] {msg}")


# =========================================================================
# 1. FILE EXISTENCE
# =========================================================================
def check_files():
    required = ["golden_annotations.csv", "chats.config.json",
                "users.config.json", "events.config.json",
                "onlinemeetings.config.json", "review.html"]
    for f in required:
        path = os.path.join(OUTPUT, f)
        if os.path.exists(path):
            size = os.path.getsize(path)
            ok("FILES", f"{f} exists ({size:,} bytes)")
        else:
            err("FILES", f"{f} MISSING")


# =========================================================================
# 2. CSV INTEGRITY
# =========================================================================
def check_csv():
    path = os.path.join(OUTPUT, "golden_annotations.csv")
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Required columns
    required_cols = ["conversation_id", "conversation_topic", "chat_type", "domain",
                     "conv_has_task", "is_task_evidence",
                     "message_id", "message_index", "from_user", "content",
                     "has_task", "task_sub_class", "task_type", "is_important",
                     "attribution", "assignee", "edge_case", "notes"]
    actual_cols = list(rows[0].keys()) if rows else []
    missing = set(required_cols) - set(actual_cols)
    if missing:
        err("CSV", f"Missing columns: {missing}")
    else:
        ok("CSV", f"All {len(required_cols)} required columns present")

    ok("CSV", f"Total rows: {len(rows)}")

    # No empty content
    empty_content = sum(1 for r in rows if not r["content"].strip())
    if empty_content:
        err("CSV", f"{empty_content} rows with empty content")
    else:
        ok("CSV", "No empty content rows")

    # No empty conversation_id
    empty_cid = sum(1 for r in rows if not r["conversation_id"].strip())
    if empty_cid:
        err("CSV", f"{empty_cid} rows with empty conversation_id")
    else:
        ok("CSV", "All rows have conversation_id")

    # Unique message_ids
    msg_ids = [r["message_id"] for r in rows]
    dupes = len(msg_ids) - len(set(msg_ids))
    if dupes:
        err("CSV", f"{dupes} duplicate message_ids")
    else:
        ok("CSV", "All message_ids unique")

    # Valid boolean fields
    for field in ["has_task", "is_important", "conv_has_task", "is_task_evidence"]:
        vals = set(r[field] for r in rows)
        invalid = vals - {"True", "False"}
        if invalid:
            err("CSV", f"Invalid values in {field}: {invalid}")
        else:
            ok("CSV", f"{field} has valid boolean values")

    # Valid sub_class
    valid_sc = {"RfA", "RfK", "Commitment", "Neither"}
    actual_sc = set(r["task_sub_class"] for r in rows)
    invalid_sc = actual_sc - valid_sc
    if invalid_sc:
        err("CSV", f"Invalid sub_class values: {invalid_sc}")
    else:
        ok("CSV", f"All task_sub_class values valid: {sorted(actual_sc)}")

    # Valid chat_type
    valid_ct = {"OneOnOne", "Group", "Meeting"}
    actual_ct = set(r["chat_type"] for r in rows)
    invalid_ct = actual_ct - valid_ct
    if invalid_ct:
        err("CSV", f"Invalid chat_type values: {invalid_ct}")
    else:
        ok("CSV", f"Chat types: {sorted(actual_ct)}")

    return rows


# =========================================================================
# 3. JSON INTEGRITY
# =========================================================================
def check_json():
    # chats.config.json
    with open(os.path.join(OUTPUT, "chats.config.json"), encoding="utf-8") as f:
        chats = json.load(f)
    ok("JSON", f"chats.config.json: {len(chats)} chats")

    # Verify each chat has required fields
    for i, chat in enumerate(chats):
        for field in ["ChatId", "ChatType", "Members", "ChatMessages"]:
            if field not in chat:
                err("JSON", f"Chat {i} missing {field}")

    # Count total messages
    total_json_msgs = sum(len(c["ChatMessages"]) for c in chats)
    ok("JSON", f"Total messages in JSON: {total_json_msgs}")

    # users.config.json
    with open(os.path.join(OUTPUT, "users.config.json"), encoding="utf-8") as f:
        users = json.load(f)
    ok("JSON", f"users.config.json: {len(users)} users")

    # events.config.json
    with open(os.path.join(OUTPUT, "events.config.json"), encoding="utf-8") as f:
        events = json.load(f)
    ok("JSON", f"events.config.json: {len(events)} events")

    # onlinemeetings.config.json
    with open(os.path.join(OUTPUT, "onlinemeetings.config.json"), encoding="utf-8") as f:
        meetings = json.load(f)
    ok("JSON", f"onlinemeetings.config.json: {len(meetings)} meetings")

    return chats, users


# =========================================================================
# 4. CSV ↔ JSON CROSS-VALIDATION
# =========================================================================
def check_csv_json_alignment(csv_rows, chats):
    csv_conv_ids = set(r["conversation_id"] for r in csv_rows)
    json_chat_ids = set(c["ChatId"] for c in chats)

    if csv_conv_ids == json_chat_ids:
        ok("ALIGN", f"CSV and JSON conversation IDs match ({len(csv_conv_ids)} conversations)")
    else:
        csv_only = csv_conv_ids - json_chat_ids
        json_only = json_chat_ids - csv_conv_ids
        if csv_only:
            err("ALIGN", f"{len(csv_only)} conversations in CSV but not JSON")
        if json_only:
            err("ALIGN", f"{len(json_only)} conversations in JSON but not CSV")

    # Message count alignment
    csv_msg_count = len(csv_rows)
    json_msg_count = sum(len(c["ChatMessages"]) for c in chats)
    if csv_msg_count == json_msg_count:
        ok("ALIGN", f"Message count matches: {csv_msg_count}")
    else:
        err("ALIGN", f"Message count mismatch: CSV={csv_msg_count}, JSON={json_msg_count}")


# =========================================================================
# 5. CONVERSATION-LEVEL TASK AUDIT
# =========================================================================
def check_conv_level(csv_rows):
    convs = {}
    for r in csv_rows:
        cid = r["conversation_id"]
        if cid not in convs:
            convs[cid] = {
                "conv_has_task": r["conv_has_task"],
                "topic": r["conversation_topic"],
                "msgs": [],
                "ht_msgs": [],
                "evidence": [],
            }
        convs[cid]["msgs"].append(r)
        if r["has_task"] == "True":
            convs[cid]["ht_msgs"].append(int(r["message_index"]))
        if r["is_task_evidence"] == "True":
            convs[cid]["evidence"].append(int(r["message_index"]))

    conv_true = sum(1 for c in convs.values() if c["conv_has_task"] == "True")
    conv_false = sum(1 for c in convs.values() if c["conv_has_task"] == "False")
    ok("CONV", f"Conversations: {len(convs)} ({conv_true} TRUE, {conv_false} FALSE)")
    ok("CONV", f"Distribution: {round(conv_true/len(convs)*100)}% TRUE / {round(conv_false/len(convs)*100)}% FALSE")

    # Rule 1: FALSE conversations must have ZERO has_task messages
    false_with_tasks = 0
    for cid, info in convs.items():
        if info["conv_has_task"] == "False" and info["ht_msgs"]:
            err("CONV", f"FALSE conv '{info['topic'][:50]}' has {len(info['ht_msgs'])} has_task=TRUE msgs: indices {info['ht_msgs']}")
            false_with_tasks += 1
    if false_with_tasks == 0:
        ok("CONV", "RULE: No has_task msgs in FALSE conversations ✓")

    # Rule 2: FALSE conversations must have ZERO evidence
    false_with_ev = 0
    for cid, info in convs.items():
        if info["conv_has_task"] == "False" and info["evidence"]:
            err("CONV", f"FALSE conv '{info['topic'][:50]}' has evidence msgs")
            false_with_ev += 1
    if false_with_ev == 0:
        ok("CONV", "RULE: No evidence msgs in FALSE conversations ✓")

    # Rule 3: TRUE conversations must have at least one evidence message
    true_no_ev = 0
    for cid, info in convs.items():
        if info["conv_has_task"] == "True" and not info["evidence"]:
            err("CONV", f"TRUE conv '{info['topic'][:50]}' has NO evidence msgs")
            true_no_ev += 1
    if true_no_ev == 0:
        ok("CONV", "RULE: All TRUE conversations have evidence msgs ✓")

    # Rule 4: has_task=TRUE messages must be evidence messages
    ht_not_ev = 0
    for cid, info in convs.items():
        ht_set = set(info["ht_msgs"])
        ev_set = set(info["evidence"])
        extra = ht_set - ev_set
        if extra:
            err("CONV", f"Conv '{info['topic'][:50]}': has_task=TRUE at {sorted(extra)} but NOT evidence")
            ht_not_ev += len(extra)
    if ht_not_ev == 0:
        ok("CONV", "RULE: All has_task=TRUE msgs are also evidence ✓")
    else:
        err("CONV", f"{ht_not_ev} msgs have has_task=TRUE but not evidence")

    # Rule 5: Evidence messages should generally have has_task=TRUE (unless commitments)
    ev_no_ht = 0
    for cid, info in convs.items():
        ev_set = set(info["evidence"])
        ht_set = set(info["ht_msgs"])
        extra = ev_set - ht_set
        ev_no_ht += len(extra)
    if ev_no_ht > 0:
        # These are commitment/expanded evidence messages — acceptable
        ok("CONV", f"Note: {ev_no_ht} evidence msgs without has_task (expanded pairs/commitments)")
    else:
        ok("CONV", "All evidence messages have has_task=TRUE")

    return convs


# =========================================================================
# 6. SPEC COMPLIANCE: HasTask Rules
# =========================================================================
def check_spec_compliance(csv_rows):
    # Commitment = has_task FALSE (per spec Section 2.1)
    commitment_errors = 0
    for r in csv_rows:
        if r["task_sub_class"] == "Commitment" and r["has_task"] == "True":
            err("SPEC", f"Commitment with has_task=TRUE: '{r['content'][:60]}' (conv: {r['conversation_topic'][:40]})")
            commitment_errors += 1
    if commitment_errors == 0:
        ok("SPEC", "RULE: No Commitment messages with has_task=TRUE ✓")

    # has_task=TRUE must have sub_class != Neither
    ht_neither = 0
    for r in csv_rows:
        if r["has_task"] == "True" and r["task_sub_class"] == "Neither":
            err("SPEC", f"has_task=TRUE with sub_class=Neither: '{r['content'][:60]}'")
            ht_neither += 1
    if ht_neither == 0:
        ok("SPEC", "RULE: All has_task=TRUE have sub_class ≠ Neither ✓")

    # has_task=TRUE must have attribution
    ht_no_attr = 0
    for r in csv_rows:
        if r["has_task"] == "True" and not r["attribution"]:
            err("SPEC", f"has_task=TRUE with empty attribution: '{r['content'][:60]}'")
            ht_no_attr += 1
    if ht_no_attr == 0:
        ok("SPEC", "RULE: All has_task=TRUE have attribution ✓")

    # has_task=TRUE must have task_type
    ht_no_tt = 0
    for r in csv_rows:
        if r["has_task"] == "True" and not r["task_type"]:
            err("SPEC", f"has_task=TRUE with empty task_type: '{r['content'][:60]}'")
            ht_no_tt += 1
    if ht_no_tt == 0:
        ok("SPEC", "RULE: All has_task=TRUE have task_type ✓")

    # has_task=FALSE should have sub_class=Neither (or Commitment)
    false_noneither = 0
    for r in csv_rows:
        if r["has_task"] == "False" and r["task_sub_class"] not in ("Neither", "Commitment"):
            warn("SPEC", f"has_task=FALSE but sub_class={r['task_sub_class']}: '{r['content'][:60]}'")
            false_noneither += 1
    if false_noneither == 0:
        ok("SPEC", "RULE: has_task=FALSE msgs have sub_class=Neither or Commitment ✓")

    # Valid attribution values
    valid_attr = {"Explicit", "Implicit", "Unassigned", "Broadcast", "N/A", ""}
    actual_attr = set(r["attribution"] for r in csv_rows)
    invalid_attr = actual_attr - valid_attr
    if invalid_attr:
        err("SPEC", f"Invalid attribution values: {invalid_attr}")
    else:
        ok("SPEC", f"All attribution values valid")

    # Valid task types
    valid_tt = {"Action Request", "Review / Approval", "Scheduling", "Delegation",
                "Question", "Confirmation / Permission", "Availability / RSVP",
                "Status Request", "Decision Request", "Follow-up", ""}
    actual_tt = set(r["task_type"] for r in csv_rows)
    invalid_tt = actual_tt - valid_tt
    if invalid_tt:
        err("SPEC", f"Invalid task_type values: {invalid_tt}")
    else:
        ok("SPEC", f"All task_type values valid")

    # Task type coverage (for has_task=TRUE messages)
    tt_counts = Counter(r["task_type"] for r in csv_rows if r["has_task"] == "True")
    ok("SPEC", f"Task types represented: {len(tt_counts)}/10")
    for tt, cnt in sorted(tt_counts.items()):
        ok("SPEC", f"  {tt}: {cnt}")


# =========================================================================
# 7. INTERACTION SIGNALS
# =========================================================================
def check_signals(chats):
    reaction_count = 0
    followed_count = 0
    saved_count = 0
    reminder_count = 0
    total_msgs = 0

    for chat in chats:
        for msg in chat["ChatMessages"]:
            total_msgs += 1
            if msg.get("Reactions"):
                reaction_count += 1
            if msg.get("Followed"):
                followed_count += 1
            if msg.get("Saved"):
                saved_count += 1
            if msg.get("Reminder"):
                reminder_count += 1

    ok("SIGNALS", f"Reactions: {reaction_count}/{total_msgs} ({round(reaction_count/total_msgs*100)}%)")
    ok("SIGNALS", f"Followed: {followed_count}/{total_msgs} ({round(followed_count/total_msgs*100)}%)")
    ok("SIGNALS", f"Saved: {saved_count}/{total_msgs} ({round(saved_count/total_msgs*100)}%)")
    ok("SIGNALS", f"Reminder: {reminder_count}/{total_msgs} ({round(reminder_count/total_msgs*100)}%)")

    if reaction_count == 0:
        warn("SIGNALS", "No reactions found")
    if followed_count == 0:
        warn("SIGNALS", "No followed found")


# =========================================================================
# 8. DOMAIN & CHAT TYPE COVERAGE
# =========================================================================
def check_coverage(csv_rows):
    domains = Counter(r["domain"] for r in csv_rows)
    ok("COVERAGE", f"Domains: {len(domains)}")
    for d, cnt in sorted(domains.items()):
        ok("COVERAGE", f"  {d}: {cnt} msgs")

    chat_types = Counter(r["chat_type"] for r in csv_rows)
    ok("COVERAGE", f"Chat types: {dict(chat_types)}")

    # Check distribution isn't too skewed
    total = len(csv_rows)
    for ct, cnt in chat_types.items():
        pct = cnt / total * 100
        if pct < 5:
            warn("COVERAGE", f"{ct} only {pct:.1f}% of messages")

    # Unique users
    users = set(r["from_user"] for r in csv_rows)
    ok("COVERAGE", f"Unique users: {len(users)}")

    # Edge cases
    edges = sum(1 for r in csv_rows if r["edge_case"])
    ok("COVERAGE", f"Edge cases: {edges} ({round(edges/total*100)}%)")


# =========================================================================
# 9. QUADRANT VERIFICATION
# =========================================================================
def check_quadrants(csv_rows):
    tt = sum(1 for r in csv_rows if r["has_task"] == "True" and r["is_important"] == "True")
    tf = sum(1 for r in csv_rows if r["has_task"] == "True" and r["is_important"] == "False")
    ft = sum(1 for r in csv_rows if r["has_task"] == "False" and r["is_important"] == "True")
    ff = sum(1 for r in csv_rows if r["has_task"] == "False" and r["is_important"] == "False")

    ok("QUADRANT", f"HasTask+Important: {tt}")
    ok("QUADRANT", f"HasTask+NotImportant: {tf}")
    ok("QUADRANT", f"NotTask+Important: {ft}")
    ok("QUADRANT", f"NotTask+NotImportant: {ff}")

    # All quadrants should be non-empty
    for label, val in [("TT", tt), ("TF", tf), ("FT", ft), ("FF", ff)]:
        if val == 0:
            err("QUADRANT", f"Quadrant {label} is EMPTY")


# =========================================================================
# 10. CONV-LEVEL QUADRANT (conv_has_task × has any important msg)
# =========================================================================
def check_conv_quadrant(csv_rows):
    convs = {}
    for r in csv_rows:
        cid = r["conversation_id"]
        if cid not in convs:
            convs[cid] = {"conv_has_task": r["conv_has_task"], "has_important": False, "topic": r["conversation_topic"]}
        if r["is_important"] == "True":
            convs[cid]["has_important"] = True

    q_tt = sum(1 for c in convs.values() if c["conv_has_task"] == "True" and c["has_important"])
    q_tf = sum(1 for c in convs.values() if c["conv_has_task"] == "True" and not c["has_important"])
    q_ft = sum(1 for c in convs.values() if c["conv_has_task"] == "False" and c["has_important"])
    q_ff = sum(1 for c in convs.values() if c["conv_has_task"] == "False" and not c["has_important"])

    ok("CONV-QUAD", f"Conv Task+Important: {q_tt}")
    ok("CONV-QUAD", f"Conv Task+NotImportant: {q_tf}")
    ok("CONV-QUAD", f"Conv NoTask+Important: {q_ft}")
    ok("CONV-QUAD", f"Conv NoTask+NotImportant: {q_ff}")


# =========================================================================
# 11. HTML BASIC CHECKS
# =========================================================================
def check_html():
    path = os.path.join(OUTPUT, "review.html")
    with open(path, encoding="utf-8") as f:
        html = f.read()

    size_kb = len(html) / 1024
    ok("HTML", f"review.html size: {size_kb:.0f} KB")

    # Check key elements exist
    checks = [
        ("conv-task-badge", "Conversation task badge"),
        ("evidence-badge", "Evidence badge"),
        ("filterConvTask", "Conv HasTask filter"),
        ("filterChatType", "Chat Type filter"),
        ("filterHasTask", "HasTask filter"),
        ("conv-card", "Conversation cards"),
        ("TASK</span>", "TASK label"),
        ("NO TASK</span>", "NO TASK label"),
        ("EVIDENCE</span>", "EVIDENCE label"),
        ("Dataset Summary", "Summary section"),
        ("Conversation-First", "Conversation-first explanation"),
    ]
    for needle, desc in checks:
        if needle in html:
            ok("HTML", f"Contains: {desc}")
        else:
            err("HTML", f"Missing: {desc}")

    # Count TASK / NO TASK badges
    task_count = html.count('>TASK</span>')
    no_task_count = html.count('>NO TASK</span>')
    ok("HTML", f"TASK badges: {task_count}, NO TASK badges: {no_task_count}")

    # Count evidence badges
    ev_count = html.count('>EVIDENCE</span>')
    ok("HTML", f"EVIDENCE badges: {ev_count}")


# =========================================================================
# 12. REACTION SEMANTIC SPOT CHECK
# =========================================================================
def check_reaction_semantics(chats):
    """Spot check: no celebration emojis on negative/incident messages."""
    happy_emojis = {"🎉", "🔥", "💯", "😂", "😊"}
    negative_kw = ["incident", "outage", "breach", "failure", "down", "critical",
                   "urgent", "emergency", "security", "production down"]

    mismatches = 0
    for chat in chats:
        for msg in chat["ChatMessages"]:
            content_lower = msg.get("Content", "").lower()
            reactions = msg.get("Reactions", [])
            if not reactions:
                continue
            is_negative = any(kw in content_lower for kw in negative_kw)
            if is_negative:
                for rxn in reactions:
                    if rxn["Reaction"] in happy_emojis:
                        # Check for resolution context
                        has_resolution = any(w in content_lower for w in
                            ["resolved", "fixed", "recovered", "restored", "back online",
                             "clean", "passed", "completed", "all clear"])
                        if not has_resolution:
                            err("REACTIONS", f"Happy emoji {rxn['Reaction']} on negative msg: '{msg['Content'][:80]}'")
                            mismatches += 1
    if mismatches == 0:
        ok("REACTIONS", "No celebration emojis on negative messages ✓")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  GOLDEN DATASET — END-TO-END QC AUDIT")
    print("=" * 70)

    check_files()
    csv_rows = check_csv()
    chats, users = check_json()
    check_csv_json_alignment(csv_rows, chats)
    check_conv_level(csv_rows)
    check_spec_compliance(csv_rows)
    check_signals(chats)
    check_coverage(csv_rows)
    check_quadrants(csv_rows)
    check_conv_quadrant(csv_rows)
    check_html()
    check_reaction_semantics(chats)

    print()
    print(f"{'=' * 70}")
    print(f"  RESULTS: {len(PASS)} PASS | {len(WARNINGS)} WARNINGS | {len(ERRORS)} ERRORS")
    print(f"{'=' * 70}")

    if ERRORS:
        print("\n❌ ERRORS:")
        for e in ERRORS:
            print(f"  {e}")

    if WARNINGS:
        print("\n⚠️  WARNINGS:")
        for w in WARNINGS:
            print(f"  {w}")

    print(f"\n✅ PASSED CHECKS ({len(PASS)}):")
    for p in PASS:
        print(f"  {p}")

    print()
    if ERRORS:
        print(f"❌ AUDIT FAILED — {len(ERRORS)} error(s)")
        sys.exit(1)
    else:
        print(f"✅ AUDIT PASSED — {len(PASS)} checks, {len(WARNINGS)} warnings")
        sys.exit(0)

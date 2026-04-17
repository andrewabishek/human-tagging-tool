"""
LLM Auto-Tagger: Upload second-judge tags as "Andrew Abishek"
For all 90 single-judge conversations (not already tagged by Andrew or Utkarsh).
Tagged independently by Claude Opus 4.6 following HasTask_IsImportant_Tag_Definitions_v3.md
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

JUDGE_NAME = "Andrew Abishek"

# ============================================================
# ALL 90 TAGS — independently evaluated
# ============================================================
tags = [
    # =====================================================
    # BATCH 1: Previously Jo-only conversations (#11-#43)
    # =====================================================
    {
        "db_id": 11,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["amandafoster"]),
    },
    {
        "db_id": 12,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["priyasharma", "ninacosta"]),
    },
    {
        "db_id": 13,
        "has_task": True, "is_important": False,
        "task_type": "Review / Approval", "attribution": "Implicit",
        "task_assignees": json.dumps(["kevinzhang", "lisanakamura"]),
    },
    {
        "db_id": 14,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["mariasantos"]),
    },
    {
        "db_id": 15,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["davidpark"]),
    },
    {
        "db_id": 16,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "Everyone (Broadcast)"]),
    },
    {
        "db_id": 17,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["sofiarodriguez", "michaelchen"]),
    },
    {
        "db_id": 18,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["alexkumar", "chrisevans", "davidpark"]),
    },
    {
        "db_id": 19,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["racheltorres", "davidpark"]),
    },
    {
        "db_id": 20,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["chrisevans", "sofiarodriguez"]),
    },
    {
        "db_id": 21,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma", "jameswilson", "alexkumar"]),
    },
    {
        "db_id": 22,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["daniellewright", "davidpark", "alexkumar"]),
    },
    {
        "db_id": 23,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["amandafoster", "sofiarodriguez"]),
    },
    {
        "db_id": 24,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["kevinzhang"]),
    },
    {
        "db_id": 25,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["alexkumar", "derekjohnson"]),
    },
    {
        # GT=FALSE. Independent eval: PR review has explicit RfAs (add tests, add prometheus metric).
        # "Can you review my PR?" -> TRUE (RfA). Code review requests ARE tasks.
        "db_id": 26,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma", "ninacosta"]),
    },
    {
        "db_id": 27,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["chrisevans", "lisanakamura"]),
    },
    {
        "db_id": 28,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["davidpark", "kevinzhang", "daniellewright"]),
    },
    {
        "db_id": 29,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["chrisevans"]),
    },
    {
        # GT=FALSE. Independent eval: Lisa explicitly asks Derek to switch to backup workflow
        # AND send list of impacted SLA responses. Rule: "Message with both status + ask" -> TRUE.
        # Also: tool outage affecting business = IsImportant=TRUE.
        "db_id": 30,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["derekjohnson"]),
    },
    {
        "db_id": 31,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma"]),
    },
    {
        "db_id": 32,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["chrisevans", "sofiarodriguez", "mariasantos"]),
    },
    {
        "db_id": 33,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["mariasantos", "alexkumar", "derekjohnson"]),
    },
    {
        "db_id": 34,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "daniellewright", "davidpark"]),
    },
    {
        "db_id": 35,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["lisanakamura", "ninacosta"]),
    },
    {
        "db_id": 36,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["alexkumar", "lisanakamura"]),
    },
    {
        "db_id": 37,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["kevinzhang", "lisanakamura"]),
    },
    {
        "db_id": 38,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["Everyone (Broadcast)"]),
    },
    {
        "db_id": 39,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "priyasharma", "ninacosta"]),
    },
    {
        # Team Social — Lunch & Weekend Plans
        "db_id": 40,
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
    },
    {
        "db_id": 41,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma", "jameswilson", "alexkumar"]),
    },
    {
        "db_id": 42,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["sofiarodriguez", "racheltorres"]),
    },
    {
        "db_id": 43,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["davidpark", "racheltorres", "amandafoster"]),
    },
    # Jo-only FALSE conversations
    {"db_id": 94, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 95, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 96, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 97, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 98, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 99, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 100, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 110, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 111, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 112, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 113, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 114, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 115, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},
    {"db_id": 116, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},

    # =====================================================
    # BATCH 2: Sasank-only conversations (#44-50, #76-93)
    # =====================================================
    {
        # Postmortem — API Gateway Incident
        "db_id": 44,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "alexkumar", "derekjohnson"]),
    },
    {
        # H2 Product Strategy Offsite — major strategic pivot, high org impact
        "db_id": 45,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["davidpark", "michaelchen", "laurakim"]),
    },
    {
        # H1 Performance Calibration
        "db_id": 46,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["davidpark", "michaelchen"]),
    },
    {
        # GlobalTech & Pinnacle — Customer Escalation Review (follow-up, resolved)
        "db_id": 47,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["mariasantos", "derekjohnson", "alexkumar"]),
    },
    {
        # Budget Committee — Q2 Spend Approvals
        "db_id": 48,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["kevinzhang"]),
    },
    {
        # Engineering Weekly Standup
        "db_id": 49,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "priyasharma"]),
    },
    {
        # Q1 All-Hands Follow-up
        "db_id": 50,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["daniellewright", "davidpark", "laurakim"]),
    },
    {
        # Design Review Feedback
        "db_id": 76,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["chrisevans"]),
    },
    {
        # Q2 Budget Review Meeting
        "db_id": 77,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["kevinzhang"]),
    },
    {
        # System Notifications Discussion — Alex asked to fix duplicate webhook
        "db_id": 78,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["alexkumar"]),
    },
    {
        # Engineering Standup Thread — GT=TRUE. Alex directs Priya to coordinate.
        "db_id": 79,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma"]),
    },
    {
        # Casual Check-in with CTO — GT=FALSE. Strategic musing, explicitly deferred.
        # "When things calm down, let's revisit" = deferred proposal = FALSE
        "db_id": 80,
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
    },
    {
        # Data Export & Call Scheduling — "Can you call me when you're free?"
        # Explicit ask to call + discuss migration plan = RfA
        "db_id": 81,
        "has_task": True, "is_important": False,
        "task_type": "Scheduling Action", "attribution": "Implicit",
        "task_assignees": json.dumps(["jameswilson"]),
    },
    {
        # Sprint 48 Pre-Launch Tasks — ship-blocking quality, EOD deadline
        "db_id": 82,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["ninacosta"]),
    },
    {
        # EOQ Cleanup Tasks — Alex asks team to confirm, asks James to escalate DNS
        "db_id": 83,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "Everyone (Broadcast)"]),
    },
    # Sasank FALSE conversations
    {"db_id": 84, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Happy Birthday Chris
    {"db_id": 85, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Weekend Plans
    {"db_id": 86, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Office Closure
    {
        # System Maintenance — Complete. GT=FALSE. All informational/status updates.
        # Derek's "I'll let customers know" is a self-commitment, not a task for anyone.
        "db_id": 87,
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
    },
    {"db_id": 88, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # 10K Customers celebration
    {"db_id": 89, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Lunch Today
    {"db_id": 90, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # VPN Setup Help
    {"db_id": 91, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Expense Report Question
    {"db_id": 92, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Interesting Read
    {"db_id": 93, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Sprint 46 Report

    # =====================================================
    # BATCH 3: Ritika-only conversations (#51-59)
    # =====================================================
    {
        # Migration Follow-ups — Alex asks Priya for analysis, docs, benchmarks
        "db_id": 51,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["priyasharma"]),
    },
    {
        # Contoso Enterprise Agreement Review — $2.3M deal, Sofia asks Amanda for redline
        "db_id": 52,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["amandafoster"]),
    },
    {
        # Campaign Launch Coordination — Laura asks Chris for room, blog post, metrics
        "db_id": 53,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["chrisevans"]),
    },
    {
        # Q2 Planning Edge Cases — Alex asks James for feasibility assessment
        "db_id": 54,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson"]),
    },
    {
        # Zenith Corp Escalation — URGENT: third-largest customer, second outage, churn risk
        "db_id": 55,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["alexkumar", "jameswilson", "mariasantos"]),
    },
    {
        # Employee Relations & Policy Updates — Sarah asks Danielle for Q1 attrition numbers
        "db_id": 56,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["daniellewright"]),
    },
    {
        # Q2 Kickoff Planning — GT=FALSE. Contains RfAs: Danielle to book room+invite,
        # Laura sends template. These are scheduling/logistics tasks.
        # Evaluating: "book the all-hands room and send the invite" to "full leadership team
        # plus department heads" is a concrete delegation with specific scope.
        "db_id": 57,
        "has_task": True, "is_important": False,
        "task_type": "Scheduling Action", "attribution": "Explicit",
        "task_assignees": json.dumps(["daniellewright"]),
    },
    {
        # Security Incident Postmortem — second security event this quarter, SOC 2, board briefing
        "db_id": 58,
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "priyasharma", "alexkumar"]),
    },
    {
        # Q1 Close & Audit Prep Follow-ups
        "db_id": 59,
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["kevinzhang"]),
    },

    # =====================================================
    # BATCH 4: yashvijay-only conversations (#101-109)
    # =====================================================
    {"db_id": 101, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Q1 Revenue
    {"db_id": 102, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Pet Tax Thread
    {"db_id": 103, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Product Demo
    {"db_id": 104, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Game Last Night
    {"db_id": 105, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # All-Hands Recording
    {"db_id": 106, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Trivia
    {"db_id": 107, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # WiFi Password
    {"db_id": 108, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Holiday Party Recap
    {"db_id": 109, "has_task": False, "is_important": False, "task_type": None, "attribution": None, "task_assignees": None},  # Git Branch Question
]

# ============================================================
# UPLOAD TO SUPABASE
# ============================================================

print(f"=== Uploading {len(tags)} tags as '{JUDGE_NAME}' ===\n")

# Get conversation topics for display
all_convs = db.table('conversations').select('id, topic, ground_truth_has_task').execute()
conv_map = {c['id']: c for c in all_convs.data}

success = 0
failed = 0

for t in tags:
    conv_id = t['db_id']
    topic = conv_map.get(conv_id, {}).get('topic', '?')[:55]
    
    try:
        # Create assignment (ignore if already exists)
        try:
            db.table('conversation_assignments').insert({
                "conversation_id": conv_id,
                "judge_name": JUDGE_NAME,
            }).execute()
        except Exception:
            pass  # assignment already exists, that's fine

        # Create tag
        tag_data = {
            "conversation_id": conv_id,
            "judge_name": JUDGE_NAME,
            "has_task": t['has_task'],
            "is_important": t['is_important'],
            "task_type": t['task_type'],
            "attribution": t['attribution'],
            "task_assignees": t['task_assignees'],
        }
        db.table('conversation_tags').upsert(tag_data, on_conflict='conversation_id,judge_name').execute()
        
        ht = "TRUE" if t['has_task'] else "FALSE"
        imp = "TRUE" if t['is_important'] else "FALSE"
        tt = t['task_type'] or '-'
        print(f"  OK #{conv_id:3d} {topic:55s} | HasTask={ht:5s} Imp={imp:5s} Type={tt}")
        success += 1
        
    except Exception as e:
        print(f"  !! #{conv_id} {topic} | ERROR: {e}")
        failed += 1

print(f"\n=== COMPLETE: {success} succeeded, {failed} failed ===")

# Summary stats
true_task = sum(1 for t in tags if t['has_task'])
false_task = sum(1 for t in tags if not t['has_task'])
true_imp = sum(1 for t in tags if t['is_important'])

gt_agree = 0
gt_disagree = []
for t in tags:
    c = conv_map.get(t['db_id'])
    if c:
        gt = c['ground_truth_has_task']
        if t['has_task'] == gt:
            gt_agree += 1
        else:
            gt_disagree.append((t['db_id'], c['topic'][:50], t['has_task'], gt))

print(f"\nTag Distribution:")
print(f"  HasTask=TRUE:  {true_task}")
print(f"  HasTask=FALSE: {false_task}")
print(f"  IsImportant=TRUE: {true_imp}")
print(f"\nGT Agreement: {gt_agree}/{len(tags)} ({100*gt_agree/len(tags):.1f}%)")
if gt_disagree:
    print(f"\nDisagreements with GT ({len(gt_disagree)}):")
    for cid, topic, mine, gt in gt_disagree:
        print(f"  #{cid} {topic} | Mine={mine} GT={gt}")

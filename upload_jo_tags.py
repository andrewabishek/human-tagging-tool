"""
LLM Auto-Tagger: Upload conversation tags to Supabase as judge "Jo"
Tagged by Claude Opus 4.6 following HasTask_IsImportant_Tag_Definitions_v3.md
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from supabase import create_client
from datetime import datetime

db = create_client('https://prcewohktalsbmyvrpgd.supabase.co', 'sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x')

JUDGE_NAME = "Jo"

# ============================================================
# ALL 47 TAGS — based on full conversation analysis
# ============================================================
tags = [
    # --- HasTask=TRUE conversations (GT=True) ---
    {
        "db_id": 11, "topic": "Northwind Traders NDA Review",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["amandafoster"]),
        "reasoning": "Sofia asks Amanda to review/redline NDA by Wednesday. 1:1 chat → implicit attribution to non-sender."
    },
    {
        "db_id": 12, "topic": "Release Blocker — Dashboard Rendering Bug",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["priyasharma", "ninacosta"]),
        "reasoning": "Release blocker for v4.2. Priya asked to fix bug, Nina asked to run regression suite. High urgency — ship-blocking."
    },
    {
        "db_id": 13, "topic": "Office Equipment & Software Procurement",
        "has_task": True, "is_important": False,
        "task_type": "Review / Approval", "attribution": "Implicit",
        "task_assignees": json.dumps(["kevinzhang", "lisanakamura"]),
        "reasoning": "Lisa asks Kevin to approve $28K PO. Kevin asks Lisa for delivery confirmation and vendor comparison. Routine procurement."
    },
    {
        "db_id": 14, "topic": "Customer Testimonial — Pinnacle Logistics",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["mariasantos"]),
        "reasoning": "Laura asks Maria to get formal sign-off from Pinnacle, share draft outline, coordinate with Chris. 1:1 implicit."
    },
    {
        "db_id": 15, "topic": "Engineering Platform Investment — Build vs Buy",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["davidpark"]),
        "reasoning": "Rachel asks David to build the business case with both options modeled out by Monday. 1:1 implicit."
    },
    {
        "db_id": 16, "topic": "Engineering Daily Standup",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "Everyone (Broadcast)"]),
        "reasoning": "Priya asks James to review PR before noon. Nina asks James to push latest build. Alex asks everyone to update Jira by EOD."
    },
    {
        "db_id": 17, "topic": "Q1 Pipeline Review & Forecast",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["sofiarodriguez", "michaelchen"]),
        "reasoning": "Michael asks Sofia for daily Contoso status updates. Sarah asks Michael for risk mitigation plan by Monday. Revenue at risk, board visibility."
    },
    {
        "db_id": 18, "topic": "Meridian v4.2 Launch Coordination",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["alexkumar", "chrisevans", "davidpark"]),
        "reasoning": "Multiple launch tasks. Laura asks Alex for screenshots. Sarah asks David+Alex for readiness review. First release since Series C — investors watching."
    },
    {
        "db_id": 19, "topic": "Board Meeting Preparation — Q1 Review",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["racheltorres", "davidpark"]),
        "reasoning": "Sarah asks Rachel for cost optimization slide, David for 3-min AI demo, Rachel to coordinate dry run. Board meeting — leadership-visible."
    },
    {
        "db_id": 20, "topic": "Q2 Campaign Alignment — Marketing + Sales",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["chrisevans", "sofiarodriguez"]),
        "reasoning": "Laura asks Chris for updated messaging draft by Monday. Chris asks Sofia for objection list. Routine campaign planning."
    },
    {
        "db_id": 21, "topic": "Production Incident — Database Connection Pool Exhaustion",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma", "jameswilson", "alexkumar"]),
        "reasoning": "Production down — 8000 users affected. Multiple urgent tasks: Priya push fix, James kill batch job, Alex schedule postmortem. Active incident."
    },
    {
        "db_id": 22, "topic": "Q2 Headcount Planning — Engineering",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["daniellewright", "davidpark", "alexkumar"]),
        "reasoning": "Rachel asks Danielle to start req process. Danielle asks David/Alex for updated JDs. Routine headcount planning."
    },
    {
        "db_id": 23, "topic": "Northwind Traders — Contract Review",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["amandafoster", "sofiarodriguez"]),
        "reasoning": "Michael asks Amanda for counter-proposal by Wed EOD. Asks Sofia to set up call with Northwind legal on Thursday."
    },
    {
        "db_id": 24, "topic": "Q1 Budget Review & Q2 Forecast",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["kevinzhang"]),
        "reasoning": "Sarah asks Kevin for cost optimization analysis ($500K savings) by next Friday. $1.1M below plan, board expects fiscal discipline."
    },
    {
        "db_id": 25, "topic": "Pinnacle Logistics — P1 Escalation Thread",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["alexkumar", "derekjohnson"]),
        "reasoning": "$1.2M ARR customer, P1 open 5 days, VP emailing CEO. Alex assigns Priya + expedites. Maria asks Derek to update customer. Churn risk + escalation."
    },
    {
        "db_id": 26, "topic": "PR #852 — Connection Pool Fix Review",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma", "ninacosta"]),
        "reasoning": "Priya asks Nina for thorough review. Nina requests abrupt disconnect tests + stress tests. Alex asks for prometheus metric. Clear RfAs within code review."
    },
    {
        "db_id": 27, "topic": "Q1 All-Hands Planning",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["chrisevans", "lisanakamura"]),
        "reasoning": "Laura asks Chris for visual deck + video montage. Danielle asks Lisa for venue/catering. Event planning tasks."
    },
    {
        "db_id": 28, "topic": "SOC 2 & GDPR Compliance — Cross-team Coordination",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["davidpark", "kevinzhang", "daniellewright"]),
        "reasoning": "SOC 2 audit April 15 — 'a failed audit would be devastating for enterprise sales.' Amanda assigns tasks to David, Kevin, Danielle. Evidence packages due April 8."
    },
    {
        "db_id": 29, "topic": "Spring Campaign — Creative Review",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["chrisevans"]),
        "reasoning": "Laura asks Chris to update all campaign assets with final tagline and send proofs by Thursday. Routine creative work."
    },
    {
        "db_id": 30, "topic": "Salesforce Down — Impact & Workaround",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["derekjohnson"]),
        "reasoning": "Lisa asks Derek to switch team to backup workflow and send list of impacted SLA responses. Tool outage affecting business processes."
    },
    {
        "db_id": 31, "topic": "AI Resource Allocation Feature — Requirements",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma"]),
        "reasoning": "David asks Priya for working demo by end of next week. Key Q2 roadmap item but no urgency/escalation."
    },
    {
        "db_id": 32, "topic": "Marketing Weekly Sync Notes",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["chrisevans", "sofiarodriguez", "mariasantos"]),
        "reasoning": "Laura assigns: Chris (landing page by Thu), Sofia (objection list by Wed), Maria (confirm Pinnacle by next Wed). Routine weekly tasks."
    },
    {
        "db_id": 33, "topic": "GlobalTech Solutions — Churn Risk Escalation",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["mariasantos", "alexkumar", "derekjohnson"]),
        "reasoning": "URGENT: $850K ARR customer threatening to cancel. CTO emailed CEO. Michael asks Maria for recovery plan. Alex assigns engineer. 24h action plan needed."
    },
    {
        "db_id": 34, "topic": "SECURITY: Potential Data Exposure Incident",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "daniellewright", "davidpark"]),
        "reasoning": "Potential GDPR/CCPA incident. 247 customers exposed. 72-hour notification window. Amanda assigns tasks to James (logs), Danielle (notification draft), David (containment)."
    },
    {
        "db_id": 35, "topic": "Spring Hackathon Planning",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["lisanakamura", "ninacosta"]),
        "reasoning": "Alex asks Lisa for logistics/catering. Nina volunteers to draft registration form. Fun event, not urgent."
    },
    {
        "db_id": 36, "topic": "New Hire Onboarding — Starting April 7",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["alexkumar", "lisanakamura"]),
        "reasoning": "Danielle asks Alex for onboarding plan/buddy pairings, asks Lisa for laptops/badges/desk setup. Routine onboarding."
    },
    {
        "db_id": 37, "topic": "Observability Vendor Evaluation — Datadog vs New Relic",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Implicit",
        "task_assignees": json.dumps(["kevinzhang", "lisanakamura"]),
        "reasoning": "David asks Kevin for final cost model by Wednesday (3 discount scenarios). David asks Lisa to schedule vendor call. Routine evaluation."
    },
    {
        "db_id": 38, "topic": "Q2 OKR Planning — Leadership Alignment",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["Everyone (Broadcast)"]),
        "reasoning": "Sarah asks all department heads to submit finalized OKR docs by Friday COB. Broadcast ask to leadership team."
    },
    {
        "db_id": 39, "topic": "Sprint 14 Retrospective Notes",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["jameswilson", "priyasharma", "ninacosta"]),
        "reasoning": "Alex assigns: James (deployment gates by Sprint 15), Priya (monitoring dashboard by next week), Nina (multi-tenant regression suite)."
    },
    {
        "db_id": 41, "topic": "Sprint 15 Planning",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["priyasharma", "jameswilson", "alexkumar"]),
        "reasoning": "David asks Priya for demo-ready prototype. Alex asks James for effort estimate + to check with Lisa. David asks Alex for sprint scope by EOD."
    },
    {
        "db_id": 42, "topic": "Q1 QBR — Sales & Revenue Review",
        "has_task": True, "is_important": False,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["sofiarodriguez", "racheltorres"]),
        "reasoning": "Sarah asks Sofia for competitive win-back plan. Sarah asks Rachel for margin analysis for mid-market tier. Standard QBR follow-ups."
    },
    {
        "db_id": 43, "topic": "Board Deck Final Review — Dry Run",
        "has_task": True, "is_important": True,
        "task_type": "Action Request", "attribution": "Explicit",
        "task_assignees": json.dumps(["davidpark", "racheltorres", "amandafoster"]),
        "reasoning": "Sarah asks David to simplify slides, Rachel for profitability appendix. Hard deadline Tuesday noon (board bylaws require 48h distribution). Leadership-visible."
    },

    # --- HasTask=FALSE conversations ---
    {
        "db_id": 40, "topic": "Team Social — Lunch & Weekend Plans",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Social/phatic conversation. Lunch coordination and weekend plans. No work tasks."
    },
    {
        "db_id": 94, "topic": "Priya's 3-Year Anniversary",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Celebration/recognition. No task or urgency."
    },
    {
        "db_id": 95, "topic": "Competitor News — Worth Knowing",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "FYI about competitor news. Pipeline team already routing inbound. No task assigned."
    },
    {
        "db_id": 96, "topic": "Amazing Customer Feedback!",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Sharing positive customer feedback. Recognition/celebration, no task."
    },
    {
        "db_id": 97, "topic": "General Chat",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Social chat about weather and sunrise. No work content."
    },
    {
        "db_id": 98, "topic": "Meeting Link",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Trivial ask for meeting link, immediately resolved ('Got it, thanks!'). Routine logistics."
    },
    {
        "db_id": 99, "topic": "Feedback on Security Training",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Sharing feedback/thanks on completed training. No new task."
    },
    {
        "db_id": 100, "topic": "New Office Tour",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Sharing photos of new office space. Social/informational."
    },
    {
        "db_id": 110, "topic": "Shoutout — Nina's QA Work",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Recognition/praise for Nina's work. No task."
    },
    {
        "db_id": 111, "topic": "Meridian v4.2 Launch Day!",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Celebration of successful launch. Status updates (positive). No new task or urgency."
    },
    {
        "db_id": 112, "topic": "Quick Status Check",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Informal check-in, 'no urgency'. Status given immediately. No task — routine FYI."
    },
    {
        "db_id": 113, "topic": "Coffee Machine Situation",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "PSA about broken coffee machine. Facilities already notified. Social/operational noise."
    },
    {
        "db_id": 114, "topic": "Traffic Alert",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "FYI about traffic. Personal logistics/social."
    },
    {
        "db_id": 115, "topic": "March Book Club Pick",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Social — book club discussion. No work task."
    },
    {
        "db_id": 116, "topic": "CI/CD — Build Notifications",
        "has_task": False, "is_important": False,
        "task_type": None, "attribution": None, "task_assignees": None,
        "reasoning": "Automated build notification + acknowledgments. Informational, no task."
    },
]

# ============================================================
# UPLOAD TO SUPABASE
# ============================================================

print(f"=== LLM Auto-Tagger: Uploading {len(tags)} tags as judge '{JUDGE_NAME}' ===\n")

# 1. Create judge session
session = db.table('judge_sessions').insert({
    "judge_name": JUDGE_NAME,
}).execute()
print(f"Created judge session: {session.data[0]['id']}")

# 2. Track stats
success = 0
failed = 0

for t in tags:
    conv_id = t['db_id']
    topic = t['topic']
    
    try:
        # Create assignment
        db.table('conversation_assignments').insert({
            "conversation_id": conv_id,
            "judge_name": JUDGE_NAME,
        }).execute()

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
        
        # Format display
        ht = "TRUE" if t['has_task'] else "FALSE"
        imp = "TRUE" if t['is_important'] else "FALSE"
        tt = t['task_type'] or '-'
        attr = t['attribution'] or '-'
        assign = t['task_assignees'] or '-'
        
        print(f"  ✓ #{conv_id:3d} {topic[:50]:50s} | HasTask={ht:5s} Important={imp:5s} Type={tt}")
        success += 1
        
    except Exception as e:
        print(f"  ✗ #{conv_id} {topic[:50]} | ERROR: {e}")
        failed += 1

print(f"\n=== COMPLETE: {success} succeeded, {failed} failed ===")

# 3. Summary stats
true_task = sum(1 for t in tags if t['has_task'])
false_task = sum(1 for t in tags if not t['has_task'])
true_imp = sum(1 for t in tags if t['is_important'])
gt_agree = 0
for t in tags:
    # Check agreement with ground truth
    convs = db.table('conversations').select('ground_truth_has_task').eq('id', t['db_id']).execute()
    if convs.data:
        gt = convs.data[0]['ground_truth_has_task']
        if t['has_task'] == gt:
            gt_agree += 1
            
print(f"\nTag Distribution:")
print(f"  HasTask=TRUE:  {true_task}")
print(f"  HasTask=FALSE: {false_task}")
print(f"  IsImportant=TRUE: {true_imp}")
print(f"\nGround Truth Agreement: {gt_agree}/{len(tags)} ({100*gt_agree/len(tags):.1f}%)")

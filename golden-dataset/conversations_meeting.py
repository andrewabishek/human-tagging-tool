"""
Golden Dataset - Meeting Chat Conversations
10 meeting chats — messages exchanged in the meeting chat panel during or
right after a Teams meeting. ChatType = "Meeting".
"""

from conversations_1on1 import m  # reuse the message helper


MEETING_CONVERSATIONS = [

    # =========================================================================
    # CONV 41: Sprint Planning Meeting
    # Covers: Action Request, Status, Delegation, Routine
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Sprint 15 Planning",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "priyasharma", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "Sharing the Sprint 15 backlog priorities in chat since the screen share isn't working for everyone.\n\n1. AI resource allocation prototype (Priya)\n2. Deployment validation gates (James)\n3. Multi-tenant regression suite (Nina)\n4. CDN monitoring improvements (James)",
              notes="Meeting notes — informational"),

            m("davidpark", "The AI prototype is top priority. @Priya, are you comfortable committing to a demo-ready version by end of sprint?",
              has_task=True, sub_class="RfK", task_type="Confirmation / Permission",
              attribution="Explicit", assignee=["priyasharma"],
              notes="Confirmation request via @mention during meeting",
              mentions=["priyasharma"]),

            m("priyasharma", "Yes, demo-ready for internal review. Not production-ready though — I'll need an additional sprint for hardening and tests.",
              notes="Confirmation — informational"),

            m("alexkumar", "@James, the deployment gates — can you estimate the effort? I want to make sure it doesn't conflict with the CDN work.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["jameswilson"],
              notes="Estimation question via @mention",
              mentions=["jameswilson"]),

            m("jameswilson", "Deployment gates: 3-4 days. CDN monitoring: 2 days. I can fit both in the sprint with a day of buffer.",
              notes="Estimation — informational"),

            m("ninacosta", "Quick flag — the multi-tenant regression suite has a dependency on a test environment that Lisa's team is setting up. If the environment isn't ready by mid-sprint, I'll be blocked.",
              is_important=True,
              notes="Dependency risk — Important because it could block sprint delivery",
              edge_case="dependency_risk_flag"),

            m("alexkumar", "Good callout. @James, can you check with Lisa on the test environment timeline?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["jameswilson"],
              notes="Action request via @mention",
              mentions=["jameswilson"]),

            m("jameswilson", "I'll follow up with her today.",
              notes="Commitment"),

            m("davidpark", "Looks like a solid plan. Alex, please send the finalized sprint scope to the team by EOD with story point allocations.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Action request directed at Alex by name"),

            m("alexkumar", "Will do. I'll update Jira and send the summary.",
              notes="Commitment"),
        ],
    },

    # =========================================================================
    # CONV 42: QBR Meeting (Quarterly Business Review)
    # Covers: Follow-up, Action Request, IsImportant (quarterly numbers)
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Q1 QBR — Sales & Revenue Review",
        "domain": "Sales",
        "members": ["sarahmitchell", "michaelchen", "sofiarodriguez", "racheltorres"],
        "messages": [
            m("michaelchen", "Sharing the pipeline summary in chat for reference. Total Q1 pipeline: $5.3M. Closed-won: $1.8M. Win rate: 34%.",
              notes="Meeting context — informational"),

            m("sarahmitchell", "34% win rate is below our 40% target. @Michael, what's driving the conversion gap?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Explicit", assignee=["michaelchen"],
              notes="Question via @mention + revenue performance → Important",
              mentions=["michaelchen"]),

            m("michaelchen", "Two main factors: 1) Longer sales cycles in enterprise segment (avg 120 days vs 90 days last year), 2) Competitive pressure from Monday.com and Asana in the mid-market.",
              notes="Analysis — informational"),

            m("racheltorres", "The longer cycle is pushing revenue into Q2 but it's not lost revenue. The real concern is win rate in mid-market where we're losing on price.",
              is_important=True,
              notes="Financial analysis — Important context about revenue risk"),

            m("sofiarodriguez", "Dropping a link to the competitive loss analysis in chat. We lost 6 deals to Monday.com specifically on the analytics feature gap. Once v4.2 ships, that changes.",
              notes="Reference material — informational"),

            m("sarahmitchell", "@Sofia, can you put together a competitive win-back plan for those 6 lost deals? If v4.2 addresses their concerns, we should re-engage.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["sofiarodriguez"],
              notes="Action request via @mention + revenue recovery → Important",
              mentions=["sofiarodriguez"]),

            m("sofiarodriguez", "Great idea. I'll draft the win-back approach and target re-engaging within 2 weeks of v4.2 launch.",
              notes="Commitment"),

            m("michaelchen", "Rachel, the pricing concern — should we consider a mid-market pricing tier? We're priced for enterprise but trying to compete in mid-market without a price point advantage.",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              is_important=True, attribution="Implicit", assignee=["racheltorres"],
              notes="Strategic pricing question — Important for revenue strategy"),

            m("sarahmitchell", "That's a bigger discussion. Let's schedule a separate pricing strategy session. @Rachel, can you pull the margin analysis for a potential mid-market tier?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["racheltorres"],
              notes="Action request via @mention",
              mentions=["racheltorres"]),

            m("racheltorres", "I'll model it out. Target: have the analysis ready for a pricing discussion in 2 weeks.",
              notes="Commitment"),

            m("sarahmitchell", "Good QBR everyone. Clear action items. Let's execute.",
              notes="Closing — no task"),
        ],
    },

    # =========================================================================
    # CONV 43: Board Prep Meeting
    # Covers: Review, Delegation, IsImportant (board deadline), Last-minute asks
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Board Deck Final Review — Dry Run",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark", "racheltorres", "amandafoster"],
        "messages": [
            m("sarahmitchell", "Good run-through everyone. A few things I want to tighten up before Thursday.",
              notes="Direction setting — no specific task yet"),

            m("sarahmitchell", "@David, your product slide has too much detail. The board doesn't need to see the Jira breakdown. Focus on: what shipped, what's coming, and the competitive moat. Can you simplify by tomorrow morning?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["davidpark"],
              notes="Action request via @mention + board deadline → Important",
              mentions=["davidpark"]),

            m("davidpark", "Fair feedback. I'll strip it down to 3 key slides: shipped features, AI roadmap, and market differentiation.",
              notes="Commitment"),

            m("sarahmitchell", "@Rachel, the revenue bridge slide is strong but I want to add a 'path to profitability' appendix. Can you prepare that?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["racheltorres"],
              notes="Action request via @mention + board prep → Important",
              mentions=["racheltorres"]),

            m("racheltorres", "Already started. I'll include our runway projection, burn rate trend, and the inflection point where subscription revenue covers operating costs.",
              notes="Commitment + detail"),

            m("amandafoster", "FYI — the board materials need to be distributed 48 hours before the meeting per the bylaws. That means everything finalized by Tuesday 6 PM.",
              is_important=True,
              notes="Compliance deadline — Important context"),

            m("sarahmitchell", "Thanks for flagging that Amanda. So our hard deadline is Tuesday 6 PM, not Thursday. Everyone — adjusted timeline. @David and @Rachel, I need final slides by Tuesday noon so Amanda can compile and distribute.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["davidpark", "racheltorres"],
              notes="Multi-assignee action request via @mentions + hard deadline → Important",
              mentions=["davidpark", "racheltorres"]),

            m("davidpark", "Tuesday noon. Got it.",
              notes="Acknowledgment"),

            m("racheltorres", "Will make it work.",
              notes="Acknowledgment"),

            m("amandafoster", "I'll have the compilation and distribution done by Tuesday 3 PM. I'll also include the standard resolutions and consent agenda.",
              notes="Commitment"),

            m("sarahmitchell", "Great team. Let's make this a strong board meeting. 💪",
              notes="Social / motivational"),
        ],
    },

    # =========================================================================
    # CONV 44: Incident Postmortem
    # Covers: Action items from review, Delegation, IsImportant (prevention)
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Postmortem — API Gateway Incident (Jan 16)",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "jameswilson", "derekjohnson"],
        "messages": [
            m("alexkumar", "Postmortem doc is in the shared drive. Sharing the action items in chat:\n\nRoot cause: Connection pool leak in cursor-based pagination (PR #847)\nImpact: 22 minutes, ~15K users affected\nResolution: Emergency fix PR #852, deployed within 45 minutes of identification",
              notes="Meeting notes — informational"),

            m("davidpark", "Good analysis. The key question for me is: how did a PR with a connection leak pass code review?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Broadcast", assignee=[],
              notes="Root cause question to the group"),

            m("alexkumar", "The connection handling was in a code path that wasn't covered by existing tests. The reviewer (me) didn't catch it because the leak only manifests under high concurrency with client disconnects — a scenario we didn't have a test for.",
              notes="Informational — accountability"),

            m("derekjohnson", "From the support side, we need better tooling to detect connection pool saturation earlier. My team saw the customer complaints 5 minutes before we got the automated alert.",
              is_important=True,
              notes="Process gap identification — Important context"),

            m("davidpark", "Action items — I want these completed by end of Sprint 15:\n\n1. @James — implement pre-deploy connection pool stress test in CI pipeline\n2. @Alex — add mandatory connection lifecycle review to the PR checklist\n3. @Derek — create a customer impact escalation runbook for production incidents",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["jameswilson", "alexkumar", "derekjohnson"],
              notes="Multi-assignee delegation via @mentions with deadline → Important (prevention)",
              mentions=["jameswilson", "alexkumar", "derekjohnson"]),

            m("jameswilson", "The CI stress test — should it run on every PR or only for PRs touching database code?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["davidpark"],
              notes="Scope question to David"),

            m("davidpark", "Start with PRs touching database or connection-related code. We can expand later if needed.",
              notes="Decision response — informational"),

            m("alexkumar", "I'll update the PR checklist template in GitHub. I'll also add a 'has_db_changes' label that triggers the connection lifecycle review requirement.",
              notes="Commitment + additional improvement"),

            m("derekjohnson", "Runbook draft will be ready by end of week. I'll base it on our existing incident response procedures and add the customer communication templates.",
              notes="Commitment"),

            m("davidpark", "Good. Let's track these in Jira and review completion at the Sprint 15 retro. Thanks everyone.",
              notes="Direction — no new task"),
        ],
    },

    # =========================================================================
    # CONV 45: Product Strategy Offsite
    # Covers: Strategic decisions, Action Request, IsImportant
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "H2 Product Strategy Offsite",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark", "michaelchen", "laurakim", "alexkumar"],
        "messages": [
            m("sarahmitchell", "Capturing the key decisions from today's strategy session in chat:\n\n1. AI will be the core differentiator for H2 — not just a feature, but platform-wide intelligence\n2. We're going all-in on enterprise, deprioritizing SMB self-serve\n3. International expansion pushed to 2027 — focus on North America first",
              is_important=True,
              notes="Strategic decisions — Important for company direction. No task."),

            m("michaelchen", "Agree with the enterprise focus. The SMB segment has high churn and low LTV. But we'll need to communicate the deprioritization carefully — want to make sure existing SMB customers don't feel abandoned.",
              notes="Input — informational"),

            m("laurakim", "I'll draft a communications plan for the pivot. We should reframe it as 'deepening our enterprise commitment' rather than 'deprioritizing SMB.'",
              notes="Commitment by sender — self-initiated",
              edge_case="self_initiated_commitment"),

            m("sarahmitchell", "Great instinct Laura. @David, for the AI platform vision — I need a detailed technical roadmap by end of month. Break it into: Q2 MVP, Q3 expansion, Q4 platform integration.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["davidpark"],
              notes="Major delegation via @mention + strategic priority → Important",
              mentions=["davidpark"]),

            m("davidpark", "Alex and I will build it out. We'll include resource requirements and key dependency milestones.",
              notes="Commitment"),

            m("sarahmitchell", "@Michael, I want you to develop an enterprise-only GTM strategy that leverages the AI features as the lead differentiator. Work with Laura's team on the messaging.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["michaelchen"],
              notes="Major delegation via @mention + strategic → Important",
              mentions=["michaelchen"]),

            m("michaelchen", "On it. I'll sync with Laura this week to align the sales narrative with the marketing messaging.",
              notes="Commitment"),

            m("alexkumar", "For the AI roadmap — should we plan for the ML engineer hire being filled by Q2, or should we plan without them as a contingency?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["davidpark"],
              notes="Planning question to David"),

            m("davidpark", "Plan for them being onboarded by mid-Q2. If the hire slips, we'll adjust. But I'd rather plan ambitiously and adjust down.",
              notes="Decision response — informational"),

            m("sarahmitchell", "This was a productive session. Let's execute with urgency. Q2 is when we prove the strategy.",
              notes="Motivational closing — no task"),
        ],
    },

    # =========================================================================
    # CONV 46: Performance Calibration
    # Covers: HR process, Decision, Sensitive, Action Request
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "H1 Performance Calibration — Engineering & Sales",
        "domain": "Human Resources",
        "members": ["sarahmitchell", "daniellewright", "davidpark", "michaelchen", "laurakim"],
        "messages": [
            m("daniellewright", "Sharing the calibration framework in chat. Each department should rank their reports into: Exceeds (top 15%), Meets (70%), Developing (10%), Below (5%). Use the rubric doc I shared Monday.",
              notes="Process guidance — informational"),

            m("davidpark", "Engineering calibration: Exceeds — Alex Kumar, Priya Sharma. Meets — James Wilson, Nina Costa. No Developing or Below.",
              notes="Input — informational"),

            m("michaelchen", "Sales: Exceeds — Sofia Rodriguez (closed 140% of target). Meets — everyone else. No below expectations.",
              notes="Input — informational"),

            m("sarahmitchell", "David, no one in Developing? I find that hard to believe for a team of 5. The calibration is supposed to force-rank, not be a feel-good exercise.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Challenge/question directed at David. Sensitive context.",
              edge_case="calibration_challenge"),

            m("davidpark", "Fair challenge. If I had to differentiate, Nina's QA lead role has been solid but she hasn't stretched beyond core responsibilities. She could be 'Meets with development areas' rather than straight 'Meets.'",
              notes="Revised assessment — informational"),

            m("daniellewright", "That's a reasonable assessment. @David, can you document the development areas in the system? And @Michael, same for your team — any development feedback for the 'Meets' group?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["davidpark", "michaelchen"],
              notes="Multi-assignee action request via @mentions",
              mentions=["davidpark", "michaelchen"]),

            m("davidpark", "Will do by end of week.",
              notes="Commitment"),

            m("michaelchen", "Same. I'll add the development feedback.",
              notes="Commitment"),

            m("laurakim", "Marketing calibration: Exceeds — Chris Evans. Meets — everyone else. Chris has been exceptional on the campaign work and the all-hands video montage was entirely his initiative.",
              notes="Input — informational"),

            m("daniellewright", "Thanks everyone. Please finalize all ratings and feedback in the system by Friday. I'll compile the final calibration report for Sarah's review on Monday.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Broadcast", assignee=[],
              notes="Broadcast action request with deadline"),

            m("sarahmitchell", "Thanks Danielle. Good session. Let's make sure the feedback is constructive and actionable — not just ratings.",
              notes="Guidance — no task"),
        ],
    },

    # =========================================================================
    # CONV 47: Customer Escalation Review Meeting
    # Covers: Follow-up, Action Request, IsImportant (customer risk)
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "GlobalTech & Pinnacle — Customer Escalation Review",
        "domain": "Customer Support",
        "members": ["michaelchen", "mariasantos", "derekjohnson", "alexkumar"],
        "messages": [
            m("mariasantos", "Status update on both escalations:\n\nPinnacle Logistics: Resolved. Export timeout fix deployed last week. Customer confirmed satisfaction. Renewal confirmed for Q2.\n\nGlobalTech Solutions: Recovery plan delivered. 2 of 3 P2 tickets resolved. Third ticket (API documentation) in progress — ETA next Wednesday.",
              notes="Status report — informational"),

            m("michaelchen", "Good progress on Pinnacle. @Alex, what's the status on the GlobalTech API documentation issue?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Explicit", assignee=["alexkumar"],
              notes="Status request via @mention",
              mentions=["alexkumar"]),

            m("alexkumar", "Priya is working on it. The documentation gap was bigger than expected — missing examples for 3 API endpoints and incorrect parameter specs on 2 others. She should have it complete by Monday.",
              notes="Status update — informational"),

            m("derekjohnson", "The GlobalTech contact has been getting daily updates from my team. Their tone has shifted from frustrated to cautiously optimistic. The dedicated account manager assignment made a big difference.",
              notes="Context — informational"),

            m("michaelchen", "@Maria, once the API documentation is complete, I want to schedule an executive call with GlobalTech's CTO. Show them we take their partnership seriously. Can you set that up?",
              has_task=True, sub_class="RfA", task_type="Scheduling Action",
              is_important=True, attribution="Explicit", assignee=["mariasantos"],
              notes="Scheduling action via @mention + customer retention → Important",
              mentions=["mariasantos"]),

            m("mariasantos", "I'll coordinate with their CTO's office. Targeting the week after the API docs are delivered.",
              notes="Commitment"),

            m("michaelchen", "Also — I want a systemic fix to prevent this from happening again. @Derek, can you propose an early warning system for at-risk customers? Look at ticket volume, response times, and sentiment patterns.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["derekjohnson"],
              notes="Action request via @mention — process improvement → Important",
              mentions=["derekjohnson"]),

            m("derekjohnson", "I've been thinking about exactly this. I'll draft a proposal with specific metrics and alerting thresholds. Target: end of next week.",
              notes="Commitment"),

            m("alexkumar", "From the engineering side, I'll also set up a weekly ticket review for top-20 accounts. Any P2+ that's open more than 48 hours gets auto-escalated.",
              notes="Self-initiated commitment",
              edge_case="self_initiated_process_improvement"),

            m("michaelchen", "Excellent. Let's make sure we don't lose another customer to neglect.",
              notes="Closing — no task"),
        ],
    },

    # =========================================================================
    # CONV 48: Budget Committee Meeting
    # Covers: Approval, Decision, IsImportant (fiscal), Cross-functional
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Budget Committee — Q2 Spend Approvals",
        "domain": "Finance",
        "members": ["sarahmitchell", "racheltorres", "kevinzhang"],
        "messages": [
            m("racheltorres", "Dropping the Q2 spend approval requests in chat:\n\n1. Datadog Enterprise license: $350K/year (3-year term) — recommended by David\n2. Enterprise customer event: $75K — Laura's marketing budget\n3. Office AV upgrades: $28K — Lisa's facilities budget\n4. Recruiting agency contingency: $100K — Danielle's HR budget",
              notes="Meeting context — informational"),

            m("sarahmitchell", "Let's go through them. The Datadog license — Rachel, did you review David's business case?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Question to Rachel by name"),

            m("racheltorres", "Yes. The TCO analysis is solid — $1.05M over 3 years vs $1.4M to build. Opportunity cost of diverting engineers is the clincher. I recommend approval.",
              notes="Analysis — informational"),

            m("sarahmitchell", "Approved. @Kevin, please process the Datadog PO. Negotiate the 3-year term for the best discount possible.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["kevinzhang"],
              notes="Action request via @mention — significant spend → Important",
              mentions=["kevinzhang"]),

            m("kevinzhang", "Will do. I'll push for 15-20% multi-year discount.",
              notes="Commitment"),

            m("sarahmitchell", "The customer event — $75K. Rachel, where does this sit in the overall marketing budget?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Budget question to Rachel"),

            m("racheltorres", "Within budget. Marketing has $320K remaining in Q2 discretionary. The event is the largest single item but it's budgeted.",
              notes="Analysis — informational"),

            m("sarahmitchell", "Approved. The AV upgrade and recruiting contingency — any concerns on either?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Broadcast", assignee=[],
              notes="Question to Rachel/Kevin"),

            m("kevinzhang", "Both are straightforward. AV is within Lisa's approval authority. Recruiting contingency is standard for an active hiring cycle.",
              notes="Analysis — informational"),

            m("sarahmitchell", "All four approved. @Kevin, please process all POs this week and send confirmation to the requestors.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["kevinzhang"],
              notes="Action request via @mention — process approvals",
              mentions=["kevinzhang"]),

            m("kevinzhang", "Will have all POs processed by Thursday and requestors notified.",
              notes="Commitment"),

            m("racheltorres", "Good. I'll update the Q2 forecast to reflect these commitments.",
              notes="Self-initiated commitment"),
        ],
    },

    # =========================================================================
    # CONV 49: Weekly Engineering Standup Meeting
    # Covers: Status updates, Quick action items, Mixed tasks/non-tasks
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Engineering Weekly Standup",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "Quick standup. Let's keep it to blockers and help needed. Status updates go in Jira.",
              notes="Process guidance — no specific task"),

            m("priyasharma", "AI prototype is on track. One blocker — I need access to the production data sample for the matching algorithm. @James, can you create a sanitized data export for me?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["jameswilson"],
              notes="Action request via @mention — unblocking dependency",
              mentions=["jameswilson"]),

            m("jameswilson", "I can have that to you by lunch. How much data do you need?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Clarifying question"),

            m("priyasharma", "At least 6 months of project allocation data. Anonymized is fine — I just need the patterns, not the actual names.",
              notes="Specification — informational"),

            m("ninacosta", "No blockers for me. Regression suite is progressing. I found 2 minor bugs in the notification module though — not release-blocking but should be fixed. Filed ENG-2915 and ENG-2916.",
              notes="Status update + bug filing — informational. No task."),

            m("alexkumar", "@Priya, can you take a look at those bugs after your prototype work? They're in your code area.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["priyasharma"],
              notes="Action request via @mention — bug fix assignment",
              mentions=["priyasharma"]),

            m("priyasharma", "Sure, I'll knock them out Thursday.",
              notes="Commitment"),

            m("jameswilson", "FYI — the CDN provider is doing maintenance tonight from 11 PM to 2 AM. Should have zero customer impact but I'll be monitoring.",
              notes="FYI — informational"),

            m("alexkumar", "Thanks for the heads up. OK, that's it. Good meeting — under 10 minutes. 🎉",
              notes="Social closing — no task"),
        ],
    },

    # =========================================================================
    # CONV 50: All-Hands Follow-up
    # Covers: Post-event action items, Feedback, Delegation
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Q1 All-Hands Follow-up",
        "domain": "Executive",
        "members": ["sarahmitchell", "laurakim", "daniellewright", "davidpark"],
        "messages": [
            m("sarahmitchell", "Great all-hands today! The fireside chat format worked much better. Got a lot of positive feedback in the Q&A.",
              notes="Positive feedback — no task"),

            m("laurakim", "Agreed. The video montage was a huge hit — kudos to Chris. I got several messages from people saying it was the best all-hands we've done.",
              notes="Praise/feedback — no task"),

            m("daniellewright", "The employee recognition segment was well-received too. A few people I spoke with mentioned they appreciated being recognized in front of the whole company.",
              notes="Feedback — no task"),

            m("sarahmitchell", "A few follow-up items from the Q&A that we owe the company:\n\n1. Several people asked about the remote work policy refresh — @Danielle, can you share the updated policy by end of next week?\n2. The international expansion question — @David, can you post a brief update in the engineering channel about the timeline shift to 2027?\n3. People want more frequent town halls — @Laura, can we do these quarterly instead of bi-annually?",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["daniellewright", "davidpark", "laurakim"],
              notes="Multi-assignee delegation via @mentions — follow-up items from all-hands",
              mentions=["daniellewright", "davidpark", "laurakim"]),

            m("daniellewright", "I'll have the updated remote work policy shared by Friday. I've been working on it — just needed final approval from Amanda on the compliance pieces.",
              notes="Commitment + context"),

            m("davidpark", "I'll post the update tomorrow. I'll frame it as a 'focus and depth' decision rather than a postponement.",
              notes="Commitment + messaging approach"),

            m("laurakim", "Quarterly town halls — absolutely. I'll build that into the communications calendar. Next one would be end of June.",
              notes="Commitment"),

            m("sarahmitchell", "Thanks team. The all-hands sets the tone for the quarter. This one hit the right notes. 👏",
              notes="Social / praise — no task"),

            m("daniellewright", "One more thing — the anonymous feedback form had some comments about work-life balance concerns on the engineering team. @David, you may want to address that in your next team meeting.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["davidpark"],
              notes="Action request via @mention — sensitive employee feedback",
              mentions=["davidpark"]),

            m("davidpark", "Thanks for flagging. I'll review the comments and discuss with Alex before bringing it to the team.",
              notes="Commitment"),
        ],
    },
]

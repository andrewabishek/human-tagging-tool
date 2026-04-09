"""
Supplemental Conversations — Purpose: reach 1000+ messages, boost edge cases to ~15%,
and fill gaps in task-type coverage (Follow-up, Scheduling, Availability/RSVP,
Review/Approval). Also adds more Unassigned attribution examples.

These are intentionally scenario-heavy, edge-case-rich conversations designed to
stress-test the HasTask/IsImportant classifier.
"""

def m(sender, content, has_task=False, is_important=False,
      sub_class="Neither", task_type="", attribution="",
      assignee=None, edge_case=None, notes="", mentions=None, reactions=None):
    msg = {
        "from": sender,
        "content": content,
        "annotations": {
            "has_task": has_task,
            "task_sub_class": sub_class,
            "task_type": task_type,
            "is_important": is_important,
            "attribution": attribution,
            "assignee": assignee or [],
            "edge_case": edge_case,
            "notes": notes,
        }
    }
    if mentions:
        msg["mentions"] = mentions
    if reactions:
        msg["reactions"] = reactions
    return msg


SUPPLEMENTAL_CONVERSATIONS = [

    # =========================================================================
    # S1: 1:1 — Follow-up Heavy (Eng Manager ↔ Engineer)
    # Covers: Follow-up, Status Request, conditional asks, stale-task pattern
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Migration Follow-ups",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma"],
        "messages": [
            m("alexkumar", "Hey Priya, just circling back on the database migration PR. You mentioned it'd be ready by last Thursday.",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Follow-up on prior unresolved ask"),

            m("priyasharma", "Yeah, sorry — I hit a blocker with the schema validation. The new constraints are rejecting about 12% of legacy records.",
              notes="Informational — status update, no ask"),

            m("alexkumar", "That's a bigger issue than expected. Can you quantify the data loss risk if we skip the validation step temporarily?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["priyasharma"],
              notes="Question + data loss risk → Important"),

            m("priyasharma", "I'll run the analysis this afternoon and get you numbers by EOD.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["priyasharma"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment → HasTask=TRUE, assignee=sender"),

            m("alexkumar", "Perfect. Also — any update on the caching layer refactor? I think that was due last sprint.",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Second follow-up in same conversation"),

            m("priyasharma", "Pushed it to this sprint. Dependencies on James's infra work weren't resolved.",
              notes="Status update — informational"),

            m("alexkumar", "OK. When James is done, loop me in so I can reprioritize your backlog if needed.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["priyasharma"],
              edge_case="conditional_task",
              notes="Conditional ask — 'when James is done' → task exists but is conditional"),

            m("priyasharma", "Will do.",
              notes="Acknowledgment"),

            m("alexkumar", "One more thing — the performance test results from two weeks ago. Did those ever get documented?",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Third follow-up — pattern of checking on stale items"),

            m("priyasharma", "I wrote up the summary in Confluence but forgot to share the link. Let me send it now.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["priyasharma"],
              edge_case="self_assigned_commitment",
              notes="Self-directed commitment to act"),

            m("alexkumar", "Thanks. And whenever you get a chance — not urgent — could you also add the latency benchmarks to the dashboard? Feel free to skip it if Q2 planning takes priority.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["priyasharma"],
              edge_case="soft_conditional_ask",
              notes="Conditional/soft ask — 'whenever you get a chance', 'feel free to skip'. Still HasTask=TRUE per spec but low urgency."),

            m("priyasharma", "Sure, I'll try to squeeze it in this week.",
              notes="Acknowledgment with soft commitment"),
        ],
    },

    # =========================================================================
    # S2: 1:1 — Sales ↔ Legal (Review/Approval heavy)
    # Covers: Review/Approval, Confirmation, Permission, deadline pressure
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Contoso Enterprise Agreement Review",
        "domain": "Legal",
        "members": ["sofiarodriguez", "amandafoster"],
        "messages": [
            m("sofiarodriguez", "Amanda, I need you to review the Contoso enterprise agreement. Deal is $2.3M ARR and they want to close by end of month.",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              is_important=True, attribution="Implicit", assignee=["amandafoster"],
              notes="Review request + revenue impact + deadline → Important"),

            m("amandafoster", "I saw the draft yesterday. There are some non-standard indemnification clauses I need to redline. How flexible is the customer on those?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Question back to sales about customer flexibility"),

            m("sofiarodriguez", "They pushed back last time we tried to modify indemnification. Can we accept their language with a cap?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Implicit", assignee=["amandafoster"],
              notes="Permission request — can we accept with modification?"),

            m("amandafoster", "I can accept a cap at 2x annual contract value. Anything beyond that needs Rachel's sign-off since it exceeds our standard risk threshold.",
              is_important=True,
              notes="Informational — stating policy, no new ask. Important because it flags risk threshold."),

            m("sofiarodriguez", "OK, I'll propose the 2x cap to Contoso. Can you meanwhile redline sections 4.2 and 7.1 and send me a clean version by Wednesday?",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              is_important=True, attribution="Implicit", assignee=["amandafoster"],
              notes="Action request with deadline tied to deal close"),

            m("amandafoster", "Wednesday is tight but doable. I'll prioritize it.",
              notes="Acknowledgment + commitment"),

            m("sofiarodriguez", "Thank you! Also, quick question — do we need a separate DPA for this deal or does our standard one cover it?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["amandafoster"],
              notes="Knowledge question about data processing agreement"),

            m("amandafoster", "Standard DPA covers it as long as they're not processing EU personal data. Confirm with the customer whether they have EU operations.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Action request back to Sofia — confirm with customer"),

            m("sofiarodriguez", "Will check and confirm. Thanks Amanda!",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # S3: 1:1 — Scheduling & Availability Heavy (Marketing)
    # Covers: Scheduling, Availability/RSVP, polite asks
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Campaign Launch Coordination",
        "domain": "Marketing",
        "members": ["laurakim", "chrisevans"],
        "messages": [
            m("laurakim", "Chris, are you free tomorrow at 2 PM for a run-through of the campaign assets?",
              has_task=True, sub_class="RfK", task_type="Availability/RSVP",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Availability check"),

            m("chrisevans", "Tomorrow's packed — I have back-to-backs from 1 to 4. How about Thursday morning?",
              has_task=True, sub_class="RfK", task_type="Scheduling",
              attribution="Implicit", assignee=["laurakim"],
              notes="Counter-proposal for scheduling — asks Laura to decide"),

            m("laurakim", "Thursday 10 AM works. Can you book a room and send the invite?",
              has_task=True, sub_class="RfA", task_type="Scheduling",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Scheduling action — book room + send invite"),

            m("chrisevans", "Done — sent for 10-11 AM in the Rainier room.",
              notes="Completed action report — no new ask"),

            m("laurakim", "Perfect. Also — can you check if the blog post draft is ready for my review? I want to approve it before the launch.",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Status request about blog post"),

            m("chrisevans", "Almost there. The writer is doing a final pass. I'll have it in your inbox by end of day.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              edge_case="self_assigned_commitment",
              notes="Self-directed commitment"),

            m("laurakim", "Great. And one more — are you attending the product marketing sync on Friday?",
              has_task=True, sub_class="RfK", task_type="Availability/RSVP",
              attribution="Implicit", assignee=["chrisevans"],
              notes="RSVP / availability check"),

            m("chrisevans", "Yes, I'll be there.",
              notes="Confirmation — no task"),

            m("laurakim", "Cool. Can you prep a 5-minute overview of the campaign metrics to share at that meeting?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Action request — prepare content for meeting"),

            m("chrisevans", "Sure thing. Want me to include social engagement numbers or just web traffic?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["laurakim"],
              notes="Clarifying question back"),

            m("laurakim", "Both please. And add the email open rates too.",
              notes="Answer to question — informational"),

            m("chrisevans", "Got it. I'll have the deck ready by Thursday EOD.",
              notes="Acknowledgment + commitment"),
        ],
    },

    # =========================================================================
    # S4: Group — Edge Case Gauntlet (Cross-functional)
    # Deliberately packed with edge cases: sarcasm, optional asks, FYI+task,
    # rhetorical questions, passive-aggressive asks, ambiguous "we" statements
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q2 Planning Edge Cases",
        "domain": "Cross-functional",
        "members": ["alexkumar", "priyasharma", "jameswilson", "ninacosta", "laurakim"],
        "messages": [
            m("alexkumar", "Team, quick update — the Q2 OKRs have been finalized. Take a look when you can.",
              edge_case="fyi_with_soft_ask",
              notes="FYI + 'take a look when you can' is optional/soft. Per spec, optional asks → FALSE"),

            m("priyasharma", "Nice. Are these the same ones we discussed last week or did anything change?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["alexkumar"],
              edge_case="question_to_group_leader",
              notes="Question directed at thread starter implicitly"),

            m("alexkumar", "Mostly the same. The only change is the reliability target moved from 99.9% to 99.95%.",
              notes="Informational response"),

            m("jameswilson", "99.95%? That's going to be fun 🙃",
              edge_case="sarcasm_not_task",
              notes="Sarcasm — not a task, not a question. Social commentary."),

            m("ninacosta", "Seriously though, has anyone actually modeled what 99.95% requires in terms of infra redundancy?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Unassigned", assignee=[],
              edge_case="broadcast_question_no_assignee",
              notes="Question to group with no specific target — Unassigned"),

            m("alexkumar", "Good question. @James, can you put together a quick feasibility assessment? Nothing fancy, just a back-of-envelope calc.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["jameswilson"],
              mentions=["jameswilson"],
              notes="Explicit @mention delegation"),

            m("jameswilson", "Sure. I'll have something by Friday.",
              notes="Acknowledgment + commitment"),

            m("laurakim", "From the marketing side — we probably should align our messaging around the reliability story. Just saying.",
              edge_case="informational_with_implicit_suggestion",
              notes="'Just saying' — observation/suggestion but no assignee, no ask. Not HasTask."),

            m("priyasharma", "We should also update the status page SLA language. Who owns that?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Unassigned", assignee=[],
              edge_case="who_owns_this",
              notes="Task exists (update SLA) but no assignee → Unassigned. Question about ownership."),

            m("alexkumar", "I think it's technically DevOps. @James?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Explicit", assignee=["jameswilson"],
              mentions=["jameswilson"],
              notes="Confirmation request via @mention"),

            m("jameswilson", "Yeah, I can update it. But I'll need legal to sign off on the new language.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["jameswilson"],
              edge_case="self_assigned_with_dependency",
              notes="Self-assigned commitment with external dependency (legal sign-off)"),

            m("alexkumar", "Great. Let's make sure this gets done before the public announcement. It would be embarrassing to promise 99.95% uptime and have the status page say 99.9%.",
              is_important=True,
              edge_case="urgency_without_explicit_task",
              notes="Urgency expressed but no new task — James already committed. IsImportant due to public announcement risk."),

            m("ninacosta", "Agreed. I'll add a QA checkpoint for the status page update before it goes live.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["ninacosta"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment by QA lead"),

            m("laurakim", "This is great teamwork. If you need any copy review on the status page language, feel free to ping me.",
              edge_case="optional_offer",
              notes="Optional offer — 'feel free to' → HasTask=FALSE per spec"),
        ],
    },

    # =========================================================================
    # S5: Group — Customer Escalation (Support + Sales + Engineering)
    # Covers: IsImportant=TRUE heavy, escalation, customer churn risk,
    #         multi-assignee, Follow-up
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Zenith Corp Escalation — System Outage Impact",
        "domain": "Customer Support",
        "members": ["derekjohnson", "mariasantos", "sofiarodriguez", "alexkumar", "davidpark"],
        "messages": [
            m("derekjohnson", "URGENT: Zenith Corp is reporting complete system unavailability for the past 45 minutes. They're our third-largest customer and their VP of Engineering just called our support line directly.",
              is_important=True,
              notes="Urgent status report — no task yet but critical. IsImportant due to outage + strategic customer."),

            m("mariasantos", "This is Zenith's second outage this quarter. They've been vocal about evaluating alternatives. We need to treat this as a potential churn event.",
              is_important=True,
              edge_case="context_setting_important",
              notes="Context/analysis — no task. IsImportant due to churn risk."),

            m("derekjohnson", "@Alex, can your team investigate the root cause immediately? We need a preliminary RCA within the hour.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["alexkumar"],
              mentions=["alexkumar"],
              notes="Explicit action request + tight deadline + customer impact → Important"),

            m("alexkumar", "On it. Pulling Priya and James into the war room now.",
              notes="Acknowledgment + delegation (but delegation is internal)"),

            m("sofiarodriguez", "I'll reach out to their VP to buy us time. @Maria, do you have the latest support ticket history for Zenith? I want to go in with full context.",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Explicit", assignee=["mariasantos"],
              mentions=["mariasantos"],
              notes="Request for information + self-commitment (reaching out to VP)"),

            m("mariasantos", "Sending it now. They've had 7 P1 tickets in the last 90 days. That's way above our threshold.",
              is_important=True,
              notes="Informational — providing data. Important due to severity."),

            m("davidpark", "I just spoke with the infra team. It's a database connection pool exhaustion issue — same pattern as the March incident. I thought we fixed this.",
              is_important=True,
              notes="Root cause identification — informational. Important due to recurring pattern."),

            m("alexkumar", "We did patch it, but the fix only covered the primary cluster. The secondary cluster wasn't updated. @James, can you confirm and apply the hotfix to secondary NOW?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["jameswilson"],
              mentions=["jameswilson"],
              edge_case="urgent_explicit_directive",
              notes="Urgent directive with explicit @mention + NOW emphasis"),

            m("derekjohnson", "Following up — it's been 30 minutes since the initial report. Do we have an ETA for resolution?",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              is_important=True, attribution="Unassigned", assignee=[],
              notes="Follow-up to group — no specific target"),

            m("alexkumar", "James is applying the hotfix now. ETA 15 minutes for connection pool recovery, then another 10 for full service restoration.",
              notes="Status update — informational"),

            m("sofiarodriguez", "I got Zenith's VP on the phone. He's willing to hold off on escalation if we can: (1) provide RCA by tomorrow, (2) commit to a permanent fix timeline, and (3) offer a service credit.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Unassigned", assignee=[],
              edge_case="multi_part_task_unassigned",
              notes="Multi-part task from customer, broadcast to group — needs multiple owners"),

            m("davidpark", "I'll own the RCA. @Alex, you and the team get the permanent fix scoped. @Maria, work with finance on the service credit — probably 1 month pro-rata.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["alexkumar", "mariasantos"],
              mentions=["alexkumar", "mariasantos"],
              notes="Multi-assignee delegation — CTO takes one part, delegates others"),

            m("mariasantos", "On it. I'll loop in Kevin from finance for the credit calculation.",
              notes="Acknowledgment + commitment"),

            m("derekjohnson", "Service is back up as of 2:47 PM. Zenith confirmed. But let's not forget — this is the SECOND time. We need the permanent fix before we lose this account.",
              is_important=True,
              edge_case="completed_action_with_urgency",
              notes="Resolution confirmation + urgency for follow-up. No new task (already delegated). IsImportant."),

            m("davidpark", "Agreed. I want the permanent fix timeline in our next leadership sync. This is now a top-3 priority.",
              is_important=True,
              notes="Priority elevation — informational/directive already captured by prior delegation"),
        ],
    },

    # =========================================================================
    # S6: 1:1 — HR ↔ CEO — Sensitive Edge Cases
    # Covers: Permission requests, borderline FYI+task, policy questions
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Employee Relations & Policy Updates",
        "domain": "Human Resources",
        "members": ["daniellewright", "sarahmitchell"],
        "messages": [
            m("daniellewright", "Sarah, I need to flag something sensitive. We received a formal complaint from an employee on the engineering team about their manager's communication style.",
              is_important=True,
              notes="FYI — no ask yet. Important due to HR/legal sensitivity."),

            m("sarahmitchell", "Thanks for bringing this to me. Is this something HR can handle through normal channels or do we need legal involved?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              is_important=True, attribution="Implicit", assignee=["daniellewright"],
              notes="Decision request about process — Important due to sensitivity"),

            m("daniellewright", "HR can handle the initial investigation. If it escalates to a formal grievance, we'll need Amanda. For now, I'd like your permission to proceed with the informal resolution process.",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              is_important=True, attribution="Implicit", assignee=["sarahmitchell"],
              notes="Permission request from HR to CEO"),

            m("sarahmitchell", "You have my go-ahead. Keep me updated on progress but use your judgment on the approach.",
              notes="Permission granted — no new task"),

            m("daniellewright", "Will do. Separately — the new PTO policy goes into effect Monday. I've sent the company-wide announcement but wanted to give you a heads-up in case anyone on the leadership team has questions.",
              edge_case="fyi_heads_up",
              notes="FYI/informational — no task, just a heads-up"),

            m("sarahmitchell", "Got it. Did you include the grandfathering clause for people who already have trips booked?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["daniellewright"],
              notes="Question about policy detail"),

            m("daniellewright", "Yes, it's in section 3 of the policy doc. Anyone with pre-approved PTO keeps their existing dates.",
              notes="Informational response"),

            m("sarahmitchell", "Perfect. One more thing — can you pull together the Q1 attrition numbers? I need them for the board deck.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["daniellewright"],
              notes="Action request + board dependency → Important"),

            m("daniellewright", "I'll have them to you by Thursday. Do you want voluntary and involuntary broken out separately?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Clarifying question"),

            m("sarahmitchell", "Yes, both. And if you can include a comparison to industry benchmarks, that would be helpful.",
              notes="Answer — informational"),

            m("daniellewright", "Will do. Thanks Sarah.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # S7: Group — Meeting Scheduling Chaos (Edge cases)
    # Covers: Scheduling, RSVP, back-and-forth, first-person-plural
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q2 Kickoff Planning",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark", "racheltorres", "michaelchen", "laurakim", "daniellewright"],
        "messages": [
            m("sarahmitchell", "We need to get the Q2 kickoff on the calendar ASAP. @David @Rachel @Michael @Laura @Danielle — what does next Tuesday look like for everyone?",
              has_task=True, sub_class="RfK", task_type="Availability/RSVP",
              is_important=True, attribution="Explicit", assignee=["davidpark", "racheltorres", "michaelchen", "laurakim", "daniellewright"],
              mentions=["davidpark", "racheltorres", "michaelchen", "laurakim", "daniellewright"],
              notes="Multi-assignee availability request with urgency"),

            m("davidpark", "Tuesday works for me. Morning is better — I have a deployment window in the afternoon.",
              notes="RSVP response — informational"),

            m("racheltorres", "I can do Tuesday before noon. I have the audit committee call at 1 PM.",
              notes="RSVP response with constraint — informational"),

            m("michaelchen", "Tuesday is out for me — I'm in New York for client meetings all day. What about Wednesday?",
              has_task=True, sub_class="RfK", task_type="Scheduling",
              attribution="Unassigned", assignee=[],
              edge_case="counter_proposal_scheduling",
              notes="Counter-proposal — scheduling back to group"),

            m("laurakim", "Either day works for me.",
              notes="RSVP — informational"),

            m("daniellewright", "Tuesday or Wednesday both fine.",
              notes="RSVP — informational"),

            m("sarahmitchell", "Let's do Wednesday 10 AM then. Michael, can you join remotely if needed?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Implicit", assignee=["michaelchen"],
              notes="Confirmation request directed at Michael by name (no @mention)"),

            m("michaelchen", "Yes, I'll dial in from the hotel.",
              notes="Confirmation — informational"),

            m("sarahmitchell", "@Danielle, can you book the all-hands room and send the invite?",
              has_task=True, sub_class="RfA", task_type="Scheduling",
              attribution="Explicit", assignee=["daniellewright"],
              mentions=["daniellewright"],
              notes="Scheduling action delegation via @mention"),

            m("daniellewright", "On it. Should I include the full leadership team or just this group?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Clarifying question to the requester"),

            m("sarahmitchell", "Full leadership team plus the department heads.",
              notes="Answer — informational"),

            m("racheltorres", "Can someone prepare the financial overview slides? I can do the numbers but need templates from marketing.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Unassigned", assignee=[],
              edge_case="partial_self_assignment_partial_unassigned",
              notes="Rachel volunteers for numbers but asks 'someone' for templates → Unassigned for the template part"),

            m("laurakim", "I'll send you the template deck today.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["laurakim"],
              edge_case="self_assigned_via_reply",
              notes="Self-assigned by replying with commitment"),

            m("sarahmitchell", "Thanks everyone. Let's make this a good kickoff. 🚀",
              notes="Social / motivational — no task"),
        ],
    },

    # =========================================================================
    # S8: Meeting Chat — Security Incident Review
    # Covers: IsImportant=TRUE, security breach, action items, compliance
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Security Incident Postmortem — March 28 Breach Attempt",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "jameswilson", "amandafoster", "priyasharma"],
        "messages": [
            m("davidpark", "OK everyone, let's walk through the March 28 incident. James, can you give us the timeline?",
              has_task=True, sub_class="RfK", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["jameswilson"],
              notes="Action request in meeting context — present timeline"),

            m("jameswilson", "At 3:12 AM Pacific, our IDS flagged anomalous traffic from an IP range associated with known threat actors. The traffic was targeting our staging environment's API gateway.",
              is_important=True,
              notes="Informational — incident details. Important due to security."),

            m("jameswilson", "By 3:24 AM, the automated WAF rules blocked the majority of requests. However, approximately 2,400 requests made it through before the rules kicked in.",
              is_important=True,
              notes="Informational — continued timeline"),

            m("amandafoster", "Were any customer data endpoints exposed during that 12-minute window?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["jameswilson"],
              notes="Critical question about data exposure — Important"),

            m("jameswilson", "No. The staging environment uses synthetic data. No customer PII was at risk.",
              notes="Informational — answering question"),

            m("amandafoster", "That's a relief. But we still need to document this for our SOC 2 compliance records. @James, can you prepare the incident report in the required format by end of week?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["jameswilson"],
              mentions=["jameswilson"],
              notes="Compliance documentation request — Important due to SOC 2"),

            m("davidpark", "Agreed. And we need to address the 12-minute gap. @Priya, can you review the WAF rule propagation latency? I want that gap under 60 seconds.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["priyasharma"],
              mentions=["priyasharma"],
              notes="Security hardening task — Important"),

            m("priyasharma", "I'll look into it. The latency is mostly due to the rule sync between our edge nodes. We might need to move to a push-based model.",
              notes="Acknowledgment + preliminary analysis"),

            m("alexkumar", "What about the staging environment access controls? Should we be putting staging behind the same WAF as production?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              is_important=True, attribution="Unassigned", assignee=[],
              edge_case="decision_request_to_group",
              notes="Decision request to group — no specific target"),

            m("davidpark", "Yes. Let's not have different security postures. @Alex, can you draft a proposal to unify the security controls across all environments?",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["alexkumar"],
              mentions=["alexkumar"],
              notes="Delegation with @mention"),

            m("amandafoster", "One more thing — given this is the second security event this quarter, I recommend we brief the board's audit committee. Sarah should be in the loop.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Unassigned", assignee=[],
              edge_case="recommendation_as_task",
              notes="Recommendation framed as 'I recommend we...' → HasTask because it requires action, but assignee unclear"),

            m("davidpark", "I'll brief Sarah today and schedule the audit committee update. Good call, Amanda.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["davidpark"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned — CTO takes ownership of board briefing"),

            m("jameswilson", "Action items from my side: (1) incident report for SOC 2 by Friday, (2) WAF rule propagation analysis with @Priya. Anything I'm missing?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Unassigned", assignee=[],
              edge_case="summary_with_confirmation_request",
              notes="Self-summary of action items + confirmation request to group"),

            m("davidpark", "That covers it. Thanks everyone. Let's close the loop on all items by next Monday.",
              notes="Closing — no new task"),
        ],
    },

    # =========================================================================
    # S9: 1:1 — Finance follow-ups
    # Covers: Follow-up, deadline, budget
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Q1 Close & Audit Prep Follow-ups",
        "domain": "Finance",
        "members": ["racheltorres", "kevinzhang"],
        "messages": [
            m("racheltorres", "Kevin, where are we on the Q1 close reconciliation? The external auditors start next Monday.",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              is_important=True, attribution="Implicit", assignee=["kevinzhang"],
              notes="Follow-up + audit deadline → Important"),

            m("kevinzhang", "Revenue recognition is done. Still working on the deferred revenue adjustments — should be complete by Thursday.",
              notes="Status update — informational"),

            m("racheltorres", "Thursday is cutting it close. Can you finish by Wednesday instead? I need a day to review before the auditors arrive.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["kevinzhang"],
              notes="Accelerated deadline request — Important"),

            m("kevinzhang", "I'll try. The main blocker is the inter-company elimination entries — I'm waiting on the UK office's numbers.",
              is_important=True,
              notes="Blocker — informational. Important because it threatens audit readiness."),

            m("racheltorres", "Follow up with them today. Tell them it's for the external audit — that usually gets fast responses.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["kevinzhang"],
              notes="Direct instruction to follow up with dependency"),

            m("kevinzhang", "Will do. Also — I noticed a $47K variance in the SaaS subscription accruals. It looks like a timing difference but I want to flag it before the auditors find it.",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["racheltorres"],
              edge_case="flag_as_implicit_question",
              notes="'I want to flag it' — implicitly asking Rachel for guidance on how to handle it"),

            m("racheltorres", "Good catch. Prepare a variance analysis memo. If it's truly a timing difference, we document it; if it's a real error, we need to correct before close.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["kevinzhang"],
              notes="Action request — prepare memo"),

            m("kevinzhang", "I'll have the memo ready alongside the reconciliation.",
              notes="Acknowledgment + commitment"),

            m("racheltorres", "Thanks Kevin. Let's make sure this audit goes smoothly. Last year's was rough.",
              notes="Social / motivational — no task"),
        ],
    },

    # =========================================================================
    # S10: Group — Product Launch Go/No-Go (Multiple decision requests)
    # Covers: Decision Request heavy, Review/Approval, multi-domain
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Meridian Analytics Pro — Launch Go/No-Go",
        "domain": "Cross-functional",
        "members": ["sarahmitchell", "davidpark", "racheltorres", "michaelchen", "laurakim", "amandafoster"],
        "messages": [
            m("sarahmitchell", "Team — we need to make the go/no-go call on the Analytics Pro launch by end of today. Let's do a quick round-robin. @David — engineering readiness?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Explicit", assignee=["davidpark"],
              mentions=["davidpark"],
              notes="Status request for go/no-go — Important"),

            m("davidpark", "Engineering is green. All P0 bugs fixed, performance benchmarks met, and we passed the security review. One P2 cosmetic issue remains but it's not a blocker.",
              notes="Status update — informational"),

            m("sarahmitchell", "@Rachel — financial projections still on track?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Explicit", assignee=["racheltorres"],
              mentions=["racheltorres"],
              notes="Status request to CFO"),

            m("racheltorres", "Yes. Break-even in 8 months with current pipeline. Michael's team has $1.2M in pre-launch commitments.",
              notes="Status update — informational"),

            m("sarahmitchell", "@Michael — sales team ready?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Explicit", assignee=["michaelchen"],
              mentions=["michaelchen"],
              notes="Status request to VP Sales"),

            m("michaelchen", "Ready. All AEs have been trained. One concern: Vertex Industries wants exclusive early access and is threatening to pull their renewal if we don't offer it.",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              is_important=True, attribution="Unassigned", assignee=[],
              edge_case="embedded_decision_in_status",
              notes="Status report that contains an embedded decision request — should we offer exclusive access?"),

            m("amandafoster", "I'd advise against exclusive access. It sets a precedent and the contract language would be complex. We can offer 30-day head start instead.",
              notes="Opinion/recommendation — informational"),

            m("sarahmitchell", "Go with Amanda's recommendation — 30-day head start, no exclusivity. @Michael, communicate that to Vertex today.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["michaelchen"],
              mentions=["michaelchen"],
              notes="Action request — communicate decision to customer"),

            m("sarahmitchell", "@Laura — marketing launch plan ready?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Explicit", assignee=["laurakim"],
              mentions=["laurakim"],
              notes="Status request to marketing"),

            m("laurakim", "All assets are staged. Press release goes out at 6 AM Pacific on launch day. Social campaign is scheduled. One ask: can we get a customer quote for the press release? @Michael, any of your accounts willing?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["michaelchen"],
              mentions=["michaelchen"],
              notes="Question to Michael — need customer quote"),

            m("michaelchen", "I'll reach out to Pinnacle Systems — they've been our most vocal champion. Should have an answer by tomorrow morning.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["michaelchen"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment"),

            m("sarahmitchell", "@Amanda — any legal blockers we should know about?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["amandafoster"],
              mentions=["amandafoster"],
              notes="Question to legal"),

            m("amandafoster", "No blockers. ToS and privacy policy updates are live. One reminder: the GDPR data processing addendum needs to be available on the product page before EU customers can sign up.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Unassigned", assignee=[],
              edge_case="reminder_as_task_no_assignee",
              notes="Reminder that someone needs to ensure DPA is on product page — but no specific assignee"),

            m("sarahmitchell", "OK — I'm calling it. We are GO for launch on Monday. The only open item is the GDPR addendum on the product page. @David, can your team handle that?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["davidpark"],
              mentions=["davidpark"],
              notes="Final action item — Important (launch gating)"),

            m("davidpark", "Will get it done by Friday.",
              notes="Acknowledgment + commitment"),

            m("sarahmitchell", "Thanks everyone. Great work getting us here. 🎉",
              notes="Social / celebratory — no task"),
        ],
    },

    # =========================================================================
    # S11: 1:1 — Edge Case Stress Test
    # Rhetorical questions, sarcasm, passive-aggressive, emoji-onry responses
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Dev Tooling Frustrations",
        "domain": "Engineering",
        "members": ["priyasharma", "jameswilson"],
        "messages": [
            m("priyasharma", "Is the CI pipeline ever going to be stable? I've had 3 failed builds today because of infra timeouts.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["jameswilson"],
              edge_case="rhetorical_but_real_question",
              notes="Sounds rhetorical but is a real question — Priya wants to know if there's a fix coming. HasTask=TRUE."),

            m("jameswilson", "I know, it's been rough. The timeout issue is related to the shared runner pool being overloaded. I've been trying to get budget approval for dedicated runners since January.",
              notes="Informational — context/explanation"),

            m("priyasharma", "January?! Who do we need to escalate to?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["jameswilson"],
              edge_case="escalation_question",
              notes="Question about escalation path — Important due to blocking dev productivity"),

            m("jameswilson", "Alex said he'd take it to David. But honestly, I don't think it's been prioritized. Maybe if it comes from your side too it'll get more attention.",
              edge_case="passive_request_for_help",
              notes="Implicit suggestion for Priya to also escalate — but not a direct ask. HasTask=FALSE because it's a suggestion, not a request."),

            m("priyasharma", "I'll mention it in the next eng sync. In the meantime, can you at least increase the timeout threshold so my builds don't fail?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["jameswilson"],
              notes="Concrete action request + self-commitment to escalate"),

            m("jameswilson", "Yeah, I can bump it from 300s to 600s. That should help for now. Done.",
              notes="Completed action — no new task"),

            m("priyasharma", "Thanks 🙏",
              edge_case="emoji_only_acknowledgment",
              notes="Acknowledgment with emoji — no task"),

            m("jameswilson", "👍",
              edge_case="emoji_only_response",
              notes="Emoji-only response — no task, social"),

            m("priyasharma", "While we're at it — the staging environment has been super slow too. Same issue?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["jameswilson"],
              notes="New question on related topic"),

            m("jameswilson", "Different issue actually. Staging is overprovisioned on apps but underprovisioned on database. We need to rebalance. I'll create a ticket.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["jameswilson"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned — will create ticket"),
        ],
    },

    # =========================================================================
    # S12: Group — Ambiguous "We" Statements & First-Person Plural
    # Edge case: first-person-plural with no assignee
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Product Roadmap Alignment",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "priyasharma", "laurakim", "michaelchen"],
        "messages": [
            m("davidpark", "We need to rethink our approach to the mobile SDK. It's been deprioritized for too long.",
              edge_case="first_person_plural_no_assignee",
              notes="'We need to' — first-person plural with no specific assignee → HasTask=FALSE per spec classification table"),

            m("alexkumar", "Agreed. But who's going to own it? We don't have mobile engineers.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Unassigned", assignee=[],
              edge_case="who_owns_this",
              notes="Ownership question → Unassigned"),

            m("michaelchen", "From a sales perspective, we're losing deals because of the mobile gap. Three prospects in Q1 went with competitors specifically because of this.",
              is_important=True,
              notes="Sales impact data — informational. Important due to revenue impact."),

            m("laurakim", "We should put together a competitive analysis of mobile offerings. It would strengthen the business case.",
              edge_case="should_statement_no_assignee",
              notes="'We should' — suggestion without specific owner → HasTask=FALSE per first-person-plural rule"),

            m("davidpark", "Here's what I propose: Let's outsource the initial SDK build. @Alex, can you vet 3 agencies and bring recommendations to next week's sync?",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["alexkumar"],
              mentions=["alexkumar"],
              notes="Explicit delegation with @mention — action request"),

            m("alexkumar", "I'll reach out to our usual vendors. @Priya, you worked with a mobile SDK shop at your last company right? Can you share the contact?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["priyasharma"],
              mentions=["priyasharma"],
              notes="Explicit question via @mention"),

            m("priyasharma", "Yeah — AppForge. They did solid work. I'll send you their info.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["priyasharma"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment to share contact"),

            m("michaelchen", "Let's also loop in Sofia — she has direct feedback from the prospects who churned over mobile.",
              edge_case="lets_also_suggestion",
              notes="'Let's also' — suggestion with no specific owner → HasTask=FALSE"),

            m("davidpark", "Good idea. @Alex, include Sofia in the vendor eval process.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["alexkumar"],
              mentions=["alexkumar"],
              notes="Explicit action request via @mention"),

            m("alexkumar", "Got it. I'll set up a shared channel for the eval.",
              notes="Acknowledgment + commitment"),
        ],
    },

    # =========================================================================
    # S13: Meeting Chat — All-Hands Q&A (Many FALSE, few TRUE)
    # Covers: Bot-like messages, social, phatic, occasional real questions
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Meridian Technologies Q1 All-Hands",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark", "racheltorres", "michaelchen", "laurakim",
                     "daniellewright", "alexkumar", "priyasharma", "sofiarodriguez", "kevinzhang"],
        "messages": [
            m("sarahmitchell", "Welcome everyone to our Q1 all-hands! We have a lot to cover today. Let's get started.",
              notes="Opening — social/phatic"),

            m("sarahmitchell", "First, I want to recognize the engineering team for shipping the Analytics Pro feature ahead of schedule. Amazing work.",
              notes="Recognition — social"),

            m("davidpark", "Team really crushed it. 🎉",
              notes="Social / celebration"),

            m("priyasharma", "Thanks! It was a team effort. 💪",
              notes="Social / acknowledgment"),

            m("sarahmitchell", "Q1 revenue came in at $14.2M against a target of $13.8M. Rachel, do you want to walk us through the highlights?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Action request in meeting — present"),

            m("racheltorres", "Sure. The overperformance was driven by three large enterprise deals that closed early. Net retention rate is at 118%, up from 112% last quarter.",
              notes="Informational — presenting"),

            m("kevinzhang", "Is the 118% net retention rate inclusive of the Zenith Corp downgrade?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Question to Rachel (she's presenting)"),

            m("racheltorres", "Yes, inclusive. Without Zenith it would be 121%.",
              notes="Informational — answering"),

            m("sofiarodriguez", "On the sales side, we closed 47 new logos in Q1. Pipeline for Q2 is looking strong.",
              notes="Informational — department update"),

            m("michaelchen", "The Vertex Industries deal alone is worth $800K ARR. Great work Sofia! 🙌",
              notes="Social / recognition"),

            m("daniellewright", "Quick HR update: we've hired 12 people this quarter. Current headcount is 187. The engagement survey results will be shared next week.",
              notes="Informational — HR update"),

            m("priyasharma", "When will the new eng hires start? We're really feeling the capacity crunch.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["daniellewright"],
              notes="Question directed at HR (she just spoke about hiring)"),

            m("daniellewright", "Four start next Monday, the rest throughout April.",
              notes="Answer — informational"),

            m("alexkumar", "Can we get them access to the dev environment before Day 1? Last batch had to wait 3 days for accounts.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["daniellewright"],
              edge_case="request_in_allhands",
              notes="Action request in all-hands context — directed at HR by context"),

            m("daniellewright", "Good point. I'll coordinate with IT to have everything set up by Friday.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["daniellewright"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment"),

            m("sarahmitchell", "Great discussion everyone. We're in a strong position heading into Q2. Let's keep the momentum going!",
              notes="Closing — motivational, no task"),

            m("laurakim", "Thanks everyone! 👏",
              notes="Social / closing"),

            m("ninacosta", "Great all-hands! 🎉",
              notes="Social / phatic"),
        ],
    },

    # =========================================================================
    # S14: 1:1 — CC vs Targeted Edge Cases (VP Sales ↔ AE)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Deal Pipeline & Forecast Review",
        "domain": "Sales",
        "members": ["michaelchen", "sofiarodriguez"],
        "messages": [
            m("michaelchen", "Sofia, I need an updated forecast for Q2 by tomorrow morning. The board package goes to Sarah at noon.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Action request + board deadline → Important"),

            m("sofiarodriguez", "I'll have it ready by 9 AM. Quick question — should I include the Acme deal at full value or weighted probability?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["michaelchen"],
              notes="Clarifying question"),

            m("michaelchen", "Weighted. We can't count on full value until legal signs off on their custom terms.",
              notes="Answer — informational"),

            m("sofiarodriguez", "Got it. Also following up — did you hear back from Rachel about the additional AE headcount? You mentioned escalating it two weeks ago.",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              attribution="Implicit", assignee=["michaelchen"],
              notes="Follow-up on prior conversation"),

            m("michaelchen", "Still pending. Rachel wants to see Q1 close rates before committing Q2 headcount. Fair point honestly.",
              notes="Status update — informational"),

            m("sofiarodriguez", "The Pinnacle Systems RFP response is due Friday. I've drafted it but need your review on the pricing section. Can you take a look today?",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              is_important=True, attribution="Implicit", assignee=["michaelchen"],
              notes="Review request + RFP deadline → Important"),

            m("michaelchen", "Send it over. I'll review after my 2 PM call.",
              notes="Acknowledgment + commitment"),

            m("sofiarodriguez", "Sent. One more thing — Vertex wants to renegotiate their payment terms from net-30 to net-60. Thoughts?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              is_important=True, attribution="Implicit", assignee=["michaelchen"],
              notes="Decision request — financial impact on large deal"),

            m("michaelchen", "That's a $800K deal — we don't want to lose it over payment terms. Accept net-60 but ask for auto-renewal in exchange. Run it by Rachel for the cash flow impact.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Decision + delegation to Sofia to run by Rachel"),

            m("sofiarodriguez", "Makes sense. I'll talk to Rachel this afternoon.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # S15: Group — Mixed social & task (Friday wrap-up cont'd)
    # Covers: lots of FALSE messages with sprinkled TRUE, bot messages
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "General - Friday Vibes & Housekeeping",
        "domain": "Cross-functional",
        "members": ["alexkumar", "priyasharma", "jameswilson", "ninacosta", "chrisevans", "mariasantos"],
        "messages": [
            m("alexkumar", "Happy Friday team! 🍕 Who's up for lunch at the new Thai place?",
              edge_case="social_question",
              notes="Social question — not a task, social coordination"),

            m("priyasharma", "I'm in! 🙋‍♀️",
              notes="Social — RSVP to lunch"),

            m("jameswilson", "Count me in. I'll drive.",
              notes="Social — acceptance"),

            m("ninacosta", "Can't today — I have a dentist appointment at noon. Have fun!",
              notes="Social — declining"),

            m("chrisevans", "I'm remote today but enjoy!",
              notes="Social / informational"),

            m("mariasantos", "Before everyone disappears for the weekend — quick reminder that the customer NPS survey results come out Monday. @Alex, can you make sure the eng dashboard is pulling the right data source?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["alexkumar"],
              mentions=["alexkumar"],
              notes="Action request via @mention embedded in casual conversation"),

            m("alexkumar", "Sure, I'll double-check it before I leave today.",
              notes="Acknowledgment + commitment"),

            m("priyasharma", "Speaking of dashboards — has anyone noticed the deploy frequency metric is wrong? It's showing 3x our actual rate.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Unassigned", assignee=[],
              edge_case="question_noticed_something",
              notes="Question/observation to group — no specific target → Unassigned"),

            m("jameswilson", "Yeah, it's double-counting rollbacks. I noticed it last week but kept forgetting to fix it. I'll do it now before I forget again.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["jameswilson"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment triggered by group question"),

            m("ninacosta", "While you're fixing metrics, can you also check if the test pass rate metric is accurate? It seemed off in yesterday's report.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["jameswilson"],
              notes="Piggyback request — directed at James since he's fixing metrics"),

            m("jameswilson", "Sure, adding it to the list.",
              notes="Acknowledgment"),

            m("chrisevans", "Anyone watching the game tonight? ⚽",
              edge_case="social_offtopic",
              notes="Social — completely off-topic, no task"),

            m("priyasharma", "Which game?",
              edge_case="social_followup_question",
              notes="Social question — not a work task"),

            m("alexkumar", "OK team, enjoy the weekend! And remember — we have the sprint planning Monday at 10 AM. Come prepared with your estimates.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Broadcast", assignee=[],
              edge_case="broadcast_reminder",
              notes="Broadcast reminder with action ('come prepared') — HasTask=TRUE, Broadcast"),

            m("priyasharma", "Have a great weekend everyone! 🎉",
              notes="Social / phatic"),
        ],
    },

    # =========================================================================
    # S16: Meeting Chat — Sales QBR
    # Covers: Review, pipeline, competitive intel, follow-ups
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Q1 Sales Quarterly Business Review",
        "domain": "Sales",
        "members": ["michaelchen", "sofiarodriguez", "racheltorres", "sarahmitchell"],
        "messages": [
            m("michaelchen", "Let's walk through the Q1 numbers. Sofia, can you start with the new business pipeline?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Meeting context — ask to present"),

            m("sofiarodriguez", "Q1 new business: $4.1M closed against a $3.8M target. 108% attainment. Win rate improved from 28% to 34%.",
              notes="Informational — presenting data"),

            m("sarahmitchell", "That's excellent. What drove the win rate improvement?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Question to presenter"),

            m("sofiarodriguez", "Two things: the new competitive battle cards Chris put together, and the faster POC turnaround from engineering.",
              notes="Informational — answering"),

            m("racheltorres", "What's the average deal size trending? I'm seeing smaller deals in the pipeline.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Analytical question"),

            m("sofiarodriguez", "Average deal size did drop from $85K to $72K, but volume is up significantly. Net effect is positive.",
              notes="Informational — answering"),

            m("michaelchen", "The big concern is Vertex. They represent 18% of our Q2 pipeline. If that deal slips, we miss target. @Sofia, what's the confidence level?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Explicit", assignee=["sofiarodriguez"],
              mentions=["sofiarodriguez"],
              notes="High-stakes question about key deal — Important"),

            m("sofiarodriguez", "I'd say 75% confidence. The main risk is their budget approval process — it's a public company and they have a new CFO who's scrutinizing all new spend.",
              is_important=True,
              notes="Risk assessment — informational. Important due to pipeline concentration."),

            m("sarahmitchell", "What's our mitigation plan if Vertex slips?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Unassigned", assignee=[],
              notes="Risk mitigation question to group"),

            m("michaelchen", "We have $600K in upside pipeline that could pull in. @Sofia, can you work those deals harder this month and give me a realistic pull-in forecast by next Friday?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["sofiarodriguez"],
              mentions=["sofiarodriguez"],
              notes="Action request with deadline — Important"),

            m("sofiarodriguez", "I'll accelerate outreach on the top 5 upside deals and have the forecast to you by Thursday.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["sofiarodriguez"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment — accelerated timeline"),

            m("racheltorres", "I'd also recommend we review the discount approval process. Some deals are taking 2 weeks to get pricing approved. That's killing deal velocity.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Unassigned", assignee=[],
              edge_case="recommendation_as_task_no_assignee",
              notes="Recommendation framed as task but no specific assignee"),

            m("sarahmitchell", "Good point. @Michael, @Rachel — work together to streamline the discount approval process. I want a proposal by end of month.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["michaelchen", "racheltorres"],
              mentions=["michaelchen", "racheltorres"],
              notes="Multi-assignee delegation with deadline"),

            m("michaelchen", "Will do.",
              notes="Acknowledgment"),

            m("racheltorres", "I'll schedule time with Michael next week.",
              notes="Acknowledgment + commitment"),
        ],
    },

    # =========================================================================
    # S17: 1:1 — Customer Success Follow-ups
    # Covers: Follow-up, customer churn risk, status requests
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "At-Risk Account Reviews",
        "domain": "Customer Success",
        "members": ["mariasantos", "derekjohnson"],
        "messages": [
            m("mariasantos", "Derek, following up on the GreenTech Support case. Did they accept our remediation plan?",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              attribution="Implicit", assignee=["derekjohnson"],
              notes="Follow-up on prior conversation"),

            m("derekjohnson", "Partially. They're OK with the process changes but still unhappy about the response time SLA. They want 1-hour response instead of 4-hour for P1 issues.",
              notes="Status update — informational"),

            m("mariasantos", "Can we realistically offer 1-hour response for their tier?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["derekjohnson"],
              notes="Question about operational feasibility"),

            m("derekjohnson", "Not with current staffing. We'd need an additional after-hours support engineer. That's a budget conversation with Rachel.",
              is_important=True,
              notes="Blocker — budget dependency. Important due to churn risk."),

            m("mariasantos", "OK, I'll raise it with Rachel. Meanwhile — any update on the NovaCorp onboarding? They were supposed to go live last week.",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              attribution="Implicit", assignee=["derekjohnson"],
              notes="Second follow-up on different account"),

            m("derekjohnson", "NovaCorp is delayed. Their IT team hasn't completed the SSO integration. I've been chasing them but they keep rescheduling.",
              notes="Status update — informational"),

            m("mariasantos", "That's been going on for 3 weeks now. Can you escalate to their project sponsor? If they don't go live soon, we risk losing the implementation window.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["derekjohnson"],
              notes="Action request + risk of losing implementation → Important"),

            m("derekjohnson", "Good idea. I'll send a formal email to their VP of IT today.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["derekjohnson"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment"),

            m("mariasantos", "Thanks. And circle back with me once you hear from them so I can update the leadership report.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["derekjohnson"],
              notes="Action request — report back"),

            m("derekjohnson", "Will do.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # S18: Group — Cross-functional edge cases with reactions
    # Covers: Reactions as signals, ambiguous messages
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Office Move Planning",
        "domain": "Operations",
        "members": ["daniellewright", "alexkumar", "laurakim", "kevinzhang", "amandafoster"],
        "messages": [
            m("daniellewright", "Hi team — we've confirmed the office move to the new building on March 15. Department heads need to submit their space requirements by end of this week.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Broadcast task with deadline — Important due to office move logistics"),

            m("alexkumar", "How many sq ft per person are we budgeting? Engineering needs more space for hardware labs.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["daniellewright"],
              notes="Question to the announcer"),

            m("daniellewright", "Standard is 120 sqft per person. Labs are separate — submit that as a special request with justification.",
              notes="Informational — answering"),

            m("kevinzhang", "Do we have the budget numbers for the move? Rachel asked me to track it.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["daniellewright"],
              notes="Question about budget"),

            m("daniellewright", "Total budget is $450K. I'll send you the breakdown.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["daniellewright"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned — will send breakdown"),

            m("amandafoster", "Make sure the new lease agreement is finalized before we start any physical move prep. I'm still reviewing clause 12.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Unassigned", assignee=[],
              edge_case="legal_gate_no_assignee",
              notes="Legal gating requirement — Important. 'Make sure' is directed at group."),

            m("laurakim", "Do we need to communicate the move to customers? Some of them visit our office.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Unassigned", assignee=[],
              edge_case="question_implies_task",
              notes="Question that implies a potential task but is genuinely asking IF it's needed"),

            m("daniellewright", "Good point. Yes, we should. @Laura, can you draft customer communication? And @Amanda, when will clause 12 be resolved?",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["laurakim", "amandafoster"],
              mentions=["laurakim", "amandafoster"],
              notes="Multi-assignee — delegation to Laura + follow-up to Amanda (2 asks in 1 message)"),

            m("laurakim", "Sure, I'll draft something by Wednesday.",
              notes="Acknowledgment + commitment"),

            m("amandafoster", "Hoping by end of week. The landlord's legal team has been slow to respond.",
              notes="Status update — informational"),

            m("alexkumar", "Thanks for organizing this, Danielle. 👏",
              notes="Social / appreciation — no task",
              reactions=[("like", "kevinzhang"), ("heart", "laurakim")]),
        ],
    },

    # =========================================================================
    # S19: 1:1 — Quick transactional (very short, common pattern)
    # Covers: Simple ask-and-done, common in real Teams usage
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Quick Ask",
        "domain": "Engineering",
        "members": ["alexkumar", "jameswilson"],
        "messages": [
            m("alexkumar", "James — what's the SSH key for the staging jumpbox? I need to debug something.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["jameswilson"],
              notes="Simple knowledge request"),

            m("jameswilson", "Check 1Password — it's in the 'Staging Infra' vault. Key name is 'jumpbox-staging-2026'.",
              notes="Answer — informational"),

            m("alexkumar", "Found it. Thanks!",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # S20: 1:1 — Quick transactional #2
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Meeting Room",
        "domain": "Operations",
        "members": ["laurakim", "daniellewright"],
        "messages": [
            m("laurakim", "Danielle, is the Cascade room available tomorrow from 2-3 PM?",
              has_task=True, sub_class="RfK", task_type="Availability/RSVP",
              attribution="Implicit", assignee=["daniellewright"],
              notes="Availability check for resource"),

            m("daniellewright", "Let me check... it's booked at 2, but free from 2:30 onward. Want me to book it for 2:30-3:30?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Implicit", assignee=["laurakim"],
              notes="Counter-offer with confirmation request"),

            m("laurakim", "2:30 works. Yes please!",
              notes="Confirmation — informational"),

            m("daniellewright", "Done! Invite sent.",
              notes="Completed action — no task"),

            m("laurakim", "Thanks! 🙏",
              notes="Social / acknowledgment"),
        ],
    },

    # =========================================================================
    # S21: Group — System outage real-time (all IsImportant, fast messages)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "PRODUCTION DOWN — API Gateway Failure",
        "domain": "Engineering",
        "members": ["jameswilson", "alexkumar", "priyasharma", "davidpark", "ninacosta"],
        "messages": [
            m("jameswilson", "🚨 PROD IS DOWN. API gateway returning 502s across all endpoints. Started 2 minutes ago.",
              is_important=True,
              notes="Incident alert — no task yet. IsImportant due to production outage."),

            m("alexkumar", "I see it. PagerDuty alert just fired. @Priya, are you available to help triage?",
              has_task=True, sub_class="RfK", task_type="Availability/RSVP",
              is_important=True, attribution="Explicit", assignee=["priyasharma"],
              mentions=["priyasharma"],
              notes="Availability request during incident"),

            m("priyasharma", "I'm here. Pulling up the dashboards now.",
              notes="Availability confirmation — no task"),

            m("jameswilson", "Root cause: the latest deploy introduced a memory leak. Pod memory usage hit 100% and OOMKilled. All replicas affected.",
              is_important=True,
              notes="Root cause — informational. Important."),

            m("davidpark", "Roll back immediately. We'll investigate after service is restored.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Unassigned", assignee=[],
              edge_case="directive_no_specific_assignee",
              notes="CTO directive but doesn't specify who rolls back — Unassigned"),

            m("jameswilson", "Rolling back now. ETA 3 minutes.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["jameswilson"],
              edge_case="self_assigned_via_action",
              notes="Self-assigned by acting on it"),

            m("alexkumar", "@Nina, can you start the incident timeline doc? We'll need it for the postmortem.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["ninacosta"],
              mentions=["ninacosta"],
              notes="Explicit delegation during incident"),

            m("ninacosta", "On it. I'll track everything in the Confluence incident page.",
              notes="Acknowledgment + commitment"),

            m("jameswilson", "Rollback complete. Services recovering. Health checks passing on 4 of 6 pods.",
              is_important=True,
              notes="Status update — informational. Important (ongoing incident)."),

            m("jameswilson", "All 6 pods healthy. API gateway responding normally. Incident over.",
              is_important=True,
              notes="Resolution — informational. Still Important context."),

            m("davidpark", "Good work on the fast recovery. @Alex, I want a postmortem doc by tomorrow with: root cause, timeline, and preventive measures. Include a section on why our canary deployment didn't catch this.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["alexkumar"],
              mentions=["alexkumar"],
              notes="Postmortem delegation — Important"),

            m("alexkumar", "Will have it ready by noon tomorrow. @Priya, @James — I'll need your input on the technical timeline.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["priyasharma", "jameswilson"],
              mentions=["priyasharma", "jameswilson"],
              notes="Multi-assignee input request"),

            m("priyasharma", "I'll write up what I found in the logs.",
              notes="Acknowledgment + commitment"),

            m("jameswilson", "Same. I'll document the deploy and rollback timeline.",
              notes="Acknowledgment + commitment"),
        ],
    },

    # =========================================================================
    # S22: 1:1 — Content Marketing Review/Approval
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Blog Post Review & Approval",
        "domain": "Marketing",
        "members": ["laurakim", "chrisevans"],
        "messages": [
            m("laurakim", "Chris, I just read the Analytics Pro launch blog post draft. Nice work but I have several rounds of feedback.",
              notes="Informational — praise + heads-up"),

            m("laurakim", "First — can you rewrite the opening paragraph? It buries the lead. I want the customer ROI stat front and center.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Specific editing request"),

            m("chrisevans", "Makes sense. The 43% efficiency gain stat?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["laurakim"],
              notes="Clarifying question"),

            m("laurakim", "Yes, that one. Second — the technical section is too jargon-heavy for our audience. Simplify it. Third — add a CTA at the end directing to the product page.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Multiple action items in one message — still one task conceptually"),

            m("chrisevans", "I'll rework all three and have a revised draft to you by tomorrow morning.",
              notes="Acknowledgment + commitment"),

            m("laurakim", "Great. I need to give final approval before it goes live on Tuesday, so tomorrow is the latest I can review.",
              is_important=True,
              notes="Deadline context — informational. Important due to launch-gating."),

            m("chrisevans", "Understood. I'll make sure it's in your inbox by 9 AM.",
              notes="Acknowledgment + commitment"),

            m("laurakim", "Also — can you check if the featured image meets our new brand guidelines? Sarah's been particular about visual consistency lately.",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Review request — brand compliance check"),

            m("chrisevans", "Will verify against the style guide.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # S23: Group — Multi-@mention with CC distinction
    # Covers: CC vs targeted, @mention edge cases
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Vendor Selection for Analytics Platform",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "racheltorres", "kevinzhang", "amandafoster"],
        "messages": [
            m("davidpark", "@Alex — I need you to evaluate DataStream and CloudMetrics as analytics vendors. @Rachel and @Kevin — FYI, this will impact the Q3 budget. @Amanda — we'll need you to review vendor contracts once we shortlist.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["alexkumar"],
              mentions=["alexkumar", "racheltorres", "kevinzhang", "amandafoster"],
              edge_case="multi_mention_cc_vs_targeted",
              notes="Only Alex has the primary task. Rachel/Kevin are CC for awareness. Amanda has a future conditional task."),

            m("alexkumar", "I'll start with technical evaluations this week. @David, any specific criteria beyond the ones in the RFP?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["davidpark"],
              mentions=["davidpark"],
              notes="Clarifying question via @mention"),

            m("davidpark", "Focus on: (1) real-time streaming support, (2) cost per query at our scale, (3) SOC 2 compliance. Those are the non-negotiables.",
              notes="Informational — criteria"),

            m("kevinzhang", "For budget context — we have $200K allocated for analytics tooling in Q3. The current Tableau license is $85K of that.",
              notes="Informational — budget context (Kevin is CC'd, providing input)"),

            m("racheltorres", "If the new vendor costs more than the Tableau allocation, we'll need a budget amendment. Just flagging now so there are no surprises.",
              edge_case="flag_without_task",
              notes="Risk flag — informational. No task, just awareness."),

            m("alexkumar", "Noted. I'll include a cost comparison in my evaluation. Aiming to have recommendations ready in two weeks.",
              notes="Acknowledgment + self-commitment"),

            m("amandafoster", "When you're ready for contract review, give me at least 5 business days. These vendor agreements tend to be complex.",
              edge_case="conditional_future_task",
              notes="Conditional future task — 'when you're ready'. Not a current task, just setting expectations."),

            m("davidpark", "Great. Let's reconvene in two weeks. @Alex, set up the review meeting.",
              has_task=True, sub_class="RfA", task_type="Scheduling",
              attribution="Explicit", assignee=["alexkumar"],
              mentions=["alexkumar"],
              notes="Scheduling action delegation"),
        ],
    },

    # =========================================================================
    # S24: Meeting Chat — Sprint Retrospective (Engineering)
    # Covers: Mixed feedback, action items from retro
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Sprint 47 Retrospective",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "OK team, let's do our retro. What went well this sprint?",
              notes="Facilitation — no task"),

            m("priyasharma", "The Analytics Pro feature shipped on time. Good collaboration between frontend and backend.",
              notes="Positive feedback — informational"),

            m("jameswilson", "The new CI pipeline improvements reduced build times by 40%. Big win.",
              notes="Positive feedback — informational"),

            m("ninacosta", "Test coverage went from 72% to 81%. The team actually wrote tests this sprint! 😄",
              notes="Positive feedback — informational"),

            m("alexkumar", "Great. Now — what didn't go well?",
              notes="Facilitation — no task"),

            m("priyasharma", "The last-minute scope change from product. We got a new requirement 2 days before the sprint ended. That's not sustainable.",
              is_important=True,
              edge_case="complaint_not_task",
              notes="Complaint/feedback — not a task. Important because it's a process issue affecting productivity."),

            m("jameswilson", "The staging environment was flaky all sprint. Cost us probably 2 days of lost productivity across the team.",
              is_important=True,
              notes="Issue flagging — informational. Important due to productivity impact."),

            m("alexkumar", "Both valid. Let's turn these into action items. For the scope change issue — @Priya, can you document the impact and I'll take it to the next product-eng sync?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["priyasharma"],
              mentions=["priyasharma"],
              notes="Action item from retro — explicit delegation"),

            m("priyasharma", "Sure. I'll write up a brief with the timeline impact.",
              notes="Acknowledgment"),

            m("alexkumar", "@James — for the staging stability, can you create a proposal for dedicated staging infrastructure? Include cost estimates so I can make the budget case.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["jameswilson"],
              mentions=["jameswilson"],
              notes="Delegation with @mention — retro action item"),

            m("jameswilson", "I actually started drafting this last week. I'll finalize it by end of sprint.",
              notes="Acknowledgment + already in progress"),

            m("ninacosta", "Can we also add a rule that no new requirements can be added in the last 3 days of a sprint?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Unassigned", assignee=[],
              edge_case="process_change_request",
              notes="Process change request — decision needed from leadership"),

            m("alexkumar", "I love that idea. Let me propose it as a team agreement. I'll bring it to the next standup for a vote.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["alexkumar"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned — will propose process change"),

            m("priyasharma", "Best retro we've had in a while. 👍",
              notes="Social — positive"),
        ],
    },

    # =========================================================================
    # S25: 1:1 — Legal quick questions (short transactional)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Quick Legal Questions",
        "domain": "Legal",
        "members": ["davidpark", "amandafoster"],
        "messages": [
            m("davidpark", "Amanda, quick question — can we use customer logos on our website without explicit written permission?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["amandafoster"],
              notes="Legal knowledge question"),

            m("amandafoster", "No. We need a written logo usage agreement or a clause in the master agreement permitting it. Some of our contracts have it, some don't.",
              notes="Informational — legal answer"),

            m("davidpark", "Can you check which of our top 10 customers have the clause and which need a separate agreement?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["amandafoster"],
              notes="Action request — contract review"),

            m("amandafoster", "I'll pull the contracts and let you know by end of week.",
              notes="Acknowledgment + commitment"),

            m("davidpark", "Thanks. One more — do we need to update our privacy policy before launching in the EU?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["amandafoster"],
              notes="Legal question — Important (GDPR/regulatory)"),

            m("amandafoster", "Yes, absolutely. GDPR requires specific disclosures. I'll send you the list of required changes.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["amandafoster"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned — will send required changes list. Important."),

            m("davidpark", "Perfect. Appreciate the quick turnaround on these.",
              notes="Social / appreciation"),
        ],
    },

    # =========================================================================
    # S26: Group — Emoji reactions as signals, minimal text
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Design Review Feedback",
        "domain": "Marketing",
        "members": ["laurakim", "chrisevans", "alexkumar", "sofiarodriguez"],
        "messages": [
            m("laurakim", "Just shared the new landing page mockups in the design channel. Everyone please review and leave feedback by tomorrow.",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              attribution="Broadcast", assignee=[],
              notes="Broadcast review request with deadline"),

            m("chrisevans", "Looks great! The hero section is much better than the last version.",
              notes="Positive feedback — not a task",
              reactions=[("like", "laurakim")]),

            m("alexkumar", "The performance metrics section is confusing. Can we restructure it to lead with the business impact numbers?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["laurakim"],
              edge_case="feedback_as_request",
              notes="Feedback framed as a question/suggestion but is really a request for change"),

            m("sofiarodriguez", "From a sales perspective, we need the pricing to be more prominent. Prospects always ask about pricing first.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["laurakim"],
              notes="Feedback with implicit request — 'we need' directed at design owner"),

            m("laurakim", "Good feedback all around. @Chris, can you mock up the restructured metrics section? And I'll work on making pricing more visible.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["chrisevans"],
              mentions=["chrisevans"],
              notes="Explicit delegation + self-assignment"),

            m("chrisevans", "On it. I'll have a revised mockup by tomorrow afternoon.",
              notes="Acknowledgment + commitment"),

            m("alexkumar", "👍",
              edge_case="emoji_only_response",
              notes="Emoji-only response — no task"),

            m("sofiarodriguez", "🙌",
              edge_case="emoji_only_response",
              notes="Emoji-only response — no task"),
        ],
    },

    # =========================================================================
    # S27: Meeting Chat — Budget Review (Finance heavy)
    # =========================================================================
    {
        "chat_type": "Meeting",
        "topic": "Q2 Budget Review Meeting",
        "domain": "Finance",
        "members": ["racheltorres", "kevinzhang", "sarahmitchell", "davidpark", "michaelchen"],
        "messages": [
            m("racheltorres", "Let's go through the Q2 budget proposals. Each department submitted their asks — we need to decide allocations today.",
              is_important=True,
              notes="Meeting opening — framing but no specific task. Important due to budget decisions."),

            m("racheltorres", "@David, engineering is requesting $1.2M. That's 30% above Q1. Walk us through the justification.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["davidpark"],
              mentions=["davidpark"],
              notes="Presentation request in budget review — Important"),

            m("davidpark", "The increase breaks down as: $400K for 4 new hires, $300K for the analytics vendor evaluation Alex is running, $200K for staging infrastructure improvements, and $300K for the security hardening initiatives we discussed after the March incident.",
              notes="Informational — justification"),

            m("sarahmitchell", "The security spend is non-negotiable given the incidents. What about the analytics vendor — can that wait?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              is_important=True, attribution="Implicit", assignee=["davidpark"],
              notes="Decision question from CEO — Important"),

            m("davidpark", "We could push it to Q3, but we'd miss the window for annual pricing negotiations. We'd likely pay 20% more.",
              notes="Informational — trade-off analysis"),

            m("racheltorres", "@Michael, sales is asking for $800K. That includes 2 new AEs at $350K total and $450K for the new CRM implementation.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["michaelchen"],
              mentions=["michaelchen"],
              notes="Ask VP Sales to justify"),

            m("michaelchen", "The AEs are critical — we're leaving pipeline on the table. The CRM is overdue — our current system is a spreadsheet nightmare.",
              notes="Informational — justification"),

            m("kevinzhang", "I ran the numbers. If we approve everything, we're $340K over the total Q2 operating budget. We'd need to either cut or pull from reserves.",
              is_important=True,
              notes="Budget constraint — informational. Important."),

            m("sarahmitchell", "OK, here's my call: approve engineering in full including analytics. Approve the AEs for sales but defer the CRM to Q3 — that saves $450K and gives us buffer. @Rachel, does that math work?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              is_important=True, attribution="Explicit", assignee=["racheltorres"],
              mentions=["racheltorres"],
              notes="CEO makes decision, asks CFO to confirm feasibility"),

            m("racheltorres", "Yes, that keeps us $110K under budget with some room for contingency. I'll update the allocations.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["racheltorres"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned — will update allocations"),

            m("michaelchen", "Can we at least start the CRM vendor evaluation in Q2 so we're ready to implement in Q3?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Permission request — can we at least evaluate?"),

            m("sarahmitchell", "That's fine — just don't sign anything until Q3 budget is confirmed.",
              notes="Permission granted with caveat — informational"),

            m("racheltorres", "@Kevin, please update the budget tracker with today's decisions and distribute to all department heads by end of day.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["kevinzhang"],
              mentions=["kevinzhang"],
              notes="Action request with deadline — Important (budget communication)"),

            m("kevinzhang", "Will do.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # S28: 1:1 — Boundary testing: bot-like / auto-generated messages
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "System Notifications Discussion",
        "domain": "Engineering",
        "members": ["jameswilson", "alexkumar"],
        "messages": [
            m("jameswilson", "Alex, I'm getting spammed with these auto-generated security scan notifications. Do you know how to filter them?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Question about system notifications"),

            m("alexkumar", "Yeah, there's a filter rule in the Outlook settings. I'll send you the steps.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["alexkumar"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment"),

            m("jameswilson", "Thanks. By the way — the automated deploy reports are showing duplicate entries. Can you check if the webhook is firing twice?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Action request — debug webhook"),

            m("alexkumar", "I noticed that too. I think it's the retry logic. Let me investigate and fix it.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["alexkumar"],
              edge_case="self_assigned_commitment",
              notes="Self-assigned commitment to investigate and fix"),

            m("jameswilson", "Perfect. Let me know when it's fixed so I can verify on my end.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Request to be notified when done"),

            m("alexkumar", "Will do 👍",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # S29: Group — Multi-threaded conversation with interleaved topics
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Engineering Standup Thread",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "Morning standup! Quick updates from everyone please.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Broadcast", assignee=[],
              notes="Broadcast request for updates"),

            m("priyasharma", "Yesterday: finished the data pipeline refactor. Today: starting on the API rate limiter. Blocker: none.",
              notes="Status update — informational"),

            m("jameswilson", "Yesterday: deployed monitoring dashboards. Today: working on the CDN migration. Blocker: waiting on DNS propagation, should be done by noon.",
              notes="Status update — informational"),

            m("ninacosta", "Yesterday: wrote integration tests for the new auth flow. Today: regression testing for the release. Blocker: I need the test environment credentials refreshed — they expired.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Unassigned", assignee=[],
              edge_case="blocker_in_standup",
              notes="Blocker with implied task — someone needs to refresh credentials. Unassigned."),

            m("jameswilson", "I can refresh those. Give me 10 minutes.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["jameswilson"],
              edge_case="self_assigned_via_reply",
              notes="Self-assigned by volunteering in reply"),

            m("ninacosta", "Thanks James! 🙏",
              notes="Acknowledgment / social"),

            m("alexkumar", "Looks like we're on track for the release. @Priya — on the rate limiter, make sure you coordinate with James on the CDN config since they'll interact.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["priyasharma"],
              mentions=["priyasharma"],
              notes="Action request — coordination directive"),

            m("priyasharma", "Already synced with him yesterday. We're good.",
              notes="Informational — already handling"),

            m("alexkumar", "Any other blockers or concerns before I close standup?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Broadcast", assignee=[],
              edge_case="broadcast_question_closing",
              notes="Broadcast question — closing standup"),

            m("priyasharma", "All good here.",
              notes="Informational — no blockers"),

            m("jameswilson", "Same.",
              notes="Informational"),

            m("ninacosta", "Nothing from me.",
              notes="Informational"),

            m("alexkumar", "Great. Let's crush it today! 💪",
              notes="Social / motivational"),
        ],
    },

    # =========================================================================
    # S30: 1:1 — Ambiguous borderline messages
    # Purpose: stress test HasTask boundary with genuinely ambiguous cases
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Casual Check-in with CTO",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark"],
        "messages": [
            m("sarahmitchell", "David, I've been thinking about our AI strategy. We might be falling behind.",
              edge_case="thinking_out_loud",
              notes="Thinking out loud — no task, no question. Informational/observation."),

            m("davidpark", "What makes you say that? I thought we were in a good spot with the analytics rollout.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Question back to Sarah — asking for reasoning"),

            m("sarahmitchell", "I saw the Gartner report yesterday. Our competitors are investing 3x what we are in ML infrastructure. I just wanted to flag it.",
              edge_case="flag_without_ask",
              notes="'I just wanted to flag it' — FYI/observation, not a task"),

            m("davidpark", "That's worth looking into. I could put together a competitive landscape analysis focused on AI/ML investments if you think it's a priority.",
              edge_case="offer_not_commitment",
              notes="Conditional offer — 'I could... if you think' — not a commitment yet, seeking confirmation"),

            m("sarahmitchell", "That would be great actually. But don't deprioritize the current release for it. When things calm down after the launch, let's revisit.",
              edge_case="deferred_soft_ask",
              notes="Deferred ask — 'when things calm down, let's revisit.' Not an immediate task. HasTask=FALSE because it's explicitly deferred."),

            m("davidpark", "Makes sense. I'll keep it on the backlog.",
              notes="Acknowledgment"),

            m("sarahmitchell", "How's the team morale? I know the last few sprints have been intense.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Genuine question — asking for information"),

            m("davidpark", "Mixed. The senior folks are energized by the Analytics Pro launch. But the junior engineers are feeling stretched. We might want to think about a team event after the launch.",
              edge_case="suggestion_not_task",
              notes="'We might want to think about' — suggestion, not a task"),

            m("sarahmitchell", "Good to know. Let's keep an eye on it.",
              edge_case="lets_keep_eye_no_task",
              notes="'Let's keep an eye on it' — no specific task or assignee. Not HasTask."),

            m("davidpark", "Will do. Thanks for checking in, Sarah.",
              notes="Social / closing"),
        ],
    },

    # =========================================================================
    # S31: 1:1 — Spec Quick-Reference Table Examples
    # Purpose: ensure exact patterns from the spec's Combined Quick-Reference
    #          Table are represented in the dataset
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Data Export & Call Scheduling",
        "domain": "Engineering",
        "members": ["priyasharma", "jameswilson"],
        "messages": [
            m("priyasharma", "Do you know how to download this data from the analytics dashboard? I can't find the export button.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["jameswilson"],
              notes="Spec example: 'Do you know how to download this data?' → HasTask=TRUE"),

            m("jameswilson", "Yeah, it's under Settings > Export > CSV. They moved it in the last release.",
              notes="Answer — informational"),

            m("priyasharma", "Thanks for the update!",
              notes="Spec example: 'Thanks for the update!' → HasTask=FALSE, acknowledgment"),

            m("priyasharma", "Can you call me when you're free? Need to discuss the migration plan.",
              has_task=True, sub_class="RfA", task_type="Scheduling",
              attribution="Implicit", assignee=["jameswilson"],
              notes="Spec example: 'Can you call?' → HasTask=TRUE"),

            m("jameswilson", "Sure, does 2 PM work for you?",
              has_task=True, sub_class="RfK", task_type="Scheduling",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Spec example: 'Does 2 PM work for you?' → HasTask=TRUE"),

            m("priyasharma", "Works",
              notes="Spec example: 'Works' → HasTask=FALSE, acknowledgment"),
        ],
    },

    # =========================================================================
    # S32: Group — More Spec Examples
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Sprint 48 Pre-Launch Tasks",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "ninacosta", "davidpark"],
        "messages": [
            m("alexkumar", "Could you please review the Status Update post before I send it to leadership? @Nina",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              attribution="Explicit", assignee=["ninacosta"],
              mentions=["ninacosta"],
              notes="Spec example: 'Could you please review the Status Update post?' → HasTask=TRUE"),

            m("ninacosta", "Sure, send it over.",
              notes="Acknowledgment — no task"),

            m("davidpark", "There's some pressure to get it to design for LT preview tomorrow. Let's make sure it's polished.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Unassigned", assignee=[],
              notes="Spec example: 'Some pressure to get it to design for LT preview tomorrow' → HasTask+IsImportant"),

            m("priyasharma", "Folks, I'm unwell. Will be OOF today and maybe tomorrow.",
              edge_case="ooof_announcement",
              notes="Spec example: 'Folks, I'm unwell. Will be OOF.' → HasTask=FALSE"),

            m("alexkumar", "Feel better Priya! We've got you covered.",
              notes="Social / well-wishes — no task"),

            m("alexkumar", "FYI: @Nikhil, @Andrew — I don't see you listed as DRIs for the dashboard module. Can you check and confirm?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Unassigned", assignee=[],
              edge_case="fyi_with_question",
              notes="Spec example: 'FYI: I don't see you listed as DRIs' → HasTask=TRUE (borderline), IsImportant=TRUE. Assignees don't exist in our user set so Unassigned."),

            m("ninacosta", "Need sign-off by EOD or we miss the ship window for the release candidate.",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              is_important=True, attribution="Unassigned", assignee=[],
              notes="Spec example: 'Need sign-off by EOD or we miss ship window' → HasTask=TRUE, IsImportant=TRUE"),

            m("davidpark", "Following up — still waiting on approval from the security team. This is blocking the rollout.",
              has_task=True, sub_class="RfK", task_type="Follow-up",
              is_important=True, attribution="Unassigned", assignee=[],
              notes="Spec example: 'Following up. Still waiting on approval; blocking rollout.' → HasTask+IsImportant"),

            m("alexkumar", "Quality is at 56% assertion rate vs our 80% production target. We need to address this before release.",
              is_important=True,
              edge_case="quality_metric_no_task",
              notes="Spec example: 'Quality is 56% assertion rate (vs 80% prod).' → HasTask=FALSE, IsImportant=TRUE"),

            m("davidpark", "We cannot proceed with module 5.3C in its current form. It needs a full rewrite of the validation layer.",
              is_important=True,
              edge_case="blocker_statement_no_ask",
              notes="Spec example: 'We cannot proceed with 5.3C in its current form.' → HasTask=FALSE, IsImportant=TRUE"),
        ],
    },

    # =========================================================================
    # S33: Group — Cleaning up stale tasks / These cleanups pattern
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "EOQ Cleanup Tasks",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "Team — these cleanups must be completed before 3/31. I've assigned owners in the tracking sheet. Check your items and confirm you're on track.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Spec example: 'These cleanups must be completed before 3/31.' → HasTask+IsImportant, Broadcast"),

            m("priyasharma", "Checked — my 3 items are on track. Should be done by Thursday.",
              notes="Status confirmation — informational"),

            m("jameswilson", "Two of mine are done. The third is blocked on the DNS propagation — same issue from last week.",
              is_important=True,
              notes="Status with blocker — informational. Important due to blocker."),

            m("ninacosta", "All QA items done. Tests pass. ✅",
              notes="Completed action report — no task"),

            m("alexkumar", "@James, can you escalate the DNS issue to the provider? We can't let this slip past 3/31.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["jameswilson"],
              mentions=["jameswilson"],
              notes="Explicit action request + hard deadline → Important"),

            m("jameswilson", "Already sent an email this morning. Waiting for their response.",
              notes="Status update — informational"),

            m("alexkumar", "Good. Keep me posted.",
              notes="Acknowledgment — no task"),
        ],
    },
]

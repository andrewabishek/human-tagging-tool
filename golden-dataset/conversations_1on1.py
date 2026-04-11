"""
Golden Dataset - 1:1 (OneOnOne) Conversations
15 conversations covering Engineering, Sales, HR, Legal, Finance, Marketing,
Executive, Customer Support, and Operations domains.

ANNOTATION KEY:
  has_task: bool
  task_sub_class: RfA | RfK | Commitment | Neither
  task_type: Action Request | Review/Approval | Scheduling | Delegation |
             Question | Confirmation/Permission | Availability/RSVP |
             Status Request | Decision Request | Follow-up
  is_important: bool
  attribution: Explicit | Implicit | Unassigned | Broadcast | N/A
  assignee: list of MailNickNames
  edge_case: str or None
  notes: str
"""

# Helper to build a message dict concisely
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


ONE_ON_ONE_CONVERSATIONS = [

    # =========================================================================
    # CONV 1: CEO ↔ CTO — Q2 Product Strategy (Executive/Engineering)
    # Covers: Decision Request, Action Request, Status Request, Commitment,
    #         IsImportant (board deadline), Attribution (Implicit - 1:1)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Q2 Product Strategy & Board Prep",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark"],
        "messages": [
            m("sarahmitchell", "David, have you had a chance to look at the competitive analysis from last week?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Implicit", assignee=["davidpark"],
              notes="1:1 → attribute to non-sender (David)"),

            m("davidpark", "Yes, reviewed it over the weekend. Solid work by the team. A few gaps in the enterprise segment though.",
              notes="Status update, no ask"),

            m("sarahmitchell", "What gaps specifically? I want to make sure we address them before the board presentation on the 28th.",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["davidpark"],
              notes="Question + board deadline → Important"),

            m("davidpark", "Mainly around our analytics offering vs. Asana and Monday.com. They've shipped AI-assisted resource allocation — we haven't. Also, our API ecosystem is lagging. I can put together a 2-pager summarizing the gaps with a proposed roadmap.",
              notes="Informational response + sender commitment. The commitment to create 2-pager is sender's own plan.",
              edge_case="commitment_with_info",),

            m("sarahmitchell", "That would be perfect. Can you have it ready by Thursday? I want to review it before the pre-board sync on Friday.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["davidpark"],
              notes="Action request + hard deadline linked to board prep → Important"),

            m("davidpark", "Thursday works. I'll pull in Alex for the technical feasibility piece.",
              edge_case="commitment_response",
              notes="Acknowledgment + commitment by sender to do the work. Not a new task for Sarah."),

            m("sarahmitchell", "Great. Also — should we position the AI roadmap as a separate initiative or fold it into the core platform story?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["davidpark"],
              notes="Decision request — asks David to weigh in on strategic direction"),

            m("davidpark", "I'd recommend folding it in. Positioning it separately risks signaling we're behind. If it's integrated, it looks like a natural evolution. Let me think on this a bit more and share my full take tomorrow.",
              edge_case="partial_answer_commitment",
              notes="Partial answer + commitment for tomorrow. No new task for Sarah."),

            m("sarahmitchell", "Makes sense. One more thing — did the infrastructure team confirm they can support the Q3 scale targets?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Knowledge question — Sarah needs confirmation"),

            m("davidpark", "James said they're at 85% confidence on the scale targets with current infra. The remaining 15% depends on the CDN migration finishing on time. I'll get a firm answer by end of week.",
              notes="Informational response + commitment for follow-up"),

            m("sarahmitchell", "OK. Let me know as soon as you have it. We can't go to the board with gaps there.",
              is_important=True,
              notes="Informational — expressing urgency but not assigning a new task. David already committed."),

            m("davidpark", "Understood. Will do.",
              notes="Acknowledgment"),

            m("sarahmitchell", "Thanks David. Talk tomorrow.",
              notes="Social/closing"),
        ],
    },

    # =========================================================================
    # CONV 2: CEO ↔ CFO — Budget Approval for Q2 Hiring
    # Covers: Approval Request, Question, Follow-up, IsImportant (budget),
    #         Deadline with consequence
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Q2 Hiring Budget Approval",
        "domain": "Finance",
        "members": ["sarahmitchell", "racheltorres"],
        "messages": [
            m("sarahmitchell", "Rachel, I need your sign-off on the Q2 hiring plan. David's team needs 4 additional engineers and Michael wants 2 more AEs.",
              has_task=True, sub_class="RfA", task_type="Review / Approval",
              is_important=True, attribution="Implicit", assignee=["racheltorres"],
              notes="Approval request + hiring impact → Important"),

            m("racheltorres", "I saw the headcount request. The engineering asks are within budget, but the sales hires push us $180K over the Q2 operating plan. We'd need to pull from the discretionary pool.",
              notes="Informational response — no ask, providing analysis"),

            m("sarahmitchell", "What's left in the discretionary pool right now?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Knowledge request in 1:1"),

            m("racheltorres", "$420K. But $200K of that is earmarked for the customer event in June. So realistically we have about $220K of true flex.",
              notes="Informational — answering the question"),

            m("sarahmitchell", "That's tight. Can we defer the customer event spend and reallocate?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Decision request — can we shift budget?"),

            m("racheltorres", "We could, but Laura and Michael have been counting on that event for pipeline gen. I'd recommend we approve the engineering hires now and table the sales hires until we see Q1 close rates. If Q1 beats forecast, we'll have the room.",
              notes="Recommendation — informational, no new task"),

            m("sarahmitchell", "Fair. Let's go with that. Can you process the approval for the 4 engineering headcount today? David's already got candidates in final rounds.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["racheltorres"],
              notes="Action request + same-day deadline + hiring urgency → Important"),

            m("racheltorres", "Will do. I'll send the approval through the system by 3 PM and copy Danielle on the HR side.",
              notes="Commitment by sender — not a task for Sarah"),

            m("sarahmitchell", "Perfect. And let's revisit the sales hires after the Q1 close on April 15.",
              notes="Planning statement, no immediate task",
              edge_case="deferred_plan",),

            m("racheltorres", "Noted. I'll flag it for our April budget sync.",
              notes="Acknowledgment + commitment"),

            m("sarahmitchell", "Thanks Rachel.",
              notes="Social closing"),
        ],
    },

    # =========================================================================
    # CONV 3: CTO ↔ Engineering Manager — Production Incident
    # Covers: Escalation, Action Request, Status Request, Follow-up,
    #         IsImportant (outage, customer impact), rapid-fire communication
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Production Incident — API Gateway Outage",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar"],
        "messages": [
            m("alexkumar", "David, heads up — we're seeing elevated error rates on the API gateway. 5xx errors spiked to 12% in the last 10 minutes.",
              is_important=True,
              notes="Incident notification — FYI but no task. IsImportant due to production impact."),

            m("davidpark", "How many customers affected? Is this the US or EU cluster?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["alexkumar"],
              notes="Urgent questions during active incident → Important"),

            m("alexkumar", "Both clusters. We're estimating 15K+ active users impacted. James is investigating — looks like the last deployment introduced a connection pool leak.",
              is_important=True,
              notes="Incident details — important context, no task"),

            m("davidpark", "Roll back the deployment immediately. Don't wait for root cause.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["alexkumar"],
              notes="Critical action request during outage → Important"),

            m("alexkumar", "James is initiating the rollback now. ETA 5 minutes for the US cluster, 8 for EU.",
              notes="Status update — rollback in progress"),

            m("davidpark", "Good. I need you to send a status update to the exec distribution list. Sarah will ask about this in the morning.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["alexkumar"],
              notes="Action request for stakeholder communication during incident"),

            m("alexkumar", "On it. I'll draft the exec update as soon as rollback is confirmed.",
              notes="Commitment by sender"),

            m("davidpark", "What's our confidence that the rollback fully resolves this? Any chance it's infrastructure-related too?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["alexkumar"],
              notes="Critical diagnostic question during incident"),

            m("alexkumar", "95% confident it's the deployment. Connection pool metrics correlate exactly with the deploy timestamp. Infra metrics are clean — CPU, memory, disk all normal.",
              notes="Informational response"),

            m("alexkumar", "Update: US cluster rollback complete. Error rates dropping. EU rollback in progress.",
              is_important=True,
              notes="Status update during incident — still important context"),

            m("davidpark", "Great. Let me know when EU is confirmed clean. And schedule a postmortem for tomorrow — I want the full team there.",
              has_task=True, sub_class="RfA", task_type="Scheduling Action",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Two tasks: notification + scheduling. Both for Alex in 1:1."),

            m("alexkumar", "EU is clean now. All error rates back to baseline. Total impact window was about 22 minutes. I'll set up the postmortem for 10 AM tomorrow and send the exec update in the next 30 minutes.",
              notes="Status report + commitment — not a new task for David"),

            m("davidpark", "Thanks Alex. Good handling tonight. Let's make sure we add deployment validation gates to prevent this class of issue.",
              edge_case="suggestion_not_task",
              notes="Praise + suggestion. 'Let's make sure' without specific assignee/deadline = not a task"),

            m("alexkumar", "Agreed. I'll add it to the postmortem action items.",
              notes="Acknowledgment + commitment"),
        ],
    },

    # =========================================================================
    # CONV 4: Eng Manager ↔ Sr Engineer — Code Review & Sprint Tasks
    # Covers: Review Request, Question, Acknowledgment, Confirmation,
    #         Routine (not Important), @mention in content
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "API v3 Migration — Code Review",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma"],
        "messages": [
            m("alexkumar", "Priya, can you review the API v3 migration PR? It's PR #847. I want to ship this by end of sprint.",
              has_task=True, sub_class="RfA", task_type="Review / Approval",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Review request in 1:1 → attribute to non-sender"),

            m("priyasharma", "Sure, I'll take a look this afternoon. Is there a specific area you want me to focus on?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Question back to Alex — needs response"),

            m("alexkumar", "Mainly the pagination logic and the rate limiting changes. Those are the riskiest parts. The rest is mostly boilerplate.",
              notes="Informational response to question"),

            m("priyasharma", "Got it. One question — did you run the load tests against the new pagination? Last time we had issues with cursor-based pagination under high concurrency.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Technical question requiring information"),

            m("alexkumar", "Good catch. I ran the basic load test but not the high-concurrency scenario. Can you include that in your review? Run the k6 suite with the 500-concurrent profile.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Action request — run specific test suite"),

            m("priyasharma", "Will do. I should have the review and load test results back to you by tomorrow morning.",
              notes="Commitment by sender"),

            m("alexkumar", "Perfect. Also, are you still on track to finish the webhook refactor this sprint?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Status question about another work item"),

            m("priyasharma", "Yes, I'm about 80% done. The event filtering piece is the last part. Should have it wrapped up by Thursday.",
              notes="Status update — no task"),

            m("alexkumar", "Great. Let me know if you hit any blockers.",
              edge_case="courtesy_not_task",
              notes="Courtesy offer — not a specific task. 'Let me know if...' = FALSE"),

            m("priyasharma", "Will do. Thanks Alex.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # CONV 5: VP Sales ↔ Account Executive — Contoso Deal at Risk
    # Covers: Follow-up, Status Request, Action Request, Delegation,
    #         IsImportant (revenue risk, customer churn), Urgency markers
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Contoso Enterprise Deal — At Risk",
        "domain": "Sales",
        "members": ["michaelchen", "sofiarodriguez"],
        "messages": [
            m("michaelchen", "Sofia, what's happening with the Contoso deal? I just got a ping from Sarah — they mentioned it in the exec sync.",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Status request escalated from CEO → Important"),

            m("sofiarodriguez", "It's complicated. Their CISO flagged data residency concerns during the security review last week. They want all data stored in the EU, and our current architecture doesn't support region-specific data isolation.",
              is_important=True,
              notes="Important context — deals with a $2.4M deal blocker"),

            m("michaelchen", "This is a $2.4M deal. We can't lose it over infrastructure. What's the timeline — when do they need an answer?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Revenue-critical question + urgency"),

            m("sofiarodriguez", "They gave us until end of next week. Their procurement cycle closes March 31 — if we miss that, the deal slips to Q3 at best, or they go with Smartsheet.",
              is_important=True,
              notes="Escalation context — hard deadline with revenue consequence"),

            m("michaelchen", "OK, I need you to do three things ASAP: 1) Set up a call with David's team to assess the EU data residency feasibility, 2) Draft a risk mitigation proposal for Contoso showing our roadmap, 3) Loop in Amanda to review any GDPR implications.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Multi-step delegation with ASAP urgency + revenue risk → Important"),

            m("sofiarodriguez", "On it. I've already pinged David's team for availability. I'll have the draft proposal ready by tomorrow EOD.",
              notes="Commitment by sender"),

            m("michaelchen", "Good. Keep me updated every day until this is resolved. I'm going to brief Sarah separately.",
              notes="Informational — Michael's own plan, no new task for Sofia beyond what's assigned"),

            m("sofiarodriguez", "Will do. One more thing — should I offer them a price concession to sweeten the deal while we work on the technical side?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["michaelchen"],
              notes="Decision request — Sofia needs Michael's guidance"),

            m("michaelchen", "Not yet. Let's see if the technical path works first. If we need to, I'll approve up to 10% off but I want that as a last resort. Don't mention it to them proactively.",
              notes="Decision response — informational"),

            m("sofiarodriguez", "Understood. I'll focus on the technical path first.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # CONV 6: HR Director ↔ CEO — Confidential Org Restructuring
    # Covers: Decision Request, Action Request, Sensitive topic,
    #         IsImportant (org change), Confirmation
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Q2 Org Restructuring — Confidential",
        "domain": "Human Resources",
        "members": ["daniellewright", "sarahmitchell"],
        "messages": [
            m("daniellewright", "Sarah, I've completed the analysis on the proposed restructuring. Can we discuss the recommendations?",
              has_task=True, sub_class="RfK", task_type="Availability / RSVP",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Availability request — needs Sarah to confirm she can discuss"),

            m("sarahmitchell", "Yes, go ahead.",
              notes="Acknowledgment / go-ahead"),

            m("daniellewright", "Based on the data, I'm recommending we consolidate the Customer Success and Support teams under Maria. Derek's team would report to her directly. This saves a headcount at the manager level and improves handoff efficiency.",
              notes="Informational/recommendation — no task for Sarah yet"),

            m("sarahmitchell", "What's the impact on Derek? Is he being let go?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["daniellewright"],
              notes="Question about personnel impact → Important due to leadership/HR sensitivity"),

            m("daniellewright", "No, the recommendation is to transition him to a senior IC role — Support Engineering Lead. Same comp band, different scope. I've modeled it both ways and this preserves the team's institutional knowledge.",
              notes="Informational response"),

            m("sarahmitchell", "I like that approach. Has Legal reviewed the restructuring for any compliance issues?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["daniellewright"],
              notes="Compliance question"),

            m("daniellewright", "Amanda reviewed the draft plan last week. She flagged that we need to update the employee handbook and send formal notifications 30 days before the effective date. I have the timeline mapped out.",
              notes="Informational — answering the question"),

            m("sarahmitchell", "Good. Let's target June 1 for the effective date. That gives us enough runway. Please prepare the formal proposal with the full timeline, role changes, and communication plan. I need it by next Friday for the leadership review.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Implicit", assignee=["daniellewright"],
              notes="Delegation with deadline + org-wide impact → Important"),

            m("daniellewright", "I'll have it ready. One question — do you want me to include a draft communication for the affected employees, or should we wait for leadership sign-off first?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Decision request — process question"),

            m("sarahmitchell", "Draft it now so we're ready to move fast after sign-off. But mark it clearly as DRAFT — don't share it beyond us and Amanda.",
              notes="Decision response — informational"),

            m("daniellewright", "Understood. Will keep it tightly held.",
              notes="Acknowledgment"),

            m("sarahmitchell", "Thanks Danielle. This is sensitive — please don't discuss with anyone outside of this until leadership approves.",
              notes="Guidance — no new task"),
        ],
    },

    # =========================================================================
    # CONV 7: Marketing Director ↔ Content Manager — Campaign Launch
    # Covers: Review Request, Action Request, Scheduling, Question,
    #         Routine (not Important)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Spring Campaign — Content and Assets",
        "domain": "Marketing",
        "members": ["laurakim", "chrisevans"],
        "messages": [
            m("laurakim", "Chris, where are we on the spring campaign blog posts? We need 3 posts live by March 20.",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Status request with deadline context"),

            m("chrisevans", "Post 1 is in final edit. Post 2 draft is done, needs your review. Post 3 I'm still outlining — the customer story angle needs more input from Maria on the success metrics.",
              notes="Status update — no task"),

            m("laurakim", "Can you send me the Post 2 draft? I'll review it today.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Action request — send the draft"),

            m("chrisevans", "Just shared it in the Marketing shared drive. It's in the Spring Campaign folder.",
              notes="Completion report — already done"),

            m("laurakim", "Great. For Post 3 — reach out to Maria directly and get the Pinnacle Logistics success metrics. Don't wait for her to come to you.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Direct action request"),

            m("chrisevans", "Will do. Should I also include a quote from the customer in the blog post, or keep it to our internal metrics?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["laurakim"],
              notes="Decision request — content direction"),

            m("laurakim", "Include a customer quote if they've approved it. Check with Maria — she should have the testimonial clearance from their marketing team.",
              notes="Decision response — informational"),

            m("chrisevans", "Got it. I'll coordinate with Maria and have the Post 3 draft ready by Friday.",
              notes="Commitment by sender"),

            m("laurakim", "Sounds good. Also, have you updated the social media calendar with the promotion schedule for these posts?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Question — checking completeness"),

            m("chrisevans", "Not yet, I'll do that this afternoon. I was waiting until the posts were finalized so the dates are accurate.",
              notes="Status + commitment — no task for Laura"),

            m("laurakim", "OK, just make sure it's done before the team sync on Thursday. Jenna will need the schedule for social planning.",
              notes="Reminder/context — not a new task, reinforcing the existing commitment",
              edge_case="reminder_not_new_task"),

            m("chrisevans", "Will have it ready by Wednesday EOD.",
              notes="Commitment"),
        ],
    },

    # =========================================================================
    # CONV 8: General Counsel ↔ Finance Manager — Audit Preparation
    # Covers: Action Request, Question, Review, Follow-up,
    #         IsImportant (audit deadline, compliance)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "SOC 2 Audit Preparation",
        "domain": "Legal",
        "members": ["amandafoster", "kevinzhang"],
        "messages": [
            m("amandafoster", "Kevin, the SOC 2 auditors are coming on-site in 3 weeks. I need the financial controls documentation updated and ready for review. Where do we stand?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Implicit", assignee=["kevinzhang"],
              notes="Status request + audit deadline → Important"),

            m("kevinzhang", "The revenue recognition controls are updated. Expense management controls are about 70% done. The biggest gap is the vendor payment authorization documentation — David's team made some changes to the approval workflow last quarter and it hasn't been documented yet.",
              notes="Status update — informational"),

            m("amandafoster", "That vendor payment gap is a risk. The auditors specifically flagged authorization controls last year. Can you get that documentation completed by end of next week?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["kevinzhang"],
              notes="Action request with deadline + audit risk → Important"),

            m("kevinzhang", "I'll prioritize it. I need to coordinate with James on the engineering side — they modified the approval thresholds in the procurement system. Can you send me the specific audit requirements so I know exactly what format they need?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["amandafoster"],
              notes="Counter-request — Kevin needs docs from Amanda"),

            m("amandafoster", "I'll send you the audit checklist this afternoon. It has the format requirements and specific controls they'll test. Also — have we resolved the access control finding from last year? That was a material finding.",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["kevinzhang"],
              notes="Question about prior audit finding + material weakness → Important"),

            m("kevinzhang", "Yes, we implemented the segregation of duties changes in November. I have the evidence package ready for that one. The only outstanding item is the quarterly access review for Q1 — we need to complete that before the auditors arrive.",
              is_important=True,
              notes="Status with remaining risk — Important because compliance gap identified"),

            m("amandafoster", "Please make sure that Q1 access review is completed within the next two weeks. If they find that incomplete, it undermines our entire remediation story.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["kevinzhang"],
              notes="Action request + compliance consequence → Important"),

            m("kevinzhang", "Understood. I'll coordinate with IT to get it done this week.",
              notes="Commitment"),

            m("amandafoster", "Good. Let's do a dry run walkthrough of all the financial controls next Friday. Can you have everything ready by then?",
              has_task=True, sub_class="RfK", task_type="Confirmation / Permission",
              attribution="Implicit", assignee=["kevinzhang"],
              notes="Confirmation request — can he meet the deadline?"),

            m("kevinzhang", "Yes, that's doable. I'll block the time.",
              notes="Confirmation / acknowledgment"),
        ],
    },

    # =========================================================================
    # CONV 9: CSM ↔ Support Lead — Customer Escalation
    # Covers: Action Request, Status Request, Follow-up,
    #         IsImportant (customer churn risk), Attribution (1:1)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Pinnacle Logistics — P1 Support Escalation",
        "domain": "Customer Support",
        "members": ["mariasantos", "derekjohnson"],
        "messages": [
            m("mariasantos", "Derek, Pinnacle Logistics just escalated to me directly. They say they've had an open P1 ticket for 4 days with no resolution. What's going on?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Implicit", assignee=["derekjohnson"],
              notes="Escalation + P1 SLA breach + top customer → Important"),

            m("derekjohnson", "I know the ticket. It's the data export timeout issue — ticket #45891. My team reproduced it but we're blocked on engineering. We filed a bug but haven't gotten traction.",
              is_important=True,
              notes="Status update revealing cross-team blocker → Important context"),

            m("mariasantos", "Pinnacle is our third-largest customer. If we don't resolve this soon, the VP of Ops there is going to escalate to Michael. Can you get me the ticket details and the engineering bug number? I'll escalate to Alex directly.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["derekjohnson"],
              notes="Action request + customer churn risk → Important"),

            m("derekjohnson", "Ticket #45891, engineering bug ENG-2847. Filed on Monday. Currently unassigned on the eng side as far as I can see.",
              notes="Informational response"),

            m("mariasantos", "Unassigned for 4 days? That's unacceptable. Is there a workaround we can offer Pinnacle in the meantime?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["derekjohnson"],
              notes="Question — seeking interim solution for customer"),

            m("derekjohnson", "There's a partial workaround — they can export in smaller batches. It's clunky but functional. My team offered it on day 2 but Pinnacle's ops team said it's not sustainable for their daily workflow.",
              notes="Informational response"),

            m("mariasantos", "OK, please prepare a formal escalation summary with the full timeline, business impact, and workaround status. I need it in the next 2 hours — I'm setting up a call with Alex this afternoon.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["derekjohnson"],
              notes="Action request with tight deadline + escalation path → Important"),

            m("derekjohnson", "I'll have it to you within the hour.",
              notes="Commitment"),

            m("mariasantos", "Thanks Derek. Also — going forward, any P1 from a top-20 customer should be flagged to me within 24 hours. Don't wait for the customer to escalate.",
              notes="Process guidance — not a specific task on a specific item",
              edge_case="process_guidance_not_task"),

            m("derekjohnson", "Noted. I'll update our triage runbook with that rule.",
              notes="Commitment by sender"),
        ],
    },

    # =========================================================================
    # CONV 10: Eng Manager ↔ DevOps — Deployment Blocker
    # Covers: Action Request, Question, Confirmation, Follow-up,
    #         IsImportant (deployment blocker), Technical context
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "CDN Migration — Deployment Blocked",
        "domain": "Engineering",
        "members": ["alexkumar", "jameswilson"],
        "messages": [
            m("alexkumar", "James, the CDN migration deploy is blocked. CI is failing on the integration tests. Can you look at it?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["jameswilson"],
              notes="Action request + deployment blocker → Important"),

            m("jameswilson", "Looking at it now. The integration test failures are all in the edge caching module — looks like a config mismatch between staging and the new CDN endpoints.",
              notes="Status update — investigating"),

            m("alexkumar", "Is this something you can fix today? We need this migration done by Friday or we're going to miss the Q1 infra target.",
              has_task=True, sub_class="RfK", task_type="Confirmation / Permission",
              is_important=True, attribution="Implicit", assignee=["jameswilson"],
              notes="Confirmation request + hard deadline → Important"),

            m("jameswilson", "The config fix itself is straightforward — maybe an hour. But I want to run the full regression suite after, which takes about 3 hours. Earliest I can have a green build is late afternoon.",
              notes="Informational — timeline estimate"),

            m("alexkumar", "That works. Go ahead with the fix and full regression. Don't cut corners on testing — this is production traffic.",
              notes="Approval / guidance — not a new task"),

            m("jameswilson", "Agreed. One thing — I noticed the CDN provider's SSL cert for the EU endpoint expires in 12 days. Should I file a renewal request now or is that handled by their operations team?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Question — seeking guidance on process ownership"),

            m("alexkumar", "Good catch. File the renewal request on our side — don't rely on them. Better safe than sorry.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["jameswilson"],
              notes="Action request arising from James's question"),

            m("jameswilson", "Will do. I'll file it today and add monitoring for cert expiration to our alerting dashboard.",
              notes="Commitment by sender"),

            m("alexkumar", "Perfect. Ping me when the build is green.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["jameswilson"],
              notes="Simple action request — notification"),

            m("jameswilson", "👍",
              notes="Acknowledgment (emoji-only)",
              edge_case="emoji_acknowledgment"),
        ],
    },

    # =========================================================================
    # CONV 11: Account Executive ↔ General Counsel — NDA Review
    # Covers: Review Request, Permission, Question, Follow-up,
    #         Cross-functional, Deadline pressure
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Northwind Traders NDA Review",
        "domain": "Legal",
        "members": ["sofiarodriguez", "amandafoster"],
        "messages": [
            m("sofiarodriguez", "Amanda, I need the Northwind Traders NDA reviewed and redlined. Can you turn it around by Wednesday?",
              has_task=True, sub_class="RfA", task_type="Review / Approval",
              attribution="Implicit", assignee=["amandafoster"],
              notes="Review request with deadline in 1:1"),

            m("amandafoster", "I can take a look. Is this their paper or ours?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Clarifying question before starting work"),

            m("sofiarodriguez", "Their paper. They sent a mutual NDA with some non-standard language around IP ownership that I'm not comfortable with. I flagged the sections in yellow in the shared doc.",
              notes="Informational response"),

            m("amandafoster", "OK, I'll review it. Non-standard IP language in an NDA is a red flag — glad you caught it. Any particular deal terms driving urgency, or can this slip to Thursday if needed?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Question about timeline flexibility"),

            m("sofiarodriguez", "Wednesday is ideal. We have a technical evaluation starting Thursday and they want the NDA executed before sharing their architecture docs. If it slips, the whole eval timeline shifts.",
              notes="Context / informational — explaining urgency"),

            m("amandafoster", "Understood. I'll prioritize it. If the IP language is as non-standard as you're saying, I may need to push back on their counsel. Are you OK if I engage directly with their legal team?",
              has_task=True, sub_class="RfK", task_type="Confirmation / Permission",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Permission request — wants OK to engage counterparty"),

            m("sofiarodriguez", "Yes, please go ahead. Their legal contact is Rebecca Walsh — I'll send you her email.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Self-initiated action — Sofia commits to sending contact info",
              edge_case="self_initiated_task"),

            m("amandafoster", "Thanks. I'll have the redline back to you by Wednesday morning.",
              notes="Commitment by sender"),

            m("sofiarodriguez", "Thanks Amanda 🙏",
              notes="Social / acknowledgment"),
        ],
    },

    # =========================================================================
    # CONV 12: QA Lead ↔ Sr Engineer — Bug Triage & Release Blocker
    # Covers: Action Request, Question, Status Request,
    #         IsImportant (ship-blocking bug), Technical detail
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Release Blocker — Dashboard Rendering Bug",
        "domain": "Engineering",
        "members": ["ninacosta", "priyasharma"],
        "messages": [
            m("ninacosta", "Priya, I found a critical rendering bug in the dashboard module. Charts aren't loading when there are more than 50 data points. This is a release blocker for v4.2.",
              is_important=True,
              notes="Bug report — ship-blocking severity → Important. No explicit task yet."),

            m("priyasharma", "That sounds like the chart library upgrade we did last sprint. Can you share the repro steps and browser/environment details?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["ninacosta"],
              notes="Action request — needs repro steps for debugging"),

            m("ninacosta", "Repro: 1) Create a project with 51+ tasks, 2) Open the analytics dashboard, 3) Click on the resource allocation chart. Browser: Chrome 121 and Edge 121 both affected. Firefox works fine. I've attached screenshots to bug ENG-2901.",
              notes="Informational response — providing requested details"),

            m("priyasharma", "Thanks. Chrome and Edge both use Blink rendering — Firefox uses Gecko. That narrows it down. Is this in all chart types or just the resource allocation chart?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["ninacosta"],
              notes="Technical diagnostic question"),

            m("ninacosta", "I tested all chart types. The resource allocation, timeline, and burndown charts are all affected. Pie charts and bar charts work fine. It seems to be specific to the time-series rendering path.",
              notes="Informational — test results"),

            m("priyasharma", "OK, I have a theory. The chart library v3 changed how it handles SVG rendering for large datasets. I'll work on a fix today. Can you also check if this regression exists in the staging environment? I want to confirm it's not a data issue.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["ninacosta"],
              notes="Action request — verify in staging"),

            m("ninacosta", "I'll check staging right now.",
              notes="Commitment"),

            m("ninacosta", "Confirmed — same issue in staging. Definitely a code regression, not data.",
              notes="Test result — informational"),

            m("priyasharma", "Found it. The library's SVG renderer has a default limit of 50 nodes per group. I need to set an explicit override. Fix is simple but I want to verify it doesn't break the rendering performance. Can you run the full visual regression suite once I push the fix?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["ninacosta"],
              notes="Action request for test verification of ship-blocking fix → Important"),

            m("ninacosta", "Absolutely. Ping me when it's pushed and I'll run it immediately. I want this closed today if possible — Alex is asking about the release timeline.",
              is_important=True,
              notes="Urgency context — release timeline pressure → Important"),

            m("priyasharma", "Pushing now. Should be in CI within 10 minutes.",
              notes="Status update"),
        ],
    },

    # =========================================================================
    # CONV 13: Finance Manager ↔ Ops Manager — Procurement
    # Covers: Approval, Question, Action Request, Routine (not Important)
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Office Equipment & Software Procurement",
        "domain": "Operations",
        "members": ["kevinzhang", "lisanakamura"],
        "messages": [
            m("lisanakamura", "Kevin, I need to submit the PO for the new conference room equipment. Can you approve the $28K spend?",
              has_task=True, sub_class="RfA", task_type="Review / Approval",
              attribution="Implicit", assignee=["kevinzhang"],
              notes="Approval request — routine procurement"),

            m("kevinzhang", "Is this the AV upgrade we discussed in the facilities planning meeting? I thought the budget was $25K.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["lisanakamura"],
              notes="Clarifying question about scope"),

            m("lisanakamura", "Yes, same project. The $3K difference is the additional cable management and mounting hardware that we didn't account for in the initial estimate. I have the detailed breakdown in the PO.",
              notes="Informational — justification"),

            m("kevinzhang", "OK, $28K is within my approval threshold. I'll approve it today. Can you make sure the vendor delivers before the end of March? We need to close this against the Q1 budget.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["lisanakamura"],
              notes="Conditional approval + action request on delivery timing"),

            m("lisanakamura", "I'll confirm the delivery timeline with the vendor today. They originally quoted 2-3 weeks lead time, so we should be fine.",
              notes="Commitment by sender"),

            m("kevinzhang", "Great. Also — did you get quotes for the software license renewals? Those are due by April 1.",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Implicit", assignee=["lisanakamura"],
              notes="Status request on another procurement item"),

            m("lisanakamura", "Got quotes from all three vendors. The Figma renewal is 12% higher than last year. Slack and Zoom are comparable. I'll send you the comparison spreadsheet.",
              has_task=True, sub_class="Commitment", task_type="Action Request",
              attribution="Implicit", assignee=["lisanakamura"],
              notes="Self-initiated action — Lisa commits to sending comparison",
              edge_case="self_initiated_action"),

            m("kevinzhang", "12% increase on Figma? That's steep. Let me know the contract terms — I may want to negotiate.",
              notes="Informational reaction — no specific task assigned"),

            m("lisanakamura", "Will do.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # CONV 14: Marketing Director ↔ CSM — Customer Testimonial
    # Covers: Permission Request, Action Request, Question,
    #         Cross-functional, customer approval
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Customer Testimonial — Pinnacle Logistics",
        "domain": "Marketing",
        "members": ["laurakim", "mariasantos"],
        "messages": [
            m("laurakim", "Maria, we want to feature Pinnacle Logistics in our spring campaign as a case study. Have they agreed to participate?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["mariasantos"],
              notes="Question — checking customer approval status"),

            m("mariasantos", "I spoke with their VP of Ops last month and she was open to it in principle. But I haven't gotten formal approval from their marketing or legal team yet.",
              notes="Informational — status update"),

            m("laurakim", "Can you reach out and get formal sign-off? I need confirmation by next Wednesday to make our production deadline. If they can't commit by then, I'll need to find an alternative customer.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["mariasantos"],
              notes="Action request with deadline"),

            m("mariasantos", "I'll reach out today. One concern though — they've had some frustrations with our support responsiveness recently. Might not be the best time to ask for a public endorsement.",
              notes="Context / risk flagging — informational"),

            m("laurakim", "Good point. Is the support issue resolved?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["mariasantos"],
              notes="Question about customer situation"),

            m("mariasantos", "Derek's team resolved the P1 last week. Pinnacle's contact seemed satisfied with the resolution. I think we're OK to ask, but I wanted you to know the context.",
              notes="Status update — informational"),

            m("laurakim", "Thanks for flagging that. Go ahead and ask. If they push back, don't force it — customer relationship comes first.",
              notes="Direction — not a new task (already assigned above)"),

            m("mariasantos", "Agreed. I'll be thoughtful in my approach. Should I share the draft case study outline with them so they know what to expect?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["laurakim"],
              notes="Decision request — process question"),

            m("laurakim", "Yes, please share the outline. It'll make them more comfortable. Chris has the draft — ask him to send it to you.",
              notes="Decision response + informational"),

            m("mariasantos", "Perfect. I'll coordinate with Chris and reach out to Pinnacle today.",
              notes="Commitment"),
        ],
    },

    # =========================================================================
    # CONV 15: CTO ↔ CFO — Engineering Investment Decision
    # Covers: Decision Request, Question, Action Request,
    #         IsImportant (strategic investment), Cross-functional
    # =========================================================================
    {
        "chat_type": "OneOnOne",
        "topic": "Engineering Platform Investment — Build vs Buy",
        "domain": "Executive",
        "members": ["davidpark", "racheltorres"],
        "messages": [
            m("davidpark", "Rachel, I need to discuss the platform observability investment. We have two options — build internally for ~$800K over 6 months, or buy Datadog Enterprise for ~$350K/year. Each has tradeoffs.",
              notes="Context setting — informational, no task yet"),

            m("racheltorres", "What's the TCO comparison over 3 years?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Financial analysis question — 1:1 non-sender attribution"),

            m("davidpark", "Build: ~$800K upfront + $200K/year maintenance = $1.4M over 3 years. Buy: $350K/year = $1.05M over 3 years. But the build option gives us custom integrations with our platform that Datadog can't match.",
              notes="Informational — providing requested analysis"),

            m("racheltorres", "The $350K difference over 3 years is meaningful but not decisive. What's the engineering opportunity cost? Those engineers could be building product features instead.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Strategic question about tradeoffs"),

            m("davidpark", "Good point. It would tie up 3 senior engineers for 6 months. That's roughly $600K in product feature velocity we'd lose. We were planning to use those engineers for the AI features roadmap.",
              notes="Informational — answering the question"),

            m("racheltorres", "The AI features are what Sarah wants to showcase to the board. I'd lean toward buying Datadog and keeping the engineering team focused on product. Can you build the business case with both options modeled out? I want to present it at the next budget committee.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["davidpark"],
              notes="Action request + board/strategic context → Important"),

            m("davidpark", "I'll have it ready by Monday. Should I include the AI features opportunity cost in the model, or keep it purely infra-focused?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Decision request — scope of analysis"),

            m("racheltorres", "Include both. Sarah will want to see the full picture — infra cost AND product velocity impact. That's what makes the decision compelling.",
              notes="Decision response — informational"),

            m("davidpark", "Makes sense. I'll model it that way.",
              notes="Acknowledgment"),

            m("racheltorres", "Thanks David. This is a good example of the kind of investment discipline we need. 👍",
              notes="Social / praise"),
        ],
    },
]

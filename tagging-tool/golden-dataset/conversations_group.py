"""
Golden Dataset - Group Chat Conversations
25 conversations covering cross-functional scenarios, edge cases, and all domains.
"""

from conversations_1on1 import m  # reuse the message helper


GROUP_CONVERSATIONS = [

    # =========================================================================
    # CONV 16: Engineering Standup (Eng team daily)
    # Covers: Status updates, blockers, action items, acknowledgments
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Engineering Daily Standup",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "Morning team. Let's do a quick standup. Where is everyone at?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Broadcast", assignee=[],
              notes="Broadcast status request to everyone in group"),

            m("priyasharma", "I wrapped up the API v3 pagination fix yesterday. PR #847 is ready for final review. Today I'm starting on the webhook refactor.",
              notes="Status update — no task"),

            m("jameswilson", "CDN migration is back on track. Config fix is deployed, regression suite passed. I'm moving on to the monitoring dashboard updates today.",
              notes="Status update — no task"),

            m("ninacosta", "I'm halfway through the visual regression test suite for v4.2. The dashboard rendering fix from Priya is verified. Remaining: export module and notification system tests.",
              notes="Status update — no task"),

            m("alexkumar", "Good progress. @Priya, who's doing the final review on your pagination PR? I want it merged today.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["priyasharma"],
              notes="Question directed at specific person via @mention",
              mentions=["priyasharma"]),

            m("priyasharma", "I assigned it to James for the infra perspective. James, can you review it before noon?",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              attribution="Implicit", assignee=["jameswilson"],
              notes="Review request directed to James by name (no @mention)"),

            m("jameswilson", "Sure, I'll look at it by 11.",
              notes="Acknowledgment/commitment"),

            m("alexkumar", "Nina, any blockers on the regression suite?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["ninacosta"],
              notes="Direct question to Nina by name in group chat"),

            m("ninacosta", "One minor blocker — the staging environment is running an older build. I need it updated to the latest before I can run the export tests. @James, can you push the latest build to staging?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["jameswilson"],
              notes="Action request via @mention in group chat",
              mentions=["jameswilson"]),

            m("jameswilson", "Will do. Give me 20 minutes.",
              notes="Acknowledgment/commitment"),

            m("alexkumar", "OK, quick reminder — v4.2 release candidate is due Friday. Let's make sure all the pieces are in place. Everyone please update Jira with your current status by EOD.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Broadcast", assignee=[],
              notes="Broadcast action request to entire group"),

            m("priyasharma", "👍",
              notes="Acknowledgment (emoji)",
              edge_case="emoji_acknowledgment"),

            m("ninacosta", "Will do.",
              notes="Acknowledgment"),

            m("jameswilson", "On it.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # CONV 17: Sales Pipeline Review
    # Covers: Status Request, Action Request, IsImportant (revenue risk),
    #         Decision Request, Follow-up
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q1 Pipeline Review & Forecast",
        "domain": "Sales",
        "members": ["michaelchen", "sofiarodriguez", "sarahmitchell"],
        "messages": [
            m("michaelchen", "Sarah, Sofia — let's align on the Q1 pipeline. We're 3 weeks from close. Sofia, can you give us the rundown on the top 5 deals?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Status request directed at Sofia by name"),

            m("sofiarodriguez", "Here's where we stand:\n1. Contoso Enterprise - $2.4M - in security review (at risk)\n2. Northwind Traders - $850K - NDA in legal, eval starting next week\n3. Fabrikam Corp - $620K - verbal commit, waiting on procurement\n4. Woodgrove Bank - $1.1M - demo scheduled this week\n5. Tailspin Toys - $340K - negotiation phase\n\nTotal pipeline: $5.3M. Committed: $1.0M. Best case: $3.9M.",
              notes="Status report — informational, no task"),

            m("sarahmitchell", "That's a big gap between committed and pipeline. What's the risk on Contoso?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Question about at-risk deal from CEO → Important"),

            m("sofiarodriguez", "Data residency concern from their CISO. We're working on it — David's team is assessing the EU hosting feasibility. I have a call with their procurement team Thursday.",
              notes="Status update — informational"),

            m("michaelchen", "Contoso is make-or-break for Q1. @Sofia, I need you to send me a daily status update on that deal until it's resolved. I'll handle the exec alignment on our side.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["sofiarodriguez"],
              notes="Action request via @mention + revenue significance → Important",
              mentions=["sofiarodriguez"]),

            m("sofiarodriguez", "Will do. I'll send updates by 5 PM daily.",
              notes="Commitment"),

            m("sarahmitchell", "Michael, what's your confidence level that we hit the $3.5M target for Q1?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["michaelchen"],
              notes="Question directed at Michael by name"),

            m("michaelchen", "Honestly, 60-40 right now. If Contoso closes, we're at $3.7M. Without it, we're at $1.3M committed which is well short. Everything hinges on the Contoso security resolution and Fabrikam getting through procurement.",
              notes="Assessment — informational"),

            m("sarahmitchell", "That's not where I need it to be for the board. Michael, can you put together a risk mitigation plan with backup deals we could accelerate? I need it by Monday.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["michaelchen"],
              notes="Action request + board deadline context → Important"),

            m("michaelchen", "I'll have it for you Sunday night.",
              notes="Commitment"),

            m("sarahmitchell", "Thanks both. Let's regroup Wednesday after Sofia's Contoso call.",
              notes="Planning statement — no immediate task"),
        ],
    },

    # =========================================================================
    # CONV 18: Product Launch Cross-functional
    # Covers: Delegation, @mentions with CC, Multi-assignee, IsImportant (launch)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Meridian v4.2 Launch Coordination",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark", "alexkumar", "laurakim", "chrisevans", "michaelchen"],
        "messages": [
            m("sarahmitchell", "Team, we're 2 weeks out from the v4.2 launch. I want to make sure every workstream is on track. Let's do a round-robin update.",
              has_task=True, sub_class="RfK", task_type="Status Request",
              attribution="Broadcast", assignee=[],
              notes="Broadcast request to all members"),

            m("davidpark", "Engineering is green. RC build is on track for Friday. One open item — the dashboard rendering fix needs to land today, but Priya and Nina are on it.",
              notes="Status update — no task"),

            m("laurakim", "Marketing is ready. Blog posts, social calendar, and email campaign are all queued. The only dependency is the final feature screenshots from the engineering team — @Alex, can you get those to Chris by Thursday?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["alexkumar"],
              notes="Action request via @mention with deadline",
              mentions=["alexkumar"]),

            m("alexkumar", "I'll get them over by Wednesday so Chris has buffer time.",
              notes="Commitment"),

            m("michaelchen", "Sales enablement deck is done. We're doing deal team training on Monday. One ask — @Laura, can we get early access to the blog posts for the sales team to share with prospects?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["laurakim"],
              notes="Action request via @mention — cross-functional ask",
              mentions=["laurakim"]),

            m("laurakim", "Sure. @Chris, please share draft links with Michael's team by Friday.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["chrisevans"],
              notes="Delegation via @mention — Laura redirects to Chris",
              mentions=["chrisevans"]),

            m("chrisevans", "Will do.",
              notes="Acknowledgment"),

            m("sarahmitchell", "David, what's our rollback plan if something goes wrong on launch day?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Question directed at David by name"),

            m("davidpark", "Blue-green deployment with instant rollback capability. We can revert within 2 minutes. James has the runbook ready.",
              notes="Informational response"),

            m("sarahmitchell", "Good. @David and @Alex — please do a launch readiness review on Thursday. I want sign-off from both of you before we go.",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              is_important=True, attribution="Explicit", assignee=["davidpark", "alexkumar"],
              notes="Multi-assignee task via @mentions + launch gating → Important",
              mentions=["davidpark", "alexkumar"]),

            m("davidpark", "Blocked on my calendar.",
              notes="Acknowledgment"),

            m("alexkumar", "Same. I'll prepare the checklist.",
              notes="Acknowledgment + commitment"),

            m("sarahmitchell", "Great. This launch needs to go smoothly — it's our first big release since the Series C and investors are watching. Let's not drop the ball.",
              is_important=True,
              notes="Motivational/context — no specific task but signals importance"),
        ],
    },

    # =========================================================================
    # CONV 19: Executive Leadership — Board Prep
    # Covers: Decision Request, Delegation, IsImportant (board-level),
    #         Strategic discussion
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Board Meeting Preparation — Q1 Review",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark", "racheltorres"],
        "messages": [
            m("sarahmitchell", "We're a week out from the board meeting. Are we aligned on the narrative? I want to lead with product momentum and address the revenue gap proactively.",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Broadcast", assignee=[],
              notes="Confirmation request to both David and Rachel"),

            m("racheltorres", "I have the financial section ready. Revenue is $800K below forecast but I've framed it with the pipeline acceleration narrative. The bridge from Q1 actuals to Q2 forecast is solid.",
              notes="Status update — informational"),

            m("davidpark", "Product section is 80% done. I'm including the competitive analysis and the AI roadmap. One question — do we want to disclose the Datadog vs. build decision to the board, or keep it internal?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Decision request directed at Sarah as CEO"),

            m("sarahmitchell", "Include it. The board will appreciate the disciplined approach to build vs buy. It shows we're thinking about TCO, not just features.",
              notes="Decision response — informational"),

            m("sarahmitchell", "Rachel, can you add a slide on the cost optimization initiatives? I want to show the board we're being responsible with the Series C capital.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["racheltorres"],
              notes="Action request + board presentation context → Important"),

            m("racheltorres", "I'll add it. I have good data on the vendor consolidation savings and the infrastructure efficiency gains from James's team.",
              notes="Commitment"),

            m("sarahmitchell", "David, I also need you to prepare a 3-minute demo of the AI-assisted resource allocation feature. Even if it's a prototype, the board needs to see where we're going.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["davidpark"],
              notes="Action request + board demo → Important"),

            m("davidpark", "I can do a prototype demo. Alex's team has a working proof of concept. I'll polish it up.",
              notes="Commitment"),

            m("racheltorres", "Sarah, should we also address the headcount discussion? The board may ask why we're hiring into a revenue gap.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Strategic question to CEO"),

            m("sarahmitchell", "Yes, good call. Frame it as investing in growth — the engineering hires are for the product features that drive the Q2-Q3 pipeline. It's correlated spend, not discretionary.",
              notes="Direction — informational"),

            m("davidpark", "Agreed. I can tie the hiring to specific product milestones that feed into Michael's pipeline forecast.",
              notes="Suggestion — no task"),

            m("sarahmitchell", "Perfect. Let's do a dry run Tuesday afternoon. Rachel, can you coordinate a time?",
              has_task=True, sub_class="RfA", task_type="Scheduling",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Scheduling action directed at Rachel by name"),

            m("racheltorres", "I'll send an invite for 3 PM Tuesday.",
              notes="Commitment"),
        ],
    },

    # =========================================================================
    # CONV 20: Marketing + Sales Alignment
    # Covers: Action Request, Review, Scheduling, Decision, Routine
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q2 Campaign Alignment — Marketing + Sales",
        "domain": "Marketing",
        "members": ["laurakim", "michaelchen", "sofiarodriguez", "chrisevans"],
        "messages": [
            m("laurakim", "Hey everyone, wanted to sync on the Q2 campaign plan. We're targeting enterprise accounts with the analytics story. @Michael, does this align with what your team is hearing from prospects?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["michaelchen"],
              notes="Question via @mention in group",
              mentions=["michaelchen"]),

            m("michaelchen", "Mostly. Analytics is the #1 feature request, but a lot of enterprise prospects also care about integrations and security certifications. Can we weave those into the campaign messaging?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["laurakim"],
              notes="Counter-question directed at Laura"),

            m("laurakim", "Good input. @Chris, can you draft updated messaging that includes the integration ecosystem and security certifications alongside analytics? I want a first draft by Monday.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["chrisevans"],
              notes="Delegation via @mention with deadline",
              mentions=["chrisevans"]),

            m("chrisevans", "On it. Sofia, can you share the top 5 objections you hear from enterprise prospects? I want to make sure the messaging addresses those.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Action request directed at Sofia by name"),

            m("sofiarodriguez", "Sure. The big ones are: 1) Data security/sovereignty, 2) Integration with existing tools, 3) Migration effort from current PM tool, 4) Reporting/analytics depth, 5) Pricing for large teams. I'll put together a one-pager with more detail.",
              notes="Informational + commitment"),

            m("michaelchen", "That's helpful. @Laura, one more thing — we're hosting a webinar with Contoso's VP of Ops if the deal closes. Could that become part of the campaign?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Explicit", assignee=["laurakim"],
              notes="Decision request via @mention",
              mentions=["laurakim"]),

            m("laurakim", "I love that idea. Let's plan for it tentatively and we can confirm once the deal closes. Chris, add a 'customer webinar' track to the campaign plan as a contingency.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Action request directed at Chris by name"),

            m("chrisevans", "Added. I'll create the webinar landing page template so we're ready to go.",
              notes="Commitment"),

            m("laurakim", "Great sync everyone. Let's regroup next Wednesday with Chris's draft messaging.",
              notes="Closing — no new task"),
        ],
    },

    # =========================================================================
    # CONV 21: Incident Response
    # Covers: Urgent Action Requests, Escalation, IsImportant (outage),
    #         Rapid-fire communication, Multiple @mentions
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "🚨 Production Incident — Database Connection Pool Exhaustion",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "jameswilson", "priyasharma"],
        "messages": [
            m("jameswilson", "🚨 ALERT: Production database connection pool exhausted. All API endpoints returning 503. Multiple customers reporting issues.",
              is_important=True,
              notes="Incident alert — Important. No task yet, but critical FYI."),

            m("alexkumar", "All hands on deck. @James, what's the current connection count vs pool limit? @Priya, check if the connection leak fix from PR #847 is deployed.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["jameswilson", "priyasharma"],
              notes="Multi-assignee action request via @mentions during incident → Important",
              mentions=["jameswilson", "priyasharma"]),

            m("jameswilson", "Pool is at 500/500. We're fully saturated. The spike started 8 minutes ago. Correlates with a batch job that kicked off at 2 PM.",
              is_important=True,
              notes="Diagnostic info during active incident → Important"),

            m("priyasharma", "PR #847 is deployed in production as of yesterday. But wait — the pagination fix changed the connection handling. Let me check if there's a connection leak in the new code path.",
              is_important=True,
              notes="Diagnostic update → Important"),

            m("davidpark", "What's customer impact right now? How many users affected?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Urgent question to anyone who can answer"),

            m("jameswilson", "Monitoring shows ~8,000 active users getting errors. The status page is still green — should I update it?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              is_important=True, attribution="Implicit", assignee=["alexkumar", "davidpark"],
              notes="Permission request during incident — who approves status page update?"),

            m("davidpark", "Yes, update the status page immediately. Mark it as partial service degradation.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["jameswilson"],
              notes="Urgent action request → Important"),

            m("priyasharma", "Found it. The new pagination code opens a new connection for each cursor-based query but doesn't release it when the client disconnects mid-stream. The batch job is triggering thousands of cursor queries.",
              is_important=True,
              notes="Root cause identified — Important context"),

            m("alexkumar", "@Priya, can you push an emergency fix? In the meantime, @James, kill the batch job and manually free the stale connections.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["priyasharma", "jameswilson"],
              notes="Two parallel action requests via @mentions during incident → Important",
              mentions=["priyasharma", "jameswilson"]),

            m("jameswilson", "Batch job killed. Freeing stale connections now... Pool is recovering. Down to 320/500.",
              is_important=True,
              notes="Status update during mitigation → Important"),

            m("priyasharma", "Fix is ready — adding a connection.close() in the finally block of the cursor handler. PR #852. Alex, can you fast-track review? It's a 3-line change.",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              is_important=True, attribution="Implicit", assignee=["alexkumar"],
              notes="Emergency review request during incident → Important"),

            m("alexkumar", "Reviewed. LGTM. Merge and deploy.",
              notes="Approval — de-escalation. Not a new task.",
              edge_case="approval_de_escalation"),

            m("jameswilson", "Pool is back to 45/500. All endpoints responding normally. Deploying Priya's fix now.",
              is_important=True,
              notes="Recovery status — still Important until confirmed resolved"),

            m("davidpark", "Good work team. Total incident duration was about 25 minutes. Alex, please schedule a postmortem for tomorrow and send the exec summary tonight.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Implicit", assignee=["alexkumar"],
              notes="Two action items assigned to Alex — postmortem + exec summary"),

            m("alexkumar", "On it. Postmortem invite going out for 10 AM tomorrow. Exec summary in the next hour.",
              notes="Commitment"),

            m("jameswilson", "Fix deployed. Monitoring confirms stable. Updating status page to resolved.",
              notes="Completion report — no task"),
        ],
    },

    # =========================================================================
    # CONV 22: Headcount Planning (HR + Eng + Finance)
    # Covers: Approval, Decision, Question, Cross-functional,
    #         IsImportant (budget impact)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q2 Headcount Planning — Engineering",
        "domain": "Human Resources",
        "members": ["daniellewright", "davidpark", "alexkumar", "racheltorres"],
        "messages": [
            m("daniellewright", "Hi everyone. I want to finalize the Q2 headcount plan for engineering. David and Alex, can you confirm your final requirements?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Implicit", assignee=["davidpark", "alexkumar"],
              notes="Confirmation request directed at two people by name"),

            m("davidpark", "We need 4 positions: 2 senior backend engineers, 1 ML engineer for the AI features, and 1 DevOps engineer to support the scaling work.",
              notes="Informational — providing requirements"),

            m("alexkumar", "I agree with David's list. The backend engineers are the most urgent — we're already short-staffed on the API team.",
              notes="Agreement/support — informational"),

            m("racheltorres", "Budget is approved for 4 engineering headcount. @Danielle, please start the req process. I'd like offers extended by end of April to manage the cash flow timing.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["daniellewright"],
              notes="Action request via @mention + budget/timing context → Important",
              mentions=["daniellewright"]),

            m("daniellewright", "I'll open the reqs today. @David, @Alex — I'll need updated job descriptions for the ML engineer and DevOps roles. The backend JDs we can reuse from last cycle.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["davidpark", "alexkumar"],
              notes="Action request via @mentions — need specific deliverables",
              mentions=["davidpark", "alexkumar"]),

            m("davidpark", "I'll update the ML engineer JD today. Alex, can you handle the DevOps one?",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Delegation within the group — David to Alex by name"),

            m("alexkumar", "Sure. I'll have it over by tomorrow morning.",
              notes="Commitment"),

            m("daniellewright", "Great. Once I have the JDs, I'll target having candidates in final rounds within 3 weeks. Rachel, any constraints on the comp bands?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Question directed at Rachel by name"),

            m("racheltorres", "Standard band for senior engineers. For the ML role, we may need to go 10-15% above band to be competitive. I've seen market data showing a premium for ML engineers right now. I'll send you the updated comp ranges.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Self-initiated action — Rachel offers to send comp data",
              edge_case="self_initiated_action"),

            m("daniellewright", "Thanks Rachel. I'll factor that in. Let's check in next week on progress.",
              notes="Acknowledgment / planning"),
        ],
    },

    # =========================================================================
    # CONV 23: Legal + Sales — Deal Review
    # Covers: Review, Question, Permission, IsImportant (deal deadline)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Northwind Traders — Contract Review",
        "domain": "Legal",
        "members": ["amandafoster", "michaelchen", "sofiarodriguez"],
        "messages": [
            m("amandafoster", "I've completed the NDA review for Northwind Traders. There are three issues I need to flag:\n1. Their IP transfer clause is overly broad\n2. The non-compete language could restrict our sales in the project management space\n3. The governing law is New York but we typically insist on Delaware",
              is_important=True,
              notes="Legal risk identification — Important due to deal impact"),

            m("sofiarodriguez", "That IP clause was the one that concerned me too. Can we push back on all three?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["amandafoster"],
              notes="Question seeking legal guidance"),

            m("amandafoster", "We should push back on #1 and #2 — those are deal-breakers from our perspective. On #3, I'm flexible — New York is workable, just not ideal. @Sofia, do you know if Northwind has flexibility on their terms?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["sofiarodriguez"],
              notes="Question via @mention",
              mentions=["sofiarodriguez"]),

            m("sofiarodriguez", "Their legal team seemed pretty firm when we first discussed. But the deal is important to them too — they specifically chose us over a competitor. I think we have leverage.",
              notes="Contextual assessment — informational"),

            m("michaelchen", "Amanda, can you prepare a counter-proposal with our preferred language on the IP and non-compete clauses? @Sofia, set up a call with their legal team for Thursday. Let's resolve this before the technical evaluation starts.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["amandafoster", "sofiarodriguez"],
              notes="Multi-assignee delegation — Amanda (counter-proposal) + Sofia (scheduling). @Sofia via mention, Amanda by name. Deal deadline → Important",
              mentions=["sofiarodriguez"]),

            m("amandafoster", "I'll have the counter-proposal ready by Wednesday EOD. That gives Sofia time to share it before the call.",
              notes="Commitment"),

            m("sofiarodriguez", "Scheduling the call now. I'll send the invite once confirmed.",
              notes="Commitment"),

            m("michaelchen", "Thanks team. Amanda — if they won't budge on the IP clause, is there a middle ground we can live with?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["amandafoster"],
              notes="Question to Amanda by name — contingency planning"),

            m("amandafoster", "We could limit the IP scope to only work products specifically created for the integration project, rather than a blanket transfer. That protects our core platform IP while giving them what they need.",
              notes="Informational — legal analysis"),

            m("michaelchen", "Smart. Let's lead with our preferred position and have that as a fallback. Good work team.",
              notes="Agreement + closing — no task"),
        ],
    },

    # =========================================================================
    # CONV 24: Budget Review (Finance + Exec)
    # Covers: Action Request, Question, Decision, IsImportant (fiscal)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q1 Budget Review & Q2 Forecast",
        "domain": "Finance",
        "members": ["racheltorres", "kevinzhang", "sarahmitchell"],
        "messages": [
            m("racheltorres", "Sarah, Kevin — here's the Q1 budget summary. We're 6% under on revenue and 3% over on opex. Net impact is about $1.1M below plan.",
              is_important=True,
              notes="Budget miss notification — Important due to financial impact. No task."),

            m("sarahmitchell", "That's concerning. What's driving the opex overage?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Question to Rachel/Kevin — Important financial discussion"),

            m("kevinzhang", "Three main factors: 1) Cloud infrastructure costs came in $180K over due to the scaling work, 2) The enterprise customer event ran $90K over budget, 3) Recruiting costs for the engineering hires were higher than planned — about $120K in agency fees.",
              notes="Analysis — informational"),

            m("sarahmitchell", "We need to course-correct for Q2. @Kevin, can you prepare a cost optimization analysis — identify at least $500K in savings opportunities across all departments?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["kevinzhang"],
              notes="Action request via @mention + financial significance → Important",
              mentions=["kevinzhang"]),

            m("kevinzhang", "I'll have it ready by next Friday. Should I coordinate with department heads, or keep the analysis independent first?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["sarahmitchell"],
              notes="Process question directed at Sarah"),

            m("sarahmitchell", "Keep it independent first. I don't want departments sandbagging their numbers. We'll share with them after Rachel and I review.",
              notes="Decision — informational"),

            m("racheltorres", "Agreed. Kevin, I'll share the department-level budget files with you today so you have the granular data. Also — I want to flag that our cash runway is still healthy. The $1.1M miss doesn't change our 18-month runway materially.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["racheltorres"],
              notes="Self-initiated action (sharing files) + reassurance",
              edge_case="self_initiated_action"),

            m("sarahmitchell", "Good to know. But I still want us operating lean. The board expects fiscal discipline post-Series C.",
              notes="Direction/philosophy — no specific task"),

            m("kevinzhang", "Understood. I'll focus the analysis on efficiency gains, not just cuts — so we're not sacrificing growth.",
              notes="Commitment + framing"),
        ],
    },

    # =========================================================================
    # CONV 25: Support Escalation Cross-team
    # Covers: Escalation, Action Request, Follow-up, IsImportant (customer risk)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Pinnacle Logistics — P1 Escalation Thread",
        "domain": "Customer Support",
        "members": ["derekjohnson", "mariasantos", "alexkumar", "michaelchen"],
        "messages": [
            m("mariasantos", "Alex, Michael — Pinnacle Logistics has an open P1 for 5 days. They're our 3rd largest customer ($1.2M ARR). The issue is a data export timeout that Derek's team can't resolve without an engineering fix. This needs immediate attention.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Implicit", assignee=["alexkumar"],
              notes="Escalation to engineering with revenue context → Important"),

            m("alexkumar", "5 days? That shouldn't have sat that long. Let me check the bug. Derek, what's the engineering ticket number?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["derekjohnson"],
              notes="Question during escalation — needs ticket info"),

            m("derekjohnson", "ENG-2847. Filed on Monday. It's been unassigned on the engineering side. I pinged the eng channel twice but got no response.",
              is_important=True,
              notes="Details revealing process gap — Important context"),

            m("alexkumar", "I see it now. This fell through the cracks — the auto-assignment was broken last week. I'm assigning this to Priya now and marking it P1. She'll have a fix or workaround by tomorrow morning.",
              notes="Commitment + resolution plan — not a task for others"),

            m("michaelchen", "Tomorrow morning isn't fast enough. Their VP of Ops is already cc'ing our CEO on emails. If we don't show progress by end of today, we risk the renewal. @Alex, can we expedite?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              is_important=True, attribution="Explicit", assignee=["alexkumar"],
              notes="Escalation pressure + churn risk → Important. @mention",
              mentions=["alexkumar"]),

            m("alexkumar", "OK, I'll pull Priya off her current work and make this the top priority. We'll have a workaround within 3 hours.",
              notes="Commitment — acknowledgment of urgency"),

            m("mariasantos", "Thank you. @Derek, please keep Pinnacle informed — let them know we've escalated internally and they should expect an update by 5 PM today.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["derekjohnson"],
              notes="Action request via @mention — customer communication",
              mentions=["derekjohnson"]),

            m("derekjohnson", "Will do. Sending them an update now.",
              notes="Commitment"),

            m("michaelchen", "Let's make sure we have a proper escalation process for top-20 accounts. This shouldn't have gone 5 days without engineering attention.",
              notes="Process feedback — not a specific task",
              edge_case="process_feedback_not_task"),

            m("alexkumar", "Agreed. I'll fix the auto-assignment and add a 24-hour SLA alert for P1s from top accounts.",
              notes="Commitment — self-assigned improvement"),

            m("mariasantos", "Thanks everyone. I'll report back once Pinnacle acknowledges the update.",
              notes="Commitment / planning"),
        ],
    },

    # =========================================================================
    # CONV 26: Code Review Discussion (Engineering)
    # Covers: Review, Technical questions, @mentions, Routine
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "PR #852 — Connection Pool Fix Review",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "ninacosta"],
        "messages": [
            m("priyasharma", "PR #852 is up for the connection pool fix. It's a 3-line change in the cursor handler. @Alex already did a quick review during the incident, but I'd like a thorough review from @Nina on the test coverage.",
              has_task=True, sub_class="RfA", task_type="Review/Approval",
              attribution="Explicit", assignee=["ninacosta"],
              notes="Review request via @mention",
              mentions=["alexkumar", "ninacosta"]),

            m("ninacosta", "Taking a look now. Does the test suite cover the case where a client disconnects mid-stream during a cursor query?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Technical question during review"),

            m("priyasharma", "Good question. I added a test for graceful disconnect but not for abrupt disconnects (like network failure). Should I add that?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["ninacosta"],
              notes="Decision request — test scope question"),

            m("ninacosta", "Yes, definitely. The original bug was caused by abrupt disconnects from the batch job. We should test both scenarios. Also, can you add a test that verifies the connection count after 100 rapid connect/disconnect cycles?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Action request — add specific tests"),

            m("priyasharma", "Will add both. Give me 30 minutes.",
              notes="Commitment"),

            m("alexkumar", "While you're at it, can you also add a prometheus metric for active connection count? That would've helped us diagnose the issue faster during the incident.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["priyasharma"],
              notes="Additional action request — observability improvement"),

            m("priyasharma", "Good idea. I'll add it in this PR since it's related.",
              notes="Commitment"),

            m("ninacosta", "Otherwise the fix itself looks clean. LGTM once the tests are added.",
              notes="Conditional approval — no new task",
              edge_case="conditional_approval"),

            m("priyasharma", "Tests added and passing. CI is green. Ready for re-review.",
              notes="Completion report — no task"),

            m("ninacosta", "Looks great. Approved. ✅",
              notes="Approval — resolution of prior ask",
              edge_case="approval_de_escalation"),
        ],
    },

    # =========================================================================
    # CONV 27: All-Hands Planning (Cross-functional)
    # Covers: Delegation, Scheduling, Action Request, Routine
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q1 All-Hands Planning",
        "domain": "Executive",
        "members": ["sarahmitchell", "laurakim", "daniellewright", "lisanakamura", "chrisevans"],
        "messages": [
            m("sarahmitchell", "Team, let's plan the Q1 all-hands. I want it to feel different this time — more interactive, less death-by-slides. Targeting the last Friday of the month.",
              notes="Direction setting — no specific task yet"),

            m("laurakim", "I agree. We could do a fireside chat format for the product update instead of slides. @Chris, can you design the visual deck for the all-hands? Something modern, less text-heavy.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["chrisevans"],
              notes="Delegation via @mention",
              mentions=["chrisevans"]),

            m("chrisevans", "Love the fireside chat idea. I'll put together a visual-first deck template. When do you need it?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["laurakim"],
              notes="Question about deadline"),

            m("laurakim", "By Wednesday of that week so we have 2 days for dry run.",
              notes="Answer — informational"),

            m("daniellewright", "I can handle the employee recognition segment. I have the Q1 award nominations finalized. @Lisa, can you coordinate with facilities on the venue setup — chairs in a semi-circle for the fireside format?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["lisanakamura"],
              notes="Action request via @mention — logistics",
              mentions=["lisanakamura"]),

            m("lisanakamura", "Sure. I'll also arrange catering for 50 in-office plus the streaming setup for remote folks. Want the usual lunch spread?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Broadcast", assignee=[],
              notes="Confirmation question to the group"),

            m("sarahmitchell", "Yes, but add some variety this time. People complained about the same sandwich platters. Budget is fine up to $1,500.",
              notes="Direction — informational"),

            m("lisanakamura", "Got it. I'll upgrade the menu. 🍕",
              notes="Acknowledgment"),

            m("sarahmitchell", "One more thing — I want to open with a 5-minute video montage of team highlights from Q1. @Chris, can you put that together too? Use clips from the product demos, team events, and customer wins.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["chrisevans"],
              notes="Action request via @mention",
              mentions=["chrisevans"]),

            m("chrisevans", "Absolutely! I'll gather clips and have a draft ready for review by the Monday before.",
              notes="Commitment"),

            m("daniellewright", "This is shaping up nicely. I'm excited!",
              notes="Social — no task",
              edge_case="social_enthusiasm"),
        ],
    },

    # =========================================================================
    # CONV 28: Compliance Initiative (Legal + Engineering + Finance + HR)
    # Covers: Delegation, Action Request, Question, IsImportant (regulatory)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "SOC 2 & GDPR Compliance — Cross-team Coordination",
        "domain": "Legal",
        "members": ["amandafoster", "kevinzhang", "davidpark", "daniellewright"],
        "messages": [
            m("amandafoster", "Everyone, the SOC 2 auditors confirmed their on-site visit for April 15. We have 3 weeks to close all open items. This is not negotiable — a failed audit would be devastating for our enterprise sales.",
              is_important=True,
              notes="Compliance deadline announcement — Important. No task yet."),

            m("amandafoster", "@David, I need engineering to complete the access control remediation and the disaster recovery test. What's the status?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Explicit", assignee=["davidpark"],
              notes="Status request via @mention + audit deadline → Important",
              mentions=["davidpark"]),

            m("davidpark", "Access control remediation is done — James implemented the segregation of duties changes in November. The DR test is scheduled for next week. I'll make sure it's completed and documented.",
              notes="Status update + commitment"),

            m("amandafoster", "@Kevin, the financial controls documentation — specifically the vendor payment authorization gap we discussed. Is that closed?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Explicit", assignee=["kevinzhang"],
              notes="Status request via @mention + audit risk → Important",
              mentions=["kevinzhang"]),

            m("kevinzhang", "Almost. I'm waiting on James for the updated approval threshold documentation. I expect to have everything finalized by end of this week.",
              notes="Status update — informational"),

            m("amandafoster", "@Danielle, HR controls — employee onboarding/offboarding procedures, access provisioning documentation, background check records. Are those audit-ready?",
              has_task=True, sub_class="RfK", task_type="Status Request",
              is_important=True, attribution="Explicit", assignee=["daniellewright"],
              notes="Status request via @mention + audit scope → Important",
              mentions=["daniellewright"]),

            m("daniellewright", "Onboarding and offboarding procedures are documented and current. Background check records are complete. One gap — we need to update the access provisioning SOP to reflect the new approval workflow David's team implemented.",
              notes="Status update with identified gap"),

            m("amandafoster", "OK, everyone please submit your final evidence packages to me by April 8. That gives me a week to compile and review before the auditors arrive. I'll send each of you a specific checklist today.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Broadcast action request with hard deadline + audit → Important"),

            m("davidpark", "Will do.",
              notes="Acknowledgment"),

            m("kevinzhang", "Understood.",
              notes="Acknowledgment"),

            m("daniellewright", "Got it. I'll coordinate with David on the access provisioning update.",
              notes="Acknowledgment + commitment"),

            m("amandafoster", "Thanks everyone. If anyone identifies a new gap, flag it immediately. No surprises during the audit.",
              notes="Guidance — no specific task"),
        ],
    },

    # =========================================================================
    # CONV 29: Campaign Planning (Marketing team)
    # Covers: Creative review, Decision Request, Action Request, Routine
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Spring Campaign — Creative Review",
        "domain": "Marketing",
        "members": ["laurakim", "chrisevans", "sofiarodriguez"],
        "messages": [
            m("chrisevans", "Draft messaging is ready for the spring enterprise campaign. I've shared the doc in the Marketing shared drive. Three tagline options to choose from:\nA) 'Enterprise Intelligence, Simplified'\nB) 'Your Projects, Powered by AI'\nC) 'The Smarter Way to Ship'",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Broadcast", assignee=[],
              notes="Decision request — tagline choice presented to group"),

            m("laurakim", "I like option B — it ties directly to the AI features we're launching. But 'powered by' feels a bit generic. Can you iterate on that one?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Action request — iterate on creative"),

            m("sofiarodriguez", "From a sales perspective, option A resonates most with enterprise buyers. They care about 'intelligence' and 'simplified' — those are the exact words I hear in discovery calls.",
              notes="Input/opinion — informational"),

            m("chrisevans", "What if we combine them? 'Enterprise Intelligence, AI-Powered'. Gets the enterprise feel from A and the AI angle from B.",
              notes="Suggestion — no task"),

            m("laurakim", "I like that. Sofia, would that work in your sales conversations?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Question directed at Sofia by name"),

            m("sofiarodriguez", "Yes, that's strong. Short, professional, and hits the right keywords for the audience.",
              notes="Feedback — informational"),

            m("laurakim", "Let's go with 'Enterprise Intelligence, AI-Powered'. Chris, please update all the campaign assets with the final tagline and send me the updated proofs by Thursday.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["chrisevans"],
              notes="Action request with deadline — finalize creative assets"),

            m("chrisevans", "On it. I'll also update the landing page header and the email templates.",
              notes="Commitment + additional self-initiated work"),

            m("laurakim", "Perfect. Great collaboration everyone 🎨",
              notes="Social closing"),
        ],
    },

    # =========================================================================
    # CONV 30: Office/Tool Issues (Ops + Engineering + Support)
    # Covers: Action Request, Question, IsImportant (tool outage),
    #         System breakage
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Salesforce Down — Impact & Workaround",
        "domain": "Operations",
        "members": ["lisanakamura", "jameswilson", "derekjohnson"],
        "messages": [
            m("lisanakamura", "Heads up everyone — Salesforce has been down for the past 2 hours. I've submitted a support ticket with Salesforce but no ETA on resolution yet.",
              is_important=True,
              notes="Tool outage notification — Important due to business process impact. No task."),

            m("derekjohnson", "This is impacting the support team badly. We can't access customer records or update tickets. Is there a workaround?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Question seeking workaround during outage → Important"),

            m("jameswilson", "I checked — it's a Salesforce-side issue, not our integration. Their status page shows 'investigating.' Unfortunately there's no workaround for the core CRM. For critical support tickets, you can use the backup spreadsheet in the shared drive.",
              notes="Informational — providing workaround info"),

            m("lisanakamura", "@Derek, can you make sure your team switches to the backup workflow for any critical tickets? And let me know if any customer-facing commitments are at risk because of this.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["derekjohnson"],
              notes="Action request via @mention during outage → Important",
              mentions=["derekjohnson"]),

            m("derekjohnson", "Will do. We have 3 customers with SLA-bound responses due today. I'll handle them via the backup process.",
              notes="Commitment"),

            m("jameswilson", "FYI — I've set up an alert. When Salesforce comes back online, I'll sync the backup data automatically. Nothing will be lost.",
              notes="FYI — informational"),

            m("lisanakamura", "Thanks James. @Derek, please send me a list of any impacted SLA responses so I can notify the customer success team.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["derekjohnson"],
              notes="Action request via @mention",
              mentions=["derekjohnson"]),

            m("derekjohnson", "Sending it now.",
              notes="Commitment"),

            m("lisanakamura", "Salesforce just came back online. Confirmed working. Total downtime: about 3 hours.",
              notes="Resolution notification — informational"),

            m("jameswilson", "Backup data sync initiated. Should be fully reconciled within 30 minutes.",
              notes="Status update — informational"),
        ],
    },

    # =========================================================================
    # CONV 31: Product Feature Discussion
    # Covers: Question, Decision, Action Request, Technical discussion
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "AI Resource Allocation Feature — Requirements",
        "domain": "Engineering",
        "members": ["davidpark", "alexkumar", "priyasharma", "michaelchen"],
        "messages": [
            m("davidpark", "Team, let's define the MVP for the AI-assisted resource allocation feature. This is the top item on our Q2 roadmap and a key board commitment. @Michael, what are the most requested capabilities from customers?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Explicit", assignee=["michaelchen"],
              notes="Question via @mention + strategic priority → Important",
              mentions=["michaelchen"]),

            m("michaelchen", "Top 3 requests:\n1. Automatic team member assignment based on skills and availability\n2. Workload balancing across projects\n3. Predictive timeline estimation based on historical data\n\nIf we nail #1 and #2 for MVP, that covers 80% of the demand.",
              notes="Informational — providing requirements"),

            m("alexkumar", "From a technical standpoint, #1 and #2 are feasible for Q2 with 2 engineers. #3 requires a trained ML model on customer data — that's at least Q3.",
              notes="Technical assessment — informational"),

            m("priyasharma", "I've been prototyping the matching algorithm. The challenge is real-time availability data — our current calendar integration only syncs every 15 minutes. Should I build for real-time or batch?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Broadcast", assignee=[],
              notes="Technical decision request to the group"),

            m("davidpark", "Build for batch first — 15-minute sync is fine for MVP. We can optimize to real-time in v2. @Priya, can you have the prototype ready for a demo by end of next week?",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["priyasharma"],
              notes="Action request via @mention with deadline",
              mentions=["priyasharma"]),

            m("priyasharma", "Yes, I can have a working demo with sample data by Friday. It won't be production-ready but it'll show the concept.",
              notes="Commitment"),

            m("michaelchen", "Can I bring a customer to see the demo? Contoso has been asking about this exact feature.",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Broadcast", assignee=[],
              notes="Permission request to the group — is it OK to show customer?"),

            m("davidpark", "Not yet. Let's get it stable first. Once we're confident in the demo, we can set up a customer preview. Probably 2-3 weeks after the initial prototype.",
              notes="Decision response — informational"),

            m("alexkumar", "Agreed. Priya, let me know if you need help with the calendar integration piece. James might have some useful infrastructure code from the scheduling service.",
              edge_case="courtesy_offer",
              notes="Courtesy offer — 'let me know if' = not a task"),

            m("priyasharma", "Thanks, I'll reach out. I think I actually have what I need from the existing API.",
              notes="Acknowledgment"),
        ],
    },

    # =========================================================================
    # CONV 32: Weekly Team Sync (mixed topics)
    # Covers: Various task types, acknowledgments, social, FYI, edge cases
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Marketing Weekly Sync Notes",
        "domain": "Marketing",
        "members": ["laurakim", "chrisevans", "sofiarodriguez", "mariasantos"],
        "messages": [
            m("laurakim", "Quick sync notes from today's meeting. Sharing here so everyone has the record:\n\n1. Spring campaign is on track. Chris finalizing assets by Thursday.\n2. Customer webinar with Pinnacle contingent on deal close.\n3. Social media metrics up 23% MoM.\n4. Blog content calendar is full through Q1.\n\nAction items below.",
              notes="Meeting notes summary — informational, no task"),

            m("laurakim", "@Chris — finalize campaign landing page and send proof to me by Thursday EOD.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["chrisevans"],
              notes="Action request via @mention with deadline",
              mentions=["chrisevans"]),

            m("laurakim", "@Sofia — share the enterprise prospect objection list with Chris by Wednesday for the messaging update.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["sofiarodriguez"],
              notes="Action request via @mention with deadline",
              mentions=["sofiarodriguez"]),

            m("laurakim", "@Maria — confirm Pinnacle's availability for the customer testimonial. Deadline: Next Wednesday.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["mariasantos"],
              notes="Action request via @mention with deadline",
              mentions=["mariasantos"]),

            m("chrisevans", "Got it. Landing page is 90% done, I'll have it finalized Thursday morning.",
              notes="Acknowledgment + status"),

            m("sofiarodriguez", "Will send the list to Chris tomorrow.",
              notes="Commitment"),

            m("mariasantos", "I'm reaching out to Pinnacle today. Will update the group once I hear back.",
              notes="Commitment"),

            m("laurakim", "Great. Also FYI — I'm OOO next Friday for a dentist appointment. Chris, you're in charge of any urgent requests that day.",
              notes="FYI / informational — OOO notice",
              edge_case="fyi_with_implicit_delegation"),

            m("chrisevans", "Noted. Safe teeth! 😄",
              notes="Social / humor — no task"),

            m("laurakim", "😂 Thanks. Have a good week everyone!",
              notes="Social closing"),
        ],
    },

    # =========================================================================
    # CONV 33: Customer Escalation Cross-team (Critical)
    # Covers: Escalation, Action Request, Follow-up, IsImportant (churn risk),
    #         Multi-department coordination
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "⚠️ GlobalTech Solutions — Churn Risk Escalation",
        "domain": "Customer Support",
        "members": ["mariasantos", "derekjohnson", "alexkumar", "michaelchen", "amandafoster"],
        "messages": [
            m("mariasantos", "URGENT: GlobalTech Solutions ($850K ARR) is threatening to cancel their contract. Their CTO sent an email directly to Sarah. Main complaints:\n1. Three unresolved P2 tickets over 2 months\n2. Missing API documentation for their custom integration\n3. No dedicated account manager assigned\n\nWe need an action plan within 24 hours.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Urgent escalation with churn risk + CEO involvement → Important"),

            m("michaelchen", "I had no idea this was escalating. Maria, why wasn't I looped in earlier?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["mariasantos"],
              notes="Question — process accountability"),

            m("mariasantos", "The individual tickets didn't seem severe enough to escalate. But the pattern is the problem — three unresolved issues compounded. My mistake — I should have flagged the trend.",
              notes="Informational — accountability"),

            m("derekjohnson", "The three tickets are legitimate. Two are feature limitations in our export API, and one is a documentation gap. The export issues need engineering work — we can't solve them on the support side.",
              notes="Status context — informational"),

            m("alexkumar", "OK, I'll get the export API issues prioritized. @Derek, can you send me the ticket details with repro steps? I'll assign an engineer today.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["derekjohnson"],
              notes="Action request via @mention during escalation → Important",
              mentions=["derekjohnson"]),

            m("michaelchen", "@Maria, I need you to draft a recovery plan for GlobalTech. Include: 1) Timeline for resolving all three issues, 2) Proposal for a dedicated account manager, 3) A goodwill offer — maybe a quarter of free premium support.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              is_important=True, attribution="Explicit", assignee=["mariasantos"],
              notes="Delegation via @mention with specific deliverables → Important",
              mentions=["mariasantos"]),

            m("mariasantos", "I'll have the draft ready by end of day tomorrow.",
              notes="Commitment"),

            m("amandafoster", "Quick note — if we're offering free premium support, I'll need to review the contract amendment. Their current agreement has specific SLA terms we can't override unilaterally. @Maria, please send me the current contract so I can check.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["mariasantos"],
              notes="Action request via @mention — legal review needed",
              mentions=["mariasantos"]),

            m("mariasantos", "Sending it now.",
              notes="Commitment"),

            m("michaelchen", "Thanks everyone. Let's regroup tomorrow at 4 PM with the action plan. I'll schedule the meeting.",
              has_task=True, sub_class="RfA", task_type="Scheduling",
              attribution="Implicit", assignee=["michaelchen"],
              notes="Self-scheduled meeting — sender's own action",
              edge_case="self_initiated_scheduling"),

            m("derekjohnson", "Ticket details sent to Alex. All three with full repro steps.",
              notes="Completion report"),
        ],
    },

    # =========================================================================
    # CONV 34: Data Privacy Incident
    # Covers: Security/compliance, Urgent actions, IsImportant (breach),
    #         Cross-functional coordination
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "🔒 SECURITY: Potential Data Exposure Incident",
        "domain": "Legal",
        "members": ["amandafoster", "davidpark", "jameswilson", "daniellewright"],
        "messages": [
            m("jameswilson", "SECURITY ALERT: During routine log review, I found that a misconfigured S3 bucket exposed customer project names and email addresses for approximately 6 hours yesterday. The bucket is now secured. Impact assessment in progress.",
              is_important=True,
              notes="Security incident notification — Important. Data exposure."),

            m("amandafoster", "This is a potential GDPR/CCPA incident. James, how many customers were affected and what data was exposed?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["jameswilson"],
              notes="Urgent question about breach scope → Important"),

            m("jameswilson", "Based on the access logs, 247 customer accounts were in the exposed bucket. Data included: project names, user email addresses, and team names. No passwords, payment data, or file contents were exposed.",
              is_important=True,
              notes="Breach scope details — Important context"),

            m("amandafoster", "OK. We need to assess whether this triggers notification requirements. Under GDPR, we have 72 hours from discovery. @David, can you confirm this has been fully contained and there's no ongoing exposure?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              is_important=True, attribution="Explicit", assignee=["davidpark"],
              notes="Confirmation request during security incident → Important",
              mentions=["davidpark"]),

            m("davidpark", "Confirmed contained. James fixed the bucket permissions last night and I verified the fix this morning. We've also audited all other S3 buckets — no similar misconfigurations.",
              notes="Confirmation — informational"),

            m("amandafoster", "@James, I need the complete access log from the exposure window. We need to determine if anyone actually accessed the data, or if it was just theoretically exposed.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["jameswilson"],
              notes="Action request via @mention — evidence gathering → Important",
              mentions=["jameswilson"]),

            m("jameswilson", "Pulling the logs now. Preliminary check shows 3 external IP addresses accessed the bucket during the window. Analyzing whether they accessed customer data or just the bucket listing.",
              is_important=True,
              notes="Concerning finding during investigation → Important"),

            m("amandafoster", "@Danielle, we may need to notify affected customers. Can you prepare a draft notification email? Use the incident response template but customize for this type of exposure.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Explicit", assignee=["daniellewright"],
              notes="Action request via @mention — customer notification prep → Important",
              mentions=["daniellewright"]),

            m("daniellewright", "I'll draft it immediately. Do we need to notify the DPA as well?",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Implicit", assignee=["amandafoster"],
              notes="Regulatory question during incident → Important"),

            m("amandafoster", "Potentially. Let's wait for James's access log analysis. If the 3 external IPs actually accessed customer data, we have a reportable incident. If they only accessed the bucket listing without customer data, we have more discretion. Either way, I'm starting the 72-hour clock from yesterday 6 PM when James discovered it.",
              is_important=True,
              notes="Legal guidance during incident — Important context"),

            m("davidpark", "What preventive measures should we implement immediately? I don't want a repeat.",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Question to the group about prevention → Important"),

            m("jameswilson", "I'm recommending: 1) Automated S3 policy scanning in CI/CD, 2) CloudTrail alerts for any public bucket creation, 3) Quarterly access review of all cloud storage. I'll implement 1 and 2 today.",
              notes="Recommendation + commitment — informational"),

            m("amandafoster", "Good. Everyone please treat this as confidential until we've completed the assessment and made notification decisions. No external communication until I clear it.",
              notes="Direction — guidance, not a specific task"),
        ],
    },

    # =========================================================================
    # CONV 35: Hackathon Planning (Fun/social + logistics)
    # Covers: Scheduling, RSVP, Action Request, Routine, Social
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Spring Hackathon Planning 🚀",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "ninacosta", "lisanakamura"],
        "messages": [
            m("alexkumar", "Hey team! I'm organizing the spring hackathon for the engineering team. Thinking April 18-19 (Friday-Saturday). Who's in? 🎉",
              has_task=True, sub_class="RfK", task_type="Availability/RSVP",
              attribution="Broadcast", assignee=[],
              notes="RSVP request to group"),

            m("priyasharma", "I'm in! Already have a project idea — AI-powered code review bot. 🤖",
              notes="Social / RSVP response — no task"),

            m("ninacosta", "Count me in. Can we invite the support team too? Derek has some great ideas for automating ticket triage.",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Permission request — expand scope?"),

            m("alexkumar", "Great idea — let's make it cross-functional. @Lisa, can you help with logistics? We'll need the large conference room for 2 days, snacks, and maybe dinner on Friday night.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Explicit", assignee=["lisanakamura"],
              notes="Action request via @mention — event logistics",
              mentions=["lisanakamura"]),

            m("lisanakamura", "Happy to help! I'll reserve the Cascade Room for both days and order catering. How many people are we expecting?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Logistics question"),

            m("alexkumar", "Probably 15-20 people if we open it up. Let's plan for 20 to be safe.",
              notes="Answer — informational"),

            m("priyasharma", "Should we have a theme this year or keep it open?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Broadcast", assignee=[],
              notes="Decision request to group"),

            m("alexkumar", "Let's keep it open but add a 'customer impact' bonus category — projects that could directly improve customer experience get extra points.",
              notes="Decision response — informational"),

            m("ninacosta", "Love it. I'll draft the registration form and share it by Friday. 📝",
              notes="Commitment"),

            m("lisanakamura", "Conference room is booked. Catering ordered for 20. 🍕🍔",
              notes="Completion report"),

            m("alexkumar", "You're the best Lisa! This is going to be fun. 🚀",
              notes="Social / praise — no task"),
        ],
    },

    # =========================================================================
    # CONV 36: New Hire Onboarding
    # Covers: Action Request, Question, Logistics, Routine
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "New Hire Onboarding — Starting April 7",
        "domain": "Human Resources",
        "members": ["daniellewright", "alexkumar", "lisanakamura"],
        "messages": [
            m("daniellewright", "Heads up — we have 2 new engineers starting on April 7. @Alex, can you prepare their onboarding plan, team assignments, and buddy pairings? @Lisa, please make sure their laptops, badges, and desk setups are ready.",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["alexkumar", "lisanakamura"],
              notes="Multi-assignee delegation via @mentions",
              mentions=["alexkumar", "lisanakamura"]),

            m("alexkumar", "I'll have the onboarding plan ready by April 3. Quick question — are both backend engineers, or is one the ML engineer?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["daniellewright"],
              notes="Clarifying question to Danielle"),

            m("daniellewright", "Both are backend engineers. The ML role is still in final rounds.",
              notes="Informational response"),

            m("lisanakamura", "Laptops are ordered and expected to arrive April 2. I'll have their desk area set up in the engineering section. Do they have any accessibility requirements?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["daniellewright"],
              notes="Question about accommodations"),

            m("daniellewright", "No specific accessibility needs flagged in their intake forms. Standard setup should be fine.",
              notes="Informational response"),

            m("alexkumar", "I'm thinking of pairing them with Priya and James as onboarding buddies. They'll cover both the codebase orientation and the DevOps workflow.",
              notes="Planning statement — informational"),

            m("daniellewright", "That sounds great. Please make sure they also complete the security awareness training in their first week — it's mandatory for SOC 2 compliance.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Action request — ensure training completion"),

            m("alexkumar", "Noted — I'll add it to the onboarding checklist.",
              notes="Acknowledgment"),

            m("lisanakamura", "All set on my end. Welcome kit, badge, parking pass, and desk setup will be ready by April 4.",
              notes="Commitment / status"),
        ],
    },

    # =========================================================================
    # CONV 37: Vendor Evaluation
    # Covers: Decision, Question, Action Request, Cross-functional
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Observability Vendor Evaluation — Datadog vs New Relic",
        "domain": "Engineering",
        "members": ["kevinzhang", "lisanakamura", "davidpark"],
        "messages": [
            m("davidpark", "Team, we need to finalize the observability vendor decision by end of month. I've narrowed it to Datadog and New Relic. Kevin, what are the cost comparisons?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["kevinzhang"],
              notes="Question directed at Kevin by name"),

            m("kevinzhang", "Datadog: $350K/year for enterprise plan. New Relic: $280K/year but with a more limited feature set. Datadog includes APM, log management, and infrastructure monitoring. New Relic's APM is included but log management is add-on at $60K.",
              notes="Informational — cost analysis"),

            m("davidpark", "So all-in, Datadog is $350K vs New Relic at $340K if we add logs. Not a significant price difference. @Lisa, did the vendor references check out?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Explicit", assignee=["lisanakamura"],
              notes="Question via @mention",
              mentions=["lisanakamura"]),

            m("lisanakamura", "I spoke with 3 references for each. Datadog got higher marks for reliability and support responsiveness. New Relic references mentioned occasional billing surprises with the consumption-based model.",
              notes="Informational — reference check results"),

            m("davidpark", "That's helpful. I'm leaning Datadog based on completeness and reliability. Kevin, can you prepare the final cost model with 3-year terms? I want to negotiate a multi-year discount.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              attribution="Implicit", assignee=["kevinzhang"],
              notes="Action request — financial modeling"),

            m("kevinzhang", "I'll have it ready by Wednesday. Should I model the 3-year TCO with a 15% discount assumption?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Clarifying question on parameters"),

            m("davidpark", "Model at 10%, 15%, and 20% so we have negotiating room. @Lisa, please schedule a final vendor call with Datadog for next week to discuss enterprise terms.",
              has_task=True, sub_class="RfA", task_type="Scheduling",
              attribution="Explicit", assignee=["lisanakamura"],
              notes="Scheduling action via @mention",
              mentions=["lisanakamura"]),

            m("lisanakamura", "I'll set it up for Tuesday or Wednesday. Any time preferences?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Scheduling follow-up question"),

            m("davidpark", "Morning works best. Before noon Pacific.",
              notes="Answer — informational"),

            m("kevinzhang", "Once the cost model is done, should I present it to Rachel too? She'll need to sign off if it's over $300K annual.",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["davidpark"],
              notes="Process question"),

            m("davidpark", "Yes, loop Rachel in. She'll want to see the ROI case too — reduced MTTR and developer productivity gains. I can help with that narrative.",
              notes="Direction — informational"),
        ],
    },

    # =========================================================================
    # CONV 38: Quarterly Planning (Leadership)
    # Covers: Decision, Delegation, Strategic, IsImportant
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Q2 OKR Planning — Leadership Alignment",
        "domain": "Executive",
        "members": ["sarahmitchell", "davidpark", "racheltorres", "michaelchen", "laurakim"],
        "messages": [
            m("sarahmitchell", "Team, I want to finalize Q2 OKRs by end of this week. Each of you should submit your department's top 3 objectives with measurable KRs. Let's target no more than 12 company-level OKRs.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Broadcast delegation to all leadership + strategic importance → Important"),

            m("davidpark", "Engineering objectives: 1) Ship v4.2 with AI features on time, 2) Reduce production incident MTTR by 40%, 3) Complete SOC 2 remediation. I'll have the KRs detailed by Thursday.",
              notes="Partial response + commitment"),

            m("michaelchen", "Sales: 1) Close $8M in new ARR, 2) Achieve 90%+ net retention, 3) Land 3 enterprise logos above $500K. I need to sync with Sofia on the pipeline actuals to finalize the KRs.",
              notes="Partial response + info"),

            m("racheltorres", "Finance: 1) Achieve quarterly operating margin of 15%, 2) Reduce SaaS tool spend by $200K, 3) Complete the audit with zero material findings.",
              notes="Complete response — informational"),

            m("laurakim", "Marketing: 1) Generate 150 MQLs from the spring campaign, 2) Increase organic search traffic by 30%, 3) Launch customer advocacy program with 5 reference customers.",
              notes="Complete response — informational"),

            m("sarahmitchell", "Good starting points. I see potential overlap between David's SOC 2 objective and Rachel's audit objective. Should we combine those into a single company-level OKR?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Broadcast", assignee=[],
              notes="Decision request to the group — organizational question"),

            m("racheltorres", "I'd recommend keeping them separate. The SOC 2 remediation is engineering-owned work. The audit is a finance/legal accountability. Different owners, different timelines.",
              notes="Input — informational"),

            m("davidpark", "Agree with Rachel. Different owners, but I'll coordinate with Kevin and Amanda to make sure the timelines are aligned.",
              notes="Agreement — informational"),

            m("sarahmitchell", "Fair point. Let's keep them separate. @Michael, your $8M target — is that consistent with the pipeline we reviewed last week? That felt aggressive given the Q1 shortfall.",
              has_task=True, sub_class="RfK", task_type="Question",
              is_important=True, attribution="Explicit", assignee=["michaelchen"],
              notes="Question via @mention + revenue context → Important",
              mentions=["michaelchen"]),

            m("michaelchen", "It's a stretch but achievable if Contoso closes and we accelerate 2-3 mid-market deals. I'd rather aim high and add hiring as a dependency. If we don't get the 2 AEs, I'd revise down to $6.5M.",
              notes="Assessment — informational"),

            m("sarahmitchell", "OK let's keep it at $8M with the AE hiring as a flagged dependency. Everyone — please send me your finalized OKR docs by Friday COB. I'll compile and share the draft company OKRs on Monday for a final review.",
              has_task=True, sub_class="RfA", task_type="Action Request",
              is_important=True, attribution="Broadcast", assignee=[],
              notes="Broadcast action request with deadline + strategic → Important"),

            m("davidpark", "Will do.",
              notes="Acknowledgment"),
            m("racheltorres", "Done — I already sent mine. 😄",
              notes="Acknowledgment — already completed"),
            m("michaelchen", "Friday works. I'll finalize with Sofia's numbers.",
              notes="Commitment"),
            m("laurakim", "Sending mine today.",
              notes="Commitment"),
        ],
    },

    # =========================================================================
    # CONV 39: Engineering Retrospective
    # Covers: Action Request, Question, Reflection, Edge Cases (rhetorical, suggestion)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Sprint 14 Retrospective Notes",
        "domain": "Engineering",
        "members": ["alexkumar", "priyasharma", "jameswilson", "ninacosta"],
        "messages": [
            m("alexkumar", "Retro notes from Sprint 14. Adding here for the record.\n\nWhat went well:\n- API v3 migration shipped on schedule\n- Connection pool fix handled well under pressure\n- Nina's regression suite caught the dashboard bug before release\n\nWhat needs improvement:\n- Bug ENG-2847 sat unassigned for 5 days (auto-assignment was broken)\n- Deployment validation needs gates\n- Postmortem action items from Sprint 12 still open",
              notes="Meeting notes — informational, no task"),

            m("alexkumar", "Action items from retro:\n1. @James — implement deployment validation gates in CI/CD by end of Sprint 15\n2. @Priya — add connection pool monitoring dashboard by next week\n3. @Nina — extend regression suite to cover multi-tenant scenarios",
              has_task=True, sub_class="RfA", task_type="Delegation",
              attribution="Explicit", assignee=["jameswilson", "priyasharma", "ninacosta"],
              notes="Multi-assignee delegation via @mentions",
              mentions=["jameswilson", "priyasharma", "ninacosta"]),

            m("jameswilson", "On the deployment gates — should this block all deploys, or just production? I'm thinking we should start with staging gates first.",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Decision question about scope"),

            m("alexkumar", "Start with production only. We can extend to staging later. Don't over-engineer it.",
              notes="Decision response — informational"),

            m("priyasharma", "For the monitoring dashboard — should I build on the existing Grafana setup or use the new Datadog instance once it's live?",
              has_task=True, sub_class="RfK", task_type="Decision Request",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Technical decision question"),

            m("alexkumar", "Use Grafana for now. Datadog decision isn't finalized yet. We can migrate later.",
              notes="Decision response — informational"),

            m("ninacosta", "Multi-tenant regression suite is going to be a bigger effort than expected. I'll need at least 2 weeks. Can I push to Sprint 16?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Implicit", assignee=["alexkumar"],
              notes="Permission request — timeline change"),

            m("alexkumar", "That's fine. Get it right rather than rushing it.",
              notes="Approval — informational"),

            m("priyasharma", "Also — shouldn't we do something about the postmortem action items from Sprint 12? Those have been open for 4 sprints now. 🤦",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Broadcast", assignee=[],
              notes="Question raising concern about stale actions",
              edge_case="follow_up_on_stale_items"),

            m("alexkumar", "Good call. I'll review them tomorrow and either close or reassign. If they've been open this long, some are probably no longer relevant.",
              notes="Commitment"),

            m("jameswilson", "Isn't that always the way with retro action items? 😅",
              notes="Rhetorical / humor — no task",
              edge_case="rhetorical_question"),

            m("ninacosta", "Harsh but fair 😂",
              notes="Social response — no task"),
        ],
    },

    # =========================================================================
    # CONV 40: Social/Casual Chat
    # Covers: Social/phatic, Availability, RSVP, No tasks (mostly),
    #         Edge cases (optional invitations, soft asks)
    # =========================================================================
    {
        "chat_type": "Group",
        "topic": "Team Social — Lunch & Weekend Plans",
        "domain": "Cross-functional",
        "members": ["priyasharma", "sofiarodriguez", "chrisevans", "ninacosta"],
        "messages": [
            m("priyasharma", "Who's up for lunch today? Thinking about trying that new Thai place on 3rd Street. 🍜",
              has_task=True, sub_class="RfK", task_type="Availability/RSVP",
              attribution="Broadcast", assignee=[],
              notes="RSVP request to the group"),

            m("sofiarodriguez", "I'm in! I've been wanting to try that place. What time?",
              has_task=True, sub_class="RfK", task_type="Question",
              attribution="Implicit", assignee=["priyasharma"],
              notes="RSVP + time question"),

            m("chrisevans", "Count me in. 12:30 work for everyone?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Broadcast", assignee=[],
              notes="Time confirmation request to group"),

            m("ninacosta", "I'm stuck in the regression suite today 😩 Going to have to grab something at my desk. Save me some pad thai! 🙏",
              notes="Social / declining invitation — no task"),

            m("priyasharma", "Aw, next time Nina! 12:30 works for me. Sofia?",
              has_task=True, sub_class="RfK", task_type="Confirmation/Permission",
              attribution="Implicit", assignee=["sofiarodriguez"],
              notes="Confirmation request directed at Sofia by name"),

            m("sofiarodriguez", "12:30 is perfect. See you all in the lobby!",
              notes="Confirmation — no task"),

            m("chrisevans", "Anyone doing anything fun this weekend? I'm thinking about checking out the new exhibit at the art museum.",
              notes="Social conversation — no task",
              edge_case="social_no_task"),

            m("priyasharma", "I'm doing a hiking trail in the Olympics. If anyone wants to join, feel free!",
              notes="Optional invitation — no task",
              edge_case="optional_invitation"),

            m("sofiarodriguez", "That sounds amazing! I might take you up on that. Let me check with my partner and get back to you.",
              notes="Social — non-committal response, no task"),

            m("ninacosta", "Jealous of all of you. I'll be debugging in my pajamas 😂",
              notes="Social / humor — no task"),

            m("chrisevans", "Happy Friday everyone! 🎉",
              notes="Social / phatic — no task"),
        ],
    },
]

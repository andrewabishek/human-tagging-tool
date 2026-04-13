"""
Conversation-Level Annotations for Golden Dataset

Maps all_conversations index -> conversation-level task classification.

RULE: conv_has_task = TRUE only when OUTSTANDING work extends BEYOND the thread.
If all questions/asks are answered/resolved within the thread, conv_has_task = FALSE.

task_evidence: 0-based message indices of messages that create the outstanding work
(requests that weren't fulfilled in-thread, commitments to do future work, etc.)
"""

CONV_ANNOTATIONS = {
    # =========================================================================
    # 1:1 Conversations (indices 0-14) — All TRUE
    # =========================================================================
    0: {  # Q2 Product Strategy & Board Prep
        "conv_has_task": True,
        "task_evidence": [4, 5, 6, 7, 8, 9],
        # Sarah's requests + David's commitments: 2-pager by Thursday,
        # strategic positioning, infrastructure targets
    },
    1: {  # Q2 Hiring Budget Approval
        "conv_has_task": True,
        "task_evidence": [5, 6],
        # Rachel must process 4 engineering headcount approvals today
    },
    2: {  # Production Incident — API Gateway Outage
        "conv_has_task": True,
        "task_evidence": [4, 5, 9, 10],
        # Exec status update + postmortem scheduling — outstanding work
    },
    3: {  # API v3 Migration — Code Review
        "conv_has_task": True,
        "task_evidence": [0, 3, 4],
        # PR review + k6 load tests — results due tomorrow morning
    },
    4: {  # Contoso Enterprise Deal — At Risk
        "conv_has_task": True,
        "task_evidence": [2, 3],
        # Engineer call, risk proposal, GDPR review — $2.4M deal at stake
    },
    5: {  # Q2 Org Restructuring — Confidential
        "conv_has_task": True,
        "task_evidence": [5, 6, 8, 9],
        # Restructuring proposal with timeline by next Friday + comms draft
    },
    6: {  # Spring Campaign — Content and Assets
        "conv_has_task": True,
        "task_evidence": [3, 4],
        # Reach out to Maria for metrics + Post 3 draft by Friday
    },
    7: {  # SOC 2 Audit Preparation
        "conv_has_task": True,
        "task_evidence": [2, 3, 5, 6, 8, 9],
        # Vendor payment docs, Q1 access review, audit checklist, dry run Friday
    },
    8: {  # Pinnacle Logistics — P1 Support Escalation
        "conv_has_task": True,
        "task_evidence": [5, 6],
        # Formal escalation summary within 1 hour for engineering escalation
    },
    9: {  # CDN Migration — Deployment Blocked
        "conv_has_task": True,
        "task_evidence": [0, 5, 6, 7, 8],
        # Fix config/run regression today + file SSL cert renewal
    },
    10: {  # Northwind Traders NDA Review
        "conv_has_task": True,
        "task_evidence": [0, 5, 6],
        # Review/redline NDA by Wednesday + send legal contact email
    },
    11: {  # Release Blocker — Dashboard Rendering Bug
        "conv_has_task": True,
        "task_evidence": [4, 5, 7, 8],
        # Fix in progress + visual regression test suite once pushed
    },
    12: {  # Office Equipment & Software Procurement
        "conv_has_task": True,
        "task_evidence": [2, 3, 5, 6, 7],
        # Vendor delivery confirmation, comparison spreadsheet, Figma contract
    },
    13: {  # Customer Testimonial — Pinnacle Logistics
        "conv_has_task": True,
        "task_evidence": [1, 2],
        # Reach out to Pinnacle by Wednesday for case study sign-off
    },
    14: {  # Engineering Platform Investment — Build vs Buy
        "conv_has_task": True,
        "task_evidence": [3, 4],
        # Build business case model with TCO by Monday
    },

    # =========================================================================
    # Group Conversations (indices 15-39)
    # =========================================================================
    15: {  # Engineering Daily Standup
        "conv_has_task": True,
        "task_evidence": [4, 5, 8, 10],
        # PR review before noon, staging build push, Jira updates — outstanding
    },
    16: {  # Q1 Pipeline Review & Forecast
        "conv_has_task": True,
        "task_evidence": [3, 4, 7, 8],
        # Daily check-ins + risk mitigation plan creation
    },
    17: {  # Meridian v4.2 Launch Coordination
        "conv_has_task": True,
        "task_evidence": [2, 4, 8, 9],
        # Feature screenshots, blog posts, readiness review — launch blocking
    },
    18: {  # Board Meeting Preparation
        "conv_has_task": True,
        "task_evidence": [3, 4, 5, 6, 11, 12],
        # Cost slide, AI demo, dry run coordination — board deadline
    },
    19: {  # Q2 Campaign Alignment
        "conv_has_task": True,
        "task_evidence": [2, 5, 6],
        # Updated messaging draft + webinar contingency plan
    },
    20: {  # 🚨 Production Incident Response
        "conv_has_task": True,
        "task_evidence": [13, 14],
        # Postmortem scheduling + exec summary — incident resolved but follow-up pending
    },
    21: {  # Q2 Headcount Planning
        "conv_has_task": True,
        "task_evidence": [3, 4],
        # Open positions, update job descriptions, finalize comp by end of April
    },
    22: {  # Northwind Traders Contract Review
        "conv_has_task": True,
        "task_evidence": [3, 4],
        # Legal counter-proposal + customer negotiation call
    },
    23: {  # Q1 Budget Review & Q2 Forecast
        "conv_has_task": True,
        "task_evidence": [2, 3],
        # Cost optimization analysis $500K target due next Friday
    },
    24: {  # Pinnacle Logistics Escalation
        "conv_has_task": True,
        "task_evidence": [0, 3, 4],
        # Engineering fix + urgent customer communication
    },
    25: {  # PR #852 Code Review
        "conv_has_task": False,
        "task_evidence": [],
        # All review feedback resolved in-thread: tests added, metrics fixed, approved
    },
    26: {  # Q1 All-Hands Planning
        "conv_has_task": True,
        "task_evidence": [1, 4, 7, 8],
        # Visual deck, video montage, catering — all with deadlines
    },
    27: {  # SOC 2 & GDPR Compliance
        "conv_has_task": True,
        "task_evidence": [6, 7],
        # April 15 audit — all teams must submit evidence packages by April 8
    },
    28: {  # Spring Campaign Creative Review
        "conv_has_task": True,
        "task_evidence": [6, 7],
        # Update all materials with approved tagline by Thursday
    },
    29: {  # Salesforce Down Workaround
        "conv_has_task": False,
        "task_evidence": [],
        # Outage + workaround fully managed in-thread; all actions immediate
    },
    30: {  # AI Resource Allocation Feature
        "conv_has_task": True,
        "task_evidence": [3, 4],
        # Prototype demo due end of week
    },
    31: {  # Marketing Weekly Sync Notes
        "conv_has_task": True,
        "task_evidence": [1, 2, 3],
        # Multiple action items with Wednesday-Thursday deadlines
    },
    32: {  # GlobalTech Churn Risk Escalation
        "conv_has_task": True,
        "task_evidence": [4, 5, 6, 7],
        # Recovery plan, contract review, ticket analysis — next-day regroup
    },
    33: {  # Data Privacy Incident
        "conv_has_task": True,
        "task_evidence": [4, 5, 6, 7],
        # Log analysis + customer notification drafting
    },
    34: {  # Spring Hackathon Planning
        "conv_has_task": True,
        "task_evidence": [7, 8],
        # Registration form draft must be shared by Friday
    },
    35: {  # New Hire Onboarding
        "conv_has_task": True,
        "task_evidence": [0, 3],
        # Onboarding plan + equipment setup before April 7 start
    },
    36: {  # Observability Vendor Evaluation
        "conv_has_task": True,
        "task_evidence": [4, 5, 6],
        # Cost models + vendor call scheduling
    },
    37: {  # Q2 OKR Planning
        "conv_has_task": True,
        "task_evidence": [0, 9, 10],
        # Finalized OKR documents due by Friday COB
    },
    38: {  # Sprint 14 Retrospective
        "conv_has_task": True,
        "task_evidence": [1, 5],
        # Deployment gates, monitoring, test suite — extend into future sprints
    },
    39: {  # Team Social — Lunch & Weekend Plans
        "conv_has_task": False,
        "task_evidence": [],
        # Purely social conversation — no business work
    },

    # =========================================================================
    # Meeting Conversations (indices 40-49) — All TRUE
    # =========================================================================
    40: {  # Sprint 15 Planning
        "conv_has_task": True,
        "task_evidence": [6, 7, 8],
        # Check test env timeline + send finalized sprint scope
    },
    41: {  # Q1 QBR — Sales & Revenue Review
        "conv_has_task": True,
        "task_evidence": [4, 5, 7, 8],
        # Draft competitive win-back plan + model mid-market pricing tier
    },
    42: {  # Board Deck Final Review — Dry Run
        "conv_has_task": True,
        "task_evidence": [1, 2, 3, 5, 6],
        # Simplify product slides by tomorrow + profitability appendix — board deadline
    },
    43: {  # Postmortem — API Gateway Incident
        "conv_has_task": True,
        "task_evidence": [4, 5],
        # 3 action items: stress test, PR checklist, escalation runbook — end of sprint
    },
    44: {  # H2 Product Strategy Offsite
        "conv_has_task": True,
        "task_evidence": [3, 4, 5],
        # AI technical roadmap + enterprise GTM strategy by end of month
    },
    45: {  # H1 Performance Calibration
        "conv_has_task": True,
        "task_evidence": [5, 6, 9, 10],
        # Document development feedback + finalize all ratings by Friday
    },
    46: {  # GlobalTech & Pinnacle Escalation Review
        "conv_has_task": True,
        "task_evidence": [3, 4, 5, 6],
        # Executive call with CTO + early warning system proposal
    },
    47: {  # Budget Committee — Q2 Spend Approvals
        "conv_has_task": True,
        "task_evidence": [2, 3, 9, 10],
        # Process POs + process all four POs by Thursday
    },
    48: {  # Engineering Weekly Standup
        "conv_has_task": True,
        "task_evidence": [1, 4, 5],
        # Sanitized data export + bug fixes ENG-2915/2916
    },
    49: {  # Q1 All-Hands Follow-up
        "conv_has_task": True,
        "task_evidence": [3, 4, 8, 9],
        # Remote policy share, international expansion post, quarterly town halls,
        # work-life balance feedback requiring David to address
    },

    # =========================================================================
    # Supplemental Conversations (indices 50-82)
    # =========================================================================
    50: {  # S1: Migration Follow-ups
        "conv_has_task": True,
        "task_evidence": [0, 2, 4, 6, 8, 10],
        # Multiple follow-up cycles: data analysis, Confluence link, latency benchmarks
    },
    51: {  # S2: Contoso Enterprise Agreement Review
        "conv_has_task": True,
        "task_evidence": [0, 2, 4, 6, 7],
        # Redline by Wednesday + EU data confirmation — legal review pending
    },
    52: {  # S3: Campaign Launch Coordination
        "conv_has_task": True,
        "task_evidence": [2, 4, 7, 8],
        # Blog draft by EOD + deck by Thursday EOD
    },
    53: {  # S4: Q2 Planning Edge Cases
        "conv_has_task": True,
        "task_evidence": [4, 5, 8, 9, 12, 13],
        # Feasibility assessment Friday + SLA update + QA checkpoint
    },
    54: {  # S5: Zenith Corp Escalation
        "conv_has_task": True,
        "task_evidence": [2, 4, 6, 7, 10, 11],
        # RCA investigation + VP outreach + hotfix + remediation negotiation
    },
    55: {  # S6: Employee Relations & Policy Updates
        "conv_has_task": True,
        "task_evidence": [1, 2, 6, 7],
        # HR investigation permission + Q1 attrition data by Thursday
    },
    56: {  # S7: Q2 Kickoff Planning
        "conv_has_task": False,
        "task_evidence": [],
        # Room booked, invite sent, all scheduling resolved in-thread
    },
    57: {  # S8: Security Incident Review
        "conv_has_task": True,
        "task_evidence": [0, 4, 5, 6, 8, 9, 11],
        # Incident report by EOW + WAF analysis + security unification + board briefing
    },
    58: {  # S9: Q1 Close & Audit Prep
        "conv_has_task": True,
        "task_evidence": [0, 2, 4, 6],
        # Reconciliation accelerated + UK follow-up + variance analysis memo
    },
    59: {  # S10: Meridian Analytics Pro Launch Go/No-Go
        "conv_has_task": True,
        "task_evidence": [7, 12, 13],
        # Vertex confirmation by EOW + GDPR DPA on product page by Friday
    },
    60: {  # S11: Dev Tooling Frustrations
        "conv_has_task": True,
        "task_evidence": [0, 2, 4, 7, 8],
        # CI pipeline escalation + staging infrastructure ticket
    },
    61: {  # S12: Product Roadmap Alignment
        "conv_has_task": True,
        "task_evidence": [4, 5, 7, 8],
        # Vet 3 agencies + share contact + include Sofia in eval
    },
    62: {  # S13: All-Hands Q&A
        "conv_has_task": True,
        "task_evidence": [11, 12],
        # Dev environment access setup before Monday
    },
    63: {  # S14: Deal Pipeline & Forecast Review
        "conv_has_task": True,
        "task_evidence": [0, 3, 4, 6, 7, 8],
        # Forecast by 9 AM + RFP review + payment term negotiation
    },
    64: {  # S15: Friday Vibes & Housekeeping
        "conv_has_task": True,
        "task_evidence": [6, 7, 8, 10, 11],
        # NPS dashboard verification + metric fixes + sprint planning prep
    },
    65: {  # S16: Q1 Sales QBR
        "conv_has_task": True,
        "task_evidence": [6, 7, 11, 12],
        # Pull-in forecast by Thursday + discount approval streamlining by month-end
    },
    66: {  # S17: At-Risk Account Reviews
        "conv_has_task": True,
        "task_evidence": [0, 3, 4, 8, 9],
        # GreenTech budget convo + NovaCorp IT VP escalation
    },
    67: {  # S18: Office Move Planning
        "conv_has_task": True,
        "task_evidence": [0, 5, 6, 7, 8],
        # Space requirements + legal clause review + customer comms by Wednesday
    },
    68: {  # S19: Quick Ask
        "conv_has_task": False,
        "task_evidence": [],
        # SSH key provided, question fully answered in-thread
    },
    69: {  # S20: Meeting Room
        "conv_has_task": False,
        "task_evidence": [],
        # Room availability checked, time negotiated, booking confirmed
    },
    70: {  # S21: PRODUCTION DOWN
        "conv_has_task": True,
        "task_evidence": [4, 5, 10, 11],
        # Incident timeline doc + postmortem by tomorrow
    },
    71: {  # S22: Blog Post Review & Approval
        "conv_has_task": True,
        "task_evidence": [1, 2, 3, 6, 7],
        # Blog revisions by tomorrow morning + image brand guidelines check
    },
    72: {  # S23: Vendor Selection for Analytics Platform
        "conv_has_task": True,
        "task_evidence": [0, 5, 6],
        # Evaluate vendors + set up review meeting
    },
    73: {  # S24: Sprint Retrospective
        "conv_has_task": True,
        "task_evidence": [6, 7, 8, 9, 12, 13],
        # Document scope change impact + staging infrastructure proposal + vote
    },
    74: {  # S25: Quick Legal Questions
        "conv_has_task": True,
        "task_evidence": [1, 2, 3, 4],
        # Review top 10 customer contracts by EOW + privacy policy changes list
    },
    75: {  # S26: Design Review Feedback
        "conv_has_task": True,
        "task_evidence": [0, 3, 4, 5],
        # Design mockup revisions + metrics section + pricing visibility
    },
    76: {  # S27: Q2 Budget Review Meeting
        "conv_has_task": True,
        "task_evidence": [9, 12],
        # Rachel updates budget allocations + Kevin distributes by EOD
    },
    77: {  # S28: System Notifications Discussion
        "conv_has_task": True,
        "task_evidence": [0, 2, 3, 4],
        # Send filter steps + fix webhook duplicates + notify when complete
    },
    78: {  # S29: Engineering Standup Thread
        "conv_has_task": True,
        "task_evidence": [7, 8, 9, 10],
        # Test credentials refresh + coordination directive
    },
    79: {  # S30: Casual Check-in with CTO
        "conv_has_task": False,
        "task_evidence": [],
        # FYI discussion only — David offers "when things calm down", no firm commitment
    },
    80: {  # S31: Data Export & Call Scheduling
        "conv_has_task": True,
        "task_evidence": [2, 3, 4],
        # James scheduled call with Priya + data export coordination
    },
    81: {  # S32: Sprint 48 Pre-Launch Tasks
        "conv_has_task": True,
        "task_evidence": [0, 2, 5, 6, 7],
        # LT preview deadline + sign-off blocker + security approval
    },
    82: {  # S33: EOQ Cleanup Tasks
        "conv_has_task": True,
        "task_evidence": [0, 3, 4],
        # 3/31 hard deadline for cleanups + DNS provider escalation
    },
}

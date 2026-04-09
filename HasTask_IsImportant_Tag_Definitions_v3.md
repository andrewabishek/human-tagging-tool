# HasTask & IsImportant — Message Tag Definition Spec

**Version:** 3.0 (Holistic)
**Date:** March 27, 2026
**Owner:** Andrew Abishek (PM — Teams AI Chats & Channels)
**Audience:** Data Science & ML Engineering
**Purpose:** Define crisp, machine-actionable classification rules for `HasTask` and `IsImportant` message tags across **all workplace domains** — not just engineering. Includes exhaustive examples, edge cases, attribution rules, known technical constraints, and alignment with the RfA / RfK / Commitment classifier taxonomy.

---

## 1. Overview & Principles

Teams messages today lack machine-readable signals for task intent and importance. BizChat must guess from raw text for every query, resulting in 41–67% SAT on task/triage queries. This spec defines two offline tags — **HasTask** and **IsImportant** — to be stamped on messages so Copilot can **filter and rank** instead of guessing.

| Principle | Detail |
|---|---|
| **HasTask** | Message expects a response or action from someone — explicitly or implicitly. Boolean. Subdivides into Request-for-Action (RfA) and Request-for-Knowledge (RfK). |
| **IsImportant** | Message has high urgency or organizational impact. Two sub-types: *Objective* (content-driven) and *User-Specific* (targeting-driven). Boolean. |
| **Independent tags** | A message can be any combination of HasTask and IsImportant (see Section 7). |
| **Attribution** | HasTask messages must carry an assignee signal: explicit, implicit, or unassigned (see Section 5). |
| **Domain-agnostic** | These definitions apply across all workplace functions — engineering, sales, HR, legal, finance, marketing, operations, executive, customer support, and more. |
| **Context** | Some classifications require ±3 surrounding messages. Called out per scenario. |
| **Limitations acknowledged** | Technical constraints (batch latency, staleness, completion state) are flagged as open items, not solved here. |

---

## 2. HasTask — Core Definition

### 2.1 Definition

`hasTask = TRUE` when a message contains an **explicit or implicit request for action, response, or decision** from one or more recipients. This includes both:
- **Requests for Action (RfA):** Asks the recipient to produce a deliverable artifact or perform a verifiable operational step.
- **Requests for Knowledge (RfK):** Asks the recipient for information, opinion, confirmation, permission, availability, or acknowledgment — answerable without producing a new artifact.

`hasTask = FALSE` when a message is:
- Purely informational with no response expected (status updates, FYIs, announcements)
- Social/phatic (greetings, pleasantries, GIFs)
- A **Commitment** by the sender (sender promises their own action — "I'll handle it")
- An acknowledgment that resolves a prior ask ("Got it", "Thanks", "LGTM")
- A completed-action report ("Done", "PR merged", "Invoice submitted")

### 2.2 Sub-Classification: RfA vs. RfK vs. Commitment

The DS team's classifiers use three categories under "intent." Here's how they map to HasTask:

| Category | HasTask | Definition | Copilot Treatment |
|---|---|---|---|
| **Request for Action (RfA)** | **TRUE** | Assigns recipient a specific, discrete, checkable task that produces a concrete deliverable or verifiable operational step | Task list — trackable, completable |
| **Request for Knowledge (RfK)** | **TRUE** | Asks recipient for information, opinion, confirmation, permission, availability, or acknowledgment — answerable without producing an artifact | Surface as "needs your response" — not a to-do but still requires attention |
| **Commitment** | **FALSE** | Sender promises their own future action ("I'll send the deck by EOD") | Do not surface as task for recipient. May surface under "What's coming your way" if recipient is the beneficiary. |
| **Neither** | **FALSE** | Status, social, acknowledgment, completed action, FYI | Do not surface |

**Why this matters:** RfA and RfK both require recipient attention, but of different kinds. "Can you send the contract?" (RfA) goes on a to-do list. "Are you available for a call at 3?" (RfK) needs a quick reply but isn't a to-do. Both are `HasTask = TRUE`.

### 2.3 Task Type Taxonomy (for classifier training)

| Task Type | Sub-class | Description | Signal Keywords | Cross-Domain Examples |
|---|---|---|---|---|
| **Action Request** | RfA | Asks recipient to perform/create/deliver something | "can you", "please", "would you", "need you to" | _Eng:_ "Can you deploy the hotfix?" · _Sales:_ "Please send the updated proposal to Acme" · _HR:_ "Please submit your self-review by March 15" · _Legal:_ "Please redline the NDA before sending to the vendor" |
| **Review / Approval** | RfA | Requests feedback, sign-off, or approval on an artifact | "please review", "can you approve", "sign off on", "thoughts on" | _Eng:_ "Please review the PR" · _Finance:_ "Can you approve the PO for $50K?" · _Marketing:_ "Please sign off on the campaign creative" · _Legal:_ "Need your approval on the partnership terms" |
| **Scheduling Action** | RfA | Asks recipient to create/send/modify a calendar event | "book the room", "send the invite", "reschedule" | _Admin:_ "Can you book the conf room for Thursday?" · _Sales:_ "Please send a demo invite to the client" · _Ops:_ "Reschedule the vendor call to next week" |
| **Delegation** | RfA | Assigns multi-step work to someone | Name + action verb(s), deliverables | _Eng:_ "Nikhil, make minor tweaks and post for review" · _Marketing:_ "Sara, draft the press release and loop in comms" · _Exec:_ "VP team — prepare board deck sections by Thursday" |
| **Question** | RfK | Seeks information or clarification | "?", "how", "what", "when", "do you know" | _Eng:_ "What's the ETA on the fix?" · _Sales:_ "What's our discount ceiling for enterprise deals?" · _Finance:_ "What's the remaining budget for Q4?" · _HR:_ "What's the policy on parental leave?" |
| **Confirmation / Permission** | RfK | Asks for a yes/no or approval to proceed | "can I", "is it ok if", "does this work", "may I" | _Legal:_ "May I share the draft externally?" · _Eng:_ "Is it ok to merge without staging?" · _Marketing:_ "Can I publish the blog post today?" |
| **Availability / RSVP** | RfK | Asks if someone can attend or is free | "are you available", "can you join", "will you attend" | _All:_ "Are you free for a quick sync at 3?" · _Sales:_ "Can you join the client call tomorrow?" · _HR:_ "Will you be at the off-site next week?" |
| **Status Request** | RfK | Asks for an update or progress report | "status on", "where are we", "ETA", "any update" | _Eng:_ "Where are we on the migration?" · _Sales:_ "Any update on the Contoso deal?" · _Finance:_ "Status on the audit prep?" · _Ops:_ "ETA on new laptop delivery?" |
| **Decision Request** | RfK | Asks for a decision or choice | "should we", "do you want to", "which option" | _Exec:_ "Should we greenlight the acquisition?" · _Marketing:_ "Which tagline do we go with?" · _Eng:_ "Go/no-go for R0?" |
| **Follow-up** | RfA or RfK | Re-surfaces a prior unresolved ask | "following up", "still waiting", "any progress on" | _All:_ "Following up on the contract — still waiting on legal sign-off" · "Any progress on the headcount request?" |

---

## 3. HasTask — Classification & Examples

### 3.1 Classification Table

| Signal | HasTask | Sub-class | Context Needed | Example |
|---|---|---|---|---|
| Direct request to named person / @mention to do something | **TRUE** | RfA | Message only | "@Sara, please send the client proposal by Friday" |
| Question that requires information | **TRUE** | RfK | Message only | "What's our headcount budget for next quarter?" |
| Ask for review, approval, or sign-off | **TRUE** | RfA | Message only | "Can you approve the vendor contract?" |
| Permission request | **TRUE** | RfK | Message only | "May I share the draft NDA with outside counsel?" |
| Availability / RSVP request | **TRUE** | RfK | Message only | "Are you available for the client call at 2 PM?" |
| Confirmation request | **TRUE** | RfK | Message only | "Does the March 30 deadline still hold?" |
| Reminder with a deadline | **TRUE** | RfA | Message only | "Expense reports due by month-end — please submit yours" |
| Follow-up on a prior unresolved ask | **TRUE** | RfA/RfK | ±3 messages | "Hi Priya, any update on the legal review?" |
| Scheduling action assigned to recipient | **TRUE** | RfA | Message only | "Can you book the boardroom for the exec review?" |
| Broadcast ask with no specific assignee | **TRUE** | RfA/RfK | Message only | "Can someone update the customer escalation tracker?" |
| Acknowledgment (Thanks / OK / Will do) | **FALSE** | — | ±2 messages | "Sure thing" / "Thanks Andrew" / "Got it" |
| Commitment by sender ("I'll handle it") | **FALSE** | Commitment | Message only | "I'll send the updated forecast by EOD" |
| Status update (no ask) | **FALSE** | — | Message only | "The contract is signed and filed" |
| FYI / informational share | **FALSE** | — | Message only | "FYI: New travel policy effective April 1" |
| Social / phatic | **FALSE** | — | Message only | "Safe travels!" / "Happy birthday!" / GIFs |
| Bot-generated content | **FALSE** | — | Message only | Meeting notes, agenda confirmations, auto-reminders |
| Optional/permission-based ("feel free to") | **FALSE** | — | Message only | "Feel free to review if you have time" |
| Sender's own plan / status | **FALSE** | Commitment | Message only | "I'm heading to the client site tomorrow" |
| First-person plural without assignee ("let's think about") | **FALSE** | — | Message only | "Let's revisit this next quarter" |

### 3.2 Exhaustive Scenario Examples — HasTask = TRUE

#### Engineering & IT

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 1 | "@Priya, can you please point me to the latest video for the demo?" | RfK | Explicit question + @mention |
| 2 | "@Gaurav, @Nikhil, please review the Status Update doc. Planning to send it today EOD." | RfA | Review request + named recipients + deadline |
| 3 | "Please note these cleanups need to be completed and experiments stopped before 3/31." | RfA | Hard deadline + explicit deliverable |
| 4 | "@Ashish please test these out and share tracking work items for these" | RfA | @mention + 2 specific deliverables |
| 5 | "What's the ETA on the hotfix for the login issue?" | RfK | Status/timeline question |
| 6 | "Is it ok to merge this PR without staging validation?" | RfK | Permission request |

#### Sales & Business Development

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 7 | "Please send the updated proposal to the Contoso team by Friday — they're expecting it for their internal review." | RfA | Named deliverable + deadline + external stakeholder |
| 8 | "@David, can you schedule a demo for the Northwind account? They want to see the new analytics dashboard." | RfA | Scheduling action + specific deliverable |
| 9 | "What's our discount ceiling for enterprise deals over $500K?" | RfK | Knowledge request — needs a factual answer |
| 10 | "Any update on the Contoso renewal? Are they leaning toward the 3-year or 1-year?" | RfK | Status + decision question |
| 11 | "Can you pull the pipeline report and share it before the QBR on Monday?" | RfA | Artifact (report) + deadline |
| 12 | "Please update the CRM with the latest touchpoints from the Fabrikam meeting." | RfA | Operational step — CRM update |

#### HR & People Operations

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 13 | "Please submit your self-review by March 15 — it's required before calibration." | RfA | Deliverable + deadline + consequence |
| 14 | "Can you approve the headcount request for the new data analyst role?" | RfA | Approval action |
| 15 | "What's the company policy on remote work for contractors?" | RfK | Knowledge request |
| 16 | "Will you be attending the off-site next week? We need a final headcount by Thursday." | RfK | RSVP/availability + deadline |
| 17 | "@Recruiter, please send the offer letter to the candidate by EOD — they have a competing offer." | RfA | Deliverable + urgency + deadline |
| 18 | "Has the background check for Candidate X cleared yet?" | RfK | Status question |

#### Legal & Compliance

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 19 | "Please review and redline the NDA before we send it to the vendor — target is end of week." | RfA | Review + deliverable + deadline |
| 20 | "Can you confirm whether our data retention policy covers third-party subprocessors?" | RfK | Knowledge/clarification |
| 21 | "We need legal sign-off on the partnership terms before the board meeting on April 3." | RfA | Approval + hard deadline |
| 22 | "Is there any IP risk with using this open-source library in our product?" | RfK | Risk assessment question |
| 23 | "Please file the trademark application for the new product name by end of quarter." | RfA | Filing action + deadline |

#### Finance & Procurement

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 24 | "Please submit your expense reports by March 31 — late submissions will be pushed to next cycle." | RfA | Deliverable + deadline + consequence |
| 25 | "Can you approve the PO for $50K for the new design tooling?" | RfA | Approval action |
| 26 | "What's the remaining budget for the AI initiatives in Q4?" | RfK | Knowledge request |
| 27 | "@Finance, please process the vendor invoice — it's been outstanding for 45 days." | RfA | Operational step (payment processing) |
| 28 | "Should we capitalize or expense the new server hardware?" | RfK | Decision/classification question |
| 29 | "Please share the updated forecast model with the leadership team before the monthly review." | RfA | Deliverable (model) + audience + deadline |

#### Marketing & Communications

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 30 | "Please finalize the blog post draft and send it to editorial by Thursday." | RfA | Deliverable + deadline |
| 31 | "Can you update the launch messaging doc with the new positioning from yesterday's workshop?" | RfA | Update action on specific artifact |
| 32 | "Which tagline do we go with — option A or option B?" | RfK | Decision request |
| 33 | "@Design team, we need the social media assets for the campaign by next Monday." | RfA | Deliverable + deadline + named team |
| 34 | "What's our current brand guideline on using customer logos in case studies?" | RfK | Knowledge/policy question |
| 35 | "Please get approval from the customer before we publish their testimonial." | RfA | Approval action (external) |

#### Executive & Leadership

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 36 | "VP team — please prepare your board deck sections by Thursday." | RfA | Deliverable + deadline + named audience |
| 37 | "Should we greenlight the acquisition, or do we need another round of diligence?" | RfK | Decision request |
| 38 | "Can you give me a 2-minute summary of the competitive landscape for the all-hands?" | RfK | Knowledge request (brief) |
| 39 | "Please schedule a 1:1 with the new CHRO — I'd like to meet them this week." | RfA | Scheduling action |
| 40 | "Need your input on the strategic priorities before I present to the board." | RfK | Opinion/input request |

#### Customer Support & Success

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 41 | "Can you escalate this ticket to engineering? The customer has been waiting 3 days." | RfA | Escalation action + urgency |
| 42 | "Please follow up with the customer on their refund request — they're threatening to churn." | RfA | Follow-up action + consequence |
| 43 | "What's the current SLA for P1 tickets?" | RfK | Knowledge/policy question |
| 44 | "Is there a workaround for the login issue customers are reporting?" | RfK | Knowledge/solution question |
| 45 | "Please update the KB article with the new troubleshooting steps." | RfA | Artifact update |

#### Operations & Facilities

| # | Message | Sub-class | Why TRUE |
|---|---|---|---|
| 46 | "Can you book the large conference room for the all-hands on Friday?" | RfA | Scheduling/booking action |
| 47 | "Please order catering for 40 people for the team event next Thursday." | RfA | Procurement action |
| 48 | "What's the status on the new office build-out? Are we still on track for June move-in?" | RfK | Status question |
| 49 | "Can you arrange visitor badges for the client delegation arriving Monday?" | RfA | Operational step |
| 50 | "Please renew the software licenses before they expire on April 15." | RfA | Operational step + deadline |

### 3.3 Exhaustive Scenario Examples — HasTask = FALSE

| # | Message | Category | Why FALSE | Domain |
|---|---|---|---|---|
| 1 | "Thanks for the update!" / "Got it" / "Sure thing" | Acknowledgment | No new action expected | All |
| 2 | "I'm unwell since last night. Will be OOF today/tomorrow." | Status / FYI | Sender's own status, no ask | All |
| 3 | "I'll send the updated forecast by EOD." | Commitment | Sender promises their own action | Finance |
| 4 | "The contract is signed and filed in SharePoint." | Completed action | Past tense — already done | Legal |
| 5 | "FYI: New travel policy effective April 1." | FYI | Informational, no ask | HR |
| 6 | "The board meeting has been moved to April 10." | Announcement | Informational update | Executive |
| 7 | "Safe travels!" / "Happy birthday!" / "Congrats on the promotion!" | Social / phatic | No work action | All |
| 8 | GIFs, memes, emoji-only messages (📷, 🎉) | Media / social | No parseable content | All |
| 9 | "Let me know if you have any questions." | Courtesy offer | Open-ended, no specific ask | All |
| 10 | "Feel free to review the deck when you get a chance." | Optional/soft | No directive; optional language | All |
| 11 | "We should think about expanding into APAC next year." | Planning/aspiration | No assignee, no deliverable, no deadline | Executive |
| 12 | "I'll be in the London office next week." | Travel/status | Sender's plan, informational | All |
| 13 | "The team shipped the feature on time — great work everyone!" | Praise/recognition | No action requested | All |
| 14 | "Our NPS score improved by 12 points this quarter." | Metric update | Informational, no ask | Cust. Support |
| 15 | "Let's revisit the pricing strategy next quarter." | Deferred proposal | Vague timeline, no assignee, no deliverable | Sales |
| 16 | "AI Facilitator: Here are the meeting notes..." | Bot-generated | Not human-authored | All |
| 17 | "Looks great" / "LGTM" / "Approved" | Approval resolution | No new task; resolves a prior ask | All |
| 18 | "I'll handle the client escalation — don't worry about it." | Sender self-assignment | Commitment by sender, no ask | Support |
| 19 | "The vendor confirmed delivery for next Wednesday." | Third-party update | Informational about someone else's action | Procurement |
| 20 | "Reach out to IT support if you run into issues." | Courtesy/contact | Generic escalation offer, not a task | All |

### 3.4 Edge Cases & Decision Rules

| Edge Case | Tag | Sub-class | Rationale |
|---|---|---|---|
| **"Let's connect on X sometime"** (vague) | **FALSE** | — | Too vague — no deliverable, no deadline. Follow-up "Does 2 PM work?" IS TRUE. |
| **"Will do" / "Sure, I'll handle it"** | **FALSE** | Commitment | Acknowledgment/acceptance of a prior task, not a new task for recipient. |
| **"FYI: @Nikhil, @Andrew — I don't see you listed as DRIs"** | **TRUE** (borderline) | RfK | Directed at specific people with a gap to address. Lean TRUE when FYI is targeted with a problem. |
| **Multi-part message with task buried in narrative** | **TRUE** | RfA | Long summary ending with "AI on @Enrique: please test these out." Named action item = TRUE. |
| **"I will cancel mine!"** (self-directed) | **FALSE** | Commitment | Sender's own action, not asking others. |
| **Image-only messages (📷)** | **FALSE** | — | Cannot determine intent without multimodal analysis. |
| **Message with both status + ask** | **TRUE** | Varies | "Contract is signed. Can you now file the IP registration?" — ask wins. |
| **Rhetorical question** ("Isn't that great?") | **FALSE** | — | No action expected. Short question + positive sentiment + no @mention → rhetorical. |
| **Conditional ask** ("If you have time, can you…") | **TRUE** | RfA | Still an ask — "if" softens urgency, not existence. |
| **Sarcasm** ("Great job breaking the build 🙂") | **FALSE** | — | Sarcasm detection is P2+. Default FALSE unless paired with explicit escalation. |
| **Message with deadline already passed** | **TRUE** | RfA | Task exists even if stale. Downstream ranking handles staleness. |
| **"Please update weekly"** (recurring ask) | **TRUE** | RfA | Tag original ask as TRUE. Recurring sub-tasks are P2. |
| **"Feel free to review if you get a chance"** | **FALSE** | — | Optional/permissive language — no directive. |
| **"Can you review my PR today?" vs. "Do you have bandwidth to review my PR?"** | TRUE (RfA) vs. TRUE (RfK) | RfA / RfK | First assigns the task; second checks capacity. Both are HasTask=TRUE but different sub-types. |
| **"Let me know if you have questions"** | **FALSE** | — | Courtesy offer, not a specific ask. |
| **"Should we loop Legal into the kick-off?"** | **TRUE** | RfK | Seeks a decision from recipient. First-person plural but requests a decision. |
| **"Loop Legal into the kick-off"** | **TRUE** | RfA | Direct imperative assigning an action. |
| **"I'll let you know how the platform works"** | **FALSE** | Commitment | Sender's commitment, not a task for recipient. |
| **"Reach out to IT if you need help"** | **FALSE** | — | Generic offer/escalation path, not a task. |
| **Event invitation ("Join us for the hackathon!")** | **FALSE** | — | Promotional/optional invitation, not a mandated task. |
| **"Please RSVP by Friday" (event)** | **TRUE** | RfK | Mandated RSVP with a deadline → asks for commitment from recipient. |

---

## 4. IsImportant

### 4.1 Definition

`isImportant = TRUE` when a message carries **high urgency, high organizational impact, or escalation risk** — independent of whether it contains a task. Two sub-types:

**4.1.1 Objectively Important (content-driven)**
Important regardless of who reads it. The content itself signals urgency or impact.

**4.1.2 Important to Specific User (targeting-driven)**
Important to a particular person due to how they are referenced or involved. Per-user relevance signal, not a content signal.

### 4.2 Objective Importance — Classification Table

| Signal | IsImportant | Cross-Domain Examples |
|---|---|---|
| Sev / incident / outage / service degradation | **TRUE** | _Eng:_ "DDOS resumed, WAF rule deployed" · _Ops:_ "Building fire alarm — evacuate floor 3" · _Support:_ "Major outage impacting 50K users" |
| Blocker or dependency on another team | **TRUE** | _Eng:_ "Cannot proceed until infra team resolves snapshot" · _Sales:_ "Deal blocked on legal review — client deadline is Friday" · _Marketing:_ "Launch blocked on product team's feature delay" |
| Hard deadline with business consequence | **TRUE** | _All:_ "Need sign-off by EOD or we miss ship window" · _Finance:_ "Tax filing deadline March 31" · _Legal:_ "Regulatory response due in 48 hours" · _HR:_ "Offer expires tomorrow — candidate has competing offer" |
| Quality gate / compliance failure | **TRUE** | _Eng:_ "Quality at 56% vs 80% target — P0s must be addressed" · _Finance:_ "Audit finding — material weakness identified" · _Legal:_ "GDPR breach detected — 72-hour notification window" |
| Escalation or leadership-visible issue | **TRUE** | _All:_ "This item tagged at SLT level" · _Sales:_ "CRO escalated — Acme threatening to churn" · _Support:_ "VP flagged — strategic customer impacted" |
| Explicit urgency marker | **TRUE** | _All:_ "ASAP" / "by EOD" / "urgent" / "blocking" / "critical" |
| Timeline slip or risk callout | **TRUE** | _Eng:_ "June launch not feasible" · _Marketing:_ "Campaign launch delayed 2 weeks — impacts revenue forecast" · _Ops:_ "Office build-out behind schedule — June move-in at risk" |
| Approval needed for gated process | **TRUE** | _Eng:_ "Need LB approval to advance rollout" · _Finance:_ "Board approval needed for $2M spend" · _HR:_ "VP sign-off required for reorg" |
| System/tool breakage affecting productivity | **TRUE** | _Eng:_ "SEVAL results broken" · _All:_ "Salesforce is down" · _Finance:_ "ERP system outage — invoicing frozen" |
| Policy change affecting many | **TRUE** | _HR:_ "Effective immediately: new PTO policy" · _Legal:_ "Updated export control rules — all deals need re-screening" · _IT:_ "MFA enforcement starting Monday" |
| Revenue/customer impact | **TRUE** | _Sales:_ "Lost $2M deal — need postmortem" · _Support:_ "Top 10 customer threatening churn" · _Finance:_ "Q3 revenue miss — $5M below forecast" |
| Security / data breach | **TRUE** | _All:_ "Unauthorized access detected in production" · _Legal:_ "Customer data exposed — incident response activated" |
| Routine scheduling | **FALSE** | "Can we meet at 2 PM?" |
| Standard status update | **FALSE** | "Weekly update posted" / "Sharing deck for tomorrow" |
| Social / greeting / GIF | **FALSE** | "Safe travels!" / "Happy Friday!" |
| Routine meeting logistics | **FALSE** | "Please accept the revised invite" |
| Acknowledgments | **FALSE** | "Thanks!" / "Got it" / "Sounds good" |
| Non-blocking FYIs | **FALSE** | "I'll be in office tomorrow" / "WFH today" |
| Routine operational updates | **FALSE** | "New printer installed on floor 4" / "Cafeteria menu updated" |
| Standard reminders without consequence | **FALSE** | "Gentle reminder to check in on your goals" |

### 4.3 User-Specific Importance — Relevance Signals

Per-user signals layered on top of objective importance. Answer: "is this important *to me*?"

| Signal | Source | Example | Attribution Tier |
|---|---|---|---|
| @Mentioned in the message | Message metadata | "@Andrew can you review this?" | EXPLICIT |
| Name referenced in content (no @) | Content parsing | "Andrew, I need your feedback" | IMPLICIT |
| Direct reply to user's message | Thread structure | User asked a question; this is the reply | IMPLICIT |
| Message from user's manager or skip-level | Org metadata | Message from user's direct manager | METADATA |
| User previously engaged in thread | Thread participation | User commented/reacted earlier | CONTEXT |
| User follows the channel + message is unread | User settings | User followed "Sales Pipeline" channel | METADATA |
| User is DRI / owner of the topic | Role metadata | User owns the product area being discussed | METADATA |

**Note:** User-specific importance is computed at query time (when we know *who* is asking Copilot), not at stamp time. The offline stamp captures objective importance + attribution signals. Copilot combines them at retrieval.

### 4.4 Exhaustive Scenario Examples — IsImportant = TRUE (Objective)

| # | Message | Domain | Why Important |
|---|---|---|---|
| 1 | "Quality currently stands at 56% assertion rate (vs 80% in prod). P0s must be addressed." | Engineering | Quality gate failure; ship-blocking |
| 2 | "We cannot proceed with 5.3C in its current unoptimized form." | Engineering | Cross-team blocker |
| 3 | "The Contoso deal is at risk — their legal team flagged data residency concerns. If we don't respond by Friday, the $3M deal falls through." | Sales | Revenue risk + hard deadline |
| 4 | "GDPR breach notification — customer data may have been exposed. We have a 72-hour window to notify regulators." | Legal / Compliance | Regulatory deadline + data breach |
| 5 | "Audit finding: material weakness in revenue recognition controls. We need to remediate before the next earnings filing." | Finance | Compliance/material weakness |
| 6 | "Candidate has a competing offer expiring tomorrow. If we don't extend by EOD, we lose them." | HR | Hiring urgency + hard deadline |
| 7 | "Campaign launch delayed 2 weeks due to product feature slip. Impacts Q2 revenue forecast by $1.2M." | Marketing | Revenue impact + schedule risk |
| 8 | "CRO escalated — Acme Corp (our largest customer) is threatening to churn over the unresolved support issue." | Customer Success | Executive escalation + churn risk |
| 9 | "Office build-out behind schedule. June move-in at risk — we may need to extend the lease on the current space." | Operations | Operational risk + financial impact |
| 10 | "Salesforce has been down for 3 hours. Pipeline tracking and forecasting are frozen." | IT / Sales | Tool outage affecting business process |
| 11 | "The board meeting is in 2 days and we're still missing 3 of 6 deck sections." | Executive | Leadership-visible deadline |
| 12 | "Unauthorized access detected in production environment. Incident response team activated." | Security | Active security incident |
| 13 | "FYI folks, SEVAL results broken." | Engineering | Tool breakage affecting team velocity |
| 14 | "This item is tagged at SLT level with 200+ days of inactivity. Hence the sense of urgency." | Engineering | Leadership escalation |

### 4.5 Exhaustive Scenario Examples — IsImportant = FALSE

| # | Message | Domain | Why NOT Important |
|---|---|---|---|
| 1 | "Hi Everyone — here is the deck for tomorrow + agenda." | All | Routine pre-meeting share |
| 2 | "Are folks in office today?" / "Lunch?" | All | Social coordination |
| 3 | "New printer installed on floor 4." | Operations | Routine operational update |
| 4 | "I tested this out. Looks good. Will update the sheet." | All | Standard task acknowledgment |
| 5 | "Everyone, I missed my cab, so WFH today." | All | Personal logistics |
| 6 | "Added the feedback to the table." | All | Routine completion |
| 7 | "[GIF Image]" / "phew" / "Happy Friday!" | All | Social / noise |
| 8 | "Gentle reminder to check in on your quarterly goals." | HR | Standard reminder, no consequence |
| 9 | "The team dinner is Thursday at 7 PM at the usual place." | All | Social coordination |
| 10 | "Congratulations on hitting the sales target!" | Sales | Praise/recognition |
| 11 | "Here's a good article on AI trends — thought you'd find it interesting." | All | Optional share, no directive |
| 12 | "Our weekly newsletter has been published." | Marketing | Routine operational note |

### 4.6 Edge Cases & Decision Rules

| Edge Case | Tag | Rationale |
|---|---|---|
| **"Need it in the next 2 hours"** | **TRUE** — flag staleness risk | If tagging runs daily, stale by tag time. Open item: `time_sensitivity` metadata. |
| **"Reminder: expense reports due EOD today"** | **TRUE** if same-day; **degrades if stale** | Importance decays rapidly. |
| **"FYI: Salesforce is down" (no explicit ask)** | **TRUE** | Tool outage affecting business processes = high impact, even without a task. |
| **Long update with risk buried in narrative** | **TRUE** if risk/blocker present | Important for the risk content, not its length. |
| **Approval given ("Approved" / "LGTM")** | **FALSE** | The ask was important; the resolution de-escalates. |
| **"Following up — still waiting on legal sign-off; blocking the deal"** | **TRUE** | Re-surfaced blocker with explicit "blocking" signal. |
| **Routine weekly status post** | **FALSE** — unless it contains a risk callout | "We are $5M below target" embedded in a status post IS important. |
| **Message from leadership with no urgency content** | **FALSE** | Sender role alone doesn't make content important. A VP saying "phew" isn't important. |
| **"I'm unwell, OOF today" from a key DRI** | **FALSE** (offline tag) | Objectively not important. User-specific relevance applied at query time. |
| **"Customer threatening to cancel" without revenue context** | **TRUE** | Churn signal inherently high-impact regardless of revenue amount. |
| **Company all-hands agenda** | **FALSE** | Informational broadcast, not urgent. |
| **"Effective immediately: new data classification policy"** | **TRUE** | Policy change with immediate effect, affects many. |

---

## 5. Attribution — Who is the task for?

Attribution is required for every `HasTask = TRUE` message. It answers: "is this task FOR ME?" when Copilot serves results.

### 5.1 Three-Tier Model

| Tier | Condition | Assignee Value | Confidence | P0 Scope |
|---|---|---|---|---|
| **EXPLICIT** | @mention or multiple @mentions in the ask | The @mentioned user(s) | HIGH | Yes |
| **IMPLICIT** | No @mention but name in text, reply-to pattern, or 1:1 chat context | The inferred user | MEDIUM | P1 |
| **UNASSIGNED** | Broadcast ask ("Can someone…"), "we/you" without clear referent | `unassigned` | LOW | Yes |

### 5.2 Attribution Examples

| Message | Domain | Tier | Assignee(s) |
|---|---|---|---|
| "@Gaurav, can you post that we recommend not to proceed?" | Engineering | Explicit | Gaurav |
| "@Sara, please send the client proposal by Friday" | Sales | Explicit | Sara |
| "@Finance, please process the vendor invoice" | Finance | Explicit (team) | Finance team |
| "Nikhil, make minor tweaks and post it" (no @, name used) | Engineering | Implicit | Nikhil |
| "Can someone update the escalation tracker?" | Support | Unassigned | `unassigned` |
| "Everyone — please submit your self-reviews" | HR | Explicit (broadcast) | `broadcast` |
| "Let me know your thoughts" (in 1:1 chat) | All | Implicit (context) | The other person |
| "@Ashish for awareness" + "@Enrique please test these out" | Engineering | Explicit + CC | Enrique (primary); Ashish is CC only |
| "VP team — please prepare board deck sections by Thursday" | Executive | Explicit (group) | VP team |

### 5.3 Attribution Edge Cases

| Scenario | Guidance |
|---|---|
| **1:1 chat**: Any HasTask message | Always attribute to the non-sender. No ambiguity. |
| **Group chat with "you"**: "Can you check?" (no names) | Mark `unassigned` unless reply-to context resolves. |
| **@channel / @team broadcast**: "Team, please review" | Mark `broadcast` — every member is a potential assignee. |
| **"CC" / "FYI" secondary mentions**: "@Ashish for awareness" | Do NOT attribute the task to CC'd people. |
| **Self-directed**: "I will handle this" | Assignee = sender (self-assigned). HasTask=FALSE (Commitment). |
| **Multiple @mentions, some CC**: "@Gaurav please review; cc @Ritika" | Gaurav = EXPLICIT. Ritika = CC. Separate the roles. |
| **"Client asked us to send the SOW"** | Unassigned — "us" is ambiguous. Not clear who will do it. |

### 5.4 Copilot Behavior When Attribution is Ambiguous

| User Query | Behavior |
|---|---|
| "Tasks pending on me" | Return only EXPLICIT and high-confidence IMPLICIT. Omit UNASSIGNED unless user asks. |
| "What do we need to follow up on?" | Show (1) tasks targeted to user, then (2) "Needs owner" section for UNASSIGNED. |
| "Did anyone ask me to do something?" (only UNASSIGNED exist) | Ask one clarifier: "Explicitly assigned to you only, or also general asks?" |

---

## 6. Tagging Granularity

### 6.1 Recommendation: Tag at message level, aggregate at conversation level for retrieval

| Aspect | Message-Level (offline stamp) | Conversation-Level (query-time roll-up) |
|---|---|---|
| HasTask | Tag individual messages | Thread `HasTask = TRUE` if ≥1 message has HasTask=TRUE and no completion signal |
| IsImportant | Tag individual messages | Thread `IsImportant = TRUE` if any message in thread is objectively important |
| Attribution | Per-message assignee | Aggregate unique assignees across thread |
| Sub-class | RfA / RfK / Commitment / Neither | Roll up: thread contains RfA if any message is RfA |

### 6.2 When conversation context IS required

| Scenario | Why | Recommended Window |
|---|---|---|
| **Task completion detection** | "Can you review?" → "Done, reviewed." Need downstream msg. | ±5 msgs after task |
| **Implicit "you" resolution** | "Can you check?" in group — resolved by reply-to. | ±3 msgs |
| **Follow-up chain** | "Following up — still waiting on sign-off." Need original ask. | ±3 msgs |
| **Acknowledgment classification** | "Works" / "Sure" — meaningless without parent. | ±2 msgs |
| **Context for "Let me know your thoughts"** | Ask is meaningless without preceding proposal. | ±1–3 msgs |

**Guidance for Science:** For P0, start with **message-level tagging with a ±3 message context window**. Conversation-level roll-up is a P1 aggregation layer.

---

## 7. HasTask × IsImportant Interaction

These are independent tags. A message can be any combination:

| HasTask | IsImportant | Example | Copilot Treatment |
|---|---|---|---|
| TRUE | TRUE | "Need legal sign-off by EOD or the deal falls through" | **Surface first** — task + urgent |
| TRUE | FALSE | "Can we meet at 2 PM?" / "What's the WiFi password?" | Surface in task list, not prioritized |
| FALSE | TRUE | "FYI: Salesforce is down, invoicing frozen" | Surface under "What should be on my radar?" |
| FALSE | FALSE | "Thanks!" / "Happy Friday!" / "Lunch?" | Do not surface in triage |

**Ranking rules for Copilot:**
- "What do I need to act on?" → Filter `HasTask = TRUE`, rank by `IsImportant = TRUE` first, then recency. Show RfA before RfK.
- "What should be on my radar?" → Show `IsImportant = TRUE` regardless of HasTask.
- "Catch me up" → Weight `IsImportant = TRUE` messages higher in summary.
- "Any open questions for me?" → Filter `HasTask = TRUE` where sub-class is RfK.

---

## 8. Combined Quick-Reference Table (cross-domain)

| Message | Domain | HasTask | Sub-class | IsImportant | Attribution | Context |
|---|---|---|---|---|---|---|
| "Please send the updated proposal to Contoso by Friday" | Sales | TRUE | RfA | FALSE | Implicit | Msg only |
| "What's our discount ceiling for enterprise deals?" | Sales | TRUE | RfK | FALSE | Unassigned | Msg only |
| "Contoso deal at risk — legal flagged data residency. $3M deal falls through Friday." | Sales | FALSE | — | TRUE | — | Msg only |
| "Can you approve the PO for $50K?" | Finance | TRUE | RfA | FALSE | Implicit (1:1) | Msg only |
| "Audit finding: material weakness in revenue recognition" | Finance | FALSE | — | TRUE | — | Msg only |
| "Please submit your self-review by March 15" | HR | TRUE | RfA | FALSE | Broadcast | Msg only |
| "Candidate has competing offer expiring tomorrow" | HR | FALSE | — | TRUE | — | Msg only |
| "Please redline the NDA before sending to the vendor" | Legal | TRUE | RfA | FALSE | Implicit | Msg only |
| "GDPR breach — 72-hour notification window" | Legal | FALSE | — | TRUE | — | Msg only |
| "@Priya, can you point me to the latest demo video?" | Eng | TRUE | RfK | FALSE | Explicit (@) | Msg only |
| "Need LB approval by EOD to avoid missing ship window" | Eng | TRUE | RfA | TRUE | Unassigned | Msg only |
| "Quality is 56% vs 80% target. P0s must be addressed." | Eng | FALSE | — | TRUE | — | Msg only |
| "Can you book the boardroom for the exec review?" | Ops | TRUE | RfA | FALSE | Implicit (1:1) | Msg only |
| "Salesforce down for 3 hours — pipeline frozen" | IT | FALSE | — | TRUE | — | Msg only |
| "Which tagline do we go with — A or B?" | Marketing | TRUE | RfK | FALSE | Unassigned | Msg only |
| "Campaign launch delayed 2 weeks — impacts Q2 revenue" | Marketing | FALSE | — | TRUE | — | Msg only |
| "Can you escalate this ticket? Customer waiting 3 days." | Support | TRUE | RfA | TRUE | Implicit | Msg only |
| "Thanks for the update!" | All | FALSE | — | FALSE | — | Msg only |
| "I'll send the forecast by EOD" | Finance | FALSE | Commitment | FALSE | — | Msg only |
| "Feel free to review if you have time" | All | FALSE | — | FALSE | — | Msg only |
| "Happy Friday! 🎉" | All | FALSE | — | FALSE | — | Msg only |

---

## 9. Technical Constraints & Open Items

Known limitations flagged for Science and Engineering. PM is calling these out; solutions are not prescribed here.

| # | Constraint | Impact | PM Recommendation |
|---|---|---|---|
| 1 | **Batch tagging cadence** (e.g., once per day) | "Need in 2 hours" is stale by tag time. Sub-hour urgency signals lose value. | Explore near-real-time path for messages with explicit urgency markers. For users: "For real-time urgent asks, use @mentions and Teams notifications." |
| 2 | **Task completion state** not solved in P0 | HasTask=TRUE may already be resolved. Stale tasks appear pending. | Accept in P0. P1: completion detection via acknowledgment patterns. |
| 3 | **Image/attachment-only messages** | Cannot extract task intent from 📷 or .pptx. | Default FALSE. Revisit with multimodal in P1. |
| 4 | **IsImportant time decay** | "Due EOD today" loses importance next day. Tags don't expire. | P1: Add `time_sensitivity` metadata (none / hours / same_day / this_week). |
| 5 | **Message edits and deletes** | Tags become stale on edit; persist on delete. | Re-tag on edit. Remove on delete. |
| 6 | **Language / code-switching** | Non-English or mixed-language messages may misclassify. | P0: English-only. P1: multilingual expansion. |
| 7 | **Long thread context** | Full context expensive. | Cap at ±3–5 messages for P0. |
| 8 | **Bot / Facilitator messages** | Should never be tagged as human tasks. | Pre-filter known bot senders. Maintain allowlist. |
| 9 | **Relative time references** | "EOD" — whose time zone? Business hours? | P1: structured deadline extraction with timezone. |
| 10 | **Conditional / soft asks** | "If you have time…" — task exists but urgency is low. | Tag HasTask=TRUE. Do NOT mark IsImportant=TRUE unless other urgency signals. |
| 11 | **Recurring asks** | "Please update weekly" — one task or N? | Tag original as TRUE. Recurring generation is P2. |
| 12 | **RfA vs. RfK disambiguation** | Some messages blend both ("Can you review and let me know if it's ready?"). | P0: Tag as HasTask=TRUE. Sub-class disambiguation (RfA vs RfK) is P1. |
| 13 | **Domain-specific jargon** | "LB approval" (eng), "SOW" (sales), "NDA" (legal) carry different urgency signals. | Build domain-aware importance signals in P1. P0: rely on explicit urgency markers. |
| 14 | **External stakeholder mentions** | "Client is expecting this by Friday" — urgency comes from external party not in Teams. | Include external deadline mentions as IsImportant signals if deadline + consequence present. |

---

## 10. Evaluation Criteria

### 10.1 Precision vs. Recall Philosophy

**Favor precision over recall.** False positives ("Copilot says I have a task, but I don't") erode trust faster than false negatives ("Copilot missed a task I can find myself"). Users will forgive occasional misses; they won't forgive a noisy, unreliable task list.

### 10.2 Targets

| Metric | P0 Target | P1 Target | Rationale |
|---|---|---|---|
| HasTask Precision | ≥ 85% | ≥ 90% | If Copilot says it's a task, it should be one. |
| HasTask Recall | ≥ 70% | ≥ 80% | Missing some tasks is acceptable; noise is not. |
| IsImportant (Objective) Precision | ≥ 80% | ≥ 85% | False "important" flags cause alert fatigue. |
| Attribution — EXPLICIT | ≥ 95% | ≥ 95% | @mention parsing should be near-perfect. |
| Attribution — IMPLICIT | N/A (P0 skips) | ≥ 70% | Name-in-text and reply-to are harder. |
| Attribution — UNASSIGNED | 100% | 100% | If we can't tell, we say so. |
| RfA vs. RfK (sub-class) | N/A (P0 skips) | ≥ 75% | Sub-type is a P1 refinement. |

### 10.3 Golden Set Construction

Build a labeled dataset of **500+ messages** sampled from real Teams conversations:
- **Conversation types:** 1:1 chats, group chats, channel L1, channel L2
- **Domain distribution:** Engineering, Sales, HR, Legal, Finance, Marketing, Executive, Support, Operations — ~minimum 10% from each non-engineering domain
- **Participant types:** ICs, managers, skip-levels, cross-functional, external
- **Edge case proportion:** ~15% of set should be deliberate edge cases
- **Labeling:** Each message labeled by 2 human annotators; disagreements resolved by PM
- **Refresh:** Re-sample quarterly as conversation patterns evolve

### 10.4 Validation Method

1. Run classifier on golden set
2. Compare predicted vs. human labels
3. Compute precision, recall, F1 per tag (and per sub-class for P1)
4. Review all false positives manually (trust-eroding)
5. Review false negatives for patterns → feed back into training data
6. **Domain-stratified analysis:** Break metrics by workplace domain to ensure no domain is systematically under-served

---

## 11. Out of Scope (Future Phases)

| Item | Phase | Notes |
|---|---|---|
| Task completion tracking (pending → resolved) | P1 | Detect "Done" / "Submitted" / "Filed" patterns |
| RfA vs. RfK sub-classification | P1 | Enable "tasks for me" vs. "questions for me" filtering |
| Task type composite label ("remind", "reply", "approve") | P1 | Move beyond boolean HasTask to structured types |
| Commitment tracking ("I'll send by EOD") | P1 | Surface under "What's coming your way" |
| Structured deadline extraction ("by March 30" → timestamp) | P1 | Enables time-decay and calendar integration |
| Multi-message task chains (ask → follow-up → resolution) | P2 | Track lifecycle of a task across a thread |
| Sentiment / tone detection | P2 | Distinguish urgent from sarcastic |
| Multimodal classification (images, attachments) | P1–P2 | Classify task intent in screenshots or shared docs |
| Non-English language support | P1 | Multilingual classifier |
| Domain-aware importance signals | P1 | Jargon-aware urgency detection by department |
| Inline BizChat actions (reply, mark complete) | P2 | Requires Phase 2 infrastructure |

---

*End of spec. Questions → Andrew Abishek / Ritika Gupta*

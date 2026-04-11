"""
Interaction Signals — Adds Followed, Saved, Reacted, Reminder to golden dataset messages.

These are Teams-level interaction signals defined in the spec:
  - Reacted: Emoji reactions on messages (like, heart, laugh, surprised, sad, angry)
  - Followed: User clicked Follow on a chat/message to track it
  - Saved: User bookmarked/saved a message for later reference
  - Reminder: User set a reminder on a message (upcoming Teams feature)

Schema (parallel to Reactions):
  Reactions:  [{"Reaction": "like", "Sender": "username"}]
  Followed:   [{"Sender": "username"}]
  Saved:      [{"Sender": "username"}]
  Reminder:   [{"Sender": "username", "ReminderDateTime": "2026-01-16T09:00:00Z"}]
"""

import random
from datetime import datetime, timedelta
from users import USER_MAP

# Seed for reproducibility
random.seed(42)

ALL_USERS = list(USER_MAP.keys())

# ---------- Reaction rules ----------
# Map content keywords/patterns → appropriate reaction emoji
# Teams standard reactions: 👍 ❤️ 😊 🎉 ✅ 🔥 💯 👀 😂 🙏 👏
REACTION_RULES = [
    # Appreciation / agreement / thanks
    (["thanks", "thank you", "great work", "well done", "nice work", "awesome",
      "good job", "excellent", "kudos", "appreciate", "amazing", "fantastic"],
     ["❤️", "👏", "🙏", "👍"]),
    # Humor / lighthearted
    (["lol", "haha", "😂", "😅", "funny", "crack me up", "vibes"],
     ["😂", "😊"]),
    # Impressive results / surprising news
    (["wow", "didn't expect", "unbelievable", "can't believe", "shocked",
      "doubled", "tripled", "300%", "500%", "zero downtime",
      "exceeded", "all-time high", "blew past", "whopping"],
     ["🔥", "💯", "🎉"]),
    # Bad news / frustration
    (["outage", "down again", "failed", "sev1", "sev2", "breach",
      "critical bug", "data loss", "missed deadline",
      "churn", "threatening to leave", "at-risk", "impacting"],
     ["👀"]),
    # Important decisions / milestones / launch
    (["approved", "greenlight", "go-ahead", "launched", "shipped", "signed",
      "closed the deal", "milestone", "completed", "done!", "merged"],
     ["🎉", "🔥", "✅"]),
    # Volunteering / helpfulness / commitments
    (["i'll handle", "i'll take", "i can do", "on it", "i got this",
      "leave it to me", "i'll pick this up", "happy to help"],
     ["👍", "✅", "🙏"]),
    # Action items / task completion
    (["done", "finished", "wrapped up", "all set", "submitted", "sent",
      "uploaded", "pushed", "deployed", "published"],
     ["✅", "👍"]),
    # Good metrics / performance
    (["on track", "ahead of schedule", "100%", "target met", "strong quarter",
      "exceeded target", "beat forecast", "pipeline", "revenue"],
     ["💯", "🔥"]),
]

# Positive/resolution keywords that override sad/angry reactions
POSITIVE_OVERRIDES = [
    "fixed", "resolved", "healthy", "green", "is green", "relief",
    "over", "incident over", "all clear", "recovered", "restored",
    "back to normal", "stabilized", "passed", "no issues",
]

# ---------- Saved rules ----------
# Messages worth bookmarking: reference info, deadlines, decisions, key metrics
SAVED_KEYWORDS = [
    "deadline", "due by", "due date", "by eod", "by end of day", "by friday",
    "by monday", "by end of week", "key decision", "final decision",
    "approved", "here's the link", "meeting notes", "summary:",
    "action items:", "quick reference", "budget", "policy", "compliance",
    "process:", "checklist", "template", "runbook", "playbook", "dashboard",
    "metrics:", "numbers:", "kpi", "target:", "goal:",
]

# ---------- Followed rules ----------
# Messages worth following: action items, unresolved asks, escalations
FOLLOWED_KEYWORDS = [
    "please", "can you", "could you", "need you to", "action item",
    "follow up", "following up", "any update", "status on", "where are we",
    "blocked", "escalat", "urgent", "asap", "critical", "by eod",
    "by friday", "by monday", "next steps", "todo", "assigned to",
]

# ---------- Reminder rules ----------
# Messages with future deadlines or events worth setting reminders for
REMINDER_KEYWORDS = [
    "by friday", "by monday", "by eod", "by end of day", "by end of week",
    "next week", "tomorrow", "by march", "by april", "due date",
    "due by", "deadline", "don't forget", "make sure", "remember to",
    "submit by", "review by", "send by", "prepare for", "before the meeting",
]


def _content_matches(content, keywords):
    """Check if content matches any of the given keywords (case-insensitive)."""
    lower = content.lower()
    return any(kw in lower for kw in keywords)


def _pick_reactors(sender, members, count=None):
    """Pick random reactors from chat members, excluding the sender."""
    candidates = [m for m in members if m != sender]
    if not candidates:
        return []
    if count is None:
        count = random.choice([1, 1, 1, 2, 2, 3])  # Weighted toward 1-2
    return random.sample(candidates, min(count, len(candidates)))


def _pick_reaction_type(content):
    """Pick a contextually appropriate reaction type based on content."""
    lower = content.lower()
    has_positive = any(p in lower for p in POSITIVE_OVERRIDES)
    for keywords, reaction_types in REACTION_RULES:
        if any(kw in lower for kw in keywords):
            # If content is positive/resolved, don't assign negative reactions
            if has_positive and all(r in ("👀",) for r in reaction_types):
                return "👍"
            return random.choice(reaction_types)
    # Default: weighted random from common Teams reactions
    return random.choices(
        ["👍", "✅", "😊", "❤️", "🎉", "🔥", "💯"],
        weights=[25, 15, 15, 10, 10, 10, 15],
        k=1
    )[0]


def _reminder_time(sent_datetime_str):
    """Generate a reminder time ~1-3 days after the message was sent."""
    # Parse the sent time and add 1-3 days
    try:
        base = datetime.strptime(sent_datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        base = datetime(2026, 1, 16, 9, 0, 0)
    offset = timedelta(days=random.choice([1, 1, 2, 2, 3]), hours=random.choice([8, 9, 10]))
    reminder = base + offset
    # Snap to morning working hours
    reminder = reminder.replace(hour=9, minute=0, second=0)
    return reminder.strftime("%Y-%m-%dT%H:%M:%SZ")


def apply_interaction_signals(all_conversations, base_time):
    """
    Post-process conversations to add contextually appropriate Teams interaction signals.
    
    Modifies messages in-place, adding:
      - reactions: list of (reaction_type, sender) tuples
      - followed_by: list of usernames
      - saved_by: list of usernames
      - reminder: list of (username, reminder_datetime) tuples
    
    Target coverage:
      - Reactions: ~15-20% of messages
      - Followed: ~5-8% of messages
      - Saved: ~4-6% of messages
      - Reminder: ~3-4% of messages
    """
    total_msgs = 0
    reactions_added = 0
    followed_added = 0
    saved_added = 0
    reminder_added = 0

    for conv_idx, conv in enumerate(all_conversations):
        members = [m if isinstance(m, str) else m.get("MailNickName", "") for m in conv["members"]]
        conv_base = base_time + timedelta(days=conv_idx, hours=(conv_idx % 8))
        
        for msg_idx, msg in enumerate(conv["messages"]):
            total_msgs += 1
            content = msg["content"]
            sender = msg["from"]
            sent_time = conv_base + timedelta(minutes=msg_idx * 2)
            sent_time_str = sent_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            ann = msg.get("annotations", {})
            has_task = ann.get("has_task", False)
            is_important = ann.get("is_important", False)

            # Skip very short messages (ack-only) for most signals
            is_short = len(content) < 25

            # ---- REACTIONS ----
            # Already has reactions from source data? Keep them.
            if not msg.get("reactions"):
                should_react = False
                
                # High-probability: important messages, appreciation, milestones
                if is_important and random.random() < 0.45:
                    should_react = True
                elif _content_matches(content, REACTION_RULES[0][0]) and random.random() < 0.55:
                    should_react = True  # Appreciation
                elif _content_matches(content, REACTION_RULES[1][0]) and random.random() < 0.50:
                    should_react = True  # Humor
                elif _content_matches(content, REACTION_RULES[2][0]) and random.random() < 0.60:
                    should_react = True  # Surprise
                elif _content_matches(content, REACTION_RULES[3][0]) and random.random() < 0.30:
                    should_react = True  # Bad news
                elif _content_matches(content, REACTION_RULES[4][0]) and random.random() < 0.40:
                    should_react = True  # Decisions/milestones
                elif _content_matches(content, REACTION_RULES[5][0]) and random.random() < 0.35:
                    should_react = True  # Volunteering
                # Low-probability random for variety
                elif not is_short and random.random() < 0.06:
                    should_react = True

                if should_react and len(members) > 1:
                    reaction_type = _pick_reaction_type(content)
                    reactors = _pick_reactors(sender, members)
                    msg["reactions"] = [(reaction_type, r) for r in reactors]
                    reactions_added += 1

            else:
                reactions_added += 1  # Count existing reactions

            # ---- FOLLOWED ----
            if not msg.get("followed_by"):
                should_follow = False
                
                if has_task and is_important and random.random() < 0.50:
                    should_follow = True
                elif has_task and _content_matches(content, FOLLOWED_KEYWORDS) and random.random() < 0.12:
                    should_follow = True
                elif is_important and random.random() < 0.10:
                    should_follow = True

                if should_follow:
                    # Followers are typically the assignee or interested parties
                    assignees = ann.get("assignee", [])
                    potential_followers = []
                    
                    # Assignees follow tasks assigned to them
                    for a in assignees:
                        if a in members and a != sender:
                            potential_followers.append(a)
                    
                    # Also managers/leads might follow important items
                    if is_important:
                        managers = [m for m in members if m != sender and 
                                   USER_MAP.get(m, {}).get("JobTitle", "").lower() in 
                                   ["ceo", "cto", "cfo", "vp sales", "engineering manager",
                                    "marketing director", "hr director", "general counsel",
                                    "finance manager", "customer success manager", "operations manager"]]
                        potential_followers.extend(managers)
                    
                    # Deduplicate and limit
                    potential_followers = list(dict.fromkeys(potential_followers))
                    if not potential_followers:
                        potential_followers = _pick_reactors(sender, members, count=1)
                    
                    if potential_followers:
                        count = min(random.choice([1, 1, 2]), len(potential_followers))
                        msg["followed_by"] = potential_followers[:count]
                        followed_added += 1

            # ---- SAVED ----
            if not msg.get("saved_by"):
                should_save = False
                
                if _content_matches(content, SAVED_KEYWORDS) and not is_short:
                    if is_important and random.random() < 0.65:
                        should_save = True
                    elif has_task and random.random() < 0.22:
                        should_save = True
                    elif random.random() < 0.12:
                        should_save = True

                if should_save:
                    # People save messages relevant to them
                    savers = _pick_reactors(sender, members, count=random.choice([1, 1, 2]))
                    if savers:
                        msg["saved_by"] = savers
                        saved_added += 1

            # ---- REMINDER ----
            if not msg.get("reminder"):
                should_remind = False
                
                if _content_matches(content, REMINDER_KEYWORDS) and has_task:
                    if is_important and random.random() < 0.80:
                        should_remind = True
                    elif random.random() < 0.35:
                        should_remind = True

                if should_remind:
                    # The assignee or a relevant member sets a reminder
                    assignees = ann.get("assignee", [])
                    reminder_setters = [a for a in assignees if a in members]
                    if not reminder_setters:
                        reminder_setters = _pick_reactors(sender, members, count=1)
                    
                    if reminder_setters:
                        setter = reminder_setters[0]
                        msg["reminder"] = [(setter, _reminder_time(sent_time_str))]
                        reminder_added += 1

    print(f"\n=== INTERACTION SIGNALS APPLIED ===")
    print(f"  Reactions: {reactions_added}/{total_msgs} messages ({round(reactions_added/total_msgs*100, 1)}%)")
    print(f"  Followed:  {followed_added}/{total_msgs} messages ({round(followed_added/total_msgs*100, 1)}%)")
    print(f"  Saved:     {saved_added}/{total_msgs} messages ({round(saved_added/total_msgs*100, 1)}%)")
    print(f"  Reminder:  {reminder_added}/{total_msgs} messages ({round(reminder_added/total_msgs*100, 1)}%)")
    
    return {
        "reactions": reactions_added,
        "followed": followed_added,
        "saved": saved_added,
        "reminder": reminder_added,
        "total": total_msgs,
    }

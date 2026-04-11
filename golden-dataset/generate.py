#!/usr/bin/env python3
"""
Golden Dataset Generator for Task Intent Tagging Evaluation
Generates: chats.config.json, users.config.json, onlinemeetings.config.json,
           events.config.json, golden_annotations.csv, review.html
"""

import json
import csv
import uuid
import os
from datetime import datetime, timedelta
from users import USERS, USER_MAP

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def gen_id():
    return str(uuid.uuid4())


def gen_datetime(base, offset_minutes):
    """Generate ISO datetime string offset from base."""
    dt = base + timedelta(minutes=offset_minutes)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def build_chat_message(msg, base_time, msg_index):
    """Convert an annotated message dict to the ingestion chat message format."""
    cm = {
        "ChatMessageId": msg.get("id", gen_id()),
        "From": msg["from"],
        "ContentType": "html",
        "Content": f"<p>{msg['content']}</p>",
        "SentDateTime": gen_datetime(base_time, msg_index * 2),  # 2 min apart
        "QuoteChatMessageId": msg.get("reply_to", ""),
        "ReadBy": None,
    }
    if msg.get("reactions"):
        cm["Reactions"] = [{"Reaction": r[0], "Sender": r[1]} for r in msg["reactions"]]
    if msg.get("mentions"):
        cm["Mentions"] = [{"MentionText": m, "Mentioned": {"User": {"DisplayName": USER_MAP.get(m, {}).get("DisplayName", m)}}} for m in msg["mentions"]]
    if msg.get("followed_by"):
        cm["Followed"] = [{"Sender": u} for u in msg["followed_by"]]
    if msg.get("saved_by"):
        cm["Saved"] = [{"Sender": u} for u in msg["saved_by"]]
    if msg.get("reminder"):
        cm["Reminder"] = [{"Sender": r[0], "ReminderDateTime": r[1]} for r in msg["reminder"]]
    return cm


def build_chat_json(conv, base_time):
    """Convert a conversation dict to ingestion format."""
    chat_id = conv.get("chat_id", gen_id())
    messages = []
    for i, msg in enumerate(conv["messages"]):
        if "id" not in msg:
            msg["id"] = gen_id()
        messages.append(build_chat_message(msg, base_time, i))

    return {
        "ChatId": chat_id,
        "ChatType": conv["chat_type"],
        "Members": conv["members"],
        "ChatMessages": messages,
    }


def build_annotation_rows(conv):
    """Extract annotation rows for CSV from conversation."""
    rows = []
    for i, msg in enumerate(conv["messages"]):
        ann = msg.get("annotations", {})
        rows.append({
            "conversation_id": conv.get("chat_id", ""),
            "conversation_topic": conv.get("topic", ""),
            "chat_type": conv["chat_type"],
            "domain": conv.get("domain", ""),
            "message_id": msg.get("id", ""),
            "message_index": i,
            "from_user": msg["from"],
            "content": msg["content"],
            "has_task": ann.get("has_task", False),
            "task_sub_class": ann.get("task_sub_class", "Neither"),
            "task_type": ann.get("task_type", ""),
            "is_important": ann.get("is_important", False),
            "attribution": ann.get("attribution", ""),
            "assignee": "|".join(ann.get("assignee", [])),
            "edge_case": ann.get("edge_case", ""),
            "notes": ann.get("notes", ""),
        })
    return rows


def build_meeting_json(conv, base_time):
    """Build online meeting entry for meeting chats."""
    meeting_id = conv.get("chat_id", gen_id())
    event_id = gen_id()
    return {
        "OnlineMeetingId": meeting_id,
        "OnlineMeetingType": "Event",
        "EventId": event_id,
        "StartDateTime": gen_datetime(base_time, 0),
        "EndDateTime": gen_datetime(base_time, 60),
        "Owner": conv["members"][0],
        "Participants": conv["members"],
        "Transcripts": [],
    }, {
        "EventId": event_id,
        "Subject": conv.get("topic", "Meeting"),
        "StartDateTime": gen_datetime(base_time, 0),
        "EndDateTime": gen_datetime(base_time, 60),
        "Organizer": conv["members"][0],
        "Attendees": conv["members"],
        "OnlineMeetingId": meeting_id,
    }


def generate_review_html(conversations, annotations):
    """Generate an interactive HTML review page for DS team."""
    # Count stats
    total_msgs = sum(len(c["messages"]) for c in conversations)
    has_task_true = sum(1 for a in annotations if a["has_task"])
    is_important_true = sum(1 for a in annotations if a["is_important"])

    # Count by quadrant
    q_tt = sum(1 for a in annotations if a["has_task"] and a["is_important"])
    q_tf = sum(1 for a in annotations if a["has_task"] and not a["is_important"])
    q_ft = sum(1 for a in annotations if not a["has_task"] and a["is_important"])
    q_ff = sum(1 for a in annotations if not a["has_task"] and not a["is_important"])

    # Count by task type
    task_types = {}
    for a in annotations:
        if a["has_task"]:
            tt = a["task_type"] or "Unspecified"
            task_types[tt] = task_types.get(tt, 0) + 1

    # Count by attribution
    attr_counts = {}
    for a in annotations:
        if a["has_task"]:
            at = a["attribution"] or "N/A"
            attr_counts[at] = attr_counts.get(at, 0) + 1

    # Count by domain
    domain_counts = {}
    for a in annotations:
        d = a["domain"] or "Unknown"
        domain_counts[d] = domain_counts.get(d, 0) + 1

    # Count by chat type
    chat_type_counts = {}
    for a in annotations:
        ct = a["chat_type"]
        chat_type_counts[ct] = chat_type_counts.get(ct, 0) + 1

    # Count edge cases
    edge_cases = sum(1 for a in annotations if a["edge_case"])

    # Count by sub-class
    sub_class_counts = {}
    for a in annotations:
        sc = a["task_sub_class"] or "Neither"
        sub_class_counts[sc] = sub_class_counts.get(sc, 0) + 1

    # Count interaction signals
    sig_reactions = sum(1 for c in conversations for m in c["messages"] if m.get("reactions"))
    sig_followed = sum(1 for c in conversations for m in c["messages"] if m.get("followed_by"))
    sig_saved = sum(1 for c in conversations for m in c["messages"] if m.get("saved_by"))
    sig_reminder = sum(1 for c in conversations for m in c["messages"] if m.get("reminder"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Golden Dataset Review - Task Intent for Teams</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f5f5f5; color: #1a1a1a; }}
.header {{ background: #0078d4; color: white; padding: 24px 32px; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }}
.header h1 {{ font-size: 22px; font-weight: 600; }}
.header .subtitle {{ font-size: 13px; opacity: 0.9; margin-top: 4px; }}
.container {{ max-width: 1400px; margin: 0 auto; padding: 24px; }}

/* Stats Dashboard */
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.stat-card {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.stat-card .value {{ font-size: 28px; font-weight: 700; color: #0078d4; }}
.stat-card .label {{ font-size: 13px; color: #666; margin-top: 4px; }}

/* Coverage section */
.coverage {{ background: white; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.coverage h2 {{ font-size: 16px; margin-bottom: 16px; color: #333; }}
.coverage-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }}
.coverage-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.coverage-table th {{ text-align: left; padding: 8px; border-bottom: 2px solid #e0e0e0; color: #666; font-weight: 600; }}
.coverage-table td {{ padding: 8px; border-bottom: 1px solid #f0f0f0; }}
.coverage-table .count {{ font-weight: 600; color: #0078d4; }}

/* Quadrant matrix */
.quadrant {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2px; background: #e0e0e0; border-radius: 8px; overflow: hidden; max-width: 400px; }}
.quadrant .cell {{ padding: 16px; text-align: center; }}
.quadrant .cell.tt {{ background: #fde8e8; }}
.quadrant .cell.tf {{ background: #e8f4fd; }}
.quadrant .cell.ft {{ background: #fff3e0; }}
.quadrant .cell.ff {{ background: #f0f0f0; }}
.quadrant .cell .val {{ font-size: 24px; font-weight: 700; }}
.quadrant .cell .desc {{ font-size: 11px; color: #666; margin-top: 4px; }}

/* Filters */
.filters {{ background: white; border-radius: 8px; padding: 16px 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }}
.filters label {{ font-size: 13px; font-weight: 600; color: #333; }}
.filters select, .filters input {{ padding: 6px 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 13px; }}
.filters input[type=text] {{ width: 250px; }}
.filter-group {{ display: flex; align-items: center; gap: 6px; }}

/* Conversation cards */
.conv-card {{ background: white; border-radius: 8px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }}
.conv-header {{ padding: 16px 20px; border-bottom: 1px solid #e8e8e8; display: flex; justify-content: space-between; align-items: center; cursor: pointer; }}
.conv-header:hover {{ background: #fafafa; }}
.conv-title {{ font-size: 15px; font-weight: 600; }}
.conv-meta {{ display: flex; gap: 12px; align-items: center; }}
.conv-meta .badge {{ padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
.badge-1on1 {{ background: #e8f4fd; color: #0078d4; }}
.badge-group {{ background: #e8fde8; color: #107c10; }}
.badge-meeting {{ background: #fff3e0; color: #ca5010; }}
.conv-body {{ display: none; padding: 0; }}
.conv-body.open {{ display: block; }}

/* Messages */
.msg-row {{ display: grid; grid-template-columns: 160px 1fr 80px 80px 100px 120px; gap: 8px; padding: 10px 20px; border-bottom: 1px solid #f5f5f5; font-size: 13px; align-items: start; }}
.msg-row:hover {{ background: #fafafa; }}
.msg-row.edge-case {{ border-left: 3px solid #ff8c00; }}
.msg-header {{ display: grid; grid-template-columns: 160px 1fr 80px 80px 100px 120px; gap: 8px; padding: 10px 20px; background: #f8f8f8; font-weight: 600; font-size: 12px; color: #666; border-bottom: 2px solid #e0e0e0; position: sticky; top: 0; }}
.msg-from {{ font-weight: 600; color: #0078d4; }}
.msg-content {{ color: #333; line-height: 1.5; }}
.tag {{ display: inline-block; padding: 1px 8px; border-radius: 3px; font-size: 11px; font-weight: 600; }}
.tag-true {{ background: #107c10; color: white; }}
.tag-false {{ background: #e0e0e0; color: #888; }}
.tag-rfa {{ background: #0078d4; color: white; }}
.tag-rfk {{ background: #8764b8; color: white; }}
.tag-commitment {{ background: #ca5010; color: white; }}
.tag-neither {{ background: #e0e0e0; color: #888; }}
.tag-explicit {{ background: #107c10; color: white; }}
.tag-implicit {{ background: #0078d4; color: white; }}
.tag-unassigned {{ background: #ff8c00; color: white; }}
.tag-broadcast {{ background: #8764b8; color: white; }}
.tag-na {{ background: #e0e0e0; color: #888; }}
.attr-detail {{ font-size: 11px; color: #666; margin-top: 2px; }}
.notes {{ font-size: 11px; color: #888; font-style: italic; margin-top: 4px; }}
.msg-count {{ font-size: 12px; color: #888; }}
.signal-badges {{ display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px; }}
.signal {{ display: inline-flex; align-items: center; gap: 2px; padding: 1px 6px; border-radius: 3px; font-size: 10px; font-weight: 600; }}
.signal-reaction {{ background: #fff3e0; color: #ca5010; }}
.signal-followed {{ background: #e8f4fd; color: #0078d4; }}
.signal-saved {{ background: #fde8e8; color: #d13438; }}
.signal-reminder {{ background: #e8fde8; color: #107c10; }}
</style>
</head>
<body>
<div class="header">
    <h1>Golden Dataset Review — Task Intent for Teams</h1>
    <div class="subtitle">Meridian Technologies · {len(conversations)} conversations · {total_msgs} messages · Generated {datetime.now().strftime('%Y-%m-%d')}</div>
</div>
<div class="container">

<!-- Stats Dashboard -->
<div class="stats-grid">
    <div class="stat-card"><div class="value">{total_msgs}</div><div class="label">Total Messages</div></div>
    <div class="stat-card"><div class="value">{len(conversations)}</div><div class="label">Conversations</div></div>
    <div class="stat-card"><div class="value">{has_task_true}</div><div class="label">HasTask = TRUE ({round(has_task_true/total_msgs*100)}%)</div></div>
    <div class="stat-card"><div class="value">{is_important_true}</div><div class="label">IsImportant = TRUE ({round(is_important_true/total_msgs*100)}%)</div></div>
    <div class="stat-card"><div class="value">{edge_cases}</div><div class="label">Edge Cases ({round(edge_cases/total_msgs*100)}%)</div></div>
</div>

<!-- Interaction Signals -->
<div class="stats-grid">
    <div class="stat-card"><div class="value">{sig_reactions}</div><div class="label">❤️ Reacted ({round(sig_reactions/total_msgs*100)}%)</div></div>
    <div class="stat-card"><div class="value">{sig_followed}</div><div class="label">👁️ Followed ({round(sig_followed/total_msgs*100)}%)</div></div>
    <div class="stat-card"><div class="value">{sig_saved}</div><div class="label">📌 Saved ({round(sig_saved/total_msgs*100)}%)</div></div>
    <div class="stat-card"><div class="value">{sig_reminder}</div><div class="label">⏰ Reminder ({round(sig_reminder/total_msgs*100)}%)</div></div>
</div>

<!-- Quadrant Matrix -->
<div class="coverage">
    <h2>HasTask × IsImportant Quadrant Distribution</h2>
    <div class="quadrant">
        <div class="cell tt"><div class="val">{q_tt}</div><div class="desc">HasTask=TRUE + IsImportant=TRUE</div></div>
        <div class="cell tf"><div class="val">{q_tf}</div><div class="desc">HasTask=TRUE + IsImportant=FALSE</div></div>
        <div class="cell ft"><div class="val">{q_ft}</div><div class="desc">HasTask=FALSE + IsImportant=TRUE</div></div>
        <div class="cell ff"><div class="val">{q_ff}</div><div class="desc">HasTask=FALSE + IsImportant=FALSE</div></div>
    </div>
</div>

<!-- Coverage Tables -->
<div class="coverage">
    <h2>Scenario Coverage</h2>
    <div class="coverage-grid">
        <div>
            <table class="coverage-table">
                <tr><th>Chat Type</th><th>Messages</th></tr>
                {"".join(f'<tr><td>{k}</td><td class="count">{v}</td></tr>' for k,v in sorted(chat_type_counts.items()))}
            </table>
        </div>
        <div>
            <table class="coverage-table">
                <tr><th>Domain</th><th>Messages</th></tr>
                {"".join(f'<tr><td>{k}</td><td class="count">{v}</td></tr>' for k,v in sorted(domain_counts.items()))}
            </table>
        </div>
        <div>
            <table class="coverage-table">
                <tr><th>Task Type</th><th>Count</th></tr>
                {"".join(f'<tr><td>{k}</td><td class="count">{v}</td></tr>' for k,v in sorted(task_types.items()))}
            </table>
        </div>
        <div>
            <table class="coverage-table">
                <tr><th>Attribution</th><th>Count</th></tr>
                {"".join(f'<tr><td>{k}</td><td class="count">{v}</td></tr>' for k,v in sorted(attr_counts.items()))}
            </table>
        </div>
        <div>
            <table class="coverage-table">
                <tr><th>Sub-class</th><th>Count</th></tr>
                {"".join(f'<tr><td>{k}</td><td class="count">{v}</td></tr>' for k,v in sorted(sub_class_counts.items()))}
            </table>
        </div>
    </div>
</div>

<!-- Filters -->
<div class="filters">
    <div class="filter-group">
        <label>Chat Type:</label>
        <select id="filterChatType" onchange="applyFilters()">
            <option value="all">All</option>
            <option value="OneOnOne">1:1</option>
            <option value="Group">Group</option>
            <option value="Meeting">Meeting</option>
        </select>
    </div>
    <div class="filter-group">
        <label>HasTask:</label>
        <select id="filterHasTask" onchange="applyFilters()">
            <option value="all">All</option>
            <option value="true">TRUE</option>
            <option value="false">FALSE</option>
        </select>
    </div>
    <div class="filter-group">
        <label>IsImportant:</label>
        <select id="filterIsImportant" onchange="applyFilters()">
            <option value="all">All</option>
            <option value="true">TRUE</option>
            <option value="false">FALSE</option>
        </select>
    </div>
    <div class="filter-group">
        <label>Domain:</label>
        <select id="filterDomain" onchange="applyFilters()">
            <option value="all">All</option>
            {"".join(f'<option value="{d}">{d}</option>' for d in sorted(domain_counts.keys()))}
        </select>
    </div>
    <div class="filter-group">
        <label>Edge Cases Only:</label>
        <input type="checkbox" id="filterEdge" onchange="applyFilters()">
    </div>
    <div class="filter-group">
        <label>Search:</label>
        <input type="text" id="filterSearch" placeholder="Search message content..." oninput="applyFilters()">
    </div>
</div>

<!-- Conversations -->
<div id="conversations">
"""

    for conv in conversations:
        chat_type = conv["chat_type"]
        badge_class = {"OneOnOne": "badge-1on1", "Group": "badge-group", "Meeting": "badge-meeting"}.get(chat_type, "badge-group")
        members_display = ", ".join(USER_MAP.get(m, {}).get("DisplayName", m) for m in conv["members"])
        msg_count = len(conv["messages"])

        # Count tags in this conversation
        conv_tasks = sum(1 for m in conv["messages"] if m.get("annotations", {}).get("has_task"))
        conv_important = sum(1 for m in conv["messages"] if m.get("annotations", {}).get("is_important"))

        html += f"""
<div class="conv-card" data-chattype="{chat_type}" data-domain="{conv.get('domain', '')}">
    <div class="conv-header" onclick="this.nextElementSibling.classList.toggle('open')">
        <div>
            <span class="conv-title">{conv.get('topic', 'Untitled')}</span>
            <span class="msg-count"> · {msg_count} messages · {conv_tasks} tasks · {conv_important} important</span>
        </div>
        <div class="conv-meta">
            <span class="badge {badge_class}">{chat_type}</span>
            <span style="font-size:12px;color:#888">{conv.get('domain', '')}</span>
        </div>
    </div>
    <div class="conv-body">
        <div style="padding:8px 20px;font-size:12px;color:#666;background:#f9f9f9;">Members: {members_display}</div>
        <div class="msg-header">
            <div>From</div><div>Message</div><div>HasTask</div><div>Important</div><div>Sub-class</div><div>Attribution</div>
        </div>
"""
        for msg in conv["messages"]:
            ann = msg.get("annotations", {})
            ht = ann.get("has_task", False)
            imp = ann.get("is_important", False)
            sc = ann.get("task_sub_class", "Neither")
            attr = ann.get("attribution", "")
            assignee = ", ".join(ann.get("assignee", []))
            edge = ann.get("edge_case", "")
            notes = ann.get("notes", "")
            sender_name = USER_MAP.get(msg["from"], {}).get("DisplayName", msg["from"])

            ht_class = "tag-true" if ht else "tag-false"
            imp_class = "tag-true" if imp else "tag-false"
            sc_class = {"RfA": "tag-rfa", "RfK": "tag-rfk", "Commitment": "tag-commitment"}.get(sc, "tag-neither")
            attr_class = {"Explicit": "tag-explicit", "Implicit": "tag-implicit", "Unassigned": "tag-unassigned", "Broadcast": "tag-broadcast"}.get(attr, "tag-na")

            edge_html = ""
            notes_html = f'<div class="notes">{notes}</div>' if notes else ""
            assignee_html = f'<div class="attr-detail">→ {assignee}</div>' if assignee else ""
            row_class = "msg-row edge-case" if edge else "msg-row"

            content_escaped = msg["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            # Build interaction signal badges
            signal_html_parts = []
            if msg.get("reactions"):
                rxn_parts = []
                for r in msg["reactions"]:
                    reactor_name = USER_MAP.get(r[1], {}).get("DisplayName", r[1])
                    rxn_parts.append(f'{r[0]} <b>{reactor_name}</b>')
                signal_html_parts.append(f'<span class="signal signal-reaction">{", ".join(rxn_parts)}</span>')
            if msg.get("followed_by"):
                followers = ", ".join(msg["followed_by"])
                signal_html_parts.append(f'<span class="signal signal-followed">👁️ {followers}</span>')
            if msg.get("saved_by"):
                savers = ", ".join(msg["saved_by"])
                signal_html_parts.append(f'<span class="signal signal-saved">📌 {savers}</span>')
            if msg.get("reminder"):
                reminders = ", ".join(f"{r[0]}" for r in msg["reminder"])
                signal_html_parts.append(f'<span class="signal signal-reminder">⏰ {reminders}</span>')
            signals_html = f'<div class="signal-badges">{" ".join(signal_html_parts)}</div>' if signal_html_parts else ""

            html += f"""
        <div class="{row_class}" data-hastask="{str(ht).lower()}" data-isimportant="{str(imp).lower()}" data-edge="{bool(edge)}">
            <div class="msg-from">{sender_name}</div>
            <div class="msg-content">{content_escaped}{edge_html}{signals_html}{notes_html}</div>
            <div><span class="tag {ht_class}">{"TRUE" if ht else "FALSE"}</span></div>
            <div><span class="tag {imp_class}">{"TRUE" if imp else "FALSE"}</span></div>
            <div><span class="tag {sc_class}">{sc}</span></div>
            <div><span class="tag {attr_class}">{attr or "N/A"}</span>{assignee_html}</div>
        </div>
"""
        html += "    </div>\n</div>\n"

    html += """
</div>
</div>

<script>
function applyFilters() {
    const chatType = document.getElementById('filterChatType').value;
    const hasTask = document.getElementById('filterHasTask').value;
    const isImportant = document.getElementById('filterIsImportant').value;
    const domain = document.getElementById('filterDomain').value;
    const edgeOnly = document.getElementById('filterEdge').checked;
    const search = document.getElementById('filterSearch').value.toLowerCase();

    document.querySelectorAll('.conv-card').forEach(card => {
        let show = true;
        if (chatType !== 'all' && card.dataset.chattype !== chatType) show = false;
        if (domain !== 'all' && card.dataset.domain !== domain) show = false;

        if (show) {
            let hasVisibleMsg = false;
            card.querySelectorAll('.msg-row').forEach(row => {
                let msgShow = true;
                if (hasTask !== 'all' && row.dataset.hastask !== hasTask) msgShow = false;
                if (isImportant !== 'all' && row.dataset.isimportant !== isImportant) msgShow = false;
                if (edgeOnly && row.dataset.edge !== 'True') msgShow = false;
                if (search && !row.querySelector('.msg-content').textContent.toLowerCase().includes(search)) msgShow = false;
                row.style.display = msgShow ? '' : 'none';
                if (msgShow) hasVisibleMsg = true;
            });
            if (!hasVisibleMsg && (hasTask !== 'all' || isImportant !== 'all' || edgeOnly || search)) show = false;
        }
        card.style.display = show ? '' : 'none';
    });
}
// Expand all conversations on load for easier review
document.querySelectorAll('.conv-body').forEach(b => b.classList.add('open'));
</script>
</body>
</html>
"""
    return html


def main():
    # Import all conversation modules
    from conversations_1on1 import ONE_ON_ONE_CONVERSATIONS
    from conversations_group import GROUP_CONVERSATIONS
    from conversations_meeting import MEETING_CONVERSATIONS
    from conversations_supplemental import SUPPLEMENTAL_CONVERSATIONS

    from interaction_signals import apply_interaction_signals

    all_conversations = ONE_ON_ONE_CONVERSATIONS + GROUP_CONVERSATIONS + MEETING_CONVERSATIONS + SUPPLEMENTAL_CONVERSATIONS

    # Assign IDs to conversations and messages
    base_time = datetime(2026, 1, 15, 9, 0, 0)
    for i, conv in enumerate(all_conversations):
        if "chat_id" not in conv:
            conv["chat_id"] = gen_id()
        conv_base = base_time + timedelta(days=i, hours=(i % 8))
        for j, msg in enumerate(conv["messages"]):
            if "id" not in msg:
                msg["id"] = gen_id()

    # Apply Teams interaction signals (Reactions, Followed, Saved, Reminder)
    signal_stats = apply_interaction_signals(all_conversations, base_time)

    # 1. Generate users.config.json
    users_out = []
    for u in USERS:
        users_out.append({
            "DisplayName": u["DisplayName"],
            "FirstName": u["FirstName"],
            "LastName": u["LastName"],
            "MailNickName": u["MailNickName"],
            "CompanyName": u["CompanyName"],
            "Department": u["Department"],
            "JobTitle": u["JobTitle"],
            "OfficeLocation": u["OfficeLocation"],
            "UsageLocation": u["UsageLocation"],
            "Licenses": u["Licenses"],
            "Manager": u["Manager"],
            "Address": {"City": u["OfficeLocation"].split(",")[0].strip(), "Country": "USA", "PostalCode": "98101", "State": u["OfficeLocation"].split(",")[-1].strip(), "Street": "100 Meridian Way"},
        })
    with open(os.path.join(OUTPUT_DIR, "users.config.json"), "w", encoding="utf-8") as f:
        json.dump(users_out, f, indent=2, ensure_ascii=False)
    print(f"✓ users.config.json ({len(users_out)} users)")

    # 2. Generate chats.config.json
    chats_out = []
    meeting_convs = []
    for i, conv in enumerate(all_conversations):
        conv_base = base_time + timedelta(days=i, hours=(i % 8))
        if conv["chat_type"] == "Meeting":
            meeting_convs.append((conv, conv_base))
        chats_out.append(build_chat_json(conv, conv_base))

    with open(os.path.join(OUTPUT_DIR, "chats.config.json"), "w", encoding="utf-8") as f:
        json.dump(chats_out, f, indent=2, ensure_ascii=False)
    print(f"✓ chats.config.json ({len(chats_out)} chats)")

    # 3. Generate onlinemeetings.config.json and events.config.json
    meetings_out = []
    events_out = []
    for conv, conv_base in meeting_convs:
        meeting, event = build_meeting_json(conv, conv_base)
        meetings_out.append(meeting)
        events_out.append(event)

    with open(os.path.join(OUTPUT_DIR, "onlinemeetings.config.json"), "w", encoding="utf-8") as f:
        json.dump(meetings_out, f, indent=2, ensure_ascii=False)
    print(f"✓ onlinemeetings.config.json ({len(meetings_out)} meetings)")

    with open(os.path.join(OUTPUT_DIR, "events.config.json"), "w", encoding="utf-8") as f:
        json.dump(events_out, f, indent=2, ensure_ascii=False)
    print(f"✓ events.config.json ({len(events_out)} events)")

    # 4. Generate golden_annotations.csv
    all_annotations = []
    for conv in all_conversations:
        all_annotations.extend(build_annotation_rows(conv))

    fieldnames = ["conversation_id", "conversation_topic", "chat_type", "domain", "message_id", "message_index",
                  "from_user", "content", "has_task", "task_sub_class", "task_type", "is_important",
                  "attribution", "assignee", "edge_case", "notes"]
    with open(os.path.join(OUTPUT_DIR, "golden_annotations.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_annotations)
    print(f"✓ golden_annotations.csv ({len(all_annotations)} rows)")

    # 5. Generate review.html
    html = generate_review_html(all_conversations, all_annotations)
    with open(os.path.join(OUTPUT_DIR, "review.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ review.html")

    # 6. Print summary stats
    total = len(all_annotations)
    ht_true = sum(1 for a in all_annotations if a["has_task"])
    ii_true = sum(1 for a in all_annotations if a["is_important"])
    edges = sum(1 for a in all_annotations if a["edge_case"])
    print(f"\n=== GOLDEN DATASET SUMMARY ===")
    print(f"Total conversations: {len(all_conversations)}")
    print(f"  1:1 chats: {sum(1 for c in all_conversations if c['chat_type'] == 'OneOnOne')}")
    print(f"  Group chats: {sum(1 for c in all_conversations if c['chat_type'] == 'Group')}")
    print(f"  Meeting chats: {sum(1 for c in all_conversations if c['chat_type'] == 'Meeting')}")
    print(f"Total messages: {total}")
    print(f"  HasTask=TRUE: {ht_true} ({round(ht_true/total*100)}%)")
    print(f"  IsImportant=TRUE: {ii_true} ({round(ii_true/total*100)}%)")
    print(f"  Edge cases: {edges} ({round(edges/total*100)}%)")
    print(f"  Domains: {sorted(set(a['domain'] for a in all_annotations))}")


if __name__ == "__main__":
    main()

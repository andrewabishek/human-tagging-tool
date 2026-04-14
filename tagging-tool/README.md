# Conversation Tagging Tool (v3)

A lightweight web tool for human judges to tag Teams conversations at the **conversation level** with `HasTask` and `IsImportant` labels, plus evidence message selection. Designed for inter-rater agreement studies and classifier evaluation.

## Quick Start

### 1. Set up Supabase

1. Go to [supabase.com](https://supabase.com) and create a project
2. Open the **SQL Editor** and run `sql/schema_v3.sql` (drops old tables, creates new schema, pre-seeds admin judge)
3. Credentials are already configured in `js/supabase-client.js`

### 2. Upload conversation data

1. Open `index.html#upload` in a browser
2. Drop the V2 CSV file (`conversation_id, conversation_topic, chat_type, Conversation body, HasTask-GroundTruth, action_score, commitment_score, knowledge_score`)
3. Click **Upload & Parse** — conversations and parsed messages are stored

### 3. Start tagging

1. Open `index.html` in a browser
2. Select your name or enter a new one
3. Conversations are auto-assigned via round-robin (2 judges per conversation)
4. Read the full conversation, then tag: **HasTask** (Yes/No) + **IsImportant** (Yes/No)
5. Click evidence buttons on individual messages to mark supporting evidence
6. Keyboard: `Enter` = Save & Next, `←` / `→` = navigate

### 4. Admin Dashboard

Open `index.html#admin` to see:

- Judge progress (assigned vs tagged)
- Disagreement table (auto-detected)
- Agreement with ground truth
- LLM classifier scores (hidden from judges)

### 5. Export

Use **⬇ CSV** or **⬇ JSON** buttons in the header.

## Architecture

```
tagging-tool/
├── index.html              # Login, tagging UI, upload, admin dashboard
├── css/styles.css          # v3 styles with evidence highlights
├── js/
│   ├── supabase-client.js  # Supabase CRUD (conversation_tags, evidence, assignments)
│   ├── csv-parser.js       # V2 CSV parser (conversation_id, scores, etc.)
│   └── app.js              # Conversation-level flow, round-robin, admin dashboard
└── sql/
    ├── schema.sql          # Original schema (deprecated)
    ├── schema_v2.sql       # Message assignments (deprecated)
    └── schema_v3.sql       # Current: conversation_tags, message_evidence, conversation_assignments
```

## Assignment Logic

- Each new judge gets ~25% of conversations (auto-calculated: `2 × total / numJudges`)
- Each conversation gets exactly 2 judges
- If 2 judges disagree, the conversation is auto-assigned to **Andrew Abishek** as tiebreaker
- Ground truth and classifier scores are stored but hidden from judges during tagging

## Keyboard Shortcuts

| Key     | Action                         |
| ------- | ------------------------------ |
| `Enter` | Save & go to next conversation |
| `←`     | Previous conversation          |
| `→`     | Next conversation              |

## Data Flow

CSV → Parser splits into messages → Stored in Supabase → Judges tag via UI → Export CSV/JSON

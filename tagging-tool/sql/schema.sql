-- ============================================================
-- Supabase Schema for Human Tagging Tool
-- Run this in your Supabase SQL Editor (https://app.supabase.com)
-- ============================================================

-- 1. Conversations table: stores parsed conversation windows
CREATE TABLE conversations (
  id BIGSERIAL PRIMARY KEY,
  source_row_index INT NOT NULL,          -- row index from original CSV
  title TEXT,                              -- conversation title/group
  datetime TIMESTAMPTZ,                   -- original DateTime column
  thread_id TEXT,                          -- ThreadId if present
  full_conversation TEXT NOT NULL,         -- raw conversation text (for context panel)
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Messages table: individual messages parsed from conversations
CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  conversation_id BIGINT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  message_index INT NOT NULL,             -- order within conversation (0-based)
  speaker_name TEXT NOT NULL,             -- extracted speaker name
  message_text TEXT NOT NULL,             -- message content (without speaker name)
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(conversation_id, message_index)
);

-- 3. Tags table: human judge annotations at message level
CREATE TABLE tags (
  id BIGSERIAL PRIMARY KEY,
  message_id BIGINT NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  judge_name TEXT NOT NULL,               -- judge alias/name
  has_task BOOLEAN NOT NULL,              -- TRUE or FALSE
  task_category TEXT,                     -- only set when has_task = TRUE
  confidence TEXT DEFAULT 'medium',       -- low / medium / high
  notes TEXT,                             -- optional free-text notes
  tagged_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(message_id, judge_name)         -- one tag per judge per message
);

-- 4. Judge sessions: track who is tagging
CREATE TABLE judge_sessions (
  id BIGSERIAL PRIMARY KEY,
  judge_name TEXT NOT NULL,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  last_active_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_tags_message ON tags(message_id);
CREATE INDEX idx_tags_judge ON tags(judge_name);
CREATE INDEX idx_tags_message_judge ON tags(message_id, judge_name);

-- Enable Row Level Security (RLS)
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE judge_sessions ENABLE ROW LEVEL SECURITY;

-- RLS Policies: allow all operations via anon key (simple alias auth)
-- For a production system, replace with proper auth policies
CREATE POLICY "Allow all reads" ON conversations FOR SELECT USING (true);
CREATE POLICY "Allow all inserts" ON conversations FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow all reads" ON messages FOR SELECT USING (true);
CREATE POLICY "Allow all inserts" ON messages FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow all reads" ON tags FOR SELECT USING (true);
CREATE POLICY "Allow all inserts" ON tags FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow all updates" ON tags FOR UPDATE USING (true);

CREATE POLICY "Allow all reads" ON judge_sessions FOR SELECT USING (true);
CREATE POLICY "Allow all inserts" ON judge_sessions FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow all updates" ON judge_sessions FOR UPDATE USING (true);

-- Allowed task categories (for reference / validation)
-- Action Request, Review/Approval, Scheduling Action, Delegation,
-- Question, Confirmation/Permission, Availability/RSVP,
-- Status Request, Decision Request, Follow-up

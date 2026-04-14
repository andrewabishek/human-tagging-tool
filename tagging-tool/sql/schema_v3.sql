-- ============================================================
-- Schema v3: Conversation-Level Tagging
-- Run in Supabase SQL Editor
-- ============================================================

-- Step 1: Drop old tables (reverse dependency order)
DROP TABLE IF EXISTS message_assignments CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS judge_sessions CASCADE;

-- ============================================================
-- 1. Conversations
-- ============================================================
CREATE TABLE conversations (
  id BIGSERIAL PRIMARY KEY,
  source_row_index INT NOT NULL,
  conversation_id TEXT,                   -- UUID from V2 CSV
  topic TEXT,                             -- conversation_topic
  chat_type TEXT,                         -- OneOnOne / Group / Meeting
  full_conversation TEXT NOT NULL,        -- raw Conversation body
  ground_truth_has_task BOOLEAN,          -- HasTask-GroundTruth (hidden from judges)
  action_score NUMERIC,                   -- LLM classifier scores (admin only)
  commitment_score NUMERIC,
  knowledge_score NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 2. Messages (parsed from conversation body)
-- ============================================================
CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  conversation_id BIGINT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  message_index INT NOT NULL,
  speaker_name TEXT NOT NULL,
  message_text TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(conversation_id, message_index)
);

-- ============================================================
-- 3. Conversation Tags (judge annotations at conversation level)
-- ============================================================
CREATE TABLE conversation_tags (
  id BIGSERIAL PRIMARY KEY,
  conversation_id BIGINT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  judge_name TEXT NOT NULL,
  has_task BOOLEAN NOT NULL,
  is_important BOOLEAN NOT NULL,
  notes TEXT,
  tagged_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(conversation_id, judge_name)
);

-- ============================================================
-- 4. Message Evidence (which messages support the tag)
-- ============================================================
CREATE TABLE message_evidence (
  id BIGSERIAL PRIMARY KEY,
  conversation_tag_id BIGINT NOT NULL REFERENCES conversation_tags(id) ON DELETE CASCADE,
  message_id BIGINT NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  evidence_type TEXT NOT NULL,            -- 'has_task' or 'is_important'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(conversation_tag_id, message_id, evidence_type)
);

-- ============================================================
-- 5. Conversation Assignments (round-robin)
-- ============================================================
CREATE TABLE conversation_assignments (
  id BIGSERIAL PRIMARY KEY,
  conversation_id BIGINT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  judge_name TEXT NOT NULL,
  is_tiebreaker BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(conversation_id, judge_name)
);

-- ============================================================
-- 6. Judge Sessions
-- ============================================================
CREATE TABLE judge_sessions (
  id BIGSERIAL PRIMARY KEY,
  judge_name TEXT NOT NULL UNIQUE,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  last_active_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Indexes
-- ============================================================
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_conv_tags_conversation ON conversation_tags(conversation_id);
CREATE INDEX idx_conv_tags_judge ON conversation_tags(judge_name);
CREATE INDEX idx_evidence_tag ON message_evidence(conversation_tag_id);
CREATE INDEX idx_evidence_message ON message_evidence(message_id);
CREATE INDEX idx_conv_assignments_conversation ON conversation_assignments(conversation_id);
CREATE INDEX idx_conv_assignments_judge ON conversation_assignments(judge_name);

-- ============================================================
-- Row Level Security
-- ============================================================
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE message_evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE judge_sessions ENABLE ROW LEVEL SECURITY;

-- Allow all operations via anon key (alias-based auth)
CREATE POLICY "anon_all" ON conversations FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "anon_all" ON messages FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "anon_all" ON conversation_tags FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "anon_all" ON message_evidence FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "anon_all" ON conversation_assignments FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "anon_all" ON judge_sessions FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- Pre-seed first judge
-- ============================================================
INSERT INTO judge_sessions (judge_name) VALUES ('Andrew Abishek');

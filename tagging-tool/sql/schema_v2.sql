-- ============================================================
-- Schema Migration v2: Message Assignments + Round-Robin
-- Run this in your Supabase SQL Editor AFTER schema.sql
-- ============================================================

-- Message assignments: tracks which judge is assigned which messages
CREATE TABLE message_assignments (
  id BIGSERIAL PRIMARY KEY,
  message_id BIGINT NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  judge_name TEXT NOT NULL,
  is_tiebreaker BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(message_id, judge_name)
);

CREATE INDEX idx_assignments_message ON message_assignments(message_id);
CREATE INDEX idx_assignments_judge ON message_assignments(judge_name);

ALTER TABLE message_assignments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all reads" ON message_assignments FOR SELECT USING (true);
CREATE POLICY "Allow all inserts" ON message_assignments FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow all updates" ON message_assignments FOR UPDATE USING (true);
CREATE POLICY "Allow all deletes" ON message_assignments FOR DELETE USING (true);

-- Add unique constraint on judge_sessions for upsert support
ALTER TABLE judge_sessions ADD CONSTRAINT judge_sessions_judge_name_key UNIQUE (judge_name);

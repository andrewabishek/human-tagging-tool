-- ============================================================
-- Migration v3.1: Add task_type + attribution columns,
--                 clear stale assignments (round-robin bug)
-- Run in Supabase SQL Editor
-- ============================================================

-- 1. Add new columns to conversation_tags
ALTER TABLE conversation_tags ADD COLUMN IF NOT EXISTS task_type TEXT;
ALTER TABLE conversation_tags ADD COLUMN IF NOT EXISTS attribution TEXT;

-- 2. Clear all assignments (round-robin bug assigned all 116 to every judge)
DELETE FROM conversation_assignments;

-- 3. Clear any tags if any were saved during broken state
-- (only run this if you want a clean slate — comment out if you want to keep existing tags)
DELETE FROM message_evidence;
DELETE FROM conversation_tags;

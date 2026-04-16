-- Migration v3.2: Add task_assignees column to conversation_tags
-- Run this in the Supabase SQL Editor

ALTER TABLE conversation_tags
ADD COLUMN IF NOT EXISTS task_assignees TEXT;

-- task_assignees stores a JSON array of assignee names, e.g. '["Alice","Bob"]'
-- NULL when has_task = FALSE

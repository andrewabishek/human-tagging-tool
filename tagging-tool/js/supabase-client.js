// ============================================================
// Supabase Client — v3 Conversation-Level Tagging
// ============================================================

const SUPABASE_URL = "https://prcewohktalsbmyvrpgd.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_bfJATnCT_90xvFbutYxL8g_nIJcJU0x";

let db = null;

function initSupabase() {
  if (!window.supabase) {
    console.error("Supabase JS library not loaded");
    return false;
  }
  db = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  return true;
}

// ---- Conversations ----

async function insertConversations(conversations) {
  const batchSize = 50;
  const results = [];
  for (let i = 0; i < conversations.length; i += batchSize) {
    const batch = conversations.slice(i, i + batchSize);
    const { data, error } = await db
      .from("conversations")
      .insert(batch)
      .select();
    if (error) throw error;
    results.push(...data);
  }
  return results;
}

async function getConversations() {
  const { data, error } = await db
    .from("conversations")
    .select("*")
    .order("source_row_index", { ascending: true });
  if (error) throw error;
  return data;
}

// ---- Messages ----

async function insertMessages(messages) {
  const batchSize = 100;
  const results = [];
  for (let i = 0; i < messages.length; i += batchSize) {
    const batch = messages.slice(i, i + batchSize);
    const { data, error } = await db.from("messages").insert(batch).select();
    if (error) throw error;
    results.push(...data);
  }
  return results;
}

async function getMessagesByConversation(conversationId) {
  const { data, error } = await db
    .from("messages")
    .select("*")
    .eq("conversation_id", conversationId)
    .order("message_index", { ascending: true });
  if (error) throw error;
  return data;
}

// ---- Conversation Tags ----

async function upsertConversationTag(tag) {
  const { data, error } = await db
    .from("conversation_tags")
    .upsert(tag, { onConflict: "conversation_id,judge_name" })
    .select();
  if (error) throw error;
  return data;
}

async function getConversationTagsByJudge(judgeName) {
  const { data, error } = await db
    .from("conversation_tags")
    .select("*")
    .eq("judge_name", judgeName);
  if (error) throw error;
  return data;
}

async function getAllConversationTags() {
  const { data, error } = await db
    .from("conversation_tags")
    .select("*, conversations(topic, chat_type, source_row_index)");
  if (error) throw error;
  return data;
}

// ---- Message Evidence ----

async function upsertEvidence(conversationTagId, messageId, evidenceType) {
  const { data, error } = await db
    .from("message_evidence")
    .upsert(
      {
        conversation_tag_id: conversationTagId,
        message_id: messageId,
        evidence_type: evidenceType,
      },
      { onConflict: "conversation_tag_id,message_id,evidence_type" },
    )
    .select();
  if (error) throw error;
  return data;
}

async function deleteEvidence(conversationTagId, messageId, evidenceType) {
  const { error } = await db
    .from("message_evidence")
    .delete()
    .eq("conversation_tag_id", conversationTagId)
    .eq("message_id", messageId)
    .eq("evidence_type", evidenceType);
  if (error) throw error;
}

async function getEvidenceForTag(conversationTagId) {
  const { data, error } = await db
    .from("message_evidence")
    .select("*")
    .eq("conversation_tag_id", conversationTagId);
  if (error) throw error;
  return data;
}

async function getAllEvidence() {
  const { data, error } = await db.from("message_evidence").select("*");
  if (error) throw error;
  return data;
}

// ---- Conversation Assignments ----

async function getAssignmentsForJudge(judgeName) {
  const { data, error } = await db
    .from("conversation_assignments")
    .select("*, conversations(*)")
    .eq("judge_name", judgeName)
    .order("conversation_id", { ascending: true });
  if (error) throw error;
  return data;
}

async function getAllAssignments() {
  const { data, error } = await db.from("conversation_assignments").select("*");
  if (error) throw error;
  return data;
}

async function insertAssignments(assignments) {
  const batchSize = 100;
  const results = [];
  for (let i = 0; i < assignments.length; i += batchSize) {
    const batch = assignments.slice(i, i + batchSize);
    const { data, error } = await db
      .from("conversation_assignments")
      .insert(batch)
      .select();
    if (error) throw error;
    results.push(...data);
  }
  return results;
}

// ---- Judge Sessions ----

async function getExistingJudges() {
  const { data, error } = await db
    .from("judge_sessions")
    .select("judge_name")
    .order("judge_name");
  if (error) throw error;
  return data.map((j) => j.judge_name);
}

async function createOrUpdateJudgeSession(judgeName) {
  const { data, error } = await db
    .from("judge_sessions")
    .upsert(
      { judge_name: judgeName, last_active_at: new Date().toISOString() },
      { onConflict: "judge_name", ignoreDuplicates: false },
    )
    .select();
  if (error) throw error;
  return data;
}

// ---- Admin: Stats ----

async function getAdminStats() {
  const convs = await getConversations();
  const assignments = await getAllAssignments();
  const tags = await getAllConversationTags();
  const evidence = await getAllEvidence();
  return { conversations: convs, assignments, tags, evidence };
}



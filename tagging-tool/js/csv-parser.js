// ============================================================
// CSV Parser — V2 format: conversation_id, conversation_topic,
// chat_type, Conversation body, HasTask-GroundTruth, scores
// ============================================================

/**
 * Parse a CSV string into rows of arrays.
 * Handles quoted fields with commas and newlines.
 */
function parseCSV(csvText) {
  const rows = [];
  let current = '';
  let inQuotes = false;
  let row = [];

  for (let i = 0; i < csvText.length; i++) {
    const ch = csvText[i];
    const next = csvText[i + 1];

    if (inQuotes) {
      if (ch === '"' && next === '"') {
        current += '"';
        i++;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        current += ch;
      }
    } else {
      if (ch === '"') {
        inQuotes = true;
      } else if (ch === ',') {
        row.push(current.trim());
        current = '';
      } else if (ch === '\n' || (ch === '\r' && next === '\n')) {
        row.push(current.trim());
        current = '';
        if (row.length > 1 || row[0] !== '') {
          rows.push(row);
        }
        row = [];
        if (ch === '\r') i++;
      } else {
        current += ch;
      }
    }
  }
  row.push(current.trim());
  if (row.length > 1 || row[0] !== '') {
    rows.push(row);
  }

  return rows;
}

/**
 * Parse conversation body into individual messages.
 * Format: "SpeakerName\n\n:Message text\n\nSpeakerName\n\n:Message text..."
 */
function parseConversationIntoMessages(conversationText) {
  if (!conversationText || !conversationText.trim()) return [];

  const messages = [];
  const lines = conversationText.split('\n');

  let currentSpeaker = null;
  let currentText = [];
  let messageIndex = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    if (line.startsWith(':')) {
      const text = line.substring(1).trim();
      if (text) currentText.push(text);
    } else if (isLikelySpeakerName(line)) {
      if (currentSpeaker && currentText.length > 0) {
        messages.push({
          speaker: currentSpeaker,
          text: currentText.join(' ').trim(),
          index: messageIndex++
        });
        currentText = [];
      }
      currentSpeaker = line;
    } else {
      if (currentSpeaker) currentText.push(line);
    }
  }

  if (currentSpeaker && currentText.length > 0) {
    messages.push({
      speaker: currentSpeaker,
      text: currentText.join(' ').trim(),
      index: messageIndex++
    });
  }

  return messages;
}

/**
 * Heuristic: check if a line looks like a speaker name.
 */
function isLikelySpeakerName(line) {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith(':')) return false;
  const words = trimmed.split(/\s+/);
  if (words.length > 4 || words.length === 0) return false;
  const alphaRatio = trimmed.replace(/[^a-zA-Z\s]/g, '').length / trimmed.length;
  return alphaRatio > 0.7;
}

/**
 * Process V2 CSV into structured conversations + messages.
 * Expected columns: conversation_id, conversation_topic, chat_type,
 *   Conversation body, HasTask-GroundTruth, action_score, commitment_score, knowledge_score
 */
function processCSVData(csvText) {
  const rows = parseCSV(csvText);
  if (rows.length < 2) {
    throw new Error('CSV must have a header row and at least one data row');
  }

  const headers = rows[0].map(h => h.trim());

  // Map column indices — support both V2 and legacy formats
  const col = (name) => headers.indexOf(name);
  const bodyIdx = col('Conversation body') >= 0 ? col('Conversation body') : col('Conversation');
  const topicIdx = col('conversation_topic') >= 0 ? col('conversation_topic') : col('Title');
  const convIdIdx = col('conversation_id');
  const chatTypeIdx = col('chat_type');
  const gtIdx = col('HasTask-GroundTruth');
  const actionIdx = col('action_score');
  const commitIdx = col('commitment_score');
  const knowledgeIdx = col('knowledge_score');

  if (bodyIdx === -1) {
    throw new Error('CSV must have a "Conversation body" or "Conversation" column');
  }

  const conversations = [];
  const allMessages = [];

  for (let r = 1; r < rows.length; r++) {
    const row = rows[r];
    const convText = row[bodyIdx] || '';
    if (!convText.trim()) continue;

    // Parse ground truth — accept TRUE/FALSE/True/False/1/0
    let gt = null;
    if (gtIdx >= 0 && row[gtIdx] !== undefined && row[gtIdx] !== '') {
      const raw = row[gtIdx].trim().toUpperCase();
      gt = raw === 'TRUE' || raw === '1';
    }

    const conv = {
      source_row_index: r - 1,
      conversation_id: convIdIdx >= 0 ? (row[convIdIdx] || '') : '',
      topic: topicIdx >= 0 ? (row[topicIdx] || '') : '',
      chat_type: chatTypeIdx >= 0 ? (row[chatTypeIdx] || '') : '',
      full_conversation: convText,
      ground_truth_has_task: gt,
      action_score: actionIdx >= 0 ? parseFloat(row[actionIdx]) || null : null,
      commitment_score: commitIdx >= 0 ? parseFloat(row[commitIdx]) || null : null,
      knowledge_score: knowledgeIdx >= 0 ? parseFloat(row[knowledgeIdx]) || null : null
    };
    conversations.push(conv);

    const msgs = parseConversationIntoMessages(convText);
    msgs.forEach(msg => {
      allMessages.push({
        _conv_index: conversations.length - 1,
        message_index: msg.index,
        speaker_name: msg.speaker,
        message_text: msg.text
      });
    });
  }

  return { conversations, messages: allMessages };
}

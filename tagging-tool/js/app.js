// ============================================================
// Main Application — v3 Conversation-Level Tagging
// ============================================================

// ---- Constants ----
const ADMIN_JUDGE = "Andrew Abishek";
const JUDGES_PER_CONV = 2;
const MAX_PER_JUDGE = 25;

// ---- State ----
let currentJudgeName = "";
let assignedConversations = []; // conversations assigned to this judge
let currentConvIdx = 0; // index into assignedConversations
let currentConvMessages = []; // messages for current conversation
let judgeTags = {}; // conversationId -> { has_task, is_important, notes, id }
let evidenceState = {}; // messageId -> Set('has_task','is_important')
let currentTagId = null; // DB id of current conversation_tag row
let isSupabaseReady = false;
let isAdmin = false;

// ---- Initialization ----

document.addEventListener("DOMContentLoaded", () => {
  const hash = window.location.hash;

  if (hash === "#admin") {
    isAdmin = true;
    initAdminMode();
    return;
  }
  if (hash === "#upload") {
    showScreen("upload");
    initSupabaseIfNeeded();
    setupUploadHandlers();
    return;
  }

  // Normal tagging mode
  initSupabaseIfNeeded();
  loadExistingJudges().catch(() => {});
  setupLoginHandlers();
  setupKeyboardShortcuts();
});

function initSupabaseIfNeeded() {
  if (!isSupabaseReady) {
    try {
      isSupabaseReady = initSupabase();
    } catch (e) {
      console.warn("Supabase init error:", e);
    }
  }
}

async function loadExistingJudges() {
  if (!isSupabaseReady) return;
  try {
    const judges = await getExistingJudges();
    const select = document.getElementById("judge-select");
    if (judges.length > 0) {
      document
        .getElementById("existing-judges-section")
        .classList.remove("hidden");
      judges.forEach((name) => {
        const opt = document.createElement("option");
        opt.value = name;
        opt.textContent = name;
        select.appendChild(opt);
      });
      const saved = localStorage.getItem("hastask_judge_name");
      if (saved && judges.includes(saved)) {
        select.value = saved;
        document.getElementById("login-btn").disabled = false;
      }
    }
  } catch (e) {
    console.warn("Could not load judges:", e);
  }
}

function setupLoginHandlers() {
  const nameInput = document.getElementById("judge-name-input");
  const judgeSelect = document.getElementById("judge-select");

  function updateLoginBtn() {
    document.getElementById("login-btn").disabled = !(
      nameInput.value.trim() || judgeSelect.value
    );
  }

  nameInput.addEventListener("input", () => {
    if (nameInput.value.trim()) judgeSelect.value = "";
    updateLoginBtn();
  });
  nameInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") startSession();
  });
  judgeSelect.addEventListener("change", () => {
    if (judgeSelect.value) nameInput.value = "";
    updateLoginBtn();
  });
  document.getElementById("login-btn").addEventListener("click", startSession);
}

function setupKeyboardShortcuts() {
  document.addEventListener("keydown", (e) => {
    if (
      e.target.tagName === "INPUT" ||
      e.target.tagName === "TEXTAREA" ||
      e.target.tagName === "SELECT"
    ) {
      if (e.key === "Enter" && e.ctrlKey && e.target.id === "notes-input") {
        e.preventDefault();
        saveAndNext();
      }
      return;
    }
    switch (e.key) {
      case "ArrowLeft":
        e.preventDefault();
        navigateConv(-1);
        break;
      case "ArrowRight":
        e.preventDefault();
        navigateConv(1);
        break;
      case "Enter":
        e.preventDefault();
        saveAndNext();
        break;
    }
  });
}

// ---- Screen Management ----

function showScreen(screen) {
  ["login-screen", "app-screen", "upload-screen", "admin-screen"].forEach(
    (id) => {
      const el = document.getElementById(id);
      if (el) el.classList.toggle("hidden", id !== screen + "-screen");
    },
  );
}

// ---- Session ----

async function startSession() {
  const selectVal = document.getElementById("judge-select").value;
  const inputVal = document.getElementById("judge-name-input").value.trim();
  const name = selectVal || inputVal;
  if (!name) {
    showToast("Please enter or select a name", "error");
    return;
  }

  currentJudgeName = name;
  localStorage.setItem("hastask_judge_name", name);

  document.getElementById("login-btn").disabled = true;
  document.getElementById("login-btn").textContent = "Connecting...";

  try {
    initSupabaseIfNeeded();
    if (!isSupabaseReady) throw new Error("Supabase not loaded");
    await db.from("conversations").select("id", { count: "exact", head: true });
  } catch (e) {
    showToast("Connection failed: " + e.message, "error");
    document.getElementById("login-btn").disabled = false;
    document.getElementById("login-btn").textContent = "Start Tagging";
    return;
  }

  showScreen("app");
  document.getElementById("judge-display-name").textContent = name;

  // Show admin link if this is the admin judge
  const adminLink = document.getElementById("admin-link");
  if (adminLink && name === ADMIN_JUDGE) adminLink.classList.remove("hidden");

  await loadData();
}

async function loadData() {
  showLoadingState(true);
  try {
    await createOrUpdateJudgeSession(currentJudgeName);
  } catch (e) {
    /* non-critical */
  }

  try {
    // Run round-robin assignment
    await autoAssignConversations(currentJudgeName);

    // Load this judge's assigned conversations
    const assignments = await getAssignmentsForJudge(currentJudgeName);
    assignedConversations = assignments.map((a) => ({
      ...a.conversations,
      is_tiebreaker: a.is_tiebreaker,
    }));

    if (assignedConversations.length === 0) {
      showToast("No conversations assigned yet.", "info");
      showLoadingState(false);
      return;
    }

    // Load existing tags
    const existingTags = await getConversationTagsByJudge(currentJudgeName);
    judgeTags = {};
    existingTags.forEach((t) => {
      judgeTags[t.conversation_id] = t;
    });

    // Find first untagged
    currentConvIdx = findNextUntagged(0);
    if (currentConvIdx === -1) currentConvIdx = 0;

    updateProgress();
    await renderCurrentConversation();
  } catch (e) {
    showToast("Error loading data: " + e.message, "error");
    console.error(e);
  }
  showLoadingState(false);
}

// ---- Round-Robin Assignment ----

async function autoAssignConversations(judgeName) {
  const allConvs = await getConversations();
  const allAssigns = await getAllAssignments();
  const allTags = await getAllConversationTags();

  // Build per-conversation info
  const convInfo = {};
  allConvs.forEach((c) => {
    convInfo[c.id] = { assignCount: 0, assignedTo: [], tags: [] };
  });
  allAssigns.forEach((a) => {
    if (convInfo[a.conversation_id]) {
      convInfo[a.conversation_id].assignCount++;
      convInfo[a.conversation_id].assignedTo.push(a.judge_name);
    }
  });
  allTags.forEach((t) => {
    if (convInfo[t.conversation_id]) {
      convInfo[t.conversation_id].tags.push(t);
    }
  });

  const myAssignments = allAssigns.filter((a) => a.judge_name === judgeName);

  // --- Tiebreaker detection (for admin only) ---
  if (judgeName === ADMIN_JUDGE) {
    const tiebreakerIds = [];
    Object.keys(convInfo).forEach((cid) => {
      const info = convInfo[cid];
      if (info.tags.length >= 2 && !info.assignedTo.includes(judgeName)) {
        const htVals = info.tags.map((t) => t.has_task);
        const iiVals = info.tags.map((t) => t.is_important);
        if (
          htVals.some((v) => v !== htVals[0]) ||
          iiVals.some((v) => v !== iiVals[0])
        ) {
          tiebreakerIds.push(parseInt(cid));
        }
      }
    });
    if (tiebreakerIds.length > 0) {
      const tbAssigns = tiebreakerIds.map((cid) => ({
        conversation_id: cid,
        judge_name: judgeName,
        is_tiebreaker: true,
      }));
      try {
        await insertAssignments(tbAssigns);
      } catch (e) {
        /* already assigned */
      }
    }
  }

  // --- Initial round-robin (new judge) ---
  if (myAssignments.length === 0) {
    const available = allConvs.filter((c) => {
      const info = convInfo[c.id];
      return (
        info.assignCount < JUDGES_PER_CONV &&
        !info.assignedTo.includes(judgeName)
      );
    });

    if (available.length === 0) return;

    // Cap at MAX_PER_JUDGE conversations per judge
    // Prioritize conversations with 0 assignments, then 1
    const zeroAssign = available.filter(
      (c) => convInfo[c.id].assignCount === 0,
    );
    const oneAssign = available.filter((c) => convInfo[c.id].assignCount === 1);
    const pool = [...zeroAssign, ...oneAssign];

    // Offset start position by judge number so different judges get
    // different conversations at the front. This ensures max coverage
    // even when judges only complete partway through their batch.
    const existingJudgeNames = [
      ...new Set(allAssigns.map((a) => a.judge_name)),
    ];
    const judgeIndex = existingJudgeNames.length; // 0-based for new judge
    const offset = (judgeIndex * MAX_PER_JUDGE) % pool.length;
    const rotated = [...pool.slice(offset), ...pool.slice(0, offset)];
    const toAssign = rotated.slice(0, Math.min(MAX_PER_JUDGE, rotated.length));

    if (toAssign.length > 0) {
      const newAssigns = toAssign.map((c) => ({
        conversation_id: c.id,
        judge_name: judgeName,
        is_tiebreaker: false,
      }));
      await insertAssignments(newAssigns);
      showToast(`${toAssign.length} conversations assigned to you`, "success");
    }
  }
}

// ---- Rendering ----

async function renderCurrentConversation() {
  if (assignedConversations.length === 0) return;

  // Check if all done
  const allTagged = assignedConversations.every((c) => judgeTags[c.id]);
  if (allTagged) {
    document.getElementById("tagging-card").classList.add("hidden");
    document.getElementById("done-card").classList.remove("hidden");
    return;
  }
  document.getElementById("tagging-card").classList.remove("hidden");
  document.getElementById("done-card").classList.add("hidden");

  const conv = assignedConversations[currentConvIdx];
  if (!conv) return;

  // Update conversation header
  const topicEl = document.getElementById("conv-topic");
  const metaEl = document.getElementById("conv-meta");
  const counterEl = document.getElementById("conv-counter");

  topicEl.textContent =
    conv.topic || `Conversation ${conv.source_row_index + 1}`;
  metaEl.textContent = [
    conv.chat_type,
    conv.is_tiebreaker ? "⚖️ TIEBREAKER" : "",
  ]
    .filter(Boolean)
    .join(" · ");
  counterEl.textContent = `${currentConvIdx + 1} / ${assignedConversations.length}`;

  // Load messages for this conversation
  currentConvMessages = await getMessagesByConversation(conv.id);
  renderMessages();

  // Restore tag state
  const existing = judgeTags[conv.id];
  if (existing) {
    document.getElementById("btn-has-task-true").className =
      "toggle-btn" + (existing.has_task ? " active-true" : "");
    document.getElementById("btn-has-task-false").className =
      "toggle-btn" + (!existing.has_task ? " active-false" : "");
    document.getElementById("btn-important-true").className =
      "toggle-btn" + (existing.is_important ? " active-true" : "");
    document.getElementById("btn-important-false").className =
      "toggle-btn" + (!existing.is_important ? " active-false" : "");
    document.getElementById("notes-input").value = existing.notes || "";
    currentTagId = existing.id;

    // Restore task type + attribution dropdowns
    document.getElementById("task-type-select").value =
      existing.task_type || "";
    document.getElementById("attribution-select").value =
      existing.attribution || "";
    document
      .getElementById("task-type-group")
      .classList.toggle("hidden", !existing.has_task);
    document
      .getElementById("attribution-group")
      .classList.toggle("hidden", !existing.has_task);

    // Load evidence
    evidenceState = {};
    try {
      const evRows = await getEvidenceForTag(existing.id);
      evRows.forEach((ev) => {
        if (!evidenceState[ev.message_id])
          evidenceState[ev.message_id] = new Set();
        evidenceState[ev.message_id].add(ev.evidence_type);
      });
    } catch (e) {
      console.warn("Evidence load error:", e);
    }
  } else {
    resetTagUI();
    evidenceState = {};
    currentTagId = null;
  }

  updateEvidenceHighlights();

  // Nav buttons
  document.getElementById("btn-prev").disabled = currentConvIdx === 0;
  const isLast = currentConvIdx === assignedConversations.length - 1;
  document.getElementById("btn-save-next").textContent = isLast
    ? "Save ✓"
    : "Save & Next →";
}

/**
 * Highlight @mentions (explicit) and plain name references (implicit) in text.
 * Escapes HTML first to prevent XSS, then applies highlights.
 */
function highlightNames(text, speakerNames) {
  // Escape HTML entities
  let safe = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

  // 1. Highlight @mentions (explicit) — blue pill
  safe = safe.replace(
    /@(\w+)/g,
    '<span class="mention-explicit" title="Explicit @mention">@$1</span>',
  );

  // 2. Highlight plain name references (implicit) — subtle underline
  // Only match names that aren't already inside an @mention highlight
  speakerNames.forEach((name) => {
    // Match the name as a standalone word, not preceded by @ or already in a tag
    const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(
      `(?<!@)(?<![\\w])(?<!">)(${escaped})(?![<\\w])`,
      "gi",
    );
    safe = safe.replace(
      regex,
      '<span class="mention-implicit" title="Implicit name reference">$1</span>',
    );
  });

  return safe;
}

function renderMessages() {
  const container = document.getElementById("conversation-messages");
  container.innerHTML = "";

  // Collect all speaker names for implicit name detection
  const speakerNames = [
    ...new Set(currentConvMessages.map((m) => m.speaker_name)),
  ];

  currentConvMessages.forEach((msg) => {
    const div = document.createElement("div");
    div.className = "conv-message";
    div.dataset.messageId = msg.id;

    const header = document.createElement("div");
    header.className = "msg-header";

    const speaker = document.createElement("span");
    speaker.className = "speaker";
    speaker.textContent = msg.speaker_name;
    header.appendChild(speaker);

    const idx = document.createElement("span");
    idx.className = "msg-index";
    idx.textContent = `#${msg.message_index + 1}`;
    header.appendChild(idx);

    div.appendChild(header);

    const text = document.createElement("div");
    text.className = "msg-text";
    text.innerHTML = highlightNames(msg.message_text, speakerNames);
    div.appendChild(text);

    // Evidence buttons
    const btnRow = document.createElement("div");
    btnRow.className = "evidence-buttons";

    const btnTask = document.createElement("button");
    btnTask.className = "evidence-btn evidence-task";
    btnTask.textContent = "Task Evidence";
    btnTask.title = "Mark as evidence for HasTask";
    btnTask.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleEvidence(msg.id, "has_task");
    });

    const btnImp = document.createElement("button");
    btnImp.className = "evidence-btn evidence-important";
    btnImp.textContent = "Important Evidence";
    btnImp.title = "Mark as evidence for IsImportant";
    btnImp.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleEvidence(msg.id, "is_important");
    });

    btnRow.appendChild(btnTask);
    btnRow.appendChild(btnImp);
    div.appendChild(btnRow);

    container.appendChild(div);
  });
}

function toggleEvidence(messageId, type) {
  if (!evidenceState[messageId]) evidenceState[messageId] = new Set();
  if (evidenceState[messageId].has(type)) {
    evidenceState[messageId].delete(type);
  } else {
    evidenceState[messageId].add(type);
  }
  updateEvidenceHighlights();
}

function updateEvidenceHighlights() {
  document.querySelectorAll(".conv-message").forEach((div) => {
    const mid = parseInt(div.dataset.messageId);
    const ev = evidenceState[mid] || new Set();

    div.classList.toggle("evidence-has-task", ev.has("has_task"));
    div.classList.toggle("evidence-is-important", ev.has("is_important"));

    const taskBtn = div.querySelector(".evidence-task");
    const impBtn = div.querySelector(".evidence-important");
    if (taskBtn) taskBtn.classList.toggle("active", ev.has("has_task"));
    if (impBtn) impBtn.classList.toggle("active", ev.has("is_important"));
  });

  // Update evidence counts
  let taskCount = 0,
    impCount = 0;
  Object.values(evidenceState).forEach((s) => {
    if (s.has("has_task")) taskCount++;
    if (s.has("is_important")) impCount++;
  });
  const countEl = document.getElementById("evidence-count");
  if (countEl)
    countEl.textContent = `${taskCount} task · ${impCount} important evidence`;
}

function resetTagUI() {
  document.getElementById("btn-has-task-true").className = "toggle-btn";
  document.getElementById("btn-has-task-false").className = "toggle-btn";
  document.getElementById("btn-important-true").className = "toggle-btn";
  document.getElementById("btn-important-false").className = "toggle-btn";
  document.getElementById("notes-input").value = "";
  document.getElementById("task-type-select").value = "";
  document.getElementById("attribution-select").value = "";
  document.getElementById("task-type-group").classList.add("hidden");
  document.getElementById("attribution-group").classList.add("hidden");
}

// ---- Tag Actions ----

function setHasTask(value) {
  document.getElementById("btn-has-task-true").className =
    "toggle-btn" + (value ? " active-true" : "");
  document.getElementById("btn-has-task-false").className =
    "toggle-btn" + (!value ? " active-false" : "");
  // Show/hide task type + attribution dropdowns
  document.getElementById("task-type-group").classList.toggle("hidden", !value);
  document
    .getElementById("attribution-group")
    .classList.toggle("hidden", !value);
}

function setIsImportant(value) {
  document.getElementById("btn-important-true").className =
    "toggle-btn" + (value ? " active-true" : "");
  document.getElementById("btn-important-false").className =
    "toggle-btn" + (!value ? " active-false" : "");
}

function getHasTaskValue() {
  if (
    document
      .getElementById("btn-has-task-true")
      .classList.contains("active-true")
  )
    return true;
  if (
    document
      .getElementById("btn-has-task-false")
      .classList.contains("active-false")
  )
    return false;
  return null;
}

function getIsImportantValue() {
  if (
    document
      .getElementById("btn-important-true")
      .classList.contains("active-true")
  )
    return true;
  if (
    document
      .getElementById("btn-important-false")
      .classList.contains("active-false")
  )
    return false;
  return null;
}

// ---- Save & Navigate ----

async function saveAndNext() {
  const conv = assignedConversations[currentConvIdx];
  if (!conv) return;

  const hasTask = getHasTaskValue();
  const isImportant = getIsImportantValue();

  if (hasTask === null) {
    showToast("Please select HasTask", "error");
    return;
  }
  if (isImportant === null) {
    showToast("Please select IsImportant", "error");
    return;
  }

  // Validate task_type + attribution when HasTask = TRUE
  const taskType = document.getElementById("task-type-select").value;
  const attribution = document.getElementById("attribution-select").value;
  if (hasTask) {
    if (!taskType) {
      showToast("Please select Task Type", "error");
      return;
    }
    if (!attribution) {
      showToast("Please select Attribution", "error");
      return;
    }
  }

  const notes = document.getElementById("notes-input").value.trim();

  // Save conversation tag
  const tag = {
    conversation_id: conv.id,
    judge_name: currentJudgeName,
    has_task: hasTask,
    is_important: isImportant,
    task_type: hasTask ? taskType : null,
    attribution: hasTask ? attribution : null,
    notes: notes || null,
    updated_at: new Date().toISOString(),
  };

  try {
    const saved = await upsertConversationTag(tag);
    const savedTag = saved[0];
    judgeTags[conv.id] = savedTag;
    currentTagId = savedTag.id;

    // Save evidence — delete old, insert new
    const oldEvidence = await getEvidenceForTag(savedTag.id);
    // Build sets for comparison
    const newEvSet = new Set();
    Object.entries(evidenceState).forEach(([mid, types]) => {
      types.forEach((t) => newEvSet.add(`${mid}:${t}`));
    });
    const oldEvSet = new Set(
      oldEvidence.map((e) => `${e.message_id}:${e.evidence_type}`),
    );

    // Delete removed evidence
    for (const old of oldEvidence) {
      const key = `${old.message_id}:${old.evidence_type}`;
      if (!newEvSet.has(key)) {
        await deleteEvidence(savedTag.id, old.message_id, old.evidence_type);
      }
    }
    // Insert new evidence
    for (const [mid, types] of Object.entries(evidenceState)) {
      for (const t of types) {
        const key = `${mid}:${t}`;
        if (!oldEvSet.has(key)) {
          await upsertEvidence(savedTag.id, parseInt(mid), t);
        }
      }
    }

    showToast("Saved", "success");
  } catch (e) {
    showToast("Save failed: " + e.message, "error");
    console.error(e);
    return;
  }

  updateProgress();

  // Navigate to next untagged
  if (currentConvIdx < assignedConversations.length - 1) {
    const next = findNextUntagged(currentConvIdx + 1);
    currentConvIdx = next >= 0 ? next : currentConvIdx + 1;
    await renderCurrentConversation();
  } else {
    await renderCurrentConversation();
  }
}

function navigateConv(delta) {
  const newIdx = currentConvIdx + delta;
  if (newIdx >= 0 && newIdx < assignedConversations.length) {
    currentConvIdx = newIdx;
    renderCurrentConversation();
  }
}

function findNextUntagged(startIdx) {
  for (let i = startIdx; i < assignedConversations.length; i++) {
    if (!judgeTags[assignedConversations[i].id]) return i;
  }
  return -1;
}

function updateProgress() {
  const total = assignedConversations.length;
  const tagged = assignedConversations.filter((c) => judgeTags[c.id]).length;
  document.getElementById("progress-badge").textContent =
    `${tagged} / ${total} conversations`;
}

// ---- Export ----

function exportCSV() {
  if (assignedConversations.length === 0) {
    showToast("No data", "error");
    return;
  }

  const headers = [
    "conversation_id",
    "topic",
    "chat_type",
    "source_row_index",
    "has_task",
    "task_type",
    "attribution",
    "is_important",
    "notes",
    "task_evidence_msg_indices",
    "important_evidence_msg_indices",
    "judge_name",
    "tagged_at",
  ];

  const rows = assignedConversations.map((conv) => {
    const tag = judgeTags[conv.id] || {};
    const taskEv = [],
      impEv = [];
    Object.entries(evidenceState).forEach(([mid, types]) => {
      const msg = currentConvMessages.find((m) => m.id === parseInt(mid));
      if (msg) {
        if (types.has("has_task")) taskEv.push(msg.message_index);
        if (types.has("is_important")) impEv.push(msg.message_index);
      }
    });
    return [
      csvEscape(conv.conversation_id || ""),
      csvEscape(conv.topic || ""),
      conv.chat_type || "",
      conv.source_row_index,
      tag.has_task !== undefined ? tag.has_task : "",
      csvEscape(tag.task_type || ""),
      csvEscape(tag.attribution || ""),
      tag.is_important !== undefined ? tag.is_important : "",
      csvEscape(tag.notes || ""),
      taskEv.join(";"),
      impEv.join(";"),
      currentJudgeName,
      tag.tagged_at || tag.updated_at || "",
    ].join(",");
  });

  const csv = headers.join(",") + "\n" + rows.join("\n");
  downloadFile(
    csv,
    `conv_tags_${currentJudgeName}_${dateStamp()}.csv`,
    "text/csv",
  );
  showToast("CSV exported", "success");
}

function exportJSON() {
  if (assignedConversations.length === 0) {
    showToast("No data", "error");
    return;
  }

  const data = assignedConversations.map((conv) => {
    const tag = judgeTags[conv.id] || {};
    return {
      conversation_id: conv.conversation_id,
      topic: conv.topic,
      chat_type: conv.chat_type,
      has_task: tag.has_task ?? null,
      task_type: tag.task_type || null,
      attribution: tag.attribution || null,
      is_important: tag.is_important ?? null,
      notes: tag.notes || null,
      judge_name: currentJudgeName,
      tagged_at: tag.tagged_at || tag.updated_at || null,
    };
  });

  downloadFile(
    JSON.stringify(data, null, 2),
    `conv_tags_${currentJudgeName}_${dateStamp()}.json`,
    "application/json",
  );
  showToast("JSON exported", "success");
}

function csvEscape(str) {
  if (!str) return "";
  str = String(str);
  if (str.includes(",") || str.includes('"') || str.includes("\n")) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

function downloadFile(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function dateStamp() {
  return new Date().toISOString().slice(0, 10);
}

// ---- Admin Upload ----

let pendingCSVData = null;

function setupUploadHandlers() {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const uploadBtn = document.getElementById("upload-btn");

  dropZone.addEventListener("click", () => fileInput.click());
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
  });
  dropZone.addEventListener("dragleave", () =>
    dropZone.classList.remove("drag-over"),
  );
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
  });
  uploadBtn.addEventListener("click", uploadParsedData);
}

function handleFile(file) {
  if (!file.name.endsWith(".csv")) {
    setUploadStatus("Please select a .csv file", "error");
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const parsed = processCSVData(e.target.result);
      pendingCSVData = parsed;
      setUploadStatus(
        `Parsed ${parsed.conversations.length} conversations with ${parsed.messages.length} messages. Ready to upload.`,
        "success",
      );
      document.getElementById("upload-btn").disabled = false;
    } catch (err) {
      setUploadStatus("Parse error: " + err.message, "error");
      pendingCSVData = null;
    }
  };
  reader.readAsText(file, "utf-8");
}

async function uploadParsedData() {
  if (!pendingCSVData) return;
  initSupabaseIfNeeded();
  if (!isSupabaseReady) {
    setUploadStatus("Supabase init failed", "error");
    return;
  }

  setUploadStatus("Uploading conversations...", "");
  document.getElementById("upload-btn").disabled = true;

  try {
    const convData = pendingCSVData.conversations.map((c) => ({
      source_row_index: c.source_row_index,
      conversation_id: c.conversation_id,
      topic: c.topic,
      chat_type: c.chat_type,
      full_conversation: c.full_conversation,
      ground_truth_has_task: c.ground_truth_has_task,
      action_score: c.action_score,
      commitment_score: c.commitment_score,
      knowledge_score: c.knowledge_score,
    }));

    const insertedConvs = await insertConversations(convData);

    const messageData = pendingCSVData.messages.map((m) => ({
      conversation_id: insertedConvs[m._conv_index].id,
      message_index: m.message_index,
      speaker_name: m.speaker_name,
      message_text: m.message_text,
    }));

    setUploadStatus(`Uploading ${messageData.length} messages...`, "");
    await insertMessages(messageData);

    setUploadStatus(
      `Done! ${insertedConvs.length} conversations, ${messageData.length} messages uploaded.`,
      "success",
    );
    pendingCSVData = null;
  } catch (e) {
    setUploadStatus("Upload error: " + e.message, "error");
    document.getElementById("upload-btn").disabled = false;
    console.error(e);
  }
}

function setUploadStatus(text, type) {
  const el = document.getElementById("upload-status");
  el.textContent = text;
  el.className = "upload-status" + (type ? " " + type : "");
}

// ---- Admin Dashboard ----

async function initAdminMode() {
  showScreen("admin");
  initSupabaseIfNeeded();
  if (!isSupabaseReady) {
    document.getElementById("admin-content").innerHTML =
      "<p>Supabase connection failed.</p>";
    return;
  }
  document
    .getElementById("admin-refresh")
    .addEventListener("click", loadAdminDashboard);
  await loadAdminDashboard();
}

async function loadAdminDashboard() {
  const content = document.getElementById("admin-content");
  content.innerHTML = "<p>Loading dashboard...</p>";

  try {
    const { conversations, assignments, tags, evidence } =
      await getAdminStats();

    // Group by judge
    const judgeAssign = {};
    assignments.forEach((a) => {
      if (!judgeAssign[a.judge_name]) judgeAssign[a.judge_name] = [];
      judgeAssign[a.judge_name].push(a);
    });

    const judgeTags = {};
    tags.forEach((t) => {
      if (!judgeTags[t.judge_name]) judgeTags[t.judge_name] = [];
      judgeTags[t.judge_name].push(t);
    });

    // Build per-conversation tag map
    const convTagMap = {};
    tags.forEach((t) => {
      if (!convTagMap[t.conversation_id]) convTagMap[t.conversation_id] = [];
      convTagMap[t.conversation_id].push(t);
    });

    // Disagreements
    const disagreements = [];
    Object.entries(convTagMap).forEach(([cid, tgs]) => {
      if (tgs.length >= 2) {
        const htVals = tgs.map((t) => t.has_task);
        const iiVals = tgs.map((t) => t.is_important);
        if (
          htVals.some((v) => v !== htVals[0]) ||
          iiVals.some((v) => v !== iiVals[0])
        ) {
          const conv = conversations.find((c) => c.id === parseInt(cid));
          disagreements.push({ conv, tags: tgs });
        }
      }
    });

    // Coverage
    const totalConvs = conversations.length;
    const taggedConvIds = new Set(tags.map((t) => t.conversation_id));
    const fullyTagged = conversations.filter((c) => {
      const tgs = convTagMap[c.id] || [];
      return tgs.length >= JUDGES_PER_CONV;
    }).length;

    // Agreement vs ground truth
    let gtMatch = 0,
      gtMismatch = 0,
      gtNA = 0;
    conversations.forEach((c) => {
      if (c.ground_truth_has_task === null) {
        gtNA++;
        return;
      }
      const tgs = convTagMap[c.id] || [];
      if (tgs.length === 0) return;
      // majority vote
      const trueCount = tgs.filter((t) => t.has_task).length;
      const majority = trueCount > tgs.length / 2;
      if (majority === c.ground_truth_has_task) gtMatch++;
      else gtMismatch++;
    });

    // Render
    let html = `
      <div class="admin-grid">
        <div class="stat-card">
          <div class="stat-value">${totalConvs}</div>
          <div class="stat-label">Total Conversations</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${taggedConvIds.size}</div>
          <div class="stat-label">With ≥1 Tag</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${fullyTagged}</div>
          <div class="stat-label">Fully Tagged (${JUDGES_PER_CONV}+ judges)</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${disagreements.length}</div>
          <div class="stat-label">Disagreements</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${gtMatch} / ${gtMatch + gtMismatch}</div>
          <div class="stat-label">Agree w/ Ground Truth</div>
        </div>
      </div>

      <h3>Judge Progress</h3>
      <table class="admin-table">
        <thead><tr><th>Judge</th><th>Assigned</th><th>Tagged</th><th>%</th></tr></thead>
        <tbody>`;

    Object.keys(judgeAssign)
      .sort()
      .forEach((judge) => {
        const assigned = judgeAssign[judge].length;
        const tagged = (judgeTags[judge] || []).length;
        const pct = assigned ? Math.round((tagged / assigned) * 100) : 0;
        html += `<tr><td>${judge}</td><td>${assigned}</td><td>${tagged}</td><td>${pct}%</td></tr>`;
      });

    html += `</tbody></table>`;

    // Disagreement table
    if (disagreements.length > 0) {
      html += `<h3>Disagreements</h3>
        <table class="admin-table">
          <thead><tr><th>#</th><th>Topic</th><th>Judge</th><th>HasTask</th><th>Type</th><th>Attribution</th><th>IsImportant</th><th>GT</th></tr></thead>
          <tbody>`;
      disagreements.forEach((d) => {
        d.tags.forEach((t, i) => {
          html += `<tr${i === 0 ? ' class="disagreement-first"' : ""}>
            <td>${i === 0 ? d.conv.source_row_index + 1 : ""}</td>
            <td>${i === 0 ? d.conv.topic || "-" : ""}</td>
            <td>${t.judge_name}</td>
            <td>${t.has_task ? "✓" : "✗"}</td>
            <td>${t.task_type || "-"}</td>
            <td>${t.attribution || "-"}</td>
            <td>${t.is_important ? "✓" : "✗"}</td>
            <td>${i === 0 ? (d.conv.ground_truth_has_task === null ? "-" : d.conv.ground_truth_has_task ? "✓" : "✗") : ""}</td>
          </tr>`;
        });
      });
      html += `</tbody></table>`;
    }

    // Conversations with scores (for Andrew to review)
    html += `<h3>LLM Classifier Scores (hidden from judges)</h3>
      <table class="admin-table compact">
        <thead><tr><th>#</th><th>Topic</th><th>GT</th><th>Action</th><th>Commit</th><th>Knowledge</th><th>Tags</th></tr></thead>
        <tbody>`;
    conversations.slice(0, 50).forEach((c) => {
      const tgs = convTagMap[c.id] || [];
      const tagSummary = tgs
        .map(
          (t) =>
            `${t.judge_name.split(" ")[0]}:${t.has_task ? "T" : "F"}/${t.is_important ? "I" : "-"}${t.task_type ? "/" + t.task_type.split(" ")[0] : ""}`,
        )
        .join(", ");
      html += `<tr>
        <td>${c.source_row_index + 1}</td>
        <td title="${c.topic || ""}">${(c.topic || "-").substring(0, 40)}</td>
        <td>${c.ground_truth_has_task === null ? "-" : c.ground_truth_has_task ? "✓" : "✗"}</td>
        <td>${c.action_score ? c.action_score.toFixed(2) : "-"}</td>
        <td>${c.commitment_score ? c.commitment_score.toFixed(2) : "-"}</td>
        <td>${c.knowledge_score ? c.knowledge_score.toFixed(2) : "-"}</td>
        <td>${tagSummary || "-"}</td>
      </tr>`;
    });
    if (conversations.length > 50)
      html += `<tr><td colspan="7" style="text-align:center;color:var(--text-muted);">...and ${conversations.length - 50} more</td></tr>`;
    html += `</tbody></table>`;

    content.innerHTML = html;
  } catch (e) {
    content.innerHTML = `<p style="color:var(--danger);">Error: ${e.message}</p>`;
    console.error(e);
  }
}

// ---- Toast ----

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = "toast " + type;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.3s";
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

function showLoadingState(loading) {
  const panel = document.getElementById("tagging-card");
  if (!panel) return;
  if (loading) {
    const loader = document.createElement("div");
    loader.className = "loading";
    loader.innerHTML = '<div class="spinner"></div>Loading conversations...';
    panel.prepend(loader);
  } else {
    const loader = panel.querySelector(".loading");
    if (loader) loader.remove();
  }
}

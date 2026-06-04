import { apiQuery } from "./api";
import { escHtml } from "./utils";
import { selectedId } from "./transcripts";

let isLoading = false;
let msgCounter = 0;

async function sendMessage() {
  const inputEl = document.getElementById('chat-input');
  const query = inputEl.value.trim();
  if (!query || isLoading) return;

  inputEl.value = '';
  autoResize(inputEl);
  hideEmptyChat();
  isLoading = true;
  updateSendBtn();

  appendMessage('user', query);
  const typingId = appendTyping();

  try {
    const answer = await apiQuery(query, selectedId);
    removeTyping(typingId);
    appendMessage('assistant', answer);

  } catch (e) {
    removeTyping(typingId);
    appendMessage('error', e.message || 'Something went wrong. Is the backend running?');
  } finally {
    isLoading = false;
    updateSendBtn();
  }
}

function handleChatKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
  document.getElementById('send-btn').disabled = !el.value.trim() || isLoading;
}

function updateSendBtn() {
  const inputEl = document.getElementById('chat-input');
  document.getElementById('send-btn').disabled = !inputEl.value.trim() || isLoading;
}

function hideEmptyChat() {
  const el = document.getElementById('empty-chat');
  if (el) el.style.display = 'none';
}

function appendMessage(role, content) {
  const area = document.getElementById('chat-area');
  const id = `msg-${++msgCounter}`;
  const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const row = document.createElement('div');
  row.className = `message-row ${role}`;
  row.id = id;
  row.innerHTML = `
    <div class="bubble ${role}">${escHtml(content)}</div>
    <div class="bubble-time">${now}</div>
  `;
  area.appendChild(row);
  area.scrollTop = area.scrollHeight;
  return id;
}

function appendTyping() {
  const area = document.getElementById('chat-area');
  const id = `typing-${++msgCounter}`;
  const row = document.createElement('div');
  row.className = 'message-row assistant';
  row.id = id;
  row.innerHTML = `<div class="typing-bubble"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>`;
  area.appendChild(row);
  area.scrollTop = area.scrollHeight;
  return id;
}

function removeTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// Init: enable send btn on input
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('chat-input').addEventListener('input', function() {
    autoResize(this);
  });
});

document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("chat-input").addEventListener("keydown", (e) => handleChatKey(e));


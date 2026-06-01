import { apiUploadTranscript } from "./api";
import { showToast, escHtml } from "./utils";

let transcripts = [];
export let selectedId = null;

function addTranscript(t) {
  transcripts.push(t);
  renderTranscriptList();
}

function markOld(id) {
  const t = transcripts.find(x => x.id === id);
  if (t) { t.isNew = false; renderTranscriptList(); }
}

function selectTranscript(id) {
  console.log(`transcript selected: ${id}`)
  selectedId = id;
  renderTranscriptList();
  updateFilterBadge();
}

function renderTranscriptList() {
  const container = document.getElementById('transcript-items');
  const emptyLabel = document.getElementById('empty-label');
  const allItem = document.getElementById('all-item');

  allItem.classList.toggle('active', selectedId === null);
  emptyLabel.style.display = transcripts.length === 0 ? 'block' : 'none';

  container.innerHTML = transcripts.map(t => `
    <div class="transcript-item${selectedId === t.id ? ' active' : ''}" data-transcript-id="${t.id}">
      <div class="transcript-item-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
      </div>
      <div class="transcript-item-info">
        <div class="transcript-item-name">${escHtml(t.label)}</div>
        <div class="transcript-item-id">${t.id.slice(0, 8)}…</div>
      </div>
      ${t.isNew ? '<span class="badge-new">new</span>' : ''}
    </div>
  `).join('');
  container.querySelectorAll(".transcript-item").forEach((item) => {
    item.addEventListener("click", () => {
      const transcriptId = item.dataset.transcriptId;
      console.log(`second selected transcript: ${transcriptId}`)
      selectTranscript(transcriptId);
    });
  });
}

function updateHeaderSub() {
  const el = document.getElementById('header-sub');
  const n = transcripts.length;
  el.textContent = n === 0 ? 'No transcripts loaded' : `${n} transcript${n !== 1 ? 's' : ''} loaded`;
}

function updateFilterBadge() {
  const badge = document.getElementById('filter-badge');
  const label = document.getElementById('filter-label');
  if (selectedId) {
    const t = transcripts.find(x => x.id === selectedId);
    label.textContent = t ? t.label : selectedId.slice(0, 8);
    badge.style.display = 'flex';
  } else {
    badge.style.display = 'none';
  }
}

async function uploadTranscript() {
  const labelEl = document.getElementById('label-input');
  const textEl  = document.getElementById('transcript-input');
  const btn     = document.getElementById('upload-btn');

  const rawText = textEl.value.trim();
  if (!rawText) return;

  btn.disabled = true;
  btn.innerHTML = '<div class="spinner"></div> Uploading…';

  try {
    const data = await apiUploadTranscript(rawText);
    const labelRaw = labelEl.value.trim();
    const label = labelRaw || `Transcript ${data.transcript_id.slice(0, 8)}`;

    addTranscript({ id: data.transcript_id, label, isNew: true });
    textEl.value = '';
    labelEl.value = '';
    showToast('Transcript uploaded successfully!', 'success');
    updateHeaderSub();

    setTimeout(() => markOld(data.transcript_id), 3000);

  } catch (e) {
    showToast(e.message || 'Upload failed. Is the backend running?', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      Upload`;
  }
}

document.getElementById("upload-btn").addEventListener("click", uploadTranscript);
document.getElementById("all-item").addEventListener("click", () => selectTranscript(null));




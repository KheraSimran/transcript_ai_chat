const API_BASE = import.meta.env.VITE_API_BASE;

export async function apiUploadTranscript(transcript) {
  const res = await fetch(`${API_BASE}/upload-transcript`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ transcript }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export async function apiQuery(query, transcriptId) {
  const params = new URLSearchParams({ query });
  if (transcriptId) params.append('transcript_id', transcriptId);

  const res = await fetch(`${API_BASE}/query?${params.toString()}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

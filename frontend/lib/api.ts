const API_BASE = "http://localhost:8000/api";

export async function sendVoiceChat(
  audioBlob: Blob,
  mode: string = "free_conversation",
  userId: number = 1
): Promise<{
  text: string;
  audio_b64: string;
  corrections: Array<{ original: string; corrected: string; rule: string }>;
  vocabulary_suggestions: Array<{ weak_word: string; alternatives: string[] }>;
}> {
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");
  formData.append("user_id", String(userId));
  formData.append("mode", mode);

  const res = await fetch(`${API_BASE}/voice/chat`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error(`Voice chat failed: ${res.status}`);
  }

  return res.json();
}

export async function fetchUser(userId: number = 1) {
  const res = await fetch(`${API_BASE}/memory/user/${userId}`);
  if (!res.ok) throw new Error("Failed to fetch user");
  return res.json();
}

export async function updateUser(userId: number, data: Record<string, unknown>) {
  const res = await fetch(`${API_BASE}/memory/user/${userId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update user");
  return res.json();
}

export async function fetchStats(userId: number = 1) {
  const res = await fetch(`${API_BASE}/dashboard/stats/${userId}`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}

export async function fetchVocabulary(userId: number = 1) {
  const res = await fetch(`${API_BASE}/memory/vocabulary/${userId}`);
  if (!res.ok) throw new Error("Failed to fetch vocabulary");
  return res.json();
}

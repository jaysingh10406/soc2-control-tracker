import { MOCK_CONTROLS } from "./mockData";

// DEMO_MODE=true runs entirely client-side against bundled mock data (e.g. GitHub
// Pages, where there's no backend to talk to). Set VITE_API_MODE=live and
// VITE_API_URL to point this at a running FastAPI backend instead.
const DEMO_MODE = (import.meta.env.VITE_API_MODE || "demo") !== "live";
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

let demoControls = MOCK_CONTROLS.map((c) => ({ ...c }));
let nextId = Math.max(...demoControls.map((c) => c.id)) + 1;

function summarize(controls) {
  const total = controls.length;
  const counts = { not_started: 0, in_progress: 0, implemented: 0, verified: 0 };
  controls.forEach((c) => counts[c.status]++);
  const percent_complete = total
    ? Math.round(((counts.implemented + counts.verified) / total) * 1000) / 10
    : 0;
  return { total, ...counts, percent_complete };
}

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  demoMode: DEMO_MODE,

  async listControls() {
    if (DEMO_MODE) return [...demoControls];
    return request("/controls");
  },

  async getSummary() {
    if (DEMO_MODE) return summarize(demoControls);
    return request("/controls/summary");
  },

  async createControl(data) {
    if (DEMO_MODE) {
      const control = { id: nextId++, evidence_url: "", description: "", last_reviewed: new Date().toISOString(), ...data };
      demoControls.push(control);
      return control;
    }
    return request("/controls", { method: "POST", body: JSON.stringify(data) });
  },

  async updateControl(id, patch) {
    if (DEMO_MODE) {
      demoControls = demoControls.map((c) =>
        c.id === id ? { ...c, ...patch, last_reviewed: new Date().toISOString() } : c
      );
      return demoControls.find((c) => c.id === id);
    }
    return request(`/controls/${id}`, { method: "PATCH", body: JSON.stringify(patch) });
  },

  async deleteControl(id) {
    if (DEMO_MODE) {
      demoControls = demoControls.filter((c) => c.id !== id);
      return null;
    }
    return request(`/controls/${id}`, { method: "DELETE" });
  },
};

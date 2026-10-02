import type { QueryResponse, HealthResponse } from "./types";

const API_BASE = import.meta.env.VITE_API_URL || "";

export async function queryApi(question: string): Promise<QueryResponse> {
  const resp = await fetch(`${API_BASE}/api/v1/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!resp.ok) {
    const body = await resp.json().catch(() => null);
    throw new Error(body?.detail || `Request failed (${resp.status})`);
  }

  return resp.json();
}

export async function healthApi(): Promise<HealthResponse> {
  const resp = await fetch(`${API_BASE}/health`);
  if (!resp.ok) throw new Error("Backend unavailable");
  return resp.json();
}

export interface Source {
  title: string;
  source: string;
  section: string;
  jurisdiction: string;
  relevance: number;
}

export interface QueryResponse {
  answer: string;
  sources: Source[];
  grounded: boolean;
  chunk_count: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  vector_store_ready: boolean;
  document_count: number;
}

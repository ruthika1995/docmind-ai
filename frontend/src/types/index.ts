export interface DocumentChunk {
  id: string;
  chunk_index: number;
  content: string;
  page_number: number;
  token_count: number;
}

export interface DocumentItem {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  raw_text?: string;
  classification: string;
  classification_confidence: number;
  classification_reason?: string;
  classification_metadata?: Record<string, any>;
  extracted_data?: Record<string, any>;
  summary?: {
    executive?: string;
    bullets?: string[];
    tldr?: string;
    action_items?: string[];
  };
  status: string;
  created_at: string;
  updated_at: string;
  chunks_count: number;
  chunks?: DocumentChunk[];
}

export interface ClauseDifference {
  clause_name: string;
  doc_a_text: string;
  doc_b_text: string;
  change_type: 'added' | 'removed' | 'modified' | 'unchanged';
  risk_level: 'low' | 'medium' | 'high';
  notes: string;
}

export interface ComparisonResult {
  id: string;
  doc_a_id: string;
  doc_b_id: string;
  doc_a_name: string;
  doc_b_name: string;
  diff_summary: string;
  clauses_comparison: ClauseDifference[];
  risk_assessment: {
    overall_risk: string;
    risk_factors: string[];
    recommendations: string[];
  };
  created_at: string;
}

export interface CitationItem {
  chunk_id: string;
  chunk_index: number;
  page_number: number;
  snippet: string;
  relevance_score: number;
}

export interface ChatMessageItem {
  id: string;
  document_id?: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  citations: CitationItem[];
  model_used: string;
  created_at: string;
}

export interface GatewayHealth {
  status: string;
  service: string;
  version: string;
  environment: string;
  openrouter: {
    configured: boolean;
    active_model: string;
    gateway_url: string;
    fallback_models: string[];
    offline_heuristic_available: boolean;
  };
  embeddings: {
    engine: string;
    dimension: number;
    provider: string;
  };
}

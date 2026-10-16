import type {
  DocumentItem,
  ComparisonResult,
  ChatMessageItem,
  GatewayHealth
} from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8010/api/v1';

export const api = {
  async getHealth(): Promise<GatewayHealth> {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Failed to reach backend gateway');
    return res.json();
  },

  async getDocuments(): Promise<DocumentItem[]> {
    const res = await fetch(`${API_BASE}/documents`);
    if (!res.ok) throw new Error('Failed to fetch documents');
    return res.json();
  },

  async getDocument(id: string): Promise<DocumentItem> {
    const res = await fetch(`${API_BASE}/documents/${id}`);
    if (!res.ok) throw new Error('Failed to fetch document details');
    return res.json();
  },

  async uploadDocument(file: File, autoAnalyze = true): Promise<DocumentItem> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('auto_analyze', autoAnalyze ? 'true' : 'false');

    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(err.detail || 'Upload failed');
    }
    return res.json();
  },

  async deleteDocument(id: string): Promise<void> {
    const res = await fetch(`${API_BASE}/documents/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete document');
  },

  async seedSampleDocuments(): Promise<DocumentItem[]> {
    const res = await fetch(`${API_BASE}/documents/seed`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to seed sample documents');
    return res.json();
  },

  async extractData(
    documentId: string,
    targetType?: string,
    customSchemaPrompt?: string
  ): Promise<{
    document_id: string;
    target_type: string;
    extracted_data: Record<string, any>;
    model_used?: string;
    is_mock?: boolean;
  }> {
    const res = await fetch(`${API_BASE}/extract`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        document_id: documentId,
        target_type: targetType,
        custom_schema_prompt: customSchemaPrompt,
      }),
    });
    if (!res.ok) throw new Error('Extraction failed');
    return res.json();
  },

  async compareDocuments(docAId: string, docBId: string): Promise<ComparisonResult> {
    const res = await fetch(`${API_BASE}/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ doc_a_id: docAId, doc_b_id: docBId }),
    });
    if (!res.ok) throw new Error('Comparison failed');
    return res.json();
  },

  async sendChatMessage(
    documentId: string | null,
    message: string,
    model?: string
  ): Promise<ChatMessageItem> {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        document_id: documentId || undefined,
        message,
        model,
        stream: false,
      }),
    });
    if (!res.ok) throw new Error('Chat message failed');
    return res.json();
  },

  async getChatHistory(documentId: string): Promise<ChatMessageItem[]> {
    const res = await fetch(`${API_BASE}/chat/history/${documentId}`);
    if (!res.ok) throw new Error('Failed to load chat history');
    return res.json();
  },
};

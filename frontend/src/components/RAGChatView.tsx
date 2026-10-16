import React, { useState, useEffect, useRef } from 'react';
import {
  Quote,
  CornerDownLeft
} from 'lucide-react';
import type { DocumentItem, ChatMessageItem, CitationItem } from '../types';
import { api } from '../services/api';

interface RAGChatViewProps {
  documents: DocumentItem[];
  selectedDocId?: string | null;
}

export const RAGChatView: React.FC<RAGChatViewProps> = ({
  documents,
  selectedDocId,
}) => {
  const [currentDocId, setCurrentDocId] = useState<string>(selectedDocId || '');
  const [messages, setMessages] = useState<ChatMessageItem[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isSending, setIsSending] = useState<boolean>(false);
  const [activeCitation, setActiveCitation] = useState<CitationItem | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentDoc = documents.find((d) => d.id === currentDocId);

  useEffect(() => {
    if (selectedDocId) {
      setCurrentDocId(selectedDocId);
    }
  }, [selectedDocId]);

  useEffect(() => {
    if (currentDocId) {
      loadHistory(currentDocId);
    } else {
      setMessages([]);
    }
  }, [currentDocId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadHistory = async (docId: string) => {
    try {
      const history = await api.getChatHistory(docId);
      setMessages(history);
    } catch {
      setMessages([]);
    }
  };

  const handleSend = async (messageToSend?: string) => {
    const text = messageToSend || inputMessage;
    if (!text.trim() || isSending) return;

    const userMsg: ChatMessageItem = {
      id: `temp-${Date.now()}`,
      document_id: currentDocId || undefined,
      role: 'user',
      content: text,
      citations: [],
      model_used: 'User',
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setIsSending(true);

    try {
      const assistantMsg = await api.sendChatMessage(
        currentDocId || null,
        text
      );
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          document_id: currentDocId || undefined,
          role: 'assistant',
          content: `Unable to complete query: ${err.message}`,
          citations: [],
          model_used: 'Error',
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const sampleQuestions = [
    'What is the total amount due and remittance address?',
    'What is the limitation of liability ceiling and SLA guarantee?',
    'Summarize the candidate\'s engineering experience.',
    'Are there auto-renewal or termination clauses?'
  ];

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px' }} className="fade-in">
      {/* Header Context Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px',
        marginBottom: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <select
            className="dm-select"
            value={currentDocId}
            onChange={(e) => setCurrentDocId(e.target.value)}
            style={{ minWidth: '300px', fontSize: '0.82rem' }}
          >
            <option value="">All Documents (Cross-document search)</option>
            {documents.map((d) => (
              <option key={d.id} value={d.id}>
                {d.filename} ({d.classification})
              </option>
            ))}
          </select>
        </div>

        <div style={{ fontSize: '0.74rem', color: 'var(--dm-text-4)', fontFamily: 'var(--font-mono)' }}>
          {currentDoc ? `${currentDoc.chunks_count || 1} indexed chunks` : `${documents.length} documents indexed`}
        </div>
      </div>

      {/* Main Chat and Citations Layout */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: activeCitation ? '1fr 360px' : '1fr',
        gap: '16px',
        alignItems: 'start'
      }}>
        {/* Chat Stream Window */}
        <div className="dm-panel" style={{ display: 'flex', flexDirection: 'column', height: '640px' }}>
          {/* Messages Flow */}
          <div style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {messages.length === 0 ? (
              <div style={{
                margin: 'auto',
                textAlign: 'center',
                maxWidth: '460px',
                padding: '40px 20px',
                color: 'var(--dm-text-3)'
              }}>
                <div style={{ fontSize: '0.925rem', color: 'var(--dm-text-1)', fontWeight: 600, marginBottom: '6px' }}>
                  Document Assistant
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--dm-text-4)', marginBottom: '18px', lineHeight: 1.5 }}>
                  Ask natural language questions against indexed documents with grounded citations.
                </p>

                {/* Suggested prompts */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', textAlign: 'left' }}>
                  {sampleQuestions.map((q, idx) => (
                    <button
                      key={idx}
                      type="button"
                      className="dm-btn dm-btn-secondary"
                      style={{ justifyContent: 'flex-start', fontSize: '0.78rem', padding: '7px 11px' }}
                      onClick={() => handleSend(q)}
                    >
                      <span style={{ textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>{q}</span>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((msg) => {
                const isUser = msg.role === 'user';
                return (
                  <div
                    key={msg.id}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: isUser ? 'flex-end' : 'flex-start',
                      maxWidth: '82%',
                      alignSelf: isUser ? 'flex-end' : 'flex-start'
                    }}
                  >
                    {/* Role header */}
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      fontSize: '0.7rem',
                      color: 'var(--dm-text-4)',
                      marginBottom: '3px'
                    }}>
                      {isUser ? (
                        <span>You</span>
                      ) : (
                        <span>DocMind · {msg.model_used.split('/').pop()}</span>
                      )}
                    </div>

                    {/* Message Bubble */}
                    <div
                      style={{
                        padding: '10px 14px',
                        borderRadius: 'var(--radius-sm)',
                        background: isUser ? 'var(--dm-surface-2)' : 'var(--dm-surface-sunken)',
                        border: '1px solid var(--dm-border-hairline)',
                        color: 'var(--dm-text-1)',
                        fontSize: '0.835rem',
                        lineHeight: 1.55,
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word'
                      }}
                    >
                      {msg.content}
                    </div>

                    {/* Citations Pills */}
                    {!isUser && msg.citations && msg.citations.length > 0 && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '5px', marginTop: '6px', flexWrap: 'wrap' }}>
                        <span style={{ fontSize: '0.68rem', color: 'var(--dm-text-4)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                          Sources:
                        </span>
                        {msg.citations.map((cite, i) => (
                          <button
                            key={i}
                            type="button"
                            onClick={() => setActiveCitation(cite)}
                            style={{
                              background: 'var(--dm-surface-0)',
                              border: '1px solid var(--dm-border-subtle)',
                              borderRadius: 'var(--radius-xs)',
                              padding: '1px 6px',
                              fontSize: '0.69rem',
                              color: 'var(--dm-text-2)',
                              cursor: 'pointer',
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '4px',
                              fontFamily: 'var(--font-mono)'
                            }}
                          >
                            <span>#{cite.chunk_index + 1} (p.{cite.page_number})</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })
            )}

            {isSending && (
              <div style={{
                color: 'var(--dm-text-4)',
                fontSize: '0.78rem',
                fontFamily: 'var(--font-mono)'
              }}>
                Generating grounded response...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Bar */}
          <div style={{
            padding: '12px 16px',
            borderTop: '1px solid var(--dm-border-hairline)',
            background: 'var(--dm-surface-0)',
            display: 'flex',
            gap: '8px'
          }}>
            <input
              type="text"
              className="dm-input"
              style={{ flex: 1, fontSize: '0.82rem' }}
              placeholder={currentDoc ? `Ask a question about ${currentDoc.filename}...` : "Ask a question across all documents..."}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleSend();
              }}
              disabled={isSending}
            />
            <button
              type="button"
              className="dm-btn dm-btn-primary"
              onClick={() => handleSend()}
              disabled={isSending || !inputMessage.trim()}
              style={{ padding: '6px 12px' }}
            >
              <CornerDownLeft size={13} />
            </button>
          </div>
        </div>

        {/* Verified Citation Drawer */}
        {activeCitation && (
          <div className="dm-panel fade-in" style={{ padding: '16px', height: '640px', overflowY: 'auto' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Quote size={13} style={{ color: 'var(--dm-text-3)' }} />
                <span style={{ fontWeight: 600, fontSize: '0.82rem', color: 'var(--dm-text-1)' }}>
                  Source Passage #{activeCitation.chunk_index + 1}
                </span>
              </div>
              <button
                type="button"
                className="dm-btn dm-btn-secondary"
                style={{ padding: '2px 6px', fontSize: '0.7rem' }}
                onClick={() => setActiveCitation(null)}
              >
                Close
              </button>
            </div>

            <div style={{
              background: 'var(--dm-surface-sunken)',
              padding: '8px 12px',
              borderRadius: 'var(--radius-xs)',
              border: '1px solid var(--dm-border-hairline)',
              marginBottom: '12px',
              display: 'flex',
              justifyContent: 'space-between',
              fontSize: '0.72rem',
              color: 'var(--dm-text-4)',
              fontFamily: 'var(--font-mono)'
            }}>
              <span>Page {activeCitation.page_number}</span>
              <span className="tnum">Score: {Math.round(activeCitation.relevance_score * 100)}%</span>
            </div>

            <div style={{ fontSize: '0.79rem', color: 'var(--dm-text-2)', lineHeight: 1.55, whiteSpace: 'pre-wrap' }}>
              "{activeCitation.snippet}"
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

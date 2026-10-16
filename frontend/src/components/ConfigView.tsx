import React from 'react';
import {
  Cpu,
  Database,
  Circle
} from 'lucide-react';
import type { GatewayHealth } from '../types';

interface ConfigViewProps {
  health: GatewayHealth | null;
}

export const ConfigView: React.FC<ConfigViewProps> = ({ health }) => {
  const isHealthy = health?.status === 'healthy';
  const openrouter = health?.openrouter;

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px' }} className="fade-in">
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(440px, 1fr))', gap: '16px' }}>
        {/* Gateway Status & Configuration Card */}
        <div className="dm-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Cpu size={16} style={{ color: 'var(--dm-text-3)' }} />
              <h3 style={{ fontSize: '0.9rem', fontWeight: 600 }}>OpenRouter AI Gateway</h3>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.72rem', color: 'var(--dm-text-3)' }}>
              <Circle size={6} fill={isHealthy ? 'var(--dm-emerald)' : 'var(--dm-amber)'} color="transparent" />
              <span>{isHealthy ? 'Connected' : 'Offline'}</span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.82rem' }}>
            <div>
              <span style={{ color: 'var(--dm-text-4)', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase' }}>
                Active Model
              </span>
              <div style={{
                fontFamily: 'var(--font-mono)',
                color: 'var(--dm-text-1)',
                background: 'var(--dm-surface-sunken)',
                padding: '6px 10px',
                borderRadius: 'var(--radius-xs)',
                border: '1px solid var(--dm-border-hairline)',
                marginTop: '4px',
                fontSize: '0.78rem'
              }}>
                {openrouter?.active_model || 'meta-llama/llama-3.3-70b-instruct:free'}
              </div>
            </div>

            <div>
              <span style={{ color: 'var(--dm-text-4)', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase' }}>
                Gateway Endpoint
              </span>
              <div style={{
                fontFamily: 'var(--font-mono)',
                color: 'var(--dm-text-3)',
                background: 'var(--dm-surface-sunken)',
                padding: '6px 10px',
                borderRadius: 'var(--radius-xs)',
                border: '1px solid var(--dm-border-hairline)',
                marginTop: '4px',
                fontSize: '0.78rem'
              }}>
                {openrouter?.gateway_url || 'https://openrouter.ai/api/v1'}
              </div>
            </div>

            <div>
              <span style={{ color: 'var(--dm-text-4)', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase' }}>
                Candidate Fallbacks
              </span>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '4px' }}>
                {(openrouter?.fallback_models || [
                  'meta-llama/llama-3.3-70b-instruct:free',
                  'google/gemini-2.0-flash-001',
                  'deepseek/deepseek-chat',
                  'mistralai/mistral-small-24b-instruct-2501:free'
                ]).map((m, i) => (
                  <span key={i} className="dm-tag dm-tag-general" style={{ fontFamily: 'var(--font-mono)', fontSize: '0.68rem' }}>
                    {m.split('/').pop()}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <span style={{ color: 'var(--dm-text-4)', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase' }}>
                Gateway Credentials
              </span>
              <div style={{ marginTop: '4px' }}>
                <span className="dm-tag dm-tag-invoice">API Key Active on Backend</span>
              </div>
            </div>
          </div>
        </div>

        {/* Decoupled Vector Embeddings Card */}
        <div className="dm-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Database size={16} style={{ color: 'var(--dm-text-3)' }} />
              <h3 style={{ fontSize: '0.9rem', fontWeight: 600 }}>Vector Indexing Engine</h3>
            </div>
            <span className="dm-tag dm-tag-invoice">Decoupled</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.82rem' }}>
            <div>
              <span style={{ color: 'var(--dm-text-4)', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase' }}>
                Vector Space
              </span>
              <div style={{
                fontFamily: 'var(--font-mono)',
                color: 'var(--dm-text-1)',
                background: 'var(--dm-surface-sunken)',
                padding: '6px 10px',
                borderRadius: 'var(--radius-xs)',
                border: '1px solid var(--dm-border-hairline)',
                marginTop: '4px',
                fontSize: '0.78rem'
              }}>
                384-Dimensional Dense Vectors (Cosine Metric)
              </div>
            </div>

            <div>
              <span style={{ color: 'var(--dm-text-4)', fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase' }}>
                Persistence
              </span>
              <div style={{
                fontFamily: 'var(--font-mono)',
                color: 'var(--dm-text-3)',
                background: 'var(--dm-surface-sunken)',
                padding: '6px 10px',
                borderRadius: 'var(--radius-xs)',
                border: '1px solid var(--dm-border-hairline)',
                marginTop: '4px',
                fontSize: '0.78rem'
              }}>
                PostgreSQL + pgvector (Production) | SQLite (Development)
              </div>
            </div>

            <div style={{
              background: 'var(--dm-surface-sunken)',
              padding: '12px',
              borderRadius: 'var(--radius-xs)',
              border: '1px solid var(--dm-border-hairline)',
              marginTop: '4px'
            }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--dm-text-3)', textTransform: 'uppercase', marginBottom: '4px' }}>
                Architecture Rationale
              </div>
              <p style={{ fontSize: '0.775rem', color: 'var(--dm-text-4)', lineHeight: 1.5 }}>
                LLM inference and vectorization are decoupled. Chunking and indexing operations run without consuming OpenRouter tokens, preventing rate-limiting cascades.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

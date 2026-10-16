import React, { useState } from 'react';
import {
  GitCompare,
  CheckCircle2,
  Play
} from 'lucide-react';
import type { DocumentItem, ComparisonResult } from '../types';
import { api } from '../services/api';

interface CompareViewProps {
  documents: DocumentItem[];
}

export const CompareView: React.FC<CompareViewProps> = ({ documents }) => {
  const contractDocs = documents.filter((d) => d.classification === 'contract');
  const availableDocs = contractDocs.length >= 2 ? contractDocs : documents;

  const [docAId, setDocAId] = useState<string>(availableDocs[0]?.id || '');
  const [docBId, setDocBId] = useState<string>(availableDocs[1]?.id || availableDocs[0]?.id || '');
  const [isComparing, setIsComparing] = useState<boolean>(false);
  const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null);

  const handleCompare = async () => {
    if (!docAId || !docBId || docAId === docBId) {
      alert('Please select two distinct documents to compare.');
      return;
    }
    setIsComparing(true);
    try {
      const res = await api.compareDocuments(docAId, docBId);
      setComparisonResult(res);
    } catch (err: any) {
      alert(`Comparison failed: ${err.message}`);
    } finally {
      setIsComparing(false);
    }
  };

  const getRiskBadge = (risk: string) => {
    const r = (risk || '').toLowerCase();
    if (r.includes('high') || r.includes('critical')) {
      return <span className="dm-tag" style={{ background: 'var(--dm-rose-bg)', color: '#fb7185', border: '1px solid rgba(244, 63, 94, 0.25)' }}>High Risk</span>;
    }
    if (r.includes('medium')) {
      return <span className="dm-tag dm-tag-contract">Medium Risk</span>;
    }
    return <span className="dm-tag dm-tag-invoice">Low Risk</span>;
  };

  const getChangeBadge = (type: string) => {
    switch (type.toLowerCase()) {
      case 'modified':
        return <span className="dm-tag dm-tag-contract">Modified</span>;
      case 'added':
        return <span className="dm-tag dm-tag-resume">Added</span>;
      case 'removed':
        return <span className="dm-tag" style={{ background: 'var(--dm-rose-bg)', color: '#fb7185' }}>Removed</span>;
      default:
        return <span className="dm-tag dm-tag-general">Unchanged</span>;
    }
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px' }} className="fade-in">
      {/* Document Selectors Strip */}
      <div className="dm-panel" style={{ padding: '16px 20px', marginBottom: '20px' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr auto 1fr auto',
          gap: '14px',
          alignItems: 'center'
        }}>
          {/* Doc A */}
          <div>
            <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 600, color: 'var(--dm-text-4)', textTransform: 'uppercase', marginBottom: '4px' }}>
              Baseline Revision (A)
            </label>
            <select
              className="dm-select"
              style={{ width: '100%' }}
              value={docAId}
              onChange={(e) => setDocAId(e.target.value)}
            >
              {documents.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.filename} ({d.classification})
                </option>
              ))}
            </select>
          </div>

          <div style={{ color: 'var(--dm-text-4)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <GitCompare size={18} />
          </div>

          {/* Doc B */}
          <div>
            <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 600, color: 'var(--dm-text-4)', textTransform: 'uppercase', marginBottom: '4px' }}>
              Target Revision (B)
            </label>
            <select
              className="dm-select"
              style={{ width: '100%' }}
              value={docBId}
              onChange={(e) => setDocBId(e.target.value)}
            >
              {documents.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.filename} ({d.classification})
                </option>
              ))}
            </select>
          </div>

          <div style={{ alignSelf: 'flex-end' }}>
            <button
              type="button"
              className="dm-btn dm-btn-primary"
              onClick={handleCompare}
              disabled={isComparing || !docAId || !docBId || docAId === docBId}
              style={{ height: '34px' }}
            >
              <Play size={12} fill="currentColor" />
              <span>{isComparing ? 'Comparing...' : 'Compare Versions'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Comparison Results */}
      {comparisonResult && (
        <div className="fade-in">
          {/* Executive Diff Summary */}
          <div className="dm-panel" style={{ padding: '18px 20px', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 size={15} style={{ color: 'var(--dm-emerald)' }} />
                <span style={{ fontWeight: 600, fontSize: '0.875rem', color: 'var(--dm-text-1)' }}>
                  Variance Summary
                </span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span style={{ fontSize: '0.73rem', color: 'var(--dm-text-4)' }}>Assessment:</span>
                {getRiskBadge(comparisonResult.risk_assessment?.overall_risk || 'Low')}
              </div>
            </div>

            <p style={{ fontSize: '0.84rem', color: 'var(--dm-text-2)', lineHeight: 1.6 }}>
              {comparisonResult.diff_summary}
            </p>

            {/* Risk Recommendations */}
            {comparisonResult.risk_assessment?.recommendations && (
              <div style={{
                marginTop: '14px',
                padding: '10px 14px',
                background: 'var(--dm-surface-sunken)',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--dm-border-subtle)'
              }}>
                <div style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--dm-text-3)', textTransform: 'uppercase', marginBottom: '4px' }}>
                  Recommendations
                </div>
                <ul style={{ paddingLeft: '16px', fontSize: '0.78rem', color: 'var(--dm-text-3)' }}>
                  {comparisonResult.risk_assessment.recommendations.map((rec, idx) => (
                    <li key={idx} style={{ marginBottom: '3px' }}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Clause Diff Breakdown Table */}
          <div className="dm-panel" style={{ overflow: 'hidden' }}>
            <div style={{
              padding: '10px 16px',
              borderBottom: '1px solid var(--dm-border-hairline)',
              background: 'var(--dm-surface-0)',
              fontSize: '0.78rem',
              fontWeight: 500,
              color: 'var(--dm-text-3)'
            }}>
              Clause Diffs ({comparisonResult.clauses_comparison.length} entries)
            </div>

            <table className="dm-table">
              <thead>
                <tr>
                  <th style={{ width: '18%' }}>Clause</th>
                  <th style={{ width: '28%' }}>{comparisonResult.doc_a_name}</th>
                  <th style={{ width: '28%' }}>{comparisonResult.doc_b_name}</th>
                  <th style={{ width: '10%' }}>Status</th>
                  <th style={{ width: '10%' }}>Risk</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                {comparisonResult.clauses_comparison.map((c, i) => (
                  <tr key={i}>
                    <td>
                      <span style={{ fontWeight: 500, color: 'var(--dm-text-1)', fontSize: '0.8rem' }}>
                        {c.clause_name}
                      </span>
                    </td>
                    <td style={{ fontSize: '0.78rem', color: 'var(--dm-text-3)', fontFamily: 'var(--font-mono)' }}>
                      {c.doc_a_text}
                    </td>
                    <td style={{ fontSize: '0.78rem', color: 'var(--dm-text-1)', fontFamily: 'var(--font-mono)' }}>
                      {c.doc_b_text}
                    </td>
                    <td>{getChangeBadge(c.change_type)}</td>
                    <td>{getRiskBadge(c.risk_level)}</td>
                    <td style={{ fontSize: '0.76rem', color: 'var(--dm-text-3)' }}>
                      {c.notes}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

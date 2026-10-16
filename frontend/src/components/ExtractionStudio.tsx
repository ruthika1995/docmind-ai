import React, { useState, useEffect } from 'react';
import {
  Copy,
  Download,
  Check,
  FileCode,
  FileText,
  Play,
  Braces
} from 'lucide-react';
import type { DocumentItem } from '../types';
import { api } from '../services/api';

interface ExtractionStudioProps {
  documents: DocumentItem[];
  selectedDocId?: string | null;
}

export const ExtractionStudio: React.FC<ExtractionStudioProps> = ({
  documents,
  selectedDocId,
}) => {
  const [currentDocId, setCurrentDocId] = useState<string>(
    selectedDocId || (documents[0]?.id ?? '')
  );
  const [targetType, setTargetType] = useState<string>('auto');
  const [customPrompt, setCustomPrompt] = useState<string>('');
  const [extractedData, setExtractedData] = useState<Record<string, any> | null>(null);
  const [isExtracting, setIsExtracting] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);
  const [modelUsed, setModelUsed] = useState<string>('');

  const currentDoc = documents.find((d) => d.id === currentDocId);

  useEffect(() => {
    if (selectedDocId) {
      setCurrentDocId(selectedDocId);
    }
  }, [selectedDocId]);

  useEffect(() => {
    if (currentDoc) {
      if (currentDoc.extracted_data && Object.keys(currentDoc.extracted_data).length > 0) {
        setExtractedData(currentDoc.extracted_data);
      } else {
        setExtractedData(null);
      }
    }
  }, [currentDocId, currentDoc]);

  const handleExtract = async () => {
    if (!currentDocId) return;
    setIsExtracting(true);
    try {
      const typeToUse = targetType === 'auto' ? currentDoc?.classification : targetType;
      const res = await api.extractData(
        currentDocId,
        typeToUse,
        targetType === 'custom' ? customPrompt : undefined
      );
      setExtractedData(res.extracted_data);
      setModelUsed(res.model_used || 'OpenRouter Gateway');
    } catch (err: any) {
      alert(`Extraction failed: ${err.message}`);
    } finally {
      setIsExtracting(false);
    }
  };

  const handleCopy = () => {
    if (!extractedData) return;
    navigator.clipboard.writeText(JSON.stringify(extractedData, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!extractedData || !currentDoc) return;
    const blob = new Blob([JSON.stringify(extractedData, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentDoc.filename.replace(/\.[^/.]+$/, '')}_extracted.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px' }} className="fade-in">
      {/* Studio Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '14px',
        marginBottom: '20px'
      }}>
        {/* Document Selector & Run Button */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <select
            className="dm-select"
            value={currentDocId}
            onChange={(e) => setCurrentDocId(e.target.value)}
            style={{ minWidth: '280px', fontSize: '0.825rem' }}
          >
            {documents.map((d) => (
              <option key={d.id} value={d.id}>
                {d.filename} ({d.classification})
              </option>
            ))}
          </select>

          <button
            type="button"
            className="dm-btn dm-btn-primary"
            onClick={handleExtract}
            disabled={isExtracting || !currentDocId}
          >
            <Play size={12} fill="currentColor" />
            <span>{isExtracting ? 'Extracting...' : 'Extract JSON'}</span>
          </button>
        </div>

        {/* Schema Selector Tabs */}
        <div style={{ display: 'flex', alignItems: 'center', background: 'var(--dm-surface-0)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--dm-border-subtle)', padding: '2px' }}>
          <button
            type="button"
            className={`dm-nav-tab ${targetType === 'auto' ? 'is-active' : ''}`}
            style={{ padding: '4px 10px', fontSize: '0.78rem' }}
            onClick={() => setTargetType('auto')}
          >
            Auto ({currentDoc?.classification || 'General'})
          </button>
          <button
            type="button"
            className={`dm-nav-tab ${targetType === 'invoice' ? 'is-active' : ''}`}
            style={{ padding: '4px 10px', fontSize: '0.78rem' }}
            onClick={() => setTargetType('invoice')}
          >
            Invoice
          </button>
          <button
            type="button"
            className={`dm-nav-tab ${targetType === 'contract' ? 'is-active' : ''}`}
            style={{ padding: '4px 10px', fontSize: '0.78rem' }}
            onClick={() => setTargetType('contract')}
          >
            Contract
          </button>
          <button
            type="button"
            className={`dm-nav-tab ${targetType === 'resume' ? 'is-active' : ''}`}
            style={{ padding: '4px 10px', fontSize: '0.78rem' }}
            onClick={() => setTargetType('resume')}
          >
            Resume
          </button>
          <button
            type="button"
            className={`dm-nav-tab ${targetType === 'custom' ? 'is-active' : ''}`}
            style={{ padding: '4px 10px', fontSize: '0.78rem' }}
            onClick={() => setTargetType('custom')}
          >
            Custom
          </button>
        </div>
      </div>

      {targetType === 'custom' && (
        <div style={{ marginBottom: '16px' }}>
          <input
            type="text"
            className="dm-input"
            style={{ width: '100%', fontSize: '0.82rem' }}
            placeholder="Specify target JSON fields, e.g.: Extract candidate name, email, top 5 skills, and recent company."
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
          />
        </div>
      )}

      {/* Split Pane: Document Text vs Extracted JSON */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))',
        gap: '16px',
        alignItems: 'start'
      }}>
        {/* Left: Document Raw Text */}
        <div className="dm-panel" style={{ display: 'flex', flexDirection: 'column', height: '640px' }}>
          <div style={{
            padding: '10px 16px',
            borderBottom: '1px solid var(--dm-border-hairline)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'var(--dm-surface-0)',
            fontSize: '0.78rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileText size={14} style={{ color: 'var(--dm-text-3)' }} />
              <span style={{ fontWeight: 500, color: 'var(--dm-text-1)' }}>
                {currentDoc?.filename || 'Document Source'}
              </span>
            </div>
            <span style={{ color: 'var(--dm-text-4)', fontFamily: 'var(--font-mono)' }}>
              {currentDoc?.raw_text?.length || 0} chars
            </span>
          </div>

          <div style={{ flex: 1, padding: '16px', overflowY: 'auto' }}>
            <pre style={{
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.78rem',
              color: 'var(--dm-text-2)',
              lineHeight: 1.6
            }}>
              {currentDoc?.raw_text || 'Select a document to inspect content.'}
            </pre>
          </div>
        </div>

        {/* Right: Extracted Structured JSON */}
        <div className="dm-panel" style={{ display: 'flex', flexDirection: 'column', height: '640px' }}>
          <div style={{
            padding: '10px 16px',
            borderBottom: '1px solid var(--dm-border-hairline)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'var(--dm-surface-0)',
            fontSize: '0.78rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Braces size={14} style={{ color: 'var(--dm-emerald)' }} />
              <span style={{ fontWeight: 500, color: 'var(--dm-text-1)' }}>
                Extracted Schema
              </span>
              {modelUsed && (
                <span style={{ fontSize: '0.7rem', color: 'var(--dm-text-4)', fontFamily: 'var(--font-mono)' }}>
                  ({modelUsed.split('/').pop()})
                </span>
              )}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <button
                type="button"
                className="dm-btn dm-btn-secondary"
                style={{ padding: '3px 8px', fontSize: '0.73rem' }}
                onClick={handleCopy}
                disabled={!extractedData}
              >
                {copied ? <Check size={12} style={{ color: 'var(--dm-emerald)' }} /> : <Copy size={12} />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>

              <button
                type="button"
                className="dm-btn dm-btn-secondary"
                style={{ padding: '3px 8px', fontSize: '0.73rem' }}
                onClick={handleDownload}
                disabled={!extractedData}
              >
                <Download size={12} />
                <span>Export JSON</span>
              </button>
            </div>
          </div>

          <div style={{ flex: 1, padding: '16px', overflowY: 'auto', background: 'var(--dm-surface-sunken)' }}>
            {extractedData ? (
              <pre style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.8rem',
                color: 'var(--dm-text-1)',
                lineHeight: 1.55
              }}>
                {JSON.stringify(extractedData, null, 2)}
              </pre>
            ) : (
              <div style={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--dm-text-4)',
                textAlign: 'center'
              }}>
                <FileCode size={30} style={{ marginBottom: '10px', opacity: 0.4 }} />
                <div style={{ fontSize: '0.85rem', color: 'var(--dm-text-3)', fontWeight: 500 }}>
                  Ready to Extract
                </div>
                <div style={{ fontSize: '0.75rem', marginTop: '2px' }}>
                  Click "Extract JSON" to parse structured fields.
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

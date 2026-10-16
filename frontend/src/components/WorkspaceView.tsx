import React, { useState, useRef } from 'react';
import {
  FileText,
  Trash2,
  Sparkles,
  Search,
  ChevronRight,
  Plus
} from 'lucide-react';
import type { DocumentItem } from '../types';

interface WorkspaceViewProps {
  documents: DocumentItem[];
  isLoading: boolean;
  onUpload: (file: File) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onSeed: () => Promise<void>;
  onSelectDocument: (doc: DocumentItem, view: 'extract' | 'chat') => void;
}

export const WorkspaceView: React.FC<WorkspaceViewProps> = ({
  documents,
  isLoading,
  onUpload,
  onDelete,
  onSeed,
  onSelectDocument,
}) => {
  const [filterType, setFilterType] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [uploading, setUploading] = useState<boolean>(false);
  const [selectedDoc, setSelectedDoc] = useState<DocumentItem | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileInput = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setUploading(true);
      try {
        await onUpload(file);
      } finally {
        setUploading(false);
        if (fileInputRef.current) fileInputRef.current.value = '';
      }
    }
  };

  const filteredDocs = documents.filter((d) => {
    const matchesType =
      filterType === 'all' ? true : d.classification === filterType;
    const matchesSearch =
      d.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (d.raw_text && d.raw_text.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesType && matchesSearch;
  });

  const getTag = (category: string) => {
    switch (category) {
      case 'invoice':
        return <span className="dm-tag dm-tag-invoice">Invoice</span>;
      case 'contract':
        return <span className="dm-tag dm-tag-contract">Contract</span>;
      case 'resume':
        return <span className="dm-tag dm-tag-resume">Resume</span>;
      default:
        return <span className="dm-tag dm-tag-general">{category || 'Document'}</span>;
    }
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px' }} className="fade-in">
      {/* Action Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '14px',
        marginBottom: '20px'
      }}>
        {/* Left: Filter Buttons & Search */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', background: 'var(--dm-surface-0)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--dm-border-subtle)', padding: '2px' }}>
            <button
              type="button"
              className={`dm-nav-tab ${filterType === 'all' ? 'is-active' : ''}`}
              style={{ padding: '4px 10px', fontSize: '0.78rem' }}
              onClick={() => setFilterType('all')}
            >
              All ({documents.length})
            </button>
            <button
              type="button"
              className={`dm-nav-tab ${filterType === 'invoice' ? 'is-active' : ''}`}
              style={{ padding: '4px 10px', fontSize: '0.78rem' }}
              onClick={() => setFilterType('invoice')}
            >
              Invoices ({documents.filter((d) => d.classification === 'invoice').length})
            </button>
            <button
              type="button"
              className={`dm-nav-tab ${filterType === 'contract' ? 'is-active' : ''}`}
              style={{ padding: '4px 10px', fontSize: '0.78rem' }}
              onClick={() => setFilterType('contract')}
            >
              Contracts ({documents.filter((d) => d.classification === 'contract').length})
            </button>
            <button
              type="button"
              className={`dm-nav-tab ${filterType === 'resume' ? 'is-active' : ''}`}
              style={{ padding: '4px 10px', fontSize: '0.78rem' }}
              onClick={() => setFilterType('resume')}
            >
              Resumes ({documents.filter((d) => d.classification === 'resume').length})
            </button>
          </div>

          {/* Search Bar */}
          <div style={{ position: 'relative' }}>
            <Search size={13} style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--dm-text-4)' }} />
            <input
              type="text"
              className="dm-input"
              style={{ paddingLeft: '30px', width: '230px', fontSize: '0.78rem' }}
              placeholder="Filter by name or text..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* Right: Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button
            type="button"
            className="dm-btn dm-btn-secondary"
            onClick={onSeed}
            disabled={isLoading}
            style={{ fontSize: '0.78rem' }}
            title="Reset sample enterprise documents"
          >
            <Sparkles size={13} />
            <span>Reset Demo Data</span>
          </button>

          <button
            type="button"
            className="dm-btn dm-btn-primary"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            style={{ fontSize: '0.78rem' }}
          >
            <Plus size={13} />
            <span>{uploading ? 'Ingesting...' : 'Upload File'}</span>
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileInput}
            accept=".pdf,.docx,.doc,.txt,.md"
            style={{ display: 'none' }}
          />
        </div>
      </div>

      {/* Main Table Layout */}
      <div className="dm-panel" style={{ overflow: 'hidden' }}>
        <table className="dm-table">
          <thead>
            <tr>
              <th style={{ width: '38%' }}>Document</th>
              <th style={{ width: '14%' }}>Category</th>
              <th style={{ width: '12%' }}>Index Size</th>
              <th style={{ width: '14%' }}>Modified</th>
              <th style={{ textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredDocs.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '36px 16px', color: 'var(--dm-text-4)' }}>
                  No documents found. Upload a PDF/DOCX or click "Reset Demo Data".
                </td>
              </tr>
            ) : (
              filteredDocs.map((doc) => {
                const isSelected = selectedDoc?.id === doc.id;
                return (
                  <tr
                    key={doc.id}
                    onClick={() => setSelectedDoc(doc)}
                    style={{
                      cursor: 'pointer',
                      background: isSelected ? 'rgba(255, 255, 255, 0.03)' : undefined
                    }}
                  >
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <FileText size={15} style={{ color: 'var(--dm-text-3)', flexShrink: 0 }} />
                        <div>
                          <div style={{ fontWeight: 500, color: 'var(--dm-text-1)', fontSize: '0.84rem' }}>
                            {doc.filename}
                          </div>
                          <div style={{ fontSize: '0.71rem', color: 'var(--dm-text-4)', fontFamily: 'var(--font-mono)' }}>
                            {(doc.file_size / 1024).toFixed(1)} KB · {doc.file_type.toUpperCase()}
                          </div>
                        </div>
                      </div>
                    </td>

                    <td>{getTag(doc.classification)}</td>

                    <td>
                      <span className="tnum" style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--dm-text-3)' }}>
                        {doc.chunks_count || 1} passages
                      </span>
                    </td>

                    <td>
                      <span style={{ fontSize: '0.76rem', color: 'var(--dm-text-4)' }}>
                        {new Date(doc.created_at).toLocaleDateString(undefined, {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric'
                        })}
                      </span>
                    </td>

                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '6px' }}>
                        <button
                          type="button"
                          className="dm-btn dm-btn-secondary"
                          style={{ padding: '3px 8px', fontSize: '0.73rem' }}
                          onClick={(e) => {
                            e.stopPropagation();
                            onSelectDocument(doc, 'extract');
                          }}
                        >
                          Extract
                        </button>

                        <button
                          type="button"
                          className="dm-btn dm-btn-secondary"
                          style={{ padding: '3px 8px', fontSize: '0.73rem' }}
                          onClick={(e) => {
                            e.stopPropagation();
                            onSelectDocument(doc, 'chat');
                          }}
                        >
                          Ask
                        </button>

                        <button
                          type="button"
                          className="dm-btn dm-btn-danger"
                          style={{ padding: '3px 6px', fontSize: '0.73rem' }}
                          onClick={(e) => {
                            e.stopPropagation();
                            onDelete(doc.id);
                          }}
                        >
                          <Trash2 size={12} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Selected Document Inline Drawer */}
      {selectedDoc && (
        <div className="dm-panel" style={{ marginTop: '16px', padding: '18px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--dm-text-1)' }}>
                {selectedDoc.filename}
              </span>
              {getTag(selectedDoc.classification)}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <button
                type="button"
                className="dm-btn dm-btn-primary"
                onClick={() => onSelectDocument(selectedDoc, 'extract')}
                style={{ fontSize: '0.75rem' }}
              >
                <span>Extract Schema</span>
                <ChevronRight size={13} />
              </button>
              <button
                type="button"
                className="dm-btn dm-btn-secondary"
                onClick={() => onSelectDocument(selectedDoc, 'chat')}
                style={{ fontSize: '0.75rem' }}
              >
                <span>Chat</span>
              </button>
              <button
                type="button"
                className="dm-btn dm-btn-secondary"
                onClick={() => setSelectedDoc(null)}
                style={{ fontSize: '0.75rem' }}
              >
                Close
              </button>
            </div>
          </div>

          {selectedDoc.summary?.executive && (
            <div style={{
              background: 'var(--dm-surface-sunken)',
              border: '1px solid var(--dm-border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '12px 14px',
              fontSize: '0.8rem',
              color: 'var(--dm-text-2)',
              lineHeight: 1.55,
              marginBottom: '12px'
            }}>
              {selectedDoc.summary.executive}
            </div>
          )}

          <div style={{
            background: 'var(--dm-surface-sunken)',
            border: '1px solid var(--dm-border-hairline)',
            borderRadius: 'var(--radius-sm)',
            padding: '12px 14px',
            maxHeight: '180px',
            overflowY: 'auto'
          }}>
            <pre style={{
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
              color: 'var(--dm-text-3)',
              fontSize: '0.76rem',
              lineHeight: 1.5,
              fontFamily: 'var(--font-mono)'
            }}>
              {selectedDoc.raw_text?.slice(0, 1200) || 'No text extracted.'}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

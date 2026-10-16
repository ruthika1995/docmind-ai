import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { WorkspaceView } from './components/WorkspaceView';
import { ExtractionStudio } from './components/ExtractionStudio';
import { CompareView } from './components/CompareView';
import { RAGChatView } from './components/RAGChatView';
import { ConfigView } from './components/ConfigView';
import { api } from './services/api';
import type { DocumentItem, GatewayHealth } from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('workspace');
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [health, setHealth] = useState<GatewayHealth | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [docsData, healthData] = await Promise.all([
        api.getDocuments().catch(() => []),
        api.getHealth().catch(() => null),
      ]);
      setDocuments(docsData);
      setHealth(healthData);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleUpload = async (file: File) => {
    const newDoc = await api.uploadDocument(file);
    setDocuments((prev) => [newDoc, ...prev]);
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this document?')) return;
    await api.deleteDocument(id);
    setDocuments((prev) => prev.filter((d) => d.id !== id));
    if (selectedDocId === id) setSelectedDocId(null);
  };

  const handleSeed = async () => {
    setIsLoading(true);
    try {
      const seeded = await api.seedSampleDocuments();
      setDocuments(seeded);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectDocument = (doc: DocumentItem, view: 'extract' | 'chat') => {
    setSelectedDocId(doc.id);
    setActiveTab(view);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--ks-bg)' }}>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} health={health} />

      <main style={{ flex: 1 }}>
        {activeTab === 'workspace' && (
          <WorkspaceView
            documents={documents}
            isLoading={isLoading}
            onUpload={handleUpload}
            onDelete={handleDelete}
            onSeed={handleSeed}
            onSelectDocument={handleSelectDocument}
          />
        )}

        {activeTab === 'extract' && (
          <ExtractionStudio
            documents={documents}
            selectedDocId={selectedDocId}
          />
        )}

        {activeTab === 'compare' && (
          <CompareView documents={documents} />
        )}

        {activeTab === 'chat' && (
          <RAGChatView
            documents={documents}
            selectedDocId={selectedDocId}
          />
        )}

        {activeTab === 'config' && (
          <ConfigView health={health} />
        )}
      </main>

      <footer style={{
        borderTop: '1px solid var(--dm-border-hairline)',
        padding: '14px 24px',
        fontSize: '0.72rem',
        color: 'var(--dm-text-4)',
        background: 'var(--dm-surface-0)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <span>DocMind Workspace</span>
        <span style={{ fontFamily: 'var(--font-mono)' }}>OpenRouter Gateway · 384-Dim Vector Layer</span>
      </footer>
    </div>
  );
};

export default App;

import React from 'react';
import {
  FileText,
  Braces,
  GitCompare,
  MessageSquare,
  Settings,
  Circle
} from 'lucide-react';
import type { GatewayHealth } from '../types';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  health: GatewayHealth | null;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, health }) => {
  const modelName = health?.openrouter?.active_model || 'meta-llama/llama-3.3-70b-instruct:free';
  const isHealthy = health?.status === 'healthy';

  return (
    <header style={{
      borderBottom: '1px solid var(--dm-border-hairline)',
      background: 'var(--dm-surface-0)',
      position: 'sticky',
      top: 0,
      zIndex: 50
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '0 24px',
        height: '52px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* Brand & Workspace Name */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '24px',
              height: '24px',
              borderRadius: 'var(--radius-xs)',
              background: '#ffffff',
              color: '#090a0f',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 700,
              fontSize: '0.85rem'
            }}>
              D
            </div>
            <span style={{
              fontWeight: 600,
              fontSize: '0.925rem',
              color: 'var(--dm-text-1)',
              letterSpacing: '-0.015em'
            }}>
              DocMind
            </span>
          </div>

          <div style={{ width: '1px', height: '16px', background: 'var(--dm-border-subtle)' }} />

          {/* Navigation Tabs */}
          <nav style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <button
              type="button"
              className={`dm-nav-tab ${activeTab === 'workspace' ? 'is-active' : ''}`}
              onClick={() => setActiveTab('workspace')}
            >
              <FileText size={14} />
              <span>Documents</span>
            </button>

            <button
              type="button"
              className={`dm-nav-tab ${activeTab === 'extract' ? 'is-active' : ''}`}
              onClick={() => setActiveTab('extract')}
            >
              <Braces size={14} />
              <span>Extract</span>
            </button>

            <button
              type="button"
              className={`dm-nav-tab ${activeTab === 'compare' ? 'is-active' : ''}`}
              onClick={() => setActiveTab('compare')}
            >
              <GitCompare size={14} />
              <span>Compare</span>
            </button>

            <button
              type="button"
              className={`dm-nav-tab ${activeTab === 'chat' ? 'is-active' : ''}`}
              onClick={() => setActiveTab('chat')}
            >
              <MessageSquare size={14} />
              <span>Assistant</span>
            </button>

            <button
              type="button"
              className={`dm-nav-tab ${activeTab === 'config' ? 'is-active' : ''}`}
              onClick={() => setActiveTab('config')}
            >
              <Settings size={14} />
              <span>Settings</span>
            </button>
          </nav>
        </div>

        {/* Live Model & Gateway Pill */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '7px',
            fontSize: '0.75rem',
            color: 'var(--dm-text-3)',
            background: 'var(--dm-surface-1)',
            padding: '4px 10px',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--dm-border-subtle)',
            fontFamily: 'var(--font-mono)'
          }}>
            <Circle size={6} fill={isHealthy ? 'var(--dm-emerald)' : 'var(--dm-amber)'} color="transparent" />
            <span>{modelName.split('/').pop()}</span>
          </div>
        </div>
      </div>
    </header>
  );
};

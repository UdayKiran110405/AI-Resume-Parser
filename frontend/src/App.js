// Update App.js
import React, { useState } from 'react';
import UploadTab from './UploadTab';
import HistoryTab from './HistoryTab';
import RawTextTab from './RawTextTab';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('upload');

  return (
    <div className="App">
      <header className="app-header">
        <h1>AI Resume Parser</h1>
        <p>Upload and analyze resumes with AI-powered insights</p>
      </header>

      <nav className="tab-navigation">
        <button 
          className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          Upload Resume
        </button>
        <button 
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          Resume History
        </button>
        <button 
          className={`tab-button ${activeTab === 'rawtext' ? 'active' : ''}`}
          onClick={() => setActiveTab('rawtext')}
        >
          Extracted Text
        </button>
      </nav>

      <main className="tab-content">
        {activeTab === 'upload' && <UploadTab />}
        {activeTab === 'history' && <HistoryTab />}
        {activeTab === 'rawtext' && <RawTextTab />}
      </main>
    </div>
  );
}

export default App;
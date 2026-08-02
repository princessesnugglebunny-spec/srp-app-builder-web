import React, { useState } from 'react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const App: React.FC = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [fragments, setFragments] = useState<{id: number, name: string, description: string}[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [prompt, setPrompt] = useState('');
  const [status, setStatus] = useState('');

  const handleIngest = async () => {
    setStatus('Ingesting repository...');
    try {
      const res = await fetch(`${API_BASE}/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: repoUrl }),
      });
      const data = await res.json();
      setStatus(data.message || 'Repository indexed successfully!');
    } catch (e) {
      setStatus('Error ingesting repository');
    }
  };

  const handleAssemble = async () => {
    setStatus('Assembling app...');
    try {
      const res = await fetch(`${API_BASE}/assemble`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fragment_ids: selectedIds, description: prompt }),
      });
      const data = await res.json();
      setStatus(`App assembled: ${data.path}`);
    } catch (e) {
      setStatus('Error assembling app');
    }
  };

  const handleDeploy = async () => {
    setStatus('Deploying to APK pipeline...');
    try {
      const res = await fetch(`${API_BASE}/deploy`, { method: 'POST' });
      const data = await res.json();
      setStatus(`Deployment started: ${data.message}`);
    } catch (e) {
      setStatus('Error deploying to APK');
    }
  };

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      <header className="text-center space-y-2">
        <h1 className="text-5xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">
          SRP App Builder
        </h1>
        <p className="text-slate-400">Decompose GitHub Repos → Assemble Kivy Apps → Deploy APK</p>
      </header>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <section className="glass-card p-6 space-y-4">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <span className="bg-indigo-500 text-white w-6 h-6 rounded-full text-sm flex items-center justify-center">1</span>
            Ingest Repo
          </h2>
          <input 
            className="w-full p-3 rounded-lg bg-slate-800 border border-slate-700 focus:ring-2 ring-indigo-500 outline-none transition-all"
            placeholder="https://github.com/user/repo"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
          />
          <button onClick={handleIngest} className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-semibold transition-colors">
            Index Repository
          </button>
        </section>
        <section className="glass-card p-6 space-y-4 lg:col-span-2">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <span className="bg-indigo-500 text-white w-6 h-6 rounded-full text-sm flex items-center justify-center">2</span>
            Select Components
          </h2>
          <div className="max-h-96 overflow-y-auto space-y-2 pr-2">
            {fragments.length === 0 && <p className="text-slate-500 italic">No components indexed yet...</p>}
            {fragments.map(f => (
              <div 
                key={f.id} 
                onClick={() => setSelectedIds(prev => prev.includes(f.id) ? prev.filter(id => id !== f.id) : [...prev, f.id])}
                className={`p-3 rounded-lg cursor-pointer border transition-all ${selectedIds.includes(f.id) ? 'bg-indigo-500/20 border-indigo-500' : 'bg-slate-800/50 border-slate-700 hover:border-slate-500'}`}
              >
                <div className="font-mono text-sm font-bold">{f.name}</div>
                <div className="text-xs text-slate-400 line-clamp-1">{f.description}</div>
              </div>
            ))}
          </div>
        </section>
      </div>
      <section className="glass-card p-8 space-y-6">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <span className="bg-indigo-500 text-white w-6 h-6 rounded-full text-sm flex items-center justify-center">3</span>
          Assemble & Deploy
        </h2>
        <textarea 
          className="w-full p-4 rounded-xl bg-slate-800 border border-slate-700 focus:ring-2 ring-indigo-500 outline-none h-32"
          placeholder="Describe the app you want to build with these components..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <div className="flex flex-wrap gap-4">
          <button onClick={handleAssemble} className="px-6 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold transition-colors">
            Assemble Package
          </button>
          <button onClick={handleDeploy} className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 rounded-lg font-semibold transition-colors shadow-lg shadow-indigo-500/20">
            🚀 Deploy to APK
          </button>
        </div>
        {status && <div className="p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-sm text-center animate-pulse">{status}</div>}
      </section>
    </div>
  );
};

export default App;

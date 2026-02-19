import React, { useState } from 'react';
import { Upload, AlertTriangle, CheckCircle, Shield, Volume2, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { uploadFile, AnalysisResult } from './services/api';

function App() {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const [selectedLang, setSelectedLang] = useState('en-IN');
    const [selectedSpeaker, setSelectedSpeaker] = useState('anushka');

    const languages = [
        { code: 'en-IN', name: 'English' },
        { code: 'hi-IN', name: 'Hindi' },
        { code: 'ta-IN', name: 'Tamil' },
        { code: 'te-IN', name: 'Telugu' },
        { code: 'kn-IN', name: 'Kannada' },
        { code: 'ml-IN', name: 'Malayalam' },
        { code: 'mr-IN', name: 'Marathi' },
        { code: 'gu-IN', name: 'Gujarati' },
        { code: 'bn-IN', name: 'Bengali' }
    ];

    const speakers = [
        { id: 'anushka', name: 'Anushka (Female)' },
        { id: 'abhilash', name: 'Abhilash (Male)' },
        { id: 'manisha', name: 'Manisha (Female)' },
        { id: 'vidya', name: 'Vidya (Female)' },
        { id: 'arya', name: 'Arya (Female)' },
        { id: 'karun', name: 'Karun (Male)' },
        { id: 'hitesh', name: 'Hitesh (Male)' }
    ];

    const [isPlaying, setIsPlaying] = useState(false);
    const [audio] = useState(new Audio());

    const toggleAudio = () => {
        if (!result?.audio_url) return;

        if (isPlaying) {
            audio.pause();
            setIsPlaying(false);
        } else {
            audio.src = result.audio_url;
            audio.play();
            setIsPlaying(true);
            audio.onended = () => setIsPlaying(false);
        }
    };

    const handleUpload = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        setError(null);
        try {
            const data = await uploadFile(file, selectedLang, selectedSpeaker);
            setResult(data);
            setIsPlaying(false); // Reset audio state on new upload
        } catch (err) {
            setError('Failed to analyze document. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <header style={{ textAlign: 'center', marginBottom: '4rem' }}>
                <h1 style={{ fontSize: '3.5rem', marginBottom: '1rem', background: 'linear-gradient(to right, #818cf8, #c084fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                    Smart Terms Agent
                </h1>
                <p style={{ color: 'var(--text-muted)', fontSize: '1.25rem' }}>
                    Analyze complex legal documents in seconds with Agentic AI.
                </p>
            </header>

            <main>
                {!result ? (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="glass-card"
                        style={{ maxWidth: '600px', margin: '0 auto', padding: '3rem' }}
                    >
                        <form onSubmit={handleUpload}>
                            <div style={{
                                border: '2px dashed var(--glass-border)',
                                padding: '3rem',
                                borderRadius: '16px',
                                textAlign: 'center',
                                marginBottom: '2rem',
                                cursor: 'pointer',
                                transition: 'border-color 0.2s'
                            }}
                                onDragOver={(e: React.DragEvent) => e.preventDefault()}
                                onDrop={(e: React.DragEvent) => {
                                    e.preventDefault();
                                    if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
                                }}
                                onClick={() => document.getElementById('fileInput')?.click()}
                            >
                                <input
                                    id="fileInput"
                                    type="file"
                                    style={{ display: 'none' }}
                                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFile(e.target.files?.[0] || null)}
                                    accept=".pdf,.docx"
                                />
                                <Upload size={48} color="var(--primary)" style={{ marginBottom: '1rem' }} />
                                <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>
                                    {file ? file.name : 'Click or drag PDF/DOCX here'}
                                </p>
                                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                                    Supports legal documents up to 20MB
                                </p>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>
                                <div>
                                    <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Audio Language</label>
                                    <select
                                        value={selectedLang}
                                        onChange={(e) => setSelectedLang(e.target.value)}
                                        style={{ width: '100%', padding: '0.75rem', borderRadius: '12px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--glass-border)', color: 'white', outline: 'none' }}
                                    >
                                        {languages.map(lang => <option key={lang.code} value={lang.code} style={{ background: '#1e293b' }}>{lang.name}</option>)}
                                    </select>
                                </div>
                                <div>
                                    <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>AI Voice</label>
                                    <select
                                        value={selectedSpeaker}
                                        onChange={(e) => setSelectedSpeaker(e.target.value)}
                                        style={{ width: '100%', padding: '0.75rem', borderRadius: '12px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--glass-border)', color: 'white', outline: 'none' }}
                                    >
                                        {speakers.map(s => <option key={s.id} value={s.id} style={{ background: '#1e293b' }}>{s.name}</option>)}
                                    </select>
                                </div>
                            </div>

                            <button
                                className="btn-primary"
                                style={{ width: '100%', fontSize: '1.1rem' }}
                                disabled={!file || loading}
                            >
                                {loading ? 'Analyzing...' : 'Analyze Document'}
                            </button>

                            {error && <p style={{ color: 'var(--danger)', marginTop: '1rem', textAlign: 'center' }}>{error}</p>}
                        </form>
                    </motion.div>
                ) : (
                    <AnimatePresence>
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}
                        >
                            {/* Sidebar: Quick Overview */}
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                                <div className="glass-card" style={{ padding: '2rem' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                                        <h3 style={{ fontSize: '1.25rem' }}>Fairness</h3>
                                        <div style={{
                                            width: '48px',
                                            height: '48px',
                                            borderRadius: '50%',
                                            border: '4px solid',
                                            borderColor: result.fairness_score > 7 ? 'var(--success)' : result.fairness_score > 4 ? 'var(--warning)' : 'var(--danger)',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            fontWeight: 'bold',
                                            fontSize: '1.2rem'
                                        }}>
                                            {result.fairness_score}
                                        </div>
                                    </div>
                                    <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6' }}>
                                        Our AI evaluates the overall balance of rights between you and the provider.
                                    </p>
                                </div>

                                <div className="glass-card" style={{ padding: '2rem' }}>
                                    <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <Info size={20} color="var(--primary)" /> Recommendation
                                    </h3>
                                    <p style={{ color: 'var(--text-main)', fontSize: '1rem', lineHeight: '1.6' }}>
                                        {result.recommendation}
                                    </p>
                                </div>

                                <motion.div
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                    className="glass-card"
                                    style={{
                                        padding: '2rem',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '1rem',
                                        cursor: 'pointer',
                                        border: isPlaying ? '1px solid var(--primary)' : '1px solid var(--glass-border)',
                                        background: isPlaying ? 'rgba(99, 102, 241, 0.1)' : 'var(--card-bg)'
                                    }}
                                    onClick={toggleAudio}
                                >
                                    <Volume2 size={24} color={isPlaying ? "var(--primary)" : "var(--text-muted)"} className={isPlaying ? "pulse" : ""} />
                                    <div>
                                        <h4 style={{ fontSize: '1rem', color: isPlaying ? 'var(--primary)' : 'var(--text-main)' }}>
                                            {isPlaying ? 'Playing Summary...' : 'Listen to Summary'}
                                        </h4>
                                        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>AI-generated audio digest</p>
                                    </div>
                                </motion.div>
                            </div>

                            {/* Main Content: Detailed Analysis */}
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                                <div className="glass-card" style={{ padding: '2.5rem' }}>
                                    <h2 style={{ marginBottom: '1.5rem' }}>Summary</h2>
                                    <p style={{ fontSize: '1.1rem', lineHeight: '1.8', color: 'var(--text-main)' }}>
                                        {result.final_summary}
                                    </p>
                                </div>

                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                                    <div className="glass-card" style={{ padding: '2rem' }}>
                                        <h3 style={{ marginBottom: '1rem', color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <CheckCircle size={20} /> Pros
                                        </h3>
                                        <ul style={{ paddingLeft: '1.5rem', color: 'var(--text-muted)' }}>
                                            {result.pros.map((pro: string, i: number) => <li key={i} style={{ marginBottom: '0.5rem' }}>{pro}</li>)}
                                        </ul>
                                    </div>
                                    <div className="glass-card" style={{ padding: '2rem' }}>
                                        <h3 style={{ marginBottom: '1rem', color: 'var(--danger)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <AlertTriangle size={20} /> Cons
                                        </h3>
                                        <ul style={{ paddingLeft: '1.5rem', color: 'var(--text-muted)' }}>
                                            {result.cons.map((con: string, i: number) => <li key={i} style={{ marginBottom: '0.5rem' }}>{con}</li>)}
                                        </ul>
                                    </div>
                                </div>

                                <div className="glass-card" style={{ padding: '2.5rem' }}>
                                    <h3 style={{ marginBottom: '1.5rem', color: 'var(--warning)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <Shield size={24} /> Hidden Risks
                                    </h3>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
                                        {result.hidden_risks.map((risk: string, i: number) => (
                                            <div key={i} style={{
                                                background: 'rgba(239, 68, 68, 0.1)',
                                                border: '1px solid rgba(239, 68, 68, 0.2)',
                                                padding: '0.75rem 1.25rem',
                                                borderRadius: '12px',
                                                color: 'var(--text-main)',
                                                fontSize: '0.95rem'
                                            }}>
                                                {risk}
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <button
                                    className="btn-primary"
                                    style={{ alignSelf: 'center', background: 'transparent', border: '1px solid var(--glass-border)' }}
                                    onClick={() => setResult(null)}
                                >
                                    Analyze Another Document
                                </button>
                            </div>
                        </motion.div>
                    </AnimatePresence>
                )}
            </main>
        </div >
    );
}

export default App;

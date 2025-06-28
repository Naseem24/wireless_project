// frontend/src/pages/OfdmPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import './CalculatorPage.css';

// !! IMPORTANT: Replace with your backend URL
const API_URL = "https://wireless-project-backend.onrender.com/api/ofdm-systems";

function OfdmPage() {
    const [formData, setFormData] = useState({
        modulationOrder: '64',
        rbBw: '180',
        subcarrierSpacing: '15',
        symbolsPerRb: '7',
        parallelRbs: '100',
        rbDurationMs: '0.5'
    });
    const [results, setResults] = useState(null);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setResults(null);
        try {
            const response = await axios.post(API_URL, formData);
            setResults(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'An error occurred.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="calculator-page">
            <h1>2. OFDM System</h1>
            <div className="calculator-container">
                <form className="form-section" onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="modulationOrder">Modulation Order (e.g., 64)</label>
                        <input id="modulationOrder" name="modulationOrder" type="number" value={formData.modulationOrder} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="rbBw">Resource Block Bandwidth (kHz)</label>
                        <input id="rbBw" name="rbBw" type="number" value={formData.rbBw} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="subcarrierSpacing">Subcarrier Spacing (kHz)</label>
                        <input id="subcarrierSpacing" name="subcarrierSpacing" type="number" value={formData.subcarrierSpacing} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="symbolsPerRb">OFDM Symbols per RB</label>
                        <input id="symbolsPerRb" name="symbolsPerRb" type="number" value={formData.symbolsPerRb} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="parallelRbs">Parallel Resource Blocks</label>
                        <input id="parallelRbs" name="parallelRbs" type="number" value={formData.parallelRbs} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="rbDurationMs">Resource Block Duration (ms)</label>
                        <input id="rbDurationMs" name="rbDurationMs" type="number" step="0.01" value={formData.rbDurationMs} onChange={handleChange} required />
                    </div>
                    <button type="submit" className="calculate-btn" disabled={isLoading}>{isLoading ? 'Calculating...' : 'Calculate & Analyze'}</button>
                </form>
                <div className="results-section">
                    <div className="results-box">
                        {isLoading && <div className="spinner"></div>}
                        {error && <div className="error-message">{error}</div>}
                        {results && (
                            <div className="results-content">
                                <h2>Analysis Results</h2>
                                <div className="numerical-results">
                                    <h3>Key Metrics</h3>
                                    {Object.entries(results.numericalResults).map(([key, value]) => <p key={key}><strong>{key}:</strong> {value}</p>)}
                                </div>
                                <div className="ai-explanation">
                                    <h3>AI-Powered Explanation</h3>
                                    {results.aiExplanation.split('\n').map((paragraph, index) => <p key={index}>{paragraph}</p>)}
                                </div>
                            </div>
                        )}
                        {!isLoading && !results && !error && <span>Results will appear here...</span>}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default OfdmPage;
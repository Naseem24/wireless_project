// frontend/src/pages/LinkBudgetPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import './CalculatorPage.css';

// !! IMPORTANT: Replace with your backend URL
const API_URL = "YOUR_BACKEND_URL_HERE/api/link-budget";

function LinkBudgetPage() {
    const [formData, setFormData] = useState({
        dataRateBps: '1000000',
        systemTempK: '290',
        noiseFigureDb: '3',
        ebNoDb: '10',
        fadeMarginDb: '10',
        pathLossDb: '120',
        txGainDbi: '5',
        rxGainDbi: '5',
        otherLossesDb: '2'
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
            <h1>3. Link Budget</h1>
            <div className="calculator-container">
                <form className="form-section" onSubmit={handleSubmit}>
                    <div className="form-group"><label>Data Rate (bps)</label><input name="dataRateBps" type="number" value={formData.dataRateBps} onChange={handleChange} required /></div>
                    <div className="form-group"><label>System Temperature (K)</label><input name="systemTempK" type="number" value={formData.systemTempK} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Receiver Noise Figure (dB)</label><input name="noiseFigureDb" type="number" value={formData.noiseFigureDb} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Required Eb/No (dB)</label><input name="ebNoDb" type="number" value={formData.ebNoDb} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Fade Margin (dB)</label><input name="fadeMarginDb" type="number" value={formData.fadeMarginDb} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Path Loss (dB)</label><input name="pathLossDb" type="number" value={formData.pathLossDb} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Transmit Antenna Gain (dBi)</label><input name="txGainDbi" type="number" value={formData.txGainDbi} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Receive Antenna Gain (dBi)</label><input name="rxGainDbi" type="number" value={formData.rxGainDbi} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Other Losses (dB)</label><input name="otherLossesDb" type="number" value={formData.otherLossesDb} onChange={handleChange} required /></div>
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

export default LinkBudgetPage;
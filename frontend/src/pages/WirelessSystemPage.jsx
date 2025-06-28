// frontend/src/pages/WirelessSystemPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import './CalculatorPage.css'; // We need to create this shared CSS file

// !! IMPORTANT: Replace with your backend URL when ready to deploy
const API_URL = "https://wireless-project-qokp.onrender.com";
// Example Deployed URL: "https://your-backend-name.onrender.com/api/wireless-system"

function WirelessSystemPage() {
    const [formData, setFormData] = useState({
        bandwidth: '4000',
        quantizerBits: '8',
        sourceCoderRate: '0.25',
        channelCoderRate: '0.5',
        burstSizeBits: '2048'
    });
    const [results, setResults] = useState(null);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setResults(null);
        try {
            const response = await axios.post(API_URL, formData);
            setResults(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'An error occurred. Please check the backend connection.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="calculator-page">
            <h1>1. Wireless Communication System</h1>
            <div className="calculator-container">
                <form className="form-section" onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="bandwidth">Bandwidth (Hz)</label>
                        <input id="bandwidth" name="bandwidth" type="number" value={formData.bandwidth} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="quantizerBits">Quantizer Bits</label>
                        <input id="quantizerBits" name="quantizerBits" type="number" value={formData.quantizerBits} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="sourceCoderRate">Source Coder Rate (e.g., 0.25 for 4:1 compression)</label>
                        <input id="sourceCoderRate" name="sourceCoderRate" type="number" step="0.01" value={formData.sourceCoderRate} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="channelCoderRate">Channel Coder Rate (e.g., 0.5 for rate-1/2)</label>
                        <input id="channelCoderRate" name="channelCoderRate" type="number" step="0.01" value={formData.channelCoderRate} onChange={handleChange} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="burstSizeBits">Burst Format Size (bits)</label>
                        <input id="burstSizeBits" name="burstSizeBits" type="number" value={formData.burstSizeBits} onChange={handleChange} required />
                    </div>
                    <button type="submit" className="calculate-btn" disabled={isLoading}>
                        {isLoading ? 'Calculating...' : 'Calculate & Analyze'}
                    </button>
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
                                    {/* This code dynamically creates a paragraph for each result */}
                                    {Object.entries(results.numericalResults).map(([key, value]) => (
                                        <p key={key}><strong>{key}:</strong> {value}</p>
                                    ))}
                                </div>
                                <div className="ai-explanation">
                                    <h3>AI-Powered Explanation</h3>
                                    {/* This code splits the AI response by newlines to preserve paragraphs */}
                                    {results.aiExplanation.split('\n').map((paragraph, index) => (
                                        <p key={index}>{paragraph}</p>
                                    ))}
                                </div>
                            </div>
                        )}
                        {/* This is the placeholder text */}
                        {!isLoading && !results && !error && <span>Results will appear here...</span>}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default WirelessSystemPage;
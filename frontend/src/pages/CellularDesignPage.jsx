// frontend/src/pages/CellularDesignPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import './CalculatorPage.css';

// !! IMPORTANT: Replace with your backend URL
const API_URL = "https://wireless-project-backend.onrender.com/api/cellular-design";

function CellularDesignPage() {
    const [formData, setFormData] = useState({
        totalAreaSqkm: '1000',
        cellRadiusKm: '2',
        numSubscribers: '50000',
        callsPerHour: '2',
        callDurationMin: '1.5',
        blockingProb: '0.02',
        sirDb: '9',
        pathLossExp: '4'
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
            <h1>4. Cellular System Design</h1>
            <div className="calculator-container">
                <form className="form-section" onSubmit={handleSubmit}>
                    <div className="form-group"><label>Total Coverage Area (km²)</label><input name="totalAreaSqkm" type="number" value={formData.totalAreaSqkm} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Cell Radius (km)</label><input name="cellRadiusKm" type="number" value={formData.cellRadiusKm} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Number of Subscribers</label><input name="numSubscribers" type="number" value={formData.numSubscribers} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Avg. Calls per User per Hour</label><input name="callsPerHour" type="number" value={formData.callsPerHour} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Avg. Call Duration (minutes)</label><input name="callDurationMin" type="number" value={formData.callDurationMin} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Desired Blocking Probability (e.g., 0.02 for 2%)</label><input name="blockingProb" type="number" step="0.001" value={formData.blockingProb} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Required SIR (dB)</label><input name="sirDb" type="number" value={formData.sirDb} onChange={handleChange} required /></div>
                    <div className="form-group"><label>Path Loss Exponent</label><input name="pathLossExp" type="number" value={formData.pathLossExp} onChange={handleChange} required /></div>
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

export default CellularDesignPage;
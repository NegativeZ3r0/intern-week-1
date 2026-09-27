import { useState, useEffect } from 'react';
import './App.css';

interface FacilityFormState {
  cleanliness_score: string;
  odor_score: string;
  waste_level: string;
  complaints: string;
  footfall: string;
  hours_since_cleaning: string;
}

const fieldConfig: Record<keyof FacilityFormState, { label: string; min: number; max?: number; step: number }> = {
  cleanliness_score: { label: 'Cleanliness Score', min: 0, max: 10, step: 0.1 },
  odor_score: { label: 'Odor Score', min: 0, max: 10, step: 0.1 },
  waste_level: { label: 'Waste Level', min: 0, max: 100, step: 0.1 },
  complaints: { label: 'Complaints', min: 0, step: 1 },
  footfall: { label: 'Footfall', min: 0, step: 1 },
  hours_since_cleaning: { label: 'Hours Since Cleaning', min: 0, step: 0.1 }
};

function App() {
  // Theme State: Check system preference on initial load
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  const [formData, setFormData] = useState<FacilityFormState>({
    cleanliness_score: '5.0',
    odor_score: '5.0',
    waste_level: '50.0',
    complaints: '0',
    footfall: '100',
    hours_since_cleaning: '12.0'
  });
  const [prediction, setPrediction] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Apply data-theme to the document root whenever isDark changes
  useEffect(() => {
    if (isDark) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  }, [isDark]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value // Keep as raw string during typing to allow backspacing
    }));
  };

  const handleSubmit = async (e: React.SubmitEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    // Parse strings to numbers only when submitting payload
    const payload = {
      cleanliness_score: parseFloat(formData.cleanliness_score) || 0,
      odor_score: parseFloat(formData.odor_score) || 0,
      waste_level: parseFloat(formData.waste_level) || 0,
      complaints: parseInt(formData.complaints, 10) || 0,
      footfall: parseInt(formData.footfall, 10) || 0,
      hours_since_cleaning: parseFloat(formData.hours_since_cleaning) || 0,
    };

    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error("Invalid data submitted or server error.");
      }

      const data = await response.json();
      setPrediction(data.predicted_hygiene_risk);
    } catch (err: any) {
      console.error("API Error:", err);
      setError(err.message || "Error generating prediction");
    } finally {
      setLoading(false);
    }
  };

  // NEW: Helper function to determine the color class safely
  // checking for keywords in case the API returns "Low Risk", etc.
  const getRiskClass = (pred: string) => {
    const lowerPred = pred.toLowerCase();
    if (lowerPred.includes('low')) return 'low';
    if (lowerPred.includes('medium')) return 'medium';
    if (lowerPred.includes('high')) return 'high';
    return ''; // Fallback to default blue if unknown
  };

  return (
    <div className="page-wrapper">
      <div className="app-container">
        <div className="app-header">
          <h2 className="app-title">Hygiene Risk Predictor</h2>
          <button
            type="button"
            className="theme-toggle"
            onClick={() => setIsDark(!isDark)}
            aria-label="Toggle Dark Mode"
            title="Toggle Theme"
          >
            {isDark ? '☀️' : '🌙'}
          </button>
        </div>

        <form onSubmit={handleSubmit} className="prediction-form">
          {(Object.keys(fieldConfig) as Array<keyof FacilityFormState>).map((key) => {
            const config = fieldConfig[key];
            return (
              <div key={key} className="form-group">
                <label className="form-label">{config.label}</label>
                <input
                  type="number"
                  name={key}
                  min={config.min}
                  max={config.max}
                  step={config.step}
                  value={formData[key]}
                  onChange={handleChange}
                  required
                  className="form-input"
                />
              </div>
            );
          })}

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? "Predicting..." : "Predict Risk"}
          </button>
        </form>

        {error && (
          <div className="result-box error-box">
            {error}
          </div>
        )}

        {prediction && (
          /* UPDATED: Apply dynamic class based on prediction value */
          <div className={`result-box ${getRiskClass(prediction)}`}>
            Prediction: {prediction}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

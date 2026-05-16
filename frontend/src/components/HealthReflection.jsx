import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

const INITIAL_VITALS = {
  spO2: "",
  systolic: "",
  diastolic: "",
  heartRate: "",
  temperature: "",
};

const vitalCards = [
  {
    key: "spO2",
    label: "Oxygen Saturation",
    shortLabel: "SpO2",
    placeholder: "98",
    unit: "%",
    hint: "Usually 95-100%",
    explainer: "Shows how much oxygen your blood is carrying.",
  },
  {
    key: "systolic",
    label: "Blood Pressure (Systolic)",
    shortLabel: "Systolic",
    placeholder: "120",
    unit: "mmHg",
    hint: "Usually below 120",
    explainer: "Top number that reflects pressure when the heart pumps.",
  },
  {
    key: "diastolic",
    label: "Blood Pressure (Diastolic)",
    shortLabel: "Diastolic",
    placeholder: "80",
    unit: "mmHg",
    hint: "Usually below 80",
    explainer: "Bottom number that reflects pressure between beats.",
  },
  {
    key: "heartRate",
    label: "Heart Rate",
    shortLabel: "Heart Rate",
    placeholder: "72",
    unit: "bpm",
    hint: "Usually 60-100 bpm",
    explainer: "How many times your heart beats in one minute at rest.",
  },
  {
    key: "temperature",
    label: "Body Temperature",
    shortLabel: "Temperature",
    placeholder: "36.8",
    unit: "deg C",
    hint: "Usually 36.1-37.2 deg C",
    explainer: "A basic sign that can reflect infection or inflammation.",
  },
];

export default function HealthReflection() {
  const navigate = useNavigate();
  const [vitals, setVitals] = useState(INITIAL_VITALS);
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const enteredCount = useMemo(
    () => Object.values(vitals).filter((value) => value !== "").length,
    [vitals]
  );

  const enteredVitals = useMemo(
    () =>
      vitalCards
        .filter((card) => vitals[card.key] !== "")
        .map((card) => ({
          label: card.label,
          value: `${vitals[card.key]} ${card.unit}`,
        })),
    [vitals]
  );

  const handleChange = ({ target }) => {
    const { name, value } = target;
    setError("");
    setVitals((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleGetInsights = () => {
    if (!enteredCount) {
      setError("Enter at least one vital to continue.");
      return;
    }

    setError("");
    setSubmitted(true);
  };

  const resetForm = () => {
    setVitals(INITIAL_VITALS);
    setSubmitted(false);
    setError("");
  };

  return (
    <div className="health-reflection-page">
      <motion.div
        className="reflection-header reflection-shell"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
      >
        <div className="feature-orbit orbit-left" aria-hidden="true" />
        <div className="feature-orbit orbit-right" aria-hidden="true" />
        <button onClick={() => navigate("/dashboard")} className="back-btn" type="button">
          {"<-"} Dashboard
        </button>
        <div className="reflection-header-copy">
          <span className="page-kicker">Profile 1</span>
          <h1 className="reflection-title">Health Reflection Tool</h1>
          <p className="reflection-desc">
            Enter whichever vitals you have and review them in one clean place.
          </p>
        </div>
        <div className="reflection-header-meta">
          <div className="reflection-meta-card">
            <span className="meta-label">Inputs added</span>
            <strong>{enteredCount}/5</strong>
            <p>Every vital stays optional.</p>
          </div>
        </div>
      </motion.div>

      <div className="reflection-shell reflection-grid reflection-grid-fluid">
        <motion.section
          className="reflection-panel"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.08 }}
        >
          <div className="panel-head">
            <div>
              <p className="panel-kicker">Input Vitals</p>
              <h2 className="panel-title">Add the readings you have today</h2>
            </div>
            <p className="panel-note">
              You can enter one vital or all of them. Every field stays optional.
            </p>
          </div>

          <div className="reflection-vitals-grid">
            {vitalCards.map((card, index) => (
              <motion.label
                key={card.key}
                className="reflection-vital-card"
                initial={{ opacity: 0, y: 14 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 + index * 0.05 }}
              >
                <div className="reflection-vital-head">
                  <div>
                    <span className="reflection-vital-short">{card.shortLabel}</span>
                    <h3>{card.label}</h3>
                  </div>
                  <span className="optional-badge">Optional</span>
                </div>
                <p className="reflection-vital-explainer">{card.explainer}</p>
                <div className="reflection-input-wrap">
                  <input
                    className="reflection-input"
                    type="number"
                    name={card.key}
                    placeholder={card.placeholder}
                    step={card.key === "temperature" || card.key === "spO2" ? "0.1" : "1"}
                    value={vitals[card.key]}
                    onChange={handleChange}
                  />
                  <span className="reflection-unit">{card.unit}</span>
                </div>
                <span className="reflection-hint">{card.hint}</span>
              </motion.label>
            ))}
          </div>

          <div className="reflection-actions">
            <motion.button
              type="button"
              className="btn-analyze"
              onClick={handleGetInsights}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
            >
              Get Insights
            </motion.button>
            <button type="button" className="btn-reset subtle-reset" onClick={resetForm}>
              Clear values
            </button>
          </div>

          {error ? <p className="reflection-error">{error}</p> : null}
        </motion.section>

        <motion.section
          className="reflection-panel reflection-results-panel reflection-status-panel"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.14 }}
        >
          <div className="panel-head">
            <div>
              <p className="panel-kicker">Insights</p>
              <h2 className="panel-title">Your reflection area</h2>
            </div>
            <p className="panel-note">
              Reflections will appear here when available.
            </p>
          </div>

          <div className="reflection-backend-card">
            <h3>Nothing to show here yet</h3>
            <p>Add your readings and this space can display your reflection when available.</p>
          </div>

          {submitted ? (
            <div className="reflection-entered-card">
              <div className="suggestions-head">
                <h3>Entered vitals</h3>
                <span>{enteredVitals.length} added</span>
              </div>
              <div className="reflection-entered-list">
                {enteredVitals.map((item) => (
                  <div key={item.label} className="reflection-entered-row">
                    <span>{item.label}</span>
                    <strong>{item.value}</strong>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="reflection-empty reflection-empty-compact">
              <div className="reflection-empty-ring">
                <span>...</span>
              </div>
              <h3>No insights yet</h3>
              <p>Enter vitals on the left to start filling this section.</p>
            </div>
          )}
        </motion.section>
      </div>
    </div>
  );
}

import { useMemo, useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { postVitals, getVitalsHistory, getCurrentUserEmail } from "../services/api";

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
  const [analysisResult, setAnalysisResult] = useState(null);
  const [vitalsHistory, setVitalsHistory] = useState([]);
  const [activePanel, setActivePanel] = useState("insights");

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

  const handleGetInsights = async () => {
    if (!enteredCount) {
      setError("Enter at least one vital to continue.");
      return;
    }

    setError("");
    setSubmitted(false);
    setAnalysisResult(null);

    const payload = {
      heart_rate: vitals.heartRate ? parseFloat(vitals.heartRate) : undefined,
      spo2: vitals.spO2 ? parseFloat(vitals.spO2) : undefined,
      temperature: vitals.temperature ? parseFloat(vitals.temperature) : undefined,
      systolic_bp: vitals.systolic ? parseFloat(vitals.systolic) : undefined,
      diastolic_bp: vitals.diastolic ? parseFloat(vitals.diastolic) : undefined,
    };

    try {
      const data = await postVitals(payload, getCurrentUserEmail());
      setAnalysisResult(data);
      setSubmitted(true);
    } catch (err) {
      setError(err.message || "Could not get vitals insights right now.");
    } finally {
      await loadVitalsHistory();
    }
  };

  const loadVitalsHistory = async () => {
    try {
      const response = await getVitalsHistory(getCurrentUserEmail());
      setVitalsHistory(response.records || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadVitalsHistory();
  }, []);

  const downloadReport = () => {
    if (!analysisResult) {
      return;
    }

    const lines = [];
    lines.push("CareInCode Health Reflection Report");
    lines.push("");
    lines.push(`Summary: ${analysisResult.summary || "No summary available."}`);
    lines.push(`Risk Level: ${analysisResult.risk_level || "Unknown"}`);
    lines.push("");

    if (analysisResult.risk_indicators?.length) {
      lines.push("Risk Indicators:");
      analysisResult.risk_indicators.forEach((item) => {
        lines.push(`- ${item.type} (${item.severity || "unknown"})`);
      });
      lines.push("");
    }

    if (analysisResult.evidence?.length) {
      lines.push("Evidence:");
      analysisResult.evidence.forEach((item) => {
        lines.push(`- ${item}`);
      });
      lines.push("");
    }

    if (analysisResult.next_steps?.length) {
      lines.push("Next Steps:");
      analysisResult.next_steps.forEach((item) => {
        lines.push(`- ${item}`);
      });
      lines.push("");
    }

    if (analysisResult.doctor_prep?.questions?.length) {
      lines.push("Questions For Doctor:");
      analysisResult.doctor_prep.questions.forEach((item) => {
        lines.push(`- ${item}`);
      });
      lines.push("");
    }

    lines.push(`Disclaimer: ${analysisResult.disclaimer || "Educational information only."}`);
    lines.push(`Confidence: ${analysisResult.confidence ?? "N/A"}`);

    const blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "vitals-reflection-report.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const resetForm = () => {
    setVitals(INITIAL_VITALS);
    setSubmitted(false);
    setAnalysisResult(null);
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
          <div className="reflection-panel-tabs">
            <button
              type="button"
              className={activePanel === "insights" ? "panel-tab active" : "panel-tab"}
              onClick={() => setActivePanel("insights")}
            >
              Insights
            </button>
            <button
              type="button"
              className={activePanel === "history" ? "panel-tab active" : "panel-tab"}
              onClick={() => setActivePanel("history")}
            >
              History
            </button>
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
            {analysisResult ? (
              <button type="button" className="btn-download subtle-reset" onClick={downloadReport}>
                Download report
              </button>
            ) : null}
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
            {activePanel === "history" ? (
              <>
                <h3>Vitals History</h3>
                {vitalsHistory.length ? (
                  <div className="history-list">
                    {vitalsHistory.map((record) => (
                      <div key={record._id} className="history-record-card">
                        <div className="history-record-header">
                          <span>{new Date(record.created_at).toLocaleString()}</span>
                          <strong>{record.analysis?.summary || "Vitals review"}</strong>
                        </div>
                        <div className="history-record-values">
                          {Object.entries(record.vitals || {}).map(([key, value]) => (
                            <span key={key}>
                              {key.replace(/_/g, " ")}: {value}
                            </span>
                          ))}
                        </div>
                        <div className="history-record-footer">
                          <span>Risk level: {record.analysis?.risk_level || "N/A"}</span>
                          <span>Confidence: {record.analysis?.confidence ?? "N/A"}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="history-empty">
                    No past vitals searches yet. Your previous analysis will appear here.
                  </div>
                )}
              </>
            ) : analysisResult ? (
              <>
                <h3>Insights</h3>
                <p>{analysisResult.summary}</p>
                <div className="reflection-report-summary">
                  <strong>Risk Level</strong>
                  <span>{analysisResult.risk_level?.toUpperCase() || "N/A"}</span>
                </div>
                {analysisResult.risk_indicators?.length ? (
                  <div className="reflection-report-section">
                    <h4>Risk Indicators</h4>
                    <ul>
                      {analysisResult.risk_indicators.map((item, idx) => (
                        <li key={idx}>{`${item.type} (${item.severity})`}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
                {analysisResult.evidence?.length ? (
                  <div className="reflection-report-section">
                    <h4>Evidence</h4>
                    <ul>
                      {analysisResult.evidence.map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
                {analysisResult.next_steps?.length ? (
                  <div className="reflection-next-steps">
                    <h4>Next steps</h4>
                    <ul>
                      {analysisResult.next_steps.map((step, idx) => (
                        <li key={idx}>{step}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
                {analysisResult.doctor_prep?.questions?.length ? (
                  <div className="reflection-report-section">
                    <h4>Questions For Doctor</h4>
                    <ul>
                      {analysisResult.doctor_prep.questions.map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}
                <div className="reflection-report-footer">
                  <p>{analysisResult.disclaimer}</p>
                  <p>Confidence: {analysisResult.confidence ?? "N/A"}</p>
                </div>
              </>
            ) : (
              <>
                <h3>Nothing to show here yet</h3>
                <p>Add your readings and this space can display your reflection when available.</p>
              </>
            )}
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

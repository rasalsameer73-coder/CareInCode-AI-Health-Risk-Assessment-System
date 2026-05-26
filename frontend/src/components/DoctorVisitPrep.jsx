import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  loadDoctorVisitPrep as loadDoctorVisitPrepService,
  saveDoctorVisitPrep,
  getDoctorVisitPrepHistory,
  downloadDoctorVisitSummaryPdf,
  getCurrentUserEmail,
} from "../services/api";

function formatIST(timestamp) {
  if (!timestamp) return "Unknown date";
  return new Date(timestamp).toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    hour12: false,
  });
}

const intensityLabels = {
  1: "Very mild",
  2: "Very mild",
  3: "Mild",
  4: "Noticeable",
  5: "Moderate",
  6: "Moderate",
  7: "Strong",
  8: "Strong",
  9: "Severe",
  10: "Severe",
};

function formatIsoDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function parseLocalDate(dateValue) {
  const [year, month, day] = dateValue.split("-").map(Number);
  return new Date(year, month - 1, day);
}

function prettyDate(dateValue) {
  return parseLocalDate(dateValue).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function buildCalendarDays(selectedDate, symptoms) {
  const selected = parseLocalDate(selectedDate);
  const weekday = selected.getDay();
  const mondayOffset = weekday === 0 ? -6 : 1 - weekday;
  const start = new Date(selected);
  start.setDate(selected.getDate() + mondayOffset);

  return Array.from({ length: 14 }, (_, index) => {
    const day = new Date(start);
    day.setDate(start.getDate() + index);
    const iso = formatIsoDate(day);
    const logsForDay = symptoms.filter((entry) => entry.date === iso);
    const strongestEntry = logsForDay.reduce(
      (current, entry) => (entry.intensity > current.intensity ? entry : current),
      { intensity: 0 }
    );

    return {
      iso,
      label: day.toLocaleDateString("en-GB", { weekday: "short" }),
      dateNumber: day.getDate(),
      month: day.toLocaleDateString("en-GB", { month: "short" }),
      isSelected: iso === selectedDate,
      hasEntries: logsForDay.length > 0,
      intensity: strongestEntry.intensity,
    };
  });
}

export default function DoctorVisitPrep() {
  const navigate = useNavigate();
  const today = formatIsoDate(new Date());
  const USER_ID = getCurrentUserEmail();

  const [medications, setMedications] = useState([
    {
      id: "med-sample",
      name: "Vitamin D3",
      dosage: "1000 IU daily",
      reason: "Low Vitamin D",
    },
  ]);
  const [medicationDraft, setMedicationDraft] = useState({
    name: "",
    dosage: "",
    reason: "",
  });
  const [symptoms, setSymptoms] = useState([
    {
      id: "sym-1",
      date: today,
      location: "Knee joints",
      intensity: 4,
      triggers: "After climbing stairs",
      notes: "Felt a dull ache in both knees by evening.",
    },
  ]);
  const [selectedDate, setSelectedDate] = useState(today);
  const [symptomDraft, setSymptomDraft] = useState({
    location: "",
    intensity: 5,
    triggers: "",
    notes: "",
  });
  const [summary, setSummary] = useState(null);
  const [historyRecords, setHistoryRecords] = useState([]);
  const [activePanel, setActivePanel] = useState("details");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [savedMessage, setSavedMessage] = useState("");
  const [error, setError] = useState("");

  const calendarDays = useMemo(
    () => buildCalendarDays(selectedDate, symptoms),
    [selectedDate, symptoms]
  );

  const selectedDayEntries = useMemo(
    () => symptoms.filter((entry) => entry.date === selectedDate),
    [selectedDate, symptoms]
  );

  useEffect(() => {
    loadDoctorVisitPrep(USER_ID);
    loadDoctorVisitPrepHistory();
  }, [USER_ID]);

  const loadDoctorVisitPrepHistory = async () => {
    try {
      const response = await getDoctorVisitPrepHistory(USER_ID);
      setHistoryRecords(response.records || []);
    } catch (err) {
      console.error(err);
    }
  };

  const sortedSymptoms = useMemo(
    () => [...symptoms].sort((a, b) => a.date.localeCompare(b.date)),
    [symptoms]
  );

  const addMedication = () => {
    if (!medicationDraft.name.trim()) {
      setError("Add the medication name before saving.");
      return;
    }

    setError("");

    const nextMedications = [
      ...medications,
      {
        id: `med-${Date.now()}`,
        ...medicationDraft,
      },
    ];

    setMedications(nextMedications);
    setMedicationDraft({ name: "", dosage: "", reason: "" });
    syncDoctorVisitData(nextMedications, symptoms);
  };

  const addSymptom = () => {
    if (!symptomDraft.notes.trim()) {
      setError("Write a short note about what you felt on that day.");
      return;
    }

    setError("");

    const nextSymptoms = [...symptoms, { id: `sym-${Date.now()}`, date: selectedDate, ...symptomDraft }].sort(
      (a, b) => a.date.localeCompare(b.date)
    );

    setSymptoms(nextSymptoms);
    setSymptomDraft({
      location: "",
      intensity: 5,
      triggers: "",
      notes: "",
    });
    syncDoctorVisitData(medications, nextSymptoms);
  };

  const removeMedication = (id) => {
    const nextMedications = medications.filter((item) => item.id !== id);
    setMedications(nextMedications);
    syncDoctorVisitData(nextMedications, symptoms);
  };

  const removeSymptom = (id) => {
    const nextSymptoms = symptoms.filter((item) => item.id !== id);
    setSymptoms(nextSymptoms);
    syncDoctorVisitData(medications, nextSymptoms);
  };

  async function syncDoctorVisitData(nextMedications, nextSymptoms) {
    setSaving(true);
    setSavedMessage("");

    try {
      const savedRecord = await saveDoctorVisitPrep({
        user_id: USER_ID,
        medications: nextMedications,
        symptoms: nextSymptoms,
      });
      setSummary(savedRecord.summary || null);
      setSavedMessage("Saved to backend");
      window.setTimeout(() => setSavedMessage(""), 2500);
      await loadDoctorVisitPrepHistory();
    } catch (err) {
      console.error(err);
      setSavedMessage("Unable to save right now.");
    } finally {
      setSaving(false);
    }
  };

  async function loadDoctorVisitPrep() {
    try {
      const data = await loadDoctorVisitPrepService(USER_ID);
      setMedications(data.medications || []);
      setSymptoms(data.symptoms || []);
      setSummary(data.summary || null);
    } catch (err) {
      console.error(err);
    }
  }

  const generateSummary = async () => {
    if (!medications.length && !symptoms.length) {
      setError("Add medication or symptom details before generating the summary.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const savedRecord = await saveDoctorVisitPrep({
        user_id: USER_ID,
        medications,
        symptoms,
      });
      setSummary(savedRecord.summary || null);
      setSavedMessage("Summary generated and saved by backend");
      window.setTimeout(() => setSavedMessage(""), 2500);
      await loadDoctorVisitPrepHistory();
    } catch (err) {
      console.error(err);
      setSavedMessage("Unable to generate summary right now.");
    } finally {
      setLoading(false);
    }
  };

  const downloadSummary = async () => {
    if (!summary) {
      return;
    }

    try {
      const blob = await downloadDoctorVisitSummaryPdf(USER_ID);
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `doctor-visit-summary-${today}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      setError(err.message || "Could not download the PDF summary.");
    }
  };

  return (
    <div className="doctor-visit-page">
      <motion.div
        className="dv-header dv-shell"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
      >
        <div className="feature-orbit orbit-left" aria-hidden="true" />
        <div className="feature-orbit orbit-right" aria-hidden="true" />
        <button onClick={() => navigate("/dashboard")} className="back-btn" type="button">
          {"<-"} Dashboard
        </button>
        <div className="profile-page-top">
          <div className="profile-page-kicker-wrap">
            <span className="page-kicker">Profile 3</span>
          </div>
          <div className="profile-page-title-wrap">
            <h1 className="dv-title profile-page-heading">Doctor Visit Preparation</h1>
          </div>
        </div>

        <div className="profile-page-copy">
          <p className="dv-desc">
            Keep a clean list of medications, log symptoms by date, and let CareInCode shape it
            into a doctor-ready summary before the appointment.
          </p>
        </div>

        <div className="profile-meta-row">
          <div className="dv-header-stat profile-meta-card">
            <span className="meta-label">Visit status</span>
            <strong>Ready for consult</strong>
            <p>Medication history and symptom progression stay together in one place.</p>
          </div>
          <div className="dv-header-stat profile-meta-card">
            <span className="meta-label">Items tracked</span>
            <strong>{medications.length + symptoms.length}</strong>
            <p>Everything logged here can later feed the final doctor summary.</p>
          </div>
        </div>
        <div className="profile-page-tabs">
          <button
            type="button"
            className={activePanel === "details" ? "panel-tab active" : "panel-tab"}
            onClick={() => setActivePanel("details")}
          >
            Prep details
          </button>
          <button
            type="button"
            className={activePanel === "history" ? "panel-tab active" : "panel-tab"}
            onClick={() => setActivePanel("history")}
          >
            Saved history
          </button>
        </div>
      </motion.div>

      {activePanel === "details" ? (
        <>
          <div className="dv-shell dv-main-grid">
            <motion.section
              className="dv-card dv-card-balanced"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08 }}
        >
          <div className="dv-card-head">
            <div>
              <p className="panel-kicker">Medication log</p>
              <h2 className="panel-title">Current medications and why you take them</h2>
            </div>
            <p className="panel-note">A simple list your doctor can scan in seconds.</p>
          </div>

          <div className="dv-form-card">
            <div className="dv-form-grid">
              <label className="dv-field">
                <span>Medication name</span>
                <input
                  className="form-input"
                  type="text"
                  placeholder="Metformin"
                  value={medicationDraft.name}
                  onChange={(event) =>
                    setMedicationDraft((current) => ({ ...current, name: event.target.value }))
                  }
                />
              </label>
              <label className="dv-field">
                <span>Dosage</span>
                <input
                  className="form-input"
                  type="text"
                  placeholder="500 mg twice daily"
                  value={medicationDraft.dosage}
                  onChange={(event) =>
                    setMedicationDraft((current) => ({ ...current, dosage: event.target.value }))
                  }
                />
              </label>
            </div>
            <label className="dv-field">
              <span>What is it for?</span>
              <textarea
                className="form-textarea"
                rows="3"
                placeholder="Diabetes management, pain relief, thyroid support..."
                value={medicationDraft.reason}
                onChange={(event) =>
                  setMedicationDraft((current) => ({ ...current, reason: event.target.value }))
                }
              />
            </label>
            <button type="button" className="btn-add-item" onClick={addMedication}>
              Add medication
            </button>
          </div>

          <div className="dv-stacked-list">
            {medications.map((medication) => (
              <article key={medication.id} className="dv-log-card">
                <div>
                  <h3>{medication.name}</h3>
                  <p>{medication.dosage || "Dosage not added yet"}</p>
                  <span>{medication.reason || "Reason not added yet"}</span>
                </div>
                <button
                  type="button"
                  className="btn-remove"
                  onClick={() => removeMedication(medication.id)}
                  aria-label={`Remove ${medication.name}`}
                >
                  x
                </button>
              </article>
            ))}
          </div>
        </motion.section>

        <motion.section
          className="dv-card dv-card-balanced"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.14 }}
        >
          <div className="dv-card-head">
            <div>
              <p className="panel-kicker">Symptom logger</p>
              <h2 className="panel-title dv-title-inline">Pick a day and write what changed</h2>
            </div>
            <p className="panel-note">
              This acts like a midway calendar: select a day, then note pain, aggravation, or new
              symptoms neatly.
            </p>
          </div>

          <div className="dv-calendar-card">
            <div className="dv-calendar-head">
              <div>
                <span className="mini-label">Selected day</span>
                <strong>{prettyDate(selectedDate)}</strong>
              </div>
              <input
                className="form-input dv-date-input"
                type="date"
                value={selectedDate}
                onChange={(event) => setSelectedDate(event.target.value)}
              />
            </div>

            <div className="dv-calendar-grid">
              {calendarDays.map((day) => (
                <button
                  key={day.iso}
                  type="button"
                  className={`dv-day-card${day.isSelected ? " selected" : ""}${
                    day.hasEntries ? " has-entry" : ""
                  }`}
                  onClick={() => setSelectedDate(day.iso)}
                >
                  <span>{day.label}</span>
                  <strong>{day.dateNumber}</strong>
                  <small>{day.month}</small>
                  {day.hasEntries ? <em>{day.intensity}/10</em> : <i>No log</i>}
                </button>
              ))}
            </div>
          </div>

          <div className="dv-form-card">
            <div className="dv-form-grid">
              <label className="dv-field">
                <span>Where is the pain or discomfort?</span>
                <input
                  className="form-input"
                  type="text"
                  placeholder="Lower back, left shoulder, joints..."
                  value={symptomDraft.location}
                  onChange={(event) =>
                    setSymptomDraft((current) => ({ ...current, location: event.target.value }))
                  }
                />
              </label>
              <label className="dv-field">
                <span>Intensity</span>
                <div className="dv-intensity-wrap">
                  <input
                    className="dv-range"
                    type="range"
                    min="1"
                    max="10"
                    value={symptomDraft.intensity}
                    onChange={(event) =>
                      setSymptomDraft((current) => ({
                        ...current,
                        intensity: Number(event.target.value),
                      }))
                    }
                  />
                  <div className="dv-intensity-meta">
                    <strong>{symptomDraft.intensity}/10</strong>
                    <span>{intensityLabels[symptomDraft.intensity]}</span>
                  </div>
                </div>
              </label>
            </div>
            <label className="dv-field">
              <span>What seemed to trigger it?</span>
              <input
                className="form-input"
                type="text"
                placeholder="After walking, after sitting for long, after meals..."
                value={symptomDraft.triggers}
                onChange={(event) =>
                  setSymptomDraft((current) => ({ ...current, triggers: event.target.value }))
                }
              />
            </label>
            <label className="dv-field">
              <span>Write what happened that day</span>
              <textarea
                className="form-textarea"
                rows="4"
                placeholder="Today I felt some joint pain. A week later it became sharper while getting up from a chair..."
                value={symptomDraft.notes}
                onChange={(event) =>
                  setSymptomDraft((current) => ({ ...current, notes: event.target.value }))
                }
              />
            </label>
            <button type="button" className="btn-add-item" onClick={addSymptom}>
              Save symptom log
            </button>
          </div>

          <div className="dv-day-summary">
            <div className="dv-day-summary-head">
              <h3>Logs for {prettyDate(selectedDate)}</h3>
              <span>{selectedDayEntries.length} entry{selectedDayEntries.length === 1 ? "" : "ies"}</span>
            </div>
            <div className="dv-stacked-list">
              {selectedDayEntries.length ? (
                selectedDayEntries.map((entry) => (
                  <article key={entry.id} className="dv-log-card">
                    <div>
                      <h3>{entry.location || "General note"}</h3>
                      <p>
                        Intensity {entry.intensity}/10
                        {entry.triggers ? ` - Trigger: ${entry.triggers}` : ""}
                      </p>
                      <span>{entry.notes}</span>
                    </div>
                    <button
                      type="button"
                      className="btn-remove"
                      onClick={() => removeSymptom(entry.id)}
                      aria-label="Remove symptom entry"
                    >
                      x
                    </button>
                  </article>
                ))
              ) : (
                <div className="dv-empty-inline">
                  No symptom note for this date yet. Pick the day, add what you felt, and it will
                  appear here.
                </div>
              )}
            </div>
          </div>
        </motion.section>
      </div>

      <motion.section
        className="dv-shell dv-summary-card"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="dv-card-head">
          <div>
            <p className="panel-kicker">Pre-consultation summary</p>
            <h2 className="panel-title">Generate a clean summary for your doctor</h2>
          </div>
          <p className="panel-note">
            This summary pulls your medications and symptom progression into one clearer story.
          </p>
        </div>

        <div className="dv-summary-actions">
          <motion.button
            type="button"
            className="btn-generate-summary"
            onClick={generateSummary}
            disabled={loading}
            whileHover={{ scale: loading ? 1 : 1.01 }}
            whileTap={{ scale: loading ? 1 : 0.99 }}
          >
            {loading ? (
              <>
                <span className="spinner-small" />
                Building summary...
              </>
            ) : (
              "Generate Summary"
            )}
          </motion.button>
          <button
            type="button"
            className="btn-new-summary"
            onClick={() => syncDoctorVisitData(medications, symptoms, summary)}
            disabled={saving}
          >
            {saving ? "Saving progress..." : "Save progress"}
          </button>
          {summary ? (
            <button type="button" className="btn-new-summary" onClick={downloadSummary}>
              Download PDF summary
            </button>
          ) : null}
        </div>

        {savedMessage ? <p className="reflection-note">{saving ? "Saving..." : savedMessage}</p> : null}

        {error ? <p className="reflection-error">{error}</p> : null}

        {!summary ? (
          <div className="summary-prompt">
            Add medication details and symptom notes first, then generate a doctor-ready summary
            with suggested questions.
          </div>
        ) : (
          <div className="dv-summary-grid">
            <div className="dv-summary-overview">
              <div className="reflection-overview-card">
                <span className="overview-label">Summary overview</span>
                <p>{summary.headline}</p>
              </div>
              <div className="dv-facts-row">
                {summary.facts.map((fact) => (
                  <div key={fact} className="dv-fact-pill">
                    {fact}
                  </div>
                ))}
              </div>
              <div className="reflection-suggestions-card">
                <div className="suggestions-head">
                  <h3>Questions to ask your doctor</h3>
                  <span>{summary.questions.length} ready</span>
                </div>
                <div className="suggestions-list">
                  {summary.questions.map((question, index) => (
                    <div key={question} className="suggestion-item">
                      <span className="question-index">{index + 1}</span>
                      <p>{question}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="summary-display">
              <div className="summary-text">
                {summary.summaryText.split("\n").map((line, index) => (
                  <p key={`${line}-${index}`} className={!line.includes(":") && line ? "summary-heading" : ""}>
                    {line || "\u00A0"}
                  </p>
                ))}
              </div>
            </div>
          </div>
        )}
      </motion.section>

      <motion.section
        className="dv-shell dv-timeline-section"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.24 }}
      >
        <div className="dv-card-head">
          <div>
            <p className="panel-kicker">Progression view</p>
            <h2 className="panel-title">How your symptom story reads over time</h2>
          </div>
          <p className="panel-note">A tidy timeline you can keep updating between appointments.</p>
        </div>

        <div className="dv-timeline-list">
          {sortedSymptoms.length ? (
            sortedSymptoms.map((entry) => (
              <article key={entry.id} className="dv-timeline-item">
                <div className="dv-timeline-marker" />
                <div className="dv-timeline-copy">
                  <div className="dv-timeline-top">
                    <strong>{prettyDate(entry.date)}</strong>
                    <span>{entry.intensity}/10 intensity</span>
                  </div>
                  <h3>{entry.location || "General symptom note"}</h3>
                  <p>{entry.notes}</p>
                  {entry.triggers ? <small>Trigger noted: {entry.triggers}</small> : null}
                </div>
              </article>
            ))
          ) : (
            <div className="dv-empty-inline">No timeline entries yet.</div>
          )}
        </div>
      </motion.section>
    </>
      ) : (
        <motion.section
          className="dv-shell dv-summary-card"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.14 }}
        >
          <div className="dv-card-head">
            <div>
              <p className="panel-kicker">Saved history</p>
              <h2 className="panel-title">Past doctor prep entries</h2>
            </div>
            <p className="panel-note">
              Review previous doctor visit preparation records for this profile.
            </p>
          </div>

          <div className="history-list">
            {historyRecords.length ? (
              historyRecords.map((record) => (
                <article key={record._id} className="history-record-card">
                  <div className="history-record-header">
                    <strong>{record.summary?.headline || "Saved preparation"}</strong>
                    <span>{formatIST(record.created_at)}</span>
                  </div>
                  <div className="history-record-values">
                    <span>Medications: {record.medications?.length ?? 0}</span>
                    <span>Symptom logs: {record.symptoms?.length ?? 0}</span>
                  </div>
                  <div className="history-record-footer">
                    <p>{record.summary?.summaryText?.split("\n")[0] || "No summary text available."}</p>
                  </div>
                </article>
              ))
            ) : (
              <div className="history-empty">
                No saved doctor visit prep history yet. Save your progress and return to see it here.
              </div>
            )}
          </div>
        </motion.section>
      )}
    </div>
  );
}

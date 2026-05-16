import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

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

function createSummary({ medications, symptoms }) {
  const sortedSymptoms = [...symptoms].sort((a, b) => a.date.localeCompare(b.date));
  const earliest = sortedSymptoms[0];
  const latest = sortedSymptoms[sortedSymptoms.length - 1];
  const averageIntensity = sortedSymptoms.length
    ? Math.round(
        sortedSymptoms.reduce((sum, entry) => sum + Number(entry.intensity || 0), 0) /
          sortedSymptoms.length
      )
    : 0;

  const symptomNarrative = sortedSymptoms.length
    ? sortedSymptoms
        .map((entry) => {
          const parts = [
            `${prettyDate(entry.date)}: ${entry.location || "General discomfort"}`,
            `intensity ${entry.intensity}/10`,
          ];
          if (entry.triggers) {
            parts.push(`triggers noted: ${entry.triggers}`);
          }
          parts.push(entry.notes);
          return parts.join(" - ");
        })
        .join("\n")
    : "No symptom entries added yet.";

  const questions = [];
  if (sortedSymptoms.length) {
    questions.push(
      `How do the symptom changes between ${prettyDate(earliest.date)} and ${prettyDate(
        latest.date
      )} affect what you think is going on?`
    );
  }
  if (medications.length) {
    questions.push("Could any of my current medications be affecting these symptoms or masking them?");
  }
  if (averageIntensity >= 6) {
    questions.push("What should I do if this pain returns at the same or higher intensity before my next visit?");
  } else {
    questions.push("What patterns should I keep tracking at home before the next appointment?");
  }
  questions.push("Are there tests, scans, or lifestyle changes I should prioritize first?");

  return {
    headline:
      sortedSymptoms.length > 0
        ? "A symptom timeline has been prepared with medication context for your consultation."
        : "A medication snapshot has been prepared for your consultation.",
    facts: [
      `${medications.length} medication${medications.length === 1 ? "" : "s"} listed`,
      `${sortedSymptoms.length} symptom log${sortedSymptoms.length === 1 ? "" : "s"} recorded`,
      sortedSymptoms.length
        ? `Average symptom intensity: ${averageIntensity}/10`
        : "No symptom intensity trend yet",
    ],
    summaryText: [
      "Doctor Visit Preparation Summary",
      "",
      `Generated on: ${new Date().toLocaleDateString("en-GB", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
      })}`,
      "",
      "Current medications:",
      medications.length
        ? medications
            .map(
              (med, index) =>
                `${index + 1}. ${med.name}${med.dosage ? ` - ${med.dosage}` : ""}${
                  med.reason ? ` | for ${med.reason}` : ""
                }`
            )
            .join("\n")
        : "None added",
      "",
      "Symptom timeline:",
      symptomNarrative,
      "",
      "Suggested discussion points:",
      questions.map((question, index) => `${index + 1}. ${question}`).join("\n"),
    ].join("\n"),
    questions,
  };
}

export default function DoctorVisitPrep() {
  const navigate = useNavigate();
  const today = formatIsoDate(new Date());

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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const calendarDays = useMemo(
    () => buildCalendarDays(selectedDate, symptoms),
    [selectedDate, symptoms]
  );

  const selectedDayEntries = useMemo(
    () => symptoms.filter((entry) => entry.date === selectedDate),
    [selectedDate, symptoms]
  );

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
    setMedications((current) => [
      ...current,
      {
        id: `med-${Date.now()}`,
        ...medicationDraft,
      },
    ]);
    setMedicationDraft({ name: "", dosage: "", reason: "" });
  };

  const addSymptom = () => {
    if (!symptomDraft.notes.trim()) {
      setError("Write a short note about what you felt on that day.");
      return;
    }

    setError("");
    setSymptoms((current) =>
      [...current, { id: `sym-${Date.now()}`, date: selectedDate, ...symptomDraft }].sort((a, b) =>
        a.date.localeCompare(b.date)
      )
    );
    setSymptomDraft({
      location: "",
      intensity: 5,
      triggers: "",
      notes: "",
    });
  };

  const removeMedication = (id) => {
    setMedications((current) => current.filter((item) => item.id !== id));
  };

  const removeSymptom = (id) => {
    setSymptoms((current) => current.filter((item) => item.id !== id));
  };

  const generateSummary = () => {
    if (!medications.length && !symptoms.length) {
      setError("Add medication or symptom details before generating the summary.");
      return;
    }

    setError("");
    setLoading(true);

    window.setTimeout(() => {
      setSummary(createSummary({ medications, symptoms }));
      setLoading(false);
    }, 900);
  };

  const downloadSummary = () => {
    if (!summary) {
      return;
    }

    const blob = new Blob([summary.summaryText], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `doctor-visit-summary-${today}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
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
      </motion.div>

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
          {summary ? (
            <button type="button" className="btn-new-summary" onClick={downloadSummary}>
              Download summary
            </button>
          ) : null}
        </div>

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
    </div>
  );
}

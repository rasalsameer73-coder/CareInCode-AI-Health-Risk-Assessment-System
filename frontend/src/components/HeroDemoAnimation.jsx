import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const steps = ["vitals", "report", "prep"];

const vitals = [
  { label: "SpO2", value: "98%", status: "Normal" },
  { label: "Blood Pressure", value: "122/80", status: "Watch" },
  { label: "Heart Rate", value: "74 bpm", status: "Normal" },
];

const reportMarkers = [
  { label: "Vitamin D", value: "18 ng/mL", note: "Low and likely linked to low outdoor activity." },
  { label: "TSH", value: "4.8 mIU/L", note: "Mildly high and worth discussing with your doctor." },
  { label: "HbA1c", value: "5.4%", note: "Within the expected range." },
];

const prepNotes = [
  "Today felt some joint pain in both knees after a longer walk.",
  "A week later the pain aggravated while climbing stairs.",
  "Can any of my medications or routine be contributing to this pattern?",
];

function PhoneShell({ children }) {
  return (
    <div style={styles.wrapper}>
      <div style={styles.card}>
        <div style={styles.topBar}>
          <div style={styles.topDots}>
            <span style={{ ...styles.dot, background: "#ff6b6b" }} />
            <span style={{ ...styles.dot, background: "#ffd166" }} />
            <span style={{ ...styles.dot, background: "#7bd88f" }} />
          </div>
          <span style={styles.topTitle}>CareInCode</span>
          <div style={{ width: 44 }} />
        </div>
        <div style={styles.content}>{children}</div>
      </div>
    </div>
  );
}

function Screen({ tag, time, title, children, footer }) {
  return (
    <motion.div
      key={tag}
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -18 }}
      transition={{ duration: 0.35 }}
      style={{ width: "100%" }}
    >
      <div style={styles.screenHeader}>
        <span style={styles.screenTag}>{tag}</span>
        <span style={styles.screenDivider} />
        <span style={styles.screenTime}>{time}</span>
      </div>
      <h3 style={styles.screenTitle}>{title}</h3>
      <div style={styles.stack}>{children}</div>
      <div style={styles.footerNote}>{footer}</div>
    </motion.div>
  );
}

function ReflectionScreen() {
  return (
    <Screen
      tag="Health Reflection"
      time="just updated"
      title="Today's Vitals"
      footer="Lifestyle-aware insight based on sleep, movement, and stress."
    >
      {vitals.map((item) => (
        <div key={item.label} style={styles.rowCard}>
          <div>
            <div style={styles.rowLabel}>{item.label}</div>
            <div style={styles.rowMeta}>Daily check-in</div>
          </div>
          <div style={styles.rowRight}>
            <strong style={styles.rowValue}>{item.value}</strong>
            <span style={styles.rowBadge(item.status)}>{item.status}</span>
          </div>
        </div>
      ))}
    </Screen>
  );
}

function ReportScreen() {
  return (
    <Screen
      tag="Report Simplifier"
      time="lab upload"
      title="Marker Highlights"
      footer="Abnormal values are explained in plain language with lifestyle context."
    >
      {reportMarkers.map((item) => (
        <div key={item.label} style={styles.reportCard}>
          <div style={styles.reportTop}>
            <strong style={styles.rowLabel}>{item.label}</strong>
            <span style={styles.reportValue}>{item.value}</span>
          </div>
          <p style={styles.reportNote}>{item.note}</p>
        </div>
      ))}
    </Screen>
  );
}

function PrepScreen() {
  return (
    <Screen
      tag="Doctor Visit Prep"
      time="timeline ready"
      title="Calendar and Summary"
      footer="Medication list, symptom changes, and doctor questions in one clean view."
    >
      <div style={styles.calendarStrip}>
        {["Mon 8", "Tue 9", "Wed 10", "Thu 11"].map((day, index) => (
          <div key={day} style={styles.calendarDay(index === 1)}>
            {day}
          </div>
        ))}
      </div>
      {prepNotes.map((note, index) => (
        <div key={note} style={styles.questionCard}>
          <span style={styles.questionNumber}>{index + 1}</span>
          <p style={styles.questionText}>{note}</p>
        </div>
      ))}
    </Screen>
  );
}

export default function HeroDemoAnimation() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setStep((current) => (current + 1) % steps.length);
    }, 2800);

    return () => window.clearInterval(timer);
  }, []);

  return (
    <PhoneShell>
      <AnimatePresence mode="wait">
        {step === 0 ? <ReflectionScreen /> : null}
        {step === 1 ? <ReportScreen /> : null}
        {step === 2 ? <PrepScreen /> : null}
      </AnimatePresence>
      <div style={styles.stepDots}>
        {steps.map((item, index) => (
          <span key={item} style={styles.stepDot(index === step)} />
        ))}
      </div>
    </PhoneShell>
  );
}

const styles = {
  wrapper: {
    position: "absolute",
    inset: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "40px 24px 40px 60px",
    overflow: "hidden",
  },
  card: {
    width: "100%",
    maxWidth: 700,
    height: 650,
    background: "#fffdf9",
    borderRadius: 20,
    border: "1px solid rgba(20,184,166,0.12)",
    boxShadow: "0 24px 60px rgba(0,0,0,0.12)",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
  },
  topBar: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "10px 16px",
    background: "#f5f0e8",
    borderBottom: "1px solid #ede8df",
  },
  topDots: {
    display: "flex",
    gap: 5,
  },
  dot: {
    width: 9,
    height: 9,
    borderRadius: "50%",
  },
  topTitle: {
    fontSize: 12,
    fontWeight: 700,
    letterSpacing: "0.1em",
    color: "#4d4030",
    textTransform: "uppercase",
  },
  content: {
    padding: "18px 18px 12px",
    display: "flex",
    flexDirection: "column",
    height: "100%",
  },
  screenHeader: {
    display: "flex",
    alignItems: "center",
    gap: 6,
    marginBottom: 10,
  },
  screenTag: {
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: "0.1em",
    textTransform: "uppercase",
    color: "#0b8f7e",
  },
  screenDivider: {
    width: 4,
    height: 4,
    borderRadius: "50%",
    background: "#b8c5bd",
  },
  screenTime: {
    fontSize: 11,
    color: "#5f7269",
  },
  screenTitle: {
    fontSize: 20,
    fontWeight: 700,
    margin: "0 0 14px",
    color: "#13261e",
  },
  stack: {
    display: "grid",
    gap: 8,
  },
  rowCard: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 12,
    background: "#ffffff",
    border: "1px solid #ede8df",
    borderRadius: 12,
    padding: "12px 14px",
  },
  rowLabel: {
    fontSize: 15,
    fontWeight: 500,
    color: "#10231d",
  },
  rowMeta: {
    fontSize: 12,
    color: "#667a72",
    marginTop: 2,
  },
  rowRight: {
    display: "flex",
    alignItems: "center",
    gap: 10,
  },
  rowValue: {
    fontSize: 18,
    color: "#0f2019",
  },
  rowBadge: (status) => ({
    fontSize: 11,
    padding: "5px 10px",
    borderRadius: 999,
    background: status === "Watch" ? "#fef3cd" : "#e6fffa",
    color: status === "Watch" ? "#8a6200" : "#0f766e",
    fontWeight: 700,
  }),
  reportCard: {
    background: "#ffffff",
    border: "1px solid #ede8df",
    borderRadius: 12,
    padding: "12px 14px",
  },
  reportTop: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 12,
  },
  reportValue: {
    fontSize: 14,
    color: "#11241d",
    fontWeight: 700,
  },
  reportNote: {
    margin: "8px 0 0",
    fontSize: 12.5,
    color: "#43584f",
    lineHeight: 1.5,
  },
  calendarStrip: {
    display: "grid",
    gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
    gap: 8,
  },
  calendarDay: (active) => ({
    background: active ? "rgba(20,184,166,0.12)" : "#ffffff",
    border: active ? "1px solid rgba(20,184,166,0.35)" : "1px solid #ede8df",
    borderRadius: 12,
    padding: "10px 8px",
    textAlign: "center",
    fontSize: 12,
    color: active ? "#0f766e" : "#4f625b",
    fontWeight: 700,
  }),
  questionCard: {
    display: "flex",
    gap: 10,
    alignItems: "flex-start",
    background: "#ffffff",
    border: "1px solid #ede8df",
    borderRadius: 12,
    padding: "12px 14px",
  },
  questionNumber: {
    width: 22,
    height: 22,
    borderRadius: 8,
    background: "rgba(20,184,166,0.12)",
    color: "#0f766e",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 11,
    fontWeight: 700,
    flexShrink: 0,
  },
  questionText: {
    margin: 0,
    fontSize: 12.5,
    lineHeight: 1.55,
    color: "#243b34",
  },
  footerNote: {
    marginTop: 12,
    padding: "12px 14px",
    background: "rgba(20,184,166,0.08)",
    border: "1px solid rgba(20,184,166,0.16)",
    borderRadius: 12,
    fontSize: 12.5,
    lineHeight: 1.5,
    color: "#1f5b48",
  },
  stepDots: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
    marginTop: "auto",
    padding: "12px 0 4px",
  },
  stepDot: (active) => ({
    width: active ? 20 : 6,
    height: 6,
    borderRadius: 999,
    background: active ? "#0d9e6e" : "#c8e6d8",
    transition: "all 0.3s ease",
  }),
};

import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import {
  uploadReport,
  getHistory,
  getCurrentUserEmail,
  downloadPdf,
} from "../services/api";

function formatIST(timestamp) {
  if (!timestamp) return "Unknown date";
  return new Date(timestamp).toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    hour12: false,
  });
}

const STORAGE_KEY = "uploadedReports";

function saveUploadedReport(file, summary) {
  const existing = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  const now = new Date();

  const record = {
    id: `${file.name}-${now.getTime()}`,
    fileName: file.name,
    category: "Pending",
    uploadedAt: now.toISOString(),
    uploadedDateLabel: now.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }),
    uploadedDay: now.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
    }),
    fileType: file.type || "unknown",
    summary,
  };

  localStorage.setItem(STORAGE_KEY, JSON.stringify([record, ...existing]));
}

function downloadSummaryFile(file, analysis) {
  const lines = [
    "CareInCode Report Simplifier",
    "",
    `File: ${file?.name || "Uploaded report"}`,
    `Report type: ${analysis?.report_type || "Unknown"}`,
    "",
    `Summary: ${analysis?.summary || "No summary available."}`,
    "",
  ];

  if (analysis?.risk_level) {
    lines.push(`Risk level: ${analysis.risk_level}`);
  }
  if (analysis?.health_score !== undefined) {
    lines.push(`Health score: ${analysis.health_score}`);
  }
  if (analysis?.risk_indicators?.length) {
    lines.push("\nRisk indicators:");
    analysis.risk_indicators.forEach((item) => {
      lines.push(`- ${item.type}${item.severity ? ` (${item.severity})` : ""}`);
    });
  }
  if (analysis?.evidence?.length) {
    lines.push("\nEvidence:");
    analysis.evidence.forEach((item) => {
      lines.push(`- ${item}`);
    });
  }
  if (analysis?.next_steps?.length) {
    lines.push("\nNext steps:");
    analysis.next_steps.forEach((item) => {
      lines.push(`- ${item}`);
    });
  }
  if (analysis?.doctor_prep?.questions?.length) {
    lines.push("\nQuestions for doctor:");
    analysis.doctor_prep.questions.forEach((item) => {
      lines.push(`- ${item}`);
    });
  }
  if (analysis?.insights?.length) {
    lines.push("\nInsights:");
    analysis.insights.forEach((item) => {
      lines.push(`- ${item}`);
    });
  }

  lines.push("\nDisclaimer: " + (analysis?.disclaimer || "Educational information only. Not a medical diagnosis."));
  lines.push(`Confidence: ${analysis?.confidence ?? "N/A"}`);

  const blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "report-simplifier-summary.txt";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export default function Report() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [insight, setInsight] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [reportHistory, setReportHistory] = useState([]);
  const [activePanel, setActivePanel] = useState("summary");
  const [loading, setLoading] = useState(false);
  const [insightLoading, setInsightLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState("");

  const handleChooseFile = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setError("");
    setInsight("");
  };

  const handleSaveUpload = async () => {
    if (!file) {
      setError("Please upload one report file first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await uploadReport(file, getCurrentUserEmail());
      const summary =
        data.analysis?.summary ||
        (data.analysis?.insights && data.analysis.insights.length > 0
          ? data.analysis.insights.join("\n\n")
          : null) ||
        data.report_type ||
        "Report saved successfully.";

      setInsight(summary);
      setAnalysisResult(data.analysis || null);
      saveUploadedReport(file, summary);
      await loadHistory();
      setLoading(false);
    } catch (err) {
      console.error(err);
      setError(err.message || "Could not save this report right now.");
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    try {
      const response = await getHistory(getCurrentUserEmail());
      setReportHistory(response.records || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleGenerateInsights = async () => {
    if (!file) {
      setError("Please upload one report file first.");
      return;
    }

    try {
      setInsightLoading(true);
      setError("");

      const data = await uploadReport(file, getCurrentUserEmail());

      const summary =
        data.analysis?.summary ||
        (data.analysis?.insights && data.analysis.insights.length > 0
          ? data.analysis.insights.join("\n\n")
          : null) ||
        data.report_type ||
        "Report analyzed successfully.";

      setInsight(summary);
      setAnalysisResult(data.analysis || null);
      saveUploadedReport(file, summary);
      await loadHistory();
    } catch (err) {
      console.error(err);
      setError(err.message || "Could not generate insights right now.");
    } finally {
      setInsightLoading(false);
    }
  };

  const handleDownloadSummary = async () => {
    if (!insight && !analysisResult) {
      setError("Generate insights first before downloading the summary.");
      return;
    }

    try {
      setDownloading(true);
      setError("");

      const blob = await downloadPdf("/export/report/pdf", {
        method: "POST",
      });

      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "report-simplifier.pdf";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      setError(err.message || "Could not download the summary.");
    } finally {
      setDownloading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="report-page">
      <motion.div
        className="report-hero"
        initial={{ opacity: 0, y: 24 }}
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
            <span className="page-kicker">Profile 2</span>
          </div>
          <div className="profile-page-title-wrap">
            <h1 className="report-heading profile-page-heading">Report Simplifier</h1>
          </div>
        </div>

        <div className="profile-page-copy">
          <p className="report-desc">
            Upload one medical report at a time and keep its summary area ready in one place.
          </p>
        </div>

        <div className="profile-meta-row">
          <section className="report-side-card profile-meta-card">
            <span className="meta-label">Report support</span>
            <strong>Single file upload</strong>
            <p className="report-side-text">PDF, PNG, JPG, and JPEG are accepted here.</p>
          </section>
        </div>
      </motion.div>

      <div className="report-workspace">
        <motion.div
          initial={{ opacity: 0, y: 26 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.06 }}
        >
          <section className="upload-shell report-panel">
            <div className="upload-shell-body">
              <div className="upload-shell-header">
                <h2 className="upload-title">Upload your report</h2>
                <p className="upload-subtitle">Supported formats: PDF, PNG, JPG, JPEG</p>
              </div>

              <div className="upload-card enhanced" onClick={handleChooseFile}>
                <div className="upload-icon-wrap" aria-hidden="true">
                  ^
                </div>

                <p className="upload-main-text">Click to select a report</p>

                <p className="upload-helper-text">
                  Upload one report file to register it here neatly.
                </p>

                {file && <div className="selected-file">{file.name}</div>}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.png,.jpg,.jpeg"
                style={{ display: "none" }}
                onChange={handleFileChange}
              />

              <div className="report-actions">
                <button
                  type="button"
                  className="btn-primary report-button"
                  onClick={handleSaveUpload}
                  disabled={loading}
                >
                  {loading ? "Saving upload..." : "Save Upload"}
                </button>
                <button
                  type="button"
                  className="btn-primary report-button"
                  onClick={handleGenerateInsights}
                  disabled={insightLoading}
                >
                  {insightLoading ? "Generating..." : "Generate Insights"}
                </button>
              </div>

              {error && <p className="report-error">{error}</p>}
            </div>
          </section>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 26 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.1 }}
        >
          <section className="insight-panel report-panel">
            <div className="upload-shell-body">
              <div className="insight-panel-header">
                <div className="insight-panel-icon" aria-hidden="true">
                  *
                </div>

                <div>
                  <h2 className="insight-title">Report Summary</h2>
                  <p className="insight-subtitle">This area shows the summary for the uploaded report.</p>
                </div>
              </div>

              <div className="report-panel-tabs">
                <button
                  type="button"
                  className={activePanel === "summary" ? "panel-tab active" : "panel-tab"}
                  onClick={() => setActivePanel("summary")}
                >
                  Summary
                </button>
                <button
                  type="button"
                  className={activePanel === "history" ? "panel-tab active" : "panel-tab"}
                  onClick={() => setActivePanel("history")}
                >
                  History
                </button>
              </div>

              <div className="insight-box upgraded">
                {activePanel === "history" ? (
                  reportHistory.length ? (
                    <div className="history-list report-history-list">
                      {reportHistory.map((record) => (
                        <article key={record._id} className="history-record-card">
                          <div className="history-record-header">
                            <strong>{record.file_name || record.analysis?.report_type || "Saved report"}</strong>
                            <span>{formatIST(record.created_at)}</span>
                          </div>
                          <div className="history-record-values">
                            <span>{record.analysis?.report_type || "Unknown type"}</span>
                            <span>Confidence: {record.analysis?.confidence ?? "N/A"}</span>
                          </div>
                          <p>{record.analysis?.summary || record.analysis?.insights?.[0] || "No summary available."}</p>
                        </article>
                      ))}
                    </div>
                  ) : (
                    <div className="history-empty">
                      No saved reports yet. Upload a report to store its history.
                    </div>
                  )
                ) : insightLoading ? (
                  "Generating insights..."
                ) : analysisResult ? (
                  <div className="report-summary-details">
                    <div className="report-summary-row">
                      <strong>Report type</strong>
                      <span>{analysisResult.report_type || "Unknown"}</span>
                    </div>
                    <div className="report-summary-row">
                      <strong>Risk level</strong>
                      <span>{analysisResult.risk_level || "N/A"}</span>
                    </div>
                    <div className="report-summary-row">
                      <strong>Health score</strong>
                      <span>{analysisResult.health_score ?? "N/A"}</span>
                    </div>
                    <div className="report-summary-row">
                      <strong>Summary</strong>
                      <p>{analysisResult.summary || insight}</p>
                    </div>
                    {analysisResult.risk_indicators?.length ? (
                      <div className="report-summary-row report-summary-list">
                        <strong>Risk indicators</strong>
                        <ul>
                          {analysisResult.risk_indicators.map((item, idx) => (
                            <li key={idx}>{`${item.type}${item.severity ? ` (${item.severity})` : ""}`}</li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    {analysisResult.evidence?.length ? (
                      <div className="report-summary-row report-summary-list">
                        <strong>Evidence</strong>
                        <ul>
                          {analysisResult.evidence.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    {analysisResult.next_steps?.length ? (
                      <div className="report-summary-row report-summary-list">
                        <strong>Next steps</strong>
                        <ul>
                          {analysisResult.next_steps.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    {analysisResult.doctor_prep?.questions?.length ? (
                      <div className="report-summary-row report-summary-list">
                        <strong>Questions for doctor</strong>
                        <ul>
                          {analysisResult.doctor_prep.questions.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    {analysisResult.insights?.length ? (
                      <div className="report-summary-row report-summary-list">
                        <strong>Insights</strong>
                        <ul>
                          {analysisResult.insights.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    <div className="report-summary-row">
                      <p>{analysisResult.disclaimer}</p>
                      <span>Confidence: {analysisResult.confidence ?? "N/A"}</span>
                    </div>
                  </div>
                ) : (
                  insight || "Nothing to show here yet."
                )}
              </div>

              {(analysisResult || insight) && (
                <div className="report-actions">
                  <button
                    type="button"
                    className="btn-primary report-button"
                    onClick={handleDownloadSummary}
                    disabled={downloading}
                  >
                    {downloading ? "Preparing file..." : "Download Report"}
                  </button>
                </div>
              )}
            </div>
          </section>
        </motion.div>
      </div>
    </div>
  );
}

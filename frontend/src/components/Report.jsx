import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

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

function downloadSummaryFile(file, insight) {
  const body = [
    "CareInCode Report Upload",
    "",
    `File: ${file?.name || "Uploaded report"}`,
    "",
    insight,
  ].join("\n");

  const blob = new Blob([body], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "ai-summary.txt";
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
      setInsight("");

      saveUploadedReport(file, "");
      setLoading(false);
    } catch (err) {
      console.error(err);
      setError("Could not save this report right now.");
      setLoading(false);
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

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/upload/report", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        const message =
          errorBody?.error || `Upload failed: ${response.statusText}`;
        throw new Error(message);
      }

      const data = await response.json();
      const summary =
        data.analysis?.summary ||
        (data.analysis?.insights && data.analysis.insights.length > 0
          ? data.analysis.insights.join("\n\n")
          : null) ||
        data.report_type ||
        "Report analyzed successfully.";

      setInsight(summary);
      saveUploadedReport(file, summary);
    } catch (err) {
      console.error(err);
      setError(err.message || "Could not generate insights right now.");
    } finally {
      setInsightLoading(false);
    }
  };

  const handleDownloadSummary = async () => {
    if (!insight) {
      setError("Generate insights first before downloading the summary.");
      return;
    }

    try {
      setDownloading(true);
      setError("");
      downloadSummaryFile(file, insight);
    } catch (err) {
      console.error(err);
      setError("Could not download the summary.");
    } finally {
      setDownloading(false);
    }
  };

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

              <div className="insight-box upgraded">
                {insightLoading ? "Generating insights..." : insight || "Nothing to show here yet."}
              </div>

              {insight && (
                <div className="report-actions">
                  <button
                    type="button"
                    className="btn-primary report-button"
                    onClick={handleDownloadSummary}
                    disabled={downloading}
                  >
                    {downloading ? "Preparing file..." : "Download Note"}
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

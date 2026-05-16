import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

function VitalsIcon() {
  return (
    <svg viewBox="0 0 64 64" aria-hidden="true" className="dashboard-medical-icon">
      <circle cx="32" cy="32" r="18" fill="none" stroke="currentColor" strokeWidth="4.5" />
      <path
        d="M14 33h9l4-8 8 17 6-11h9"
        fill="none"
        stroke="currentColor"
        strokeWidth="4.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function ReportIcon() {
  return (
    <svg viewBox="0 0 64 64" aria-hidden="true" className="dashboard-medical-icon">
      <rect x="18" y="10" width="28" height="44" rx="8" fill="none" stroke="currentColor" strokeWidth="4.5" />
      <path d="M26 24h12M26 32h12M26 40h8" stroke="currentColor" strokeWidth="4.5" strokeLinecap="round" />
      <path d="M43 18l5 5" stroke="currentColor" strokeWidth="4.5" strokeLinecap="round" />
    </svg>
  );
}

function DoctorPrepIcon() {
  return (
    <svg viewBox="0 0 64 64" aria-hidden="true" className="dashboard-medical-icon">
      <rect x="14" y="14" width="36" height="40" rx="10" fill="none" stroke="currentColor" strokeWidth="4.5" />
      <path d="M24 12v8M40 12v8M23 30h18M23 40h11" stroke="currentColor" strokeWidth="4.5" strokeLinecap="round" />
      <circle cx="46" cy="46" r="8" fill="#ffffff" />
      <path d="M46 42v8M42 46h8" stroke="currentColor" strokeWidth="4.5" strokeLinecap="round" />
    </svg>
  );
}

function PulseMiniIcon() {
  return (
    <svg viewBox="0 0 32 32" aria-hidden="true" className="dashboard-mini-svg">
      <path
        d="M4 17h5l3-6 5 10 3-6h8"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function PlusMiniIcon() {
  return (
    <svg viewBox="0 0 32 32" aria-hidden="true" className="dashboard-mini-svg">
      <path d="M16 8v16M8 16h16" fill="none" stroke="currentColor" strokeWidth="2.8" strokeLinecap="round" />
    </svg>
  );
}

const cards = [
  {
    title: "Health Reflection Tool",
    desc: "Review your daily vitals with simple explanations grounded in your routine.",
    Icon: VitalsIcon,
    route: "/health-reflection",
    tag: "Vitals",
    tone: "mint",
    accents: [PulseMiniIcon, PlusMiniIcon],
    subtext: "See patterns in blood pressure, heart rate, oxygen, and everyday lifestyle habits.",
  },
  {
    title: "Report Simplifier",
    desc: "Upload reports and receive clear AI-driven explanations.",
    Icon: ReportIcon,
    route: "/report",
    tag: "AI Insights",
    tone: "sand",
    accents: [ReportIcon, PlusMiniIcon],
    subtext: "Understand difficult medical terms in plain language without leaving the dashboard.",
  },
  {
    title: "Doctor Visit Prep",
    desc: "Organize medications, log symptoms, and prepare for your appointment.",
    Icon: DoctorPrepIcon,
    route: "/doctor-visit-prep",
    tag: "Preparation",
    tone: "sky",
    accents: [DoctorPrepIcon, PulseMiniIcon],
    subtext: "Generate a comprehensive summary to share with your doctor.",
  },
];

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard dashboard-refined">
      <div className="dashboard-section-header">
        <h2 className="dashboard-title">Welcome to your dashboard</h2>
      </div>

      <div className="card-grid dashboard-card-grid-refined">
        {cards.map((card, i) => (
          <motion.div
            key={card.title}
            className="dashboard-card-wrap"
            style={{ width: "100%", height: "100%" }}
            initial={{ opacity: 0, y: 35 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.12 }}
          >
            <article
              onClick={() => navigate(card.route)}
              className={`dashboard-card dashboard-card-${card.tone}`}
              role="button"
              tabIndex={0}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  navigate(card.route);
                }
              }}
            >
              <motion.div
                className={`dashboard-card-glow dashboard-orbit-${card.tone}`}
                animate={{
                  scale: [1, 1.14, 1],
                  opacity: [0.35, 0.72, 0.35],
                }}
                transition={{
                  duration: 3.2,
                  repeat: Infinity,
                }}
              />

              <div className="dashboard-card-ornaments" aria-hidden="true">
                {card.accents.map((AccentIcon, index) => (
                  <span key={`${card.title}-accent-${index}`} className="dashboard-ornament-badge">
                    <AccentIcon />
                  </span>
                ))}
              </div>

              <div className="dashboard-card-content">
                <div className="dashboard-card-main">
                  <motion.div
                    className="card-icon"
                    animate={{ y: [0, -7, 0] }}
                    transition={{
                      duration: 2.4,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  >
                    <span className="dashboard-card-icon">
                      <card.Icon />
                    </span>
                  </motion.div>

                  <span className="dashboard-chip">{card.tag}</span>

                  <h3 className="card-title">{card.title}</h3>
                  <p className="card-desc">{card.desc}</p>
                </div>

                <div className="dashboard-card-footer">
                  <p className="dashboard-subtext">{card.subtext}</p>
                  <span className="dashboard-link">
                    Explore now
                    <span className="dashboard-link-arrow" aria-hidden="true">
                      {"->"}
                    </span>
                  </span>
                </div>
              </div>
            </article>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

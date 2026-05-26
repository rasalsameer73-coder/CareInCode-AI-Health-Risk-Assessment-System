from typing import Optional


def build_structured_response(

    summary: str,

    risk_indicators: list,

    evidence: list,

    doctor_questions: list,

    next_steps: list,

    confidence: float = 0.75,

    insights: Optional[list] = None,

    biomarker_table: Optional[list] = None,

    health_score: Optional[int] = None
):

    # =========================
    # DEFAULTS
    # =========================

    if insights is None:

        insights = []

    if not risk_indicators:

        risk_indicators = [
            {
                "indicator": "General health observation",
                "severity": "low",
                "reason":
                    "No major abnormalities detected."
            }
        ]

    if not evidence:

        evidence = [
            "User-reported symptoms were analyzed."
        ]

    if not doctor_questions:

        doctor_questions = [
            "Should I monitor these symptoms further?",
            "Are additional tests recommended?"
        ]

    if not next_steps:

        next_steps = [
            "Monitor symptoms closely",
            "Seek medical attention if symptoms worsen"
        ]

    # =========================
    # DETERMINE RISK LEVEL
    # =========================

    risk_level = "low"

    for risk in risk_indicators:

        severity = risk.get(
            "severity",
            "low"
        )

        if severity == "high":

            risk_level = "high"
            break

        elif (
            severity == "moderate"
            and risk_level != "high"
        ):

            risk_level = "moderate"

    # =========================
    # CLEAN SUMMARY
    # =========================

    summary = summary.replace(
        "**",
        ""
    ).strip()

    if len(summary) > 300:

        summary = summary[:300] + "..."

    # =========================
    # FINAL RESPONSE
    # =========================

    return {

        "summary":
            summary,

        "risk_level":
            risk_level,

        "risk_indicators":
            risk_indicators,

        "insights":
            insights,

        "evidence":
            evidence,

        "doctor_prep": {

            "questions":
                doctor_questions
        },

        "next_steps":
            next_steps,

        "confidence":
            confidence,

        "disclaimer":
            "Educational information only. Not a medical diagnosis."
    }
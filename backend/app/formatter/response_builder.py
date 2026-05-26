from typing import Optional


def _resolve_health_score(
    health_score: Optional[int],
    risk_indicators: list
):
    if health_score is not None:
        return health_score

    if not risk_indicators:
        return 98

    score = 100
    for risk in risk_indicators:
        severity = risk.get(
            "severity",
            "low"
        )
        if severity == "high":
            score -= 25
        elif severity == "moderate":
            score -= 12
        elif severity == "low":
            score -= 5

    return max(0, score)


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

    if biomarker_table is None:

        biomarker_table = []

    health_score = _resolve_health_score(
        health_score,
        risk_indicators
    )

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

        "health_score":
            health_score,

        "biomarker_table":
            biomarker_table,

        "confidence":
            confidence,

        "disclaimer":
            "Educational information only. Not a medical diagnosis."
    }
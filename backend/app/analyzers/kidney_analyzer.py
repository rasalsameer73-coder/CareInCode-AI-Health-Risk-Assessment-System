def analyze_kidney_biomarkers(
    biomarkers: dict
):

    risk_indicators = []

    insights = []

    evidence = []

    doctor_questions = []

    next_steps = []

    health_score = 100

    risk_level = "low"

    # =========================
    # CREATININE
    # =========================

    creatinine = biomarkers.get(
        "creatinine"
    )

    if creatinine is not None:

        evidence.append(
            f"Creatinine: {creatinine}"
        )

        if creatinine > 1.3:

            risk_indicators.append({

                "type":
                    "Elevated Creatinine",

                "severity":
                    "moderate"
            })

            insights.append(
                "Creatinine appears elevated."
            )

            next_steps.append(
                "Discuss kidney function evaluation with your doctor."
            )

            health_score -= 15

            risk_level = "moderate"

    # =========================
    # UREA
    # =========================

    urea = biomarkers.get(
        "urea"
    )

    if urea is not None:

        evidence.append(
            f"Urea: {urea}"
        )

        if urea > 50:

            risk_indicators.append({

                "type":
                    "Elevated Urea",

                "severity":
                    "moderate"
            })

            insights.append(
                "Urea levels appear elevated."
            )

            health_score -= 10

    # =========================
    # BUN
    # =========================

    bun = biomarkers.get(
        "bun"
    )

    if bun is not None:

        evidence.append(
            f"BUN: {bun}"
        )

        if bun > 20:

            risk_indicators.append({

                "type":
                    "Elevated BUN",

                "severity":
                    "moderate"
            })

            insights.append(
                "BUN appears elevated."
            )

            health_score -= 8

    # =========================
    # eGFR
    # =========================

    egfr = biomarkers.get(
        "egfr"
    )

    if egfr is not None:

        evidence.append(
            f"eGFR: {egfr}"
        )

        if egfr < 60:

            risk_indicators.append({

                "type":
                    "Reduced eGFR",

                "severity":
                    "high"
            })

            insights.append(
                "eGFR appears lower than common reference ranges."
            )

            next_steps.append(
                "Discuss kidney filtration function with your doctor."
            )

            health_score -= 20

            risk_level = "high"

    # =========================
    # DOCTOR QUESTIONS
    # =========================

    doctor_questions.extend([

        "Should kidney function be monitored regularly?",

        "Would repeat kidney testing be helpful?",

        "Could medications affect kidney function?",

        "Are additional renal investigations needed?"
    ])

    # =========================
    # MINIMUM SCORE
    # =========================

    if health_score < 0:

        health_score = 0

    # =========================
    # SUMMARY
    # =========================

    if risk_indicators:

        summary = (
            "Kidney biomarkers show some "
            "values outside common reference ranges."
        )

    else:

        summary = (
            "Kidney biomarkers appear "
            "within common reference ranges."
        )

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

        "doctor_questions":
            doctor_questions,

        "next_steps":
            list(set(next_steps)),

        "health_score":
            health_score
    }
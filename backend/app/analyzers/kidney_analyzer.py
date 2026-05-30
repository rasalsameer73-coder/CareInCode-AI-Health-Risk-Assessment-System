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

        if creatinine > 3.0:

            risk_indicators.append({

                "type":
                    "Critical Elevated Creatinine",

                "severity":
                    "critical"
            })

            insights.append(
                "Creatinine is critically elevated. Seek immediate medical attention."
            )

            next_steps.append(
                "Urgent nephrologist evaluation required."
            )

            health_score -= 30

            risk_level = "critical"

        elif creatinine > 1.8:

            risk_indicators.append({

                "type":
                    "Severely Elevated Creatinine",

                "severity":
                    "high"
            })

            insights.append(
                "Creatinine is significantly elevated (severe kidney dysfunction)."
            )

            next_steps.append(
                "Discuss kidney function evaluation with your doctor."
            )

            health_score -= 20

            risk_level = "high"

        elif creatinine > 1.3:

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
                "Monitor kidney function regularly."
            )

            health_score -= 12

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

        if egfr < 15:
            # Stage G5 - Kidney failure
            risk_indicators.append({

                "type":
                    "Critical Kidney Function Loss",

                "severity":
                    "critical"
            })

            insights.append(
                "eGFR indicates kidney failure (Stage G5). Seek immediate medical attention."
            )

            next_steps.append(
                "Urgent nephrology consultation required."
            )

            health_score -= 35

            risk_level = "critical"

        elif egfr < 30:
            # Stage G4 - Severely reduced function
            risk_indicators.append({

                "type":
                    "Severely Reduced eGFR",

                "severity":
                    "high"
            })

            insights.append(
                "eGFR indicates severely reduced kidney function (Stage G4)."
            )

            next_steps.append(
                "Discuss kidney function evaluation with your doctor."
            )

            health_score -= 25

            risk_level = "high"

        elif egfr < 45:
            # Stage G3b - Moderate to severe reduction
            risk_indicators.append({

                "type":
                    "Moderately Reduced eGFR",

                "severity":
                    "moderate"
            })

            insights.append(
                "eGFR indicates moderate reduction in kidney function (Stage G3b)."
            )

            next_steps.append(
                "Monitor kidney function regularly."
            )

            health_score -= 15

            risk_level = "moderate"

        elif egfr < 60:
            # Stage G3a - Mild to moderate reduction
            risk_indicators.append({

                "type":
                    "Mildly Reduced eGFR",

                "severity":
                    "low"
            })

            insights.append(
                "eGFR indicates mild reduction in kidney function (Stage G3a)."
            )

            health_score -= 8

    # =========================
    # DETERMINE FINAL RISK LEVEL
    # =========================

    final_risk_level = "low"

    for risk in risk_indicators:

        severity = risk.get(
            "severity",
            "low"
        )

        if severity == "critical":

            final_risk_level = "critical"
            break

        elif severity == "high" and final_risk_level != "critical":

            final_risk_level = "high"

        elif severity == "moderate" and final_risk_level not in ["critical", "high"]:

            final_risk_level = "moderate"

    risk_level = final_risk_level

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
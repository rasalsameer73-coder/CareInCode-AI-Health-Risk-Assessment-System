def analyze_diabetes_biomarkers(
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
    # HbA1c
    # =========================

    hba1c = biomarkers.get(
        "hba1c"
    )

    if hba1c is not None:

        evidence.append(
            f"HbA1c: {hba1c}"
        )

        if hba1c >= 9:

            risk_indicators.append({

                "type":
                    "Critical Elevated HbA1c",

                "severity":
                    "critical"
            })

            insights.append(
                "HbA1c is critically elevated (poor diabetes control)."
            )

            next_steps.append(
                "Seek immediate diabetes management review."
            )

            health_score -= 30

            risk_level = "critical"

        elif hba1c >= 8:

            risk_indicators.append({

                "type":
                    "Severely Elevated HbA1c",

                "severity":
                    "high"
            })

            insights.append(
                "HbA1c is significantly elevated (suboptimal diabetes control)."
            )

            next_steps.append(
                "Discuss blood sugar management intensification with your doctor."
            )

            health_score -= 25

            risk_level = "high"

        elif hba1c >= 6.5:

            risk_indicators.append({

                "type":
                    "Elevated HbA1c",

                "severity":
                    "moderate"
            })

            insights.append(
                "HbA1c levels indicate diabetes."
            )

            next_steps.append(
                "Discuss blood sugar management with your doctor."
            )

            health_score -= 15

            risk_level = "moderate"

        elif hba1c >= 5.7:

            risk_indicators.append({

                "type":
                    "Prediabetes Range HbA1c",

                "severity":
                    "low"
            })

            insights.append(
                "HbA1c falls within the prediabetes range."
            )

            next_steps.append(
                "Monitor blood sugar and lifestyle habits."
            )

            health_score -= 8

            if risk_level == "low":
                risk_level = "low"

    # =========================
    # FASTING GLUCOSE
    # =========================

    fasting_glucose = biomarkers.get(
        "fasting_glucose"
    )

    if fasting_glucose is not None:

        evidence.append(
            f"Fasting Glucose: {fasting_glucose}"
        )

        if fasting_glucose >= 200:

            risk_indicators.append({

                "type":
                    "Critical Elevated Fasting Glucose",

                "severity":
                    "critical"
            })

            insights.append(
                "Fasting glucose is critically elevated."
            )

            next_steps.append(
                "Seek urgent diabetes/endocrine assessment."
            )

            health_score -= 30

            risk_level = "critical"

        elif fasting_glucose >= 126:

            risk_indicators.append({

                "type":
                    "High Fasting Glucose",

                "severity":
                    "high"
            })

            insights.append(
                "Fasting glucose is significantly elevated (diabetes range)."
            )

            next_steps.append(
                "Discuss fasting glucose levels with your doctor."
            )

            health_score -= 20

            risk_level = "high"

        elif fasting_glucose >= 100:

            risk_indicators.append({

                "type":
                    "Borderline Fasting Glucose",

                "severity":
                    "low"
            })

            insights.append(
                "Fasting glucose is mildly elevated (impaired fasting glucose)."
            )

            health_score -= 8

    # =========================
    # RANDOM GLUCOSE
    # =========================

    random_glucose = biomarkers.get(
        "random_glucose"
    )

    if random_glucose is not None:

        evidence.append(
            f"Random Glucose: {random_glucose}"
        )

        if random_glucose >= 200:

            risk_indicators.append({

                "type":
                    "High Random Glucose",

                "severity":
                    "high"
            })

            insights.append(
                "Random glucose appears elevated."
            )

            next_steps.append(
                "Discuss glucose monitoring with your doctor."
            )

            health_score -= 15

            risk_level = "high"

        elif random_glucose >= 140:

            risk_indicators.append({

                "type":
                    "Borderline Random Glucose",

                "severity":
                    "moderate"
            })

            insights.append(
                "Random glucose is mildly elevated."
            )

            health_score -= 8

    # =========================
    # DOCTOR QUESTIONS
    # =========================

    doctor_questions.extend([

        "Should repeat HbA1c testing be considered?",

        "Would lifestyle or dietary changes help?",

        "Should blood sugar be monitored more frequently?",

        "Are additional diabetes-related tests needed?"
    ])

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

        elif severity == "low" and final_risk_level == "low":

            final_risk_level = "low"

    risk_level = final_risk_level

    # =========================
    # SUMMARY
    # =========================

    if risk_indicators:

        summary = (
            "Diabetes-related biomarkers show "
            "some values outside common "
            "reference ranges."
        )

    else:

        summary = (
            "Diabetes-related biomarkers appear "
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
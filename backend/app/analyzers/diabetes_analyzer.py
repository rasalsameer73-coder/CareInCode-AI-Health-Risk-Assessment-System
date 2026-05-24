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

        if hba1c >= 6.5:

            risk_indicators.append({

                "type":
                    "Elevated HbA1c",

                "severity":
                    "high"
            })

            insights.append(
                "HbA1c levels are elevated."
            )

            next_steps.append(
                "Discuss blood sugar management with your doctor."
            )

            health_score -= 20

            risk_level = "high"

        elif hba1c >= 5.7:

            risk_indicators.append({

                "type":
                    "Prediabetes Range HbA1c",

                "severity":
                    "moderate"
            })

            insights.append(
                "HbA1c falls within the prediabetes range."
            )

            next_steps.append(
                "Monitor blood sugar and lifestyle habits."
            )

            health_score -= 10

            risk_level = "moderate"

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

        if fasting_glucose >= 126:

            risk_indicators.append({

                "type":
                    "High Fasting Glucose",

                "severity":
                    "high"
            })

            insights.append(
                "Fasting glucose appears elevated."
            )

            next_steps.append(
                "Discuss fasting glucose levels with your doctor."
            )

            health_score -= 15

            risk_level = "high"

        elif fasting_glucose >= 100:

            risk_indicators.append({

                "type":
                    "Borderline Fasting Glucose",

                "severity":
                    "moderate"
            })

            insights.append(
                "Fasting glucose is mildly elevated."
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
    # MINIMUM SCORE
    # =========================

    if health_score < 0:

        health_score = 0

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
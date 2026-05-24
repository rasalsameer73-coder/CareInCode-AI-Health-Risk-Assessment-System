def analyze_thyroid_biomarkers(
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
    # TSH
    # =========================

    tsh = biomarkers.get(
        "tsh"
    )

    if tsh is not None:

        evidence.append(
            f"TSH: {tsh}"
        )

        # HIGH TSH

        if tsh > 4.5:

            risk_indicators.append({

                "type":
                    "Elevated TSH",

                "severity":
                    "moderate"
            })

            insights.append(
                "TSH appears elevated and may indicate hypothyroid patterns."
            )

            next_steps.append(
                "Discuss thyroid hormone evaluation with your doctor."
            )

            health_score -= 15

            risk_level = "moderate"

        # LOW TSH

        elif tsh < 0.4:

            risk_indicators.append({

                "type":
                    "Low TSH",

                "severity":
                    "moderate"
            })

            insights.append(
                "TSH appears lower than common reference ranges."
            )

            next_steps.append(
                "Discuss possible thyroid overactivity with your doctor."
            )

            health_score -= 15

            risk_level = "moderate"

    # =========================
    # T3
    # =========================

    t3 = biomarkers.get(
        "t3"
    )

    if t3 is not None:

        evidence.append(
            f"T3: {t3}"
        )

        if t3 < 0.8:

            risk_indicators.append({

                "type":
                    "Low T3",

                "severity":
                    "moderate"
            })

            insights.append(
                "T3 appears lower than common reference ranges."
            )

            health_score -= 8

        elif t3 > 2.0:

            risk_indicators.append({

                "type":
                    "High T3",

                "severity":
                    "moderate"
            })

            insights.append(
                "T3 appears elevated."
            )

            health_score -= 8

    # =========================
    # T4
    # =========================

    t4 = biomarkers.get(
        "t4"
    )

    if t4 is not None:

        evidence.append(
            f"T4: {t4}"
        )

        if t4 < 4.5:

            risk_indicators.append({

                "type":
                    "Low T4",

                "severity":
                    "moderate"
            })

            insights.append(
                "T4 appears lower than common reference ranges."
            )

            health_score -= 8

        elif t4 > 12.0:

            risk_indicators.append({

                "type":
                    "High T4",

                "severity":
                    "moderate"
            })

            insights.append(
                "T4 appears elevated."
            )

            health_score -= 8

    # =========================
    # DOCTOR QUESTIONS
    # =========================

    doctor_questions.extend([

        "Should repeat thyroid testing be considered?",

        "Would thyroid hormone monitoring help?",

        "Are additional thyroid-related tests necessary?",

        "Could symptoms be related to thyroid imbalance?"
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
            "Thyroid biomarkers show some "
            "values outside common reference ranges."
        )

    else:

        summary = (
            "Thyroid biomarkers appear "
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
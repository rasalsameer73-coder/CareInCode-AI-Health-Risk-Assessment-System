def analyze_lipid_biomarkers(
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
    # TOTAL CHOLESTEROL
    # =========================

    cholesterol = biomarkers.get(
        "cholesterol"
    )

    if cholesterol is not None:

        evidence.append(
            f"Total Cholesterol: {cholesterol}"
        )

        if cholesterol >= 240:

            risk_indicators.append({

                "type":
                    "High Cholesterol",

                "severity":
                    "high"
            })

            insights.append(
                "Total cholesterol is significantly elevated."
            )

            next_steps.append(
                "Discuss cholesterol management with your doctor."
            )

            health_score -= 20

            risk_level = "high"

        elif cholesterol >= 200:

            risk_indicators.append({

                "type":
                    "Borderline High Cholesterol",

                "severity":
                    "moderate"
            })

            insights.append(
                "Total cholesterol is mildly elevated."
            )

            next_steps.append(
                "Monitor cholesterol and lifestyle factors."
            )

            health_score -= 10

            risk_level = "moderate"

    # =========================
    # LDL
    # =========================

    ldl = biomarkers.get(
        "ldl"
    )

    if ldl is not None:

        evidence.append(
            f"LDL: {ldl}"
        )

        if ldl >= 160:

            risk_indicators.append({

                "type":
                    "Elevated LDL",

                "severity":
                    "high"
            })

            insights.append(
                "LDL cholesterol is elevated."
            )

            next_steps.append(
                "Consider discussing cardiovascular risk factors."
            )

            health_score -= 15

            risk_level = "high"

        elif ldl >= 130:

            risk_indicators.append({

                "type":
                    "Borderline LDL",

                "severity":
                    "moderate"
            })

            insights.append(
                "LDL cholesterol is mildly elevated."
            )

            health_score -= 8

    # =========================
    # HDL
    # =========================

    hdl = biomarkers.get(
        "hdl"
    )

    if hdl is not None:

        evidence.append(
            f"HDL: {hdl}"
        )

        if hdl < 40:

            risk_indicators.append({

                "type":
                    "Low HDL",

                "severity":
                    "moderate"
            })

            insights.append(
                "HDL cholesterol appears lower than recommended."
            )

            next_steps.append(
                "Discuss heart health and exercise habits."
            )

            health_score -= 10

            risk_level = "moderate"

    # =========================
    # TRIGLYCERIDES
    # =========================

    triglycerides = biomarkers.get(
        "triglycerides"
    )

    if triglycerides is not None:

        evidence.append(
            f"Triglycerides: {triglycerides}"
        )

        if triglycerides >= 200:

            risk_indicators.append({

                "type":
                    "High Triglycerides",

                "severity":
                    "high"
            })

            insights.append(
                "Triglyceride levels are elevated."
            )

            next_steps.append(
                "Discuss dietary and metabolic risk factors."
            )

            health_score -= 15

            risk_level = "high"

        elif triglycerides >= 150:

            risk_indicators.append({

                "type":
                    "Borderline Triglycerides",

                "severity":
                    "moderate"
            })

            insights.append(
                "Triglycerides are mildly elevated."
            )

            health_score -= 8

    # =========================
    # DOCTOR QUESTIONS
    # =========================

    doctor_questions.extend([

        "Should cardiovascular risk factors be evaluated?",

        "Would lifestyle changes help improve lipid levels?",

        "Should repeat lipid testing be considered?",

        "Are additional heart health tests necessary?"
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
            "Lipid profile analysis detected "
            "some parameters outside "
            "common reference ranges."
        )

    else:

        summary = (
            "Lipid profile appears "
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
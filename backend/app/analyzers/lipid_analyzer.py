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

        if cholesterol >= 300:

            risk_indicators.append({

                "type":
                    "Critical Cholesterol",

                "severity":
                    "critical"
            })

            insights.append(
                "Total cholesterol is critically elevated."
            )

            next_steps.append(
                "Seek urgent cardiovascular risk assessment."
            )

            health_score -= 30

            risk_level = "critical"

        elif cholesterol >= 240:

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
                    "low"
            })

            insights.append(
                "Total cholesterol is mildly elevated."
            )

            next_steps.append(
                "Monitor cholesterol and lifestyle factors."
            )

            health_score -= 8

            if risk_level == "low":
                risk_level = "low"

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

        if ldl >= 190:

            risk_indicators.append({

                "type":
                    "Critical LDL",

                "severity":
                    "critical"
            })

            insights.append(
                "LDL cholesterol is critically elevated (very high cardiovascular risk)."
            )

            next_steps.append(
                "Seek urgent cardiovascular evaluation."
            )

            health_score -= 30

            risk_level = "critical"

        elif ldl >= 160:

            risk_indicators.append({

                "type":
                    "Elevated LDL",

                "severity":
                    "high"
            })

            insights.append(
                "LDL cholesterol is significantly elevated."
            )

            next_steps.append(
                "Consider discussing cardiovascular risk factors."
            )

            health_score -= 18

            risk_level = "high"

        elif ldl >= 130:

            risk_indicators.append({

                "type":
                    "Borderline LDL",

                "severity":
                    "low"
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

        if hdl < 30:

            risk_indicators.append({

                "type":
                    "Critically Low HDL",

                "severity":
                    "high"
            })

            insights.append(
                "HDL cholesterol is significantly low (high cardiovascular risk)."
            )

            next_steps.append(
                "Urgent cardiovascular risk assessment needed."
            )

            health_score -= 20

            risk_level = "high"

        elif hdl < 40:

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

            health_score -= 12

            if risk_level not in ["critical", "high"]:
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

        if triglycerides >= 500:

            risk_indicators.append({

                "type":
                    "Critical Triglycerides",

                "severity":
                    "critical"
            })

            insights.append(
                "Triglyceride levels are critically elevated (pancreatitis risk)."
            )

            next_steps.append(
                "Seek urgent assessment for triglyceride management."
            )

            health_score -= 30

            risk_level = "critical"

        elif triglycerides >= 200:

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

            health_score -= 18

            if risk_level not in ["critical"]:
                risk_level = "high"

        elif triglycerides >= 150:

            risk_indicators.append({

                "type":
                    "Borderline Triglycerides",

                "severity":
                    "low"
            })

            insights.append(
                "Triglycerides are mildly elevated."
            )

            health_score -= 8

            if risk_level == "low":
                risk_level = "low"

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
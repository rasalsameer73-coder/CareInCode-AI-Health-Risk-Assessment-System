def analyze_liver_biomarkers(
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
    # ALT
    # =========================

    alt = biomarkers.get(
        "alt"
    )

    if alt is not None:

        evidence.append(
            f"ALT: {alt}"
        )

        if alt > 200:

            risk_indicators.append({

                "type":
                    "Critical Elevated ALT",

                "severity":
                    "critical"
            })

            insights.append(
                "ALT is critically elevated (severe liver injury)."
            )

            next_steps.append(
                "Seek immediate hepatology evaluation."
            )

            health_score -= 30

            risk_level = "critical"

        elif alt > 100:

            risk_indicators.append({

                "type":
                    "Severely Elevated ALT",

                "severity":
                    "high"
            })

            insights.append(
                "ALT is significantly elevated (liver dysfunction)."
            )

            next_steps.append(
                "Urgent liver function assessment needed."
            )

            health_score -= 20

            risk_level = "high"

        elif alt > 55:

            risk_indicators.append({

                "type":
                    "Elevated ALT",

                "severity":
                    "moderate"
            })

            insights.append(
                "ALT appears elevated and may indicate liver stress."
            )

            next_steps.append(
                "Discuss liver enzyme evaluation with your doctor."
            )

            health_score -= 12

            risk_level = "moderate"

    # =========================
    # AST
    # =========================

    ast = biomarkers.get(
        "ast"
    )

    if ast is not None:

        evidence.append(
            f"AST: {ast}"
        )

        if ast > 200:

            risk_indicators.append({

                "type":
                    "Critical Elevated AST",

                "severity":
                    "critical"
            })

            insights.append(
                "AST is critically elevated (severe liver injury)."
            )

            health_score -= 30

            risk_level = "critical"

        elif ast > 100:

            risk_indicators.append({

                "type":
                    "Severely Elevated AST",

                "severity":
                    "high"
            })

            insights.append(
                "AST is significantly elevated (liver dysfunction)."
            )

            health_score -= 20

            risk_level = "high"

        elif ast > 45:

            risk_indicators.append({

                "type":
                    "Elevated AST",

                "severity":
                    "moderate"
            })

            insights.append(
                "AST appears elevated."
            )

            health_score -= 12

            if risk_level not in ["critical", "high"]:
                risk_level = "moderate"

    # =========================
    # BILIRUBIN
    # =========================

    bilirubin = biomarkers.get(
        "bilirubin"
    )

    if bilirubin is not None:

        evidence.append(
            f"Bilirubin: {bilirubin}"
        )

        if bilirubin > 3.0:

            risk_indicators.append({

                "type":
                    "Critical Elevated Bilirubin",

                "severity":
                    "high"
            })

            insights.append(
                "Bilirubin is significantly elevated (severe jaundice)."
            )

            next_steps.append(
                "Urgent assessment needed for bilirubin levels."
            )

            health_score -= 20

            risk_level = "high"

        elif bilirubin > 1.2:

            risk_indicators.append({

                "type":
                    "Elevated Bilirubin",

                "severity":
                    "moderate"
            })

            insights.append(
                "Bilirubin appears elevated."
            )

            next_steps.append(
                "Discuss bilirubin levels with your doctor."
            )

            health_score -= 12

            if risk_level not in ["critical", "high"]:
                risk_level = "moderate"

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

        "Should repeat liver testing be considered?",

        "Could medications affect liver enzymes?",

        "Would additional liver investigations help?",

        "Should lifestyle or diet changes be discussed?"
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
            "Liver biomarkers show some "
            "values outside common reference ranges."
        )

    else:

        summary = (
            "Liver biomarkers appear "
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
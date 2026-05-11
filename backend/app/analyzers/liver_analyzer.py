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

        if alt > 55:

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

            health_score -= 15

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

        if ast > 45:

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

        if bilirubin > 1.2:

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
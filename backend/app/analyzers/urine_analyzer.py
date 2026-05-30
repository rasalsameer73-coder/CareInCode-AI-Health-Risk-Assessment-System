def analyze_urine_biomarkers(
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
    # PROTEIN
    # =========================

    protein = biomarkers.get(
        "protein"
    )

    if protein is not None:

        evidence.append(
            f"Protein: {protein}"
        )

        if protein > 100:

            risk_indicators.append({

                "type":
                    "Critically Elevated Urine Protein",

                "severity":
                    "high"
            })

            insights.append(
                "Protein is significantly elevated in urine (proteinuria)."
            )

            next_steps.append(
                "Urgent kidney function assessment needed."
            )

            health_score -= 22

            risk_level = "high"

        elif protein > 15:

            risk_indicators.append({

                "type":
                    "Elevated Urine Protein",

                "severity":
                    "moderate"
            })

            insights.append(
                "Protein appears elevated in urine."
            )

            next_steps.append(
                "Discuss kidney or urinary health with your doctor."
            )

            health_score -= 12

            risk_level = "moderate"

    # =========================
    # KETONES
    # =========================

    ketones = biomarkers.get(
        "ketones"
    )

    if ketones is not None:

        evidence.append(
            f"Ketones: {ketones}"
        )

        if ketones > 10:

            risk_indicators.append({

                "type":
                    "Critically Elevated Ketones",

                "severity":
                    "critical"
            })

            insights.append(
                "Ketones are critically elevated (risk of ketoacidosis)."
            )

            next_steps.append(
                "Seek immediate medical evaluation."
            )

            health_score -= 30

            risk_level = "critical"

        elif ketones > 3:

            risk_indicators.append({

                "type":
                    "Elevated Ketones",

                "severity":
                    "moderate"
            })

            insights.append(
                "Ketones appear elevated in urine."
            )

            next_steps.append(
                "Discuss possible metabolic causes with your doctor."
            )

            health_score -= 12

            if risk_level not in ["critical"]:
                risk_level = "moderate"

    # =========================
    # PUS CELLS
    # =========================

    pus_cells = biomarkers.get(
        "pus_cells"
    )

    if pus_cells is not None:

        evidence.append(
            f"Pus Cells: {pus_cells}"
        )

        if pus_cells > 15:

            risk_indicators.append({

                "type":
                    "Severely Elevated Pus Cells",

                "severity":
                    "high"
            })

            insights.append(
                "Pus cells are significantly elevated (serious infection)."
            )

            next_steps.append(
                "Urgent urinary tract evaluation needed."
            )

            health_score -= 22

            if risk_level not in ["critical"]:
                risk_level = "high"

        elif pus_cells > 5:

            risk_indicators.append({

                "type":
                    "Elevated Pus Cells",

                "severity":
                    "moderate"
            })

            insights.append(
                "Pus cells appear elevated and may indicate urinary tract irritation or infection."
            )

            next_steps.append(
                "Discuss possible urinary infection evaluation with your doctor."
            )

            health_score -= 15

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

        "Should urine testing be repeated?",

        "Could dehydration affect these results?",

        "Are additional kidney or urinary investigations needed?",

        "Could symptoms indicate urinary tract infection?"
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
            "Urine biomarkers show some "
            "values outside common reference ranges."
        )

    else:

        summary = (
            "Urine biomarkers appear "
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